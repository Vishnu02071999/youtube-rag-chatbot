from dotenv import load_dotenv
from langchain_core import documents
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from videoid_extractor import YouTubeUtils

load_dotenv()


class YouTubeIndexer:
    """
    Creates a FAISS vector database from a YouTube video's transcript.
    """

    def __init__(self):
        self.embeddings = OpenAIEmbeddings()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def fetch_transcript(self, url):
        video_id = YouTubeUtils.extract_video_id(url)

        print("=" * 60)
        print("Original URL :", url)
        print("Extracted ID :", video_id)
        print("=" * 60)

        api = YouTubeTranscriptApi()
        transcript = api.fetch(
        video_id,
        languages=["en"]
    )

        return transcript

        

    def split_transcript(self, transcript):
        documents = []
        for chunk in transcript:
            documents.append(Document(
                page_content=chunk.text,
                metadata={
                    "start": chunk.start,
                    "duration": chunk.duration
                }
                )
            )

        split_docs = self.text_splitter.split_documents(documents)
        return split_docs

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

    def index_video(self, url: str):
        """
        Complete indexing pipeline.
        """

        transcript = self.fetch_transcript(url)

        documents = self.split_transcript(transcript)

        vector_store = self.create_vector_store(documents)

        return vector_store


if __name__ == "__main__":

    url = input("Enter YouTube URL: ")

    try:

        indexer = YouTubeIndexer()

        indexer.index_video(url)

        print("✅ Video indexed successfully!")

    except TranscriptsDisabled:
        print("This video doesn't have captions.")

    except Exception as e:
        print(f"Error: {e}")