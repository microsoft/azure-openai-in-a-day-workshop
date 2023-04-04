# Email summarization and answering web app

## Introduction

In this exercise you'll be building a simple web app that allows to summarize and answer your emails!
We'll be using the following technology:

* Python
* Streamlit library (web frontend)
* Azure OpenAI Service (summarization, answering)

## Guided help

### Use Streamlit to build the UI

Use streamlit to build a simple UI. First, follow the [getting started guide](https://docs.streamlit.io/library/get-started/main-concepts).

Once you have that running, create a new Python file called `email_app.py` and use the following components to build the UI:

* [Header for your app](https://docs.streamlit.io/library/api-reference/text/st.title)
* [Write text to the page](https://docs.streamlit.io/library/api-reference/write-magic/st.write)
* [Buttons](https://docs.streamlit.io/library/api-reference/widgets/st.button)
* [Text area for entering your email](https://docs.streamlit.io/library/api-reference/widgets/st.text_area)

1. Create a title, a text area where you can enter an email, and two buttons ("Generate Summary" and "Generate Answer")
2. Run the app via `streamlit run email_app.py`
3. Add fake functionality that when somebody presses one of the buttons, that the UI prints something

### Add Azure OpenAI Service

Once your app UI is running, add Azure OpenAI Service:

1. Add Azure OpenAI Service to generate a summary
2. Add Azure OpenAI Service to generate an answer