# MediMate
Hackathon solution for lablab's TruEra Challenge: Build LLM Applications with Google Cloud Vertex AI Hackathon

## Inspiration
MediMateAI is a cutting-edge tool designed to assist you in extracting essential information from your prescriptions. Utilizing artificial intelligence, it not only provides you with comprehensive details on the potential side effects of your medication but also alerts you to any possible conflicts between your current prescription and previous medications. Moreover, MediMateAI serves as a reminder to ensureyou take your medication as prescribed, helping you maintain a consistent schedule.Please note that this is a beta version, and while it offers valuable insights,it is not intended as a substitute for professional medical advice from your doctor Additionally, it is not yet ready for widespread use and should not be relied upon for predictive purposes.

## What it does
- Enables users to upload a photo of their prescription and receive a detailed report on the medication's side effects, potential conflicts, and dosage instructions.
- Provides users with a reminder to take their medication as prescribed.
- Allows users to view their prescription history and track their medication intake.


## How we built it
- We used Google Cloud's Vertex AI to train our model and deploy it to the cloud.
- We used ZILLIZ as vector database to store the vector of the image.
- We used openAi embedding to get the vector of the image.
- We used Langchin to designe and integrate LLM service.
- We used Streamlit to build the web app.
- We used trulens to evaluate the model result.


## How to run it
- Clone the repo
- create a virtual environment with python 3.11
- install the requirements.txt
- create a .env file with the following variables:
```bash
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
PROCESSOR_ID=YOUR_PROCESSOR_ID(Google Document AI Processor ID)
PROCESSOR_PROJECT_ID= YOUR_PROCESSOR_PROJECT_ID (Google Document AI Processor Project ID)
PROCESSOR_LOCATION=YOUR_PROCESSOR_LOCATION (Google Document AI Processor Location)
ZILLIZ_CLOUD_URI = YOUR_ZILLIZ_CLOUD_URI
ZILLIZ_CLOUD_API_KEY = YOUR_ZILLIZ_CLOUD_API_KEY
``` 

- run the 0_🏠MediMate.py file via the command line 
```bash
streamlit run 0_🏠MediMate.py
```
- upload google cloud credentials json file
- upload an image of your prescription and wait for the results to be displayed
- enjoy!



