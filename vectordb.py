import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from langchain.vectorstores import Milvus
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

@dataclass
class Config:
    persist_directory: str = os.path.join(os.getcwd(), "db")
    zilliz_uri:str = os.getenv("ZILLIZ_CLOUD_URI")
    zilliz_token:str = os.getenv("ZILLIZ_CLOUD_API_KEY")


class VectorDBFactory(ABC):
    @abstractmethod
    def create_db(self, config: Config, docs, embeddings=None):
        pass



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
    connector_factory = ZillizConnectorFactory()
    connector = connector_factory.create_db(config, docs=None, embeddings=embeddings)
    connector.connect()
    db_instance = connector.get_db()