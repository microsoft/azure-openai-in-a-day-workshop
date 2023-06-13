# azure-openai-in-a-day-workshop

> *In this technical workshop, you will get a comprehensive introduction to Azure OpenAI Service and Azure OpenAI Studio. You will learn how to create and refine prompts for various scenarios using hands-on exercises. You will also discover how to leverage Azure OpenAI Service to access and analyze your company data. Moreover, you will explore existing solution accelerators and best practices for prototyping and deploying use cases end-to-end. The workshop will end with a Q&A session and a wrap-up.*

## Workshop agenda

### 🌅 Morning (9:00 – 12:00)

> *Fokus: Introduction and first steps*

* 📣 Intro (90min)
  * Into Workshop (15mins)
  * Intro Azure OpenAI Service (30mins)
  * Azure Azure OpenAI Studio (45mins)
* 🧑🏼‍💻 Prompt Engineering Exercises using Studio (90mins)

### 🌆 Afternoon (1:00 – 4:30)

> *Focus: Solutions*

* Recap (15min)
* 📣 Using Azure OpenAI Service to access company data (60min)
  * How to bring your own data
  * Fine-tuning and embedding
  * Solutions Accelerators
* QnA session (30min)
* 💻 Hands-on lab on two exemplay use-cases (90min)

<sup>
📣 Presentation, 🧑🏼‍💻 Hands-on lab
</sup>

-------------------

## Preparation

> *This is only required for the hands-on lab. If you are only attending the presentation, you can skip this section.*

### Azure OpenAI Service subscription and deployments

Grant the participant access to the Azure OpenAI Service subscription and create the required deployments.

Ideally, grant the participants access to Azure OpenAI Service service be assigning the `Cognitive Service OpenAI user`. If the participant is a `Cognitive Service OpenAI contributor`, they can create the following deployments themselves.

Otherwise, create 'text-davinci-003' and 'text-embedding-ada-002' deployments (and assign the participant to the deployments).

There are two ways to authenticate (see Jupyter notebooks):
1. (Recommended) Use the Azure CLI to authenticate to Azure and Azure OpenAI Service
2. Using a token (not needed if using the Azure CLI)

Get the Azure OpenAI Service endpoint (and key) from the Azure portal.

### Workspace environment

Choose one of the following options to set up your environment: Codespaces, Devcontainer or bring your own environment (Anaconda). Building the environment can take a few minutes, so please start early.

#### 1️⃣ Codespaces

> 🌟 Highly recommended: *Best option if you already have a Github account. You can develop on local VSCode or in a browser window. *

The following instructions will discribe how to setup Codespace on your browser This option does not required any software installation or preparation on your Computer

* Login to your Github account or create your own in 5 mins.
* Go to Github repository and click on `Code` button then choose `Create Codespace on Main`.
* Github will start preparing the envireoment and container which might take some minutes.
* After Github finishs setting up the Codespace enviroment a new window will open, and in the terminal at the bottom of the window type  `pip install -r requirements.txt`, this will make sure that all requried python liberaries are installed and good to go.
* At the left Explorer Panel create a new file named `.env`. Make sure you are in the base folder when you are creating the file.
* Open the file and type Azure OpenAI Service endpoint and key as follows:
  - `OPENAI_API_KEY=xxxxxx`
  - `OPENAI_API_BASE=xxxxx`
* To test that everything is running, from the left Explorer panel open `excersizes\quickstart.ipynb`.
* Press run on the first Notebook the Codespace will ask you to choose your python Enviroment, select `Python Enviroments` then select `Python 3.9.2`

#### 2️⃣ Devcontainer

> *Usually a good option if VSCode and Docker Desktop are already installed.*

* Install [Docker](https://www.docker.com/products/docker-desktop)
* Install [Visual Studio Code](https://code.visualstudio.com/) or you can install it from the Company Portal.
* Install [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
* Clone this repository
* Open the repository in Visual Studio Code.
* Click on the green button in the bottom left corner of the window
* Select `Reopen in Container`
* Wait for the container to be built and started.
* create a new file named `.env`. Make sure you are in the base folder when you are creating the file.
* Open the file and type Azure OpenAI Service endpoint and key as follows:
  - `OPENAI_API_KEY=xxxxxx`
  - `OPENAI_API_BASE=xxxxx`
* To test that everything is running open `excersizes\quickstart.ipynb`.
* Press run on the first Notebook, choose your python Enviroment, select `Python Enviroments` then select `Python 3.9.2`.

#### 3️⃣ Bring your own environment

> *If you already have a Python environment with Jupyter Notebook and the Azure CLI installed.*

Make sure you have the requirements installed in your Python environment using `pip install -r requirements.txt`.

-------------------

## Content of the repository

* :bulb: [Guideline for writing better prompts](lectures/prompt_writing_help.md)

## Exercises

* :muscle: [Simple prompt writing exercises](exercises/exercises.md)
* :muscle: [Quickstart](exercises/quickstart.ipynb) - just to make sure everything works!
* :muscle: [Preprocessing](exercises/preprocessing.ipynb) - principles of preprocessing and token handling!
* :muscle: [Q&A with embeddings](exercises/qna_with_embeddings_exercise.ipynb)
* :muscle: [Unsupervised movie classification and recommendations](exercises/movie_classification_unsupervised_incl_recommendations_exercise.ipynb)
* :muscle: [Email Summarization and Answering App](exercises/email_app.md)

## Solutions

Do not cheat! :sweat_smile:

* :bulb: Solution - [Q&A with embeddings](exercises/solutions/qna_with_embeddings_solution.ipynb)
* :bulb: Solution - [Unsupervised movie classification and recommendations](exercises/solutions/movie_classification_unsupervised_incl_recommendations_solution.ipynb)
* :bulb: Solution - [Email Summarization and Answering App](exercises/solutions/email_app.py)

## Q&A Quick Start

If you want to quickly create a Q&A webapp using your own data, please follow the [quickstart guide notebook](qna-quickstart-template/qna-app-quickstart.ipynb).

If you want to use LangChain to build an interactive chat experience on your own data, follow the [quickstart chat on private data using LangChain](qna-chat-with-langchain/qna-chat-with-langchain.ipynb).

If you want to use LlamaIndex 🦙 (GPT Index), follow the [quickstart guide notebook with llama-index](qna-quickstart-with-gpt-index/qna-quickstart-with-llama-index.ipynb).
