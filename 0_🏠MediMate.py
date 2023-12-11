import streamlit as st
from PIL import Image
from streamlit_chat import message
from google.oauth2 import service_account
from google.cloud import aiplatform
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import time
import os
from utils import save_uploaded_file
from prescription_ocr import process_prescription, prescription_to_json
from dotenv import load_dotenv, find_dotenv
from langchain.llms import VertexAI
from langchain.vectorstores import Milvus
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate
load_dotenv(find_dotenv())


MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'media')
icon = Image.open(os.path.join(MEDIA_PATH, 'icon.jpg'))
logo = Image.open(os.path.join(MEDIA_PATH, 'logo.jpg'))
st.set_page_config(page_title='MediMateAi', page_icon=icon, layout='wide')
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


# set sidebar config to set openAI key and upload Google credentials service account key and data if need
st.sidebar.image(logo, width=300)
st.sidebar.title('MediMateAi')
st.sidebar.markdown("""MediMateAI is a cutting-edge tool designed to assist you in extracting\
                     essential information from your prescriptions. Utilizing artificial intelligence,\
                     it not only provides you with comprehensive details on the potential side effects\
                     of your medication but also alerts you to any possible conflicts between your current\
                     prescription and previous medications. Moreover, MediMateAI serves as a reminder to ensure\
                     you take your medication as prescribed, helping you maintain a consistent schedule.\
                    Please note that this is a beta version, and while it offers valuable insights,\
                     it is not intended as a substitute for professional medical advice from your doctor.\
                     Additionally, it is not yet ready for widespread use and should not be relied upon for predictive purposes.""")
st.sidebar.markdown('---')
st.sidebar.title('Google Cloud')
google_cloud_credentials_uploader =st.sidebar.file_uploader('Upload Google Cloud Credentials', type=['json'])
use_env = st.sidebar.checkbox('Use environment variables', value=False)
st.sidebar.markdown('---')
st.sidebar.title('Settings')
st.sidebar.markdown('---')
st.sidebar.title('OpenAI')
openai_key = st.sidebar.text_input('OpenAI Key')
st.sidebar.markdown('---')
st.sidebar.title('Zilliz_URI')
zilliz_uri = st.sidebar.text_input('Zilliz_URI')
st.sidebar.markdown('---')
st.sidebar.title('Zilliz_API_KEY')
zilliz_api_key = st.sidebar.text_input('Zilliz_API_KEY')
st.sidebar.markdown('---')
st.sidebar.title('Processor_Project_ID')
processor_project_id = st.sidebar.text_input('Processor_Project_ID')
st.sidebar.markdown('---')
st.sidebar.title('Processor_Location')
processor_location = st.sidebar.text_input('Processor_Location')
st.sidebar.markdown('---')
st.sidebar.title('Processor_ID')
processor_id = st.sidebar.text_input('Processor_ID')
st.sidebar.markdown('---')

@st.cache_resource
def get_config():
    return zilliz_api_key, zilliz_uri, processor_project_id, processor_location, processor_id

if not google_cloud_credentials_uploader or not openai_key or not zilliz_api_key or not zilliz_uri or not processor_project_id or not processor_location or not processor_id:
    st.write('Please set up your environment variables and upload your Google Cloud Credentials')
