from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

load_dotenv()


class YouTubeChatbot:

    def __init__(self):

        self.llm = ChatOpenAI (
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=1000
        )

        self.embeddings = OpenAIEmbeddings()

        self.vectorstore = FAISS.load_local(
            "vectorstore",
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 6, "fetch_k": 10}
        )

        self.store = {}

        self.chain = self.build_chain()

    def get_session_history(self, session_id: str):

        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()

        return self.store[session_id]

    def clear_chat(self, session_id="youtube_chat"):
        """
        Clears the chat history for a given session.
        """
        if session_id in self.store:
            self.store[session_id].clear()
    

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """
        Convert seconds to MM:SS format.
        """

        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        return f"{minutes:02}:{seconds:02}"

    def build_chain(self):

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Given a chat history and the latest user question,
rewrite the question so that it can be understood without the chat history.

Do NOT answer the question.

Only rewrite it if necessary.
Otherwise return it unchanged."""
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm,
            self.retriever,
            contextualize_q_prompt
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful and highly intelligent AI assistant.

Answer using the provided transcript context.
Give a thorough, detailed answer — at least 5-6 sentences when the
context supports it. Explain the reasoning, add relevant detail from
the context, and elaborate rather than giving a one-line answer.

If the answer is not available in the transcript, simply say:

'I couldn't find any information related to the context you mentioned in the available knowledge base. Please try rephrasing your question or providing more specific details'

Context:
{context}
"""
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        question_answer_chain = create_stuff_documents_chain(
            self.llm,
            qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            question_answer_chain
        )

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        return conversational_rag_chain

    def ask(self, question: str, session_id: str):
      # Run the conversational RAG chain
      response = self.chain.invoke(
        {"input": question},
        config={
            "configurable": {
                "session_id": session_id
            }
        }
        )

      # Use the documents actually retrieved/used by the chain
      # (avoids re-retrieving with the raw, non-contextualized question)
      retrieved_docs = response.get("context", [])

      timestamp = None

      if retrieved_docs:
        start = retrieved_docs[0].metadata.get("start")

        if start is not None:
            timestamp = self.format_timestamp(start)

      return {
        "answer": response["answer"],
        "timestamp": timestamp
      }

if __name__ == "__main__":

    chatbot = YouTubeChatbot()

    print("\n🎥 YouTube Chatbot")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        response = chatbot.ask(
    question,
    "youtube_chat"
       )

        print("\nBot:", response["answer"])

        if response["timestamp"]:
            print(f"\n📍 Mentioned around {response['timestamp']}")

        print()