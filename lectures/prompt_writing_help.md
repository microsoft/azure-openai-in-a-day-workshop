# Writing good prompts for OpenAI GPT-3

Here are a few tips that will help you to write good prompts with OpenAI.
All examples use `text-davinci-002` as the model and use a temperature of `0.7`.

## Being descriptive

Just like when telling somebody else what to do, GPT-3 heavily benefits if we tell it exactly what we want from it.

:arrow_forward: **Prompt:**
> Write an article about spring cleaning.

:repeat: **Completion (shortened):**
> After a long, cold winter, there’s nothing like the feeling of springtime in the air. And with that comes the urge to spring clean our homes! Whether you’re a neat freak or a bit of a messy person, there’s no denying that a good spring clean can make your home feel fresh and new again.
> 
> Here are a few tips to help you get started on your spring cleaning:
> 
> 1. Make a plan. Decide what areas of your home you want to focus on and make a list of all the tasks you need to do. This will help you stay organized and on track.
> ...
> With these tips, your spring cleaning will be a breeze!

The article looks good, but maybe we just want to have 3 takeaways:

:arrow_forward: **Prompt:**
> Write an short article about spring cleaning. The article should have 3 bullet points as the main talking points and a short intro and summary.

:repeat: **Completion:**
> It's that time of year again! Time to break out the cleaning supplies and get to work. Spring cleaning is a great way to freshen up your home and get rid of all the dust and cobwebs that have accumulated over the winter. Here are a few tips to help you get the most out of your spring cleaning:
> 
> -Start from the top and work your way down. Dust and cobwebs tend to collect on ceilings, so start there and work your way down to the floors.
> 
> -Don't forget the nooks and crannies. Spring cleaning is a great opportunity to get into all those hard-to-reach places and give them a good cleaning.
> 
> -Make it a family affair. Spring cleaning is a great way to get the whole family involved in cleaning up the house. Assign tasks to everyone and make it a fun activity.
> 
> With these tips, your spring cleaning will be a breeze!

## Output formats for completions

Let's say we want the article as markdown:

:arrow_forward: **Prompt:**
> Write an short article about spring cleaning. The article should have 3 bullet points as the main talking points and a short intro and summary. Write the article formatted as markdown with proper H1 and H2 headers.

:repeat: **Completion:**
> ```
> # Spring Cleaning
> 
> It's that time of year again! Time to open up the windows, let in some fresh air, and deep clean our homes. Spring cleaning is a great way to get rid of the stuff we don't need and make our living spaces more inviting. Here are a few tips to help you get started:
> 
> * Start with a plan: make a list of the rooms you want to tackle and what needs to be done in each.
> 
> * Set some realistic goals: you don't have to do everything in one day, or even one weekend. Break your plan down into smaller chunks and take your time.
> 
> * Get everyone involved: enlist the help of family and friends to make the job go faster.
> 
> With a little planning and some elbow grease, your home will be sparkling in no time!
> ```

Let's take a different example:

:arrow_forward: **Prompt:**
> For the companies Microsoft, UBS, FedEx, classify each company into its industry and also write their yearly revenue.

:repeat: **Completion:**
> ```
> Microsoft: Technology; $127.8 billion
> UBS: Banking; $51.2 billion
> FedEx: Courier services; $65.5 billion
> ```

Now, we can manually "force" a more machine readable format:

:arrow_forward: **Prompt:**
> For the companies Microsoft, UBS, FedEx, classify each company into its industry and also write their yearly revenue. Write the results as COMPANY:INDUSTRY:REVENUE.

:repeat: **Completion:**
> ```
> Microsoft:Technology:$127.8 billion
> UBS:Banking:$67.7 billion
> FedEx:Transportation:$65.5 billion
> ```

Or we can directly ask to generate a csv:

:arrow_forward: **Prompt:**
> For the companies Microsoft, UBS, FedEx, classify each company into its industry and also write their yearly revenue. Give the results as a CSV. Use COMPANY, INDUSTRY and REVENUE as headers.

