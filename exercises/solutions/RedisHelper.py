import os
import numpy as np
import redis
from redis import Redis
import logging
import copy
from redis.commands.search.field import VectorField
from redis.commands.search.field import TextField
from redis.commands.search.field import TagField
from redis.commands.search.query import Query
from redis.commands.search.result import Result


## https://redis-py.readthedocs.io/en/stable/commands.html
## https://redis.io/docs/stack/search/reference/query_syntax/



from utils.kb_doc import KB_Doc

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


from utils.env_vars import *


def get_model_dims(embedding_model):
    if embedding_model == "text-search-davinci-doc-001":
        return DAVINCI_003_EMBED_NUM_DIMS
    elif embedding_model == "text-embedding-ada-002":
        return ADA_002_EMBED_NUM_DIMS
    else:
        return ADA_002_EMBED_NUM_DIMS


def create_search_index (redis_new_conn, vector_field_name, number_of_vectors, vector_dimensions=512, distance_metric='L2'):
    if (REDIS_ADDR is None) or (REDIS_ADDR == ''): return None

    M=40
    EF=200

    fields = [VectorField(vector_field_name, "HNSW", {"TYPE": "FLOAT32", "DIM": vector_dimensions, "DISTANCE_METRIC": distance_metric, "INITIAL_CAP": number_of_vectors, "M": M, "EF_CONSTRUCTION": EF})] + \
             [TextField(f) for f in KB_Doc().get_fields() if f != VECTOR_FIELD_IN_REDIS]

    redis_new_conn.ft(REDIS_INDEX_NAME).create_index(fields)


def flush_cached_values_only():
    if (REDIS_ADDR is None) or (REDIS_ADDR == ''): return None

    redis_conn = get_new_conn()
    ks = redis_conn.keys()
    print(f"Found {len(ks)} values that are cached in Redis")

    for k in ks:
        ttl = redis_conn.ttl(k)
        if ttl > 0:
            print(f"Key has {ttl} seconds to live, deleting...")
            redis_conn.expire(name=k, time=1)



def redis_reset_index(redis_new_conn):
    #flush all data
    redis_new_conn.flushall()

    #create flat index & load vectors
    create_search_index(redis_new_conn,VECTOR_FIELD_IN_REDIS, NUMBER_PRODUCTS_INDEX, get_model_dims(CHOSEN_EMB_MODEL), 'COSINE')


def test_redis(redis_new_conn):
    if (REDIS_ADDR is None) or (REDIS_ADDR == ''): return None

    try:
        out = redis_new_conn.ft(REDIS_INDEX_NAME).info()
        # print(f"Found Redis Index {REDIS_INDEX_NAME}")
    except Exception as e:
        # print(f"Redis Index {REDIS_INDEX_NAME} not found. Creating a new index.")
        logging.error(f"Redis Index {REDIS_INDEX_NAME} not found. Creating a new index.")
        redis_reset_index(redis_new_conn)


def get_new_conn():
    if (REDIS_ADDR is None) or (REDIS_ADDR == ''): return None

    if REDIS_PASSWORD == '':
        redis_conn = Redis(host = REDIS_ADDR, port = REDIS_PORT)
    else:
        redis_conn = redis.StrictRedis(host=REDIS_ADDR, port=int(REDIS_PORT), password=REDIS_PASSWORD, ssl=True)

    #print('Connected to redis', redis_conn)
    test_redis(redis_conn)
    
    return redis_conn


@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(4))
def redis_upsert_embedding(redis_conn, e_dict):   
    if (REDIS_ADDR is None) or (REDIS_ADDR == ''): return None

    try:
        #embeds = np.array(e[VECTOR_FIELD_IN_REDIS]).astype(np.float32).tobytes()
        #meta = {'text_en': e['text_en'], 'text':e['text'], 'doc_url': e['doc_url'], 'timestamp': e['timestamp'], VECTOR_FIELD_IN_REDIS:embeds}
        e = copy.deepcopy(e_dict)

        for k in e: 
            if isinstance(e[k], list) and (len(e[k]) > 0):
                if isinstance(e[k][0], float): e[k] = np.array(e[k]).astype(np.float32).tobytes()
                if isinstance(e[k][0], str): e[k] = ', '.join(e[k])

        # e[VECTOR_FIELD_IN_REDIS] = np.array(e[VECTOR_FIELD_IN_REDIS]).astype(np.float32).tobytes()

        for k in e: 
            if isinstance(e[k], list):
                print(e[k])

        p = redis_conn.pipeline(transaction=False)
        p.hset(e['id'], mapping=e)
        p.execute()   
        return 1

    except Exception as e:
        print(f"Embedding Except: {e}")
        logging.error(f"Embedding Except: {e}")
        return 0



@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(4))
def redis_query_embedding_index(redis_conn, query_emb, t_id, topK=5, filter_param=None):
    if (REDIS_ADDR is None) or (REDIS_ADDR == ''): return None

    if (filter_param is None) or (filter_param == '*'):
        filter_param = '*'
    else:
        if not filter_param.startswith('@'):
            filter_param = '@' + filter_param

    filter_param = filter_param.replace('-', '\-')
    fields = list(KB_Doc().get_fields()) + ['vector_score']
    query_vector = np.array(query_emb).astype(np.float32).tobytes()
    query_string = f'({filter_param})=>[KNN {topK} @{VECTOR_FIELD_IN_REDIS} $vec_param AS vector_score]'

    q = Query(query_string).sort_by('vector_score').paging(0,topK).return_fields(*fields).dialect(2)
    params_dict = {"vec_param": query_vector}
    results = redis_conn.ft(REDIS_INDEX_NAME).search(q, query_params = params_dict)
    
    return [{k: match.__dict__[k] for k in (set(list(match.__dict__.keys())) - set([VECTOR_FIELD_IN_REDIS]))} for match in results.docs if match.id != t_id]



@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(4))
def redis_set(redis_conn, key, field, value, expiry = None, verbose = False):
    if (REDIS_ADDR is None) or (REDIS_ADDR == '') or (USE_REDIS_CACHE != 1): return None

    key = key.replace('"', '')
    res = redis_conn.hset(key, field, value)

    if expiry is not None:
        redis_conn.expire(name=key, time=expiry)
    if verbose: print("\nSetting Redis Key: ", key, field, expiry)
    return res
        


@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(4))
def redis_get(redis_conn, key, field, expiry = CONVERSATION_TTL_SECS, verbose = False):
    if (REDIS_ADDR is None) or (REDIS_ADDR == '') or (USE_REDIS_CACHE != 1): return None

    key = key.replace('"', '')
    if verbose: print("\nGetting Redis Key: ", key, field)
    if redis_conn.ttl(key) > 0: redis_conn.expire(name=key, time=expiry)
    return redis_conn.hget(key, field)
    


 