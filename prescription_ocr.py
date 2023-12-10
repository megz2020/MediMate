from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from typing import Dict
from utils import convert_text_to_dict
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate

def process_prescription(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    field_mask = None,
    processor_version_id= None,
    credentials = None
) -> str:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials= credentials)

    if processor_version_id:
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:

        name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    process_options = documentai.ProcessOptions(
        individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
            pages=[1]
        )
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)
    document = result.document


    return document.text


def prescription_to_json(prescription:str, llm) -> Dict:
    """
    Convert prescription text to json
    """
    
    medical_prescription_template = """\
    For the following text, extract the following information:
    - medicine name : list of medicine names that are mentioned in the text
    - taken number : number of times a day the medicine should be taken for each medicine name
    - patient name : name of the patient
    - doctor name : name of the doctor
    - date : date of the prescription
    text: {text}
    << FORMATTING >>
    Return a markdown code snippet with a Json  object formatted like this:
    ```json
        {{
        "medicine name": taken_number,
        "patient": "patient_name",
        "doctor": "doctor_name",
        "date": "date",
        }}
        ```
    """

    full_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        template=medical_prescription_template,
        input_variables=["text"],
    )
)
    chat_prompt_template = ChatPromptTemplate.from_messages([full_prompt])
    chat_prompt_template = ChatPromptTemplate.from_messages([full_prompt])
    chain = LLMChain(llm=llm, prompt=chat_prompt_template, verbose=True)
    llm_response = chain(prescription)
    uncleaned_data = llm_response["text"].split('\n')

    input_text = uncleaned_data[2:-2]
    cleaned_data = convert_text_to_dict(input_text)

    return cleaned_data




