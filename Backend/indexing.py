from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()


class YouTubeIndexer:
    """
    Creates a FAISS vector database from a transcript.
    """

    def __init__(self):

        self.embeddings = OpenAIEmbeddings()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def split_transcript(self, transcript):
        """
        Converts transcript into LangChain Documents.
        """

        documents = []

        for chunk in transcript:

            documents.append(
                Document(
                    page_content=chunk["text"],
                    metadata={
                        "start": chunk["start"],
                        "duration": chunk["duration"]
                    }
                )
            )

        return self.text_splitter.split_documents(documents)

    def create_vector_store(self, documents):
        """
        Generate embeddings and create a FAISS vector database.
        """

        vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )

        vector_store.save_local("vectorstore")

        return vector_store

    def index_video(self, transcript):
        """
        Complete indexing pipeline.
        """

        print("✅ Transcript received from frontend")

        # Save the raw full transcript text too — needed later for
        # whole-video questions ("summarize this", "what's it about")
        # that plain chunk retrieval can't answer well.
        full_text = "\n".join(chunk["text"] for chunk in transcript)
        os.makedirs("vectorstore", exist_ok=True)
        with open("vectorstore/full_transcript.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        documents = self.split_transcript(transcript)
        print("✅ Transcript split into chunks")

        vector_store = self.create_vector_store(documents)
        print("✅ Vector store created")

        return vector_store