:repeat: **Completion:**
> ```
> COMPANY,INDUSTRY,REVENUE
> Microsoft,Software,118640
> UBS,Banking,30549
> FedEx,Transportation,65.45
> ```

Here, the revenue seems to look off, so let's ask it to format it:

:arrow_forward: **Prompt:**
> For the companies Microsoft, UBS, FedEx, classify each company into its industry and also write their yearly revenue. Give the results as a CSV. Use COMPANY, INDUSTRY and REVENUE as headers and make sure revenue is printed as $x.xxbn.


:repeat: **Completion:**
> ```
> COMPANY,INDUSTRY,REVENUE
> Microsoft,Technology,$127.8bn
> UBS,Banking,$51.8bn
> FedEx,Logistics,$69.0bn
> ```

As we notice, the revenue numbers differ between calls. This is mostly because GPT-3 is not deterministic and we should try specifying the year. However, it might still remain that the numbers are incorrect.

## Operating on a "payload"

Often, we want to extract various data points from a text "payload". Here, it helps to tell GPT-3 where the text starts, by explicitly naming it (e.g., "book chapter"):

:arrow_forward: **Prompt:**
> Extract all the names of all the persons who are mentioned in the book chapter below.
> 
> Book chapter:
> Peter went into the forest. Marry spend her day at the lake.
> 
> Persons:

:repeat: **Completion:**
> Peter, Marry

In this case, GPT-3 also does better when you end the prompt with "Persons:", so it knows what you expect.

## Dealing with non-English text

Sometimes we have non-English text that we want to process. In many cases, OpenAI is pretty good at understanding that text, but it can struggle when the prompt is also written in non-English. Therefore, it often works better to the have the "payload" text in the non-English language, while keeping the prompt in English. OpenAI often answers in English:

:arrow_forward: **Prompt:**
> Summarize what things I did buy in the following sentence.
> Give the results as a bullet point list and just list the items.
> 
> Sentence: Ich ging in den Supermarkt und kaufte Äpfel, Karotten und Pasta.
> Items:

:repeat: **Completion:**
> -Apples
> -Carrots
> -Pasta

However, running the same prompt again might give you a German answer.

:repeat: **Completion (re-generated):**
> - Äpfel
> - Karotten
> - Pasta

So in order to get an English completion, we can ask for an English-only answer:

:arrow_forward: **Prompt:**
> Summarize what things I did buy in the following sentence.
> Give the results as a bullet point list and just list the items. Make sure to answer only in English.
> 
> Sentence: Ich ging in den Supermarkt und kaufte Äpfel, Karotten und Pasta.
> Items:

:repeat: **Completion:**
> -Apples
> -Carrots
> -Pasta

Starting with `text-davinci-003`, GPT-3 is getting better at also answering in your preferred non-English language. Hence specifying that you want an, e.g. German response, might then give consistent results. However, this does not work reliably with `text-davinci-002`.

## Avoiding false information

In some cases, we might want to answer certain questions given some text. If you ask a question where the answer is within the text, OpenAI does a good job:

:arrow_forward: **Prompt:**
> The insurance covers the driver and any family members.
> 
> Does the insurance cover my wife?

:repeat: **Completion:**
> Yes, the insurance covers your wife and any other family members.

However, when you ask a question that can't be answered from the text, OpenAI starts coming up with its own thoughts:

:arrow_forward: **Prompt:**
> The insurance covers the driver and any family members.
> 
> Am I also insured when driving outside of Europe?

:repeat: **Completion:**
> No, the insurance does not cover driving outside of Europe. If you plan to drive outside of Europe, you will need to purchase additional insurance coverage.

In order to avoid such a scenario, it helps to tell OpenAI how it should behave if the answer is not in the text:

**Insurance policy:**
> The insurance covers the driver and any family members.
> 
> Am I also insured when driving outside of Europe? If the information is not present in the policy, then write "Answer not found in text!".

:repeat: **Completion:**
Answer not found in text!