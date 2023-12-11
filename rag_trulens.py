from trulens_eval import TruChain, Feedback, Tru, LiteLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate
from trulens_eval.tru_custom_app import instrument


class RAGMediMate:
    def __init__(self, db, llm):
        self.db = db
        self.llm = llm
        self.response = None
    @instrument
    def retrieve(self, query: str) -> list:
        """
        Retrieve relevant text from vector store.
        """
        results = self.db.similarity_search(query)
        return results[0].page_content

    @instrument
    def generated_response(self, query: str, context: str) -> str:
        """
        Generate answer from context.
        """
        prompt = f"""Here is the context: {context}
             Using the relevant information from the context,
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

        chain = LLMChain(llm=self.llm, prompt=chat_prompt_template, verbose=True)

        llm_response = chain({"context":context, "query": query})
        self.response = llm_response["text"]
        return self.response

    @instrument
    def query(self, query: str) -> str:
        context = self.retrieve(query)
        res = self.generated_response(query, context)
        return res

