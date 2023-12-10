from abc import ABC, abstractmethod
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from vectordb import Config, ZillizConnectorFactory
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class LoaderFactory(ABC):
    @abstractmethod
    def create_loader(self):
        pass


class CSVLoaderFactory(LoaderFactory):
    def create_loader(self, file_path, source_column="drug_name"):
        return CSVLoader(file_path, source_column=source_column,
                         encoding="utf-8", csv_args={
                'delimiter': ','}
                            )


class EmbedderFactory(ABC):
    @abstractmethod
    def create_embedder(self):
        pass


class OpenAIEmbedderFactory(EmbedderFactory):
    def create_embedder(self):
        return OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


class DocumentLoader:
    def __init__(self, loader_factory, file_path=None, source_column="drug_name"):
        self.loader = loader_factory.create_loader(file_path, source_column=source_column)

    def load_documents(self):
        try:
            return self.loader.load()
        except Exception as e:
            print(f"Error loading documents: {e}")
            raise e


class ConnectorFactory:
    def __init__(self, db_factory, embedder_factory):
        self.db_factory = db_factory
        self.embedder_factory = embedder_factory

    def create_connector(self, config, docs):
        embeddings = self.embedder_factory.create_embedder()
        return self.db_factory.create_db(config, docs=docs, embeddings=embeddings)


class DocumentProcessor:
    def __init__(self, loader, connector_factory):
        self.loader = loader
        self.connector_factory = connector_factory
        self.db = None

    def process(self, config):
        docs = self.loader.load_documents()
        non_empty_docs = [doc for doc in docs if doc is not None]
        connector = self.connector_factory.create_connector(config, non_empty_docs)
        connector.connect()
        self.db = connector.get_db()
        return self.db


if __name__ == "__main__":

    config = Config()
    embedder_factory = OpenAIEmbedderFactory()
    db_factory = ZillizConnectorFactory()
    loader_factory = CSVLoaderFactory()

    document_loader = DocumentLoader(loader_factory, file_path=os.path.join(os.getcwd(), "data", "mini_enhanced_db.csv"), source_column="drug_name")
    connector_factory = ConnectorFactory(db_factory, embedder_factory)

    processor = DocumentProcessor(document_loader, connector_factory)
    db = processor.process(config)