elif google_cloud_credentials_uploader:
    zilliz_api_key, zilliz_uri, processor_project_id, processor_location, processor_id = get_config()
    google_cloud_credentials = os.path.join(os.getcwd(), google_cloud_credentials_uploader.name)
    save_uploaded_file(google_cloud_credentials_uploader, google_cloud_credentials)



    @st.cache_resource
    def init_google_service_account_client(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        aiplatform.init(credentials=credentials, project=credentials.project_id)
        llm = VertexAI()
        return credentials, llm

    @st.cache_resource
    def _init_db(_embeddings, _collection_name="medimate"):
        _db =Milvus(
        _embeddings,
        collection_name=_collection_name,
        connection_args={
            "uri": zilliz_api_key,
            "token": zilliz_uri,
            "secure": True,
        },
            )
        return _db
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    credentials, llm = init_google_service_account_client(google_cloud_credentials)

    if use_env:
        openai_key = os.getenv('OPENAI_KEY')
        openai_key = os.getenv('OPENAI_KEY')
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))
        db = _init_db(embeddings)

    db = _init_db(embeddings)

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "Welcome to MediMateAi, Plese upload your prescription"}
        ]

    def generate_response(prompt, llm):
        st.session_state['messages'].append({"role": "user", "content": prompt})
        retrived_query = db.similarity_search(prompt)[0].page_content
        context = "Question: " + prompt +\
        "\n Answer: " + retrived_query
        prompt = f"""Here is the context: {context}\
                    Using the relevant information from the context,\
                    provide an answer to the query: {prompt}."\
                    If the context doesn't provide \
                    any relevant information, \
                    answer with \
                    [I couldn't find a good match in the \
                    document database for your query]
                    """

        response= llm(prompt)
        st.session_state['messages'].append({"role": "assistant", "content": response})
        return response
    prescription = st.file_uploader("Upload your prescription", type=['png', 'jpg', 'jpeg', 'pdf'])
    enhanced_prescription = None
    if ("enhanced_message" not in st.session_state or prescription) and not enhanced_prescription:
        if prescription:
            prescription_path = os.path.join(os.getcwd(), prescription.name)
            progress_bar = st.progress(0)  # Initialize progress bar
            save_uploaded_file(prescription, prescription_path)        
            st.write("Uploading prescription...")
            time.sleep(2)
            progress_bar.progress(20)
            st.write("Processing prescription...")
            prescription_text = process_prescription(
                project_id=os.getenv('PROCESSOR_PROJECT_ID'),
                location=os.getenv('PROCESSOR_LOCATION'),
                processor_id=os.getenv('PROCESSOR_ID'),
                file_path=prescription_path,
                mime_type=prescription.type,
                credentials=credentials
            )
            progress_bar.progress(50)
            st.write("Enhancing prescription...")
            
            enhanced_prescription = prescription_to_json(prescription_text, llm)
            
            st.write("Generating prescription...")
            time.sleep(1)
            progress_bar.progress(80)
            if enhanced_prescription:
                enhanced_message = "Here is your prescription:\n"
                patient = enhanced_prescription.get('patient', 'N/A')
                doctor = enhanced_prescription.get('doctor', 'N/A')
                date = enhanced_prescription.get('date', 'N/A')
                enhanced_message += f"Patient: {patient}\n"
                enhanced_message += f"Doctor: {doctor}\n"
                enhanced_message += f"Date: {date}\n"
                enhanced_message += "Medicine:\n"
                medicine = enhanced_prescription['medicine name']
                prescription_medication = {
                        "drugs_name": [],
                        "number_of_times": [],
                        "side_effects": [],
                }
                for key, value in medicine.items():
                    enhanced_message += f"{key}: {value}\n"
                    query = f"What are the side effects of {key}?"
                    side_effects = db.similarity_search(query)[0].page_content
                    context = "Question: " + query[0] +\
                    "\n Answer: " + side_effects
                    prompt = f"""Here is the context: {context}\
                                Using the relevant information from the context,\
                                provide an answer to the query: {query}."
                                If the context doesn't provide \
                                any relevant information, \
                                answer with \
                                [I couldn't find a good match in the \
                                document database for your query]
                                """
                    side_effect_prompt = HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                            template=prompt,
                            input_variables=["context", "query"],
                        )
                    )

                    chat_prompt_template = ChatPromptTemplate.from_messages([side_effect_prompt])

                    llm = VertexAI()

                    chain = LLMChain(llm=llm, prompt=chat_prompt_template, verbose=True)


                    llm_response = chain({"context":context, "query": query})
                    prescription_medication["drugs_name"].append(key)
                    prescription_medication["number_of_times"].append(value)
                    prescription_medication["side_effects"].append(llm_response['text'])
                    enhanced_message += f"Side effects: {llm_response['text']}\n"
                    enhanced_message += "------------------------\n"
                time.sleep(1)
                progress_bar.progress(100)       
                status = st.empty()
                status.write("Done!")
                st.session_state['generated'].append(enhanced_message)
                st.session_state['past'].append(' ')
                st.session_state['enhanced_message'] = enhanced_message
                prescription_detailes = {
                        "patient": patient,
                        "doctor": doctor,
                        "date": date,
                    }
                st.session_state['prescription_detailes'] = prescription_detailes
                st.session_state['prescription_medication'] = prescription_medication            
                if os.path.exists(prescription_path):
                    os.remove(prescription_path)

            else:
                status = st.empty()
                st.session_state['generated'].append("Error processing prescription")
                st.session_state['past'].append(' ')
                if os.path.exists(prescription_path):
                    os.remove(prescription_path)
                status.write("Please upload a good quality image of your prescription")

    response_container = st.container()
    container = st.container()



    # clear_button = st.sidebar.button("Clear Conversation", key="clear")
    # if clear_button:
    #     st.session_state['generated'] = []
    #     st.session_state['past'] = []
    #     st.session_state['messages'] = [
    #         {"role": "system", "content": "You are a helpful assistant."}
    #     ]

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = generate_response(user_input, llm)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))
        