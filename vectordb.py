import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from langchain.vectorstores import Chroma
from langchain.vectorstores import Milvus
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

@dataclass
class Config:
    persist_directory: str = os.path.join(os.getcwd(), "chroma_db")
    zilliz_uri:str = os.getenv("ZILLIZ_CLOUD_URI")
    zilliz_token:str = os.getenv("ZILLIZ_CLOUD_API_KEY")


class VectorDBFactory(ABC):
    @abstractmethod
    def create_db(self, config: Config, docs, embeddings=None):
        pass


class ChromaConnector:
    def __init__(self, config: Config, docs=None, embeddings=None):
        self.config = config
        self.embeddings = embeddings
        self.docs = docs
        self.db = None

    def connect(self):
        if not os.path.exists(self.config.persist_directory):
            if self.docs is None:
                raise Exception("Documents must be provided to create a new database")
            self._create_new_db()
        else:
            self._load_existing_db()

    def _create_new_db(self):
        self.db = Chroma.from_documents(self.docs, self.embeddings, self.config.persist_directory)

    def _load_existing_db(self):
        self.db = Chroma(self.embeddings, self.config.persist_directory)

    def get_db(self):
        return self.db


class ChromaConnectorFactory(VectorDBFactory):
    def create_db(self, config: Config, docs, embeddings=None):
        return ChromaConnector(config, docs, embeddings)



class ZillizConnector:
    def __init__(self, config: Config, docs=None, embeddings=None):
        self.config = config
        self.embeddings = embeddings
        self.docs = docs
        self.db = None

    def connect(self):
        self.db = Milvus.from_documents(self.docs, 
                              self.embeddings,
                              collection_name="medimate", 
                              connection_args ={
                                  "uri": self.config.zilliz_uri,
                                    "token": self.config.zilliz_token,
                                    "secure": True
                              }
                                )
                              
    def get_db(self):
        return self.db
    
class ZillizConnectorFactory(VectorDBFactory):
    def create_db(self, config: Config, docs, embeddings=None):
        return ZillizConnector(config, docs, embeddings)

# Usage example:
if __name__ == "__main__":
    from langchain.embeddings.openai import OpenAIEmbeddings

    config = Config()
    embeddings = OpenAIEmbeddings()
    connector_factory = ChromaConnectorFactory()
    connector = connector_factory.create_db(config, docs=None, embeddings=embeddings)
    connector.connect()
    db_instance = connector.get_db()