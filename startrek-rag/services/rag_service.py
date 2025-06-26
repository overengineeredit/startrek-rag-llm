import logging
from typing import Any, Dict, List, Optional

from config import config
from db_config import get_collection
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

logger = logging.getLogger(__name__)


class RAGService:
    """Service class for RAG (Retrieval-Augmented Generation) operations."""

    def __init__(self):
        self.llm = None
        self.collection = None
        self._initialize_components()

    def _initialize_components(self):
        """Initialize LLM and database components."""
        try:
            # Initialize Ollama client
            self.llm = ChatOllama(model=config.ollama.model, base_url=config.ollama_url)
            logger.info(f"Initialized Ollama client with model={config.ollama.model}")

            # Initialize database collection
            self.collection = get_collection()
            logger.info("Initialized database collection")

        except Exception as e:
            logger.error(f"Failed to initialize RAG components: {e}")
            raise

    def _get_prompt_templates(self):
        """Get prompt templates for query expansion and answering."""
        query_expansion_prompt = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five
            different versions of the given user question to retrieve relevant documents from
            a vector database. By generating multiple perspectives on the user question, your
            goal is to help the user overcome some of the limitations of the distance-based
            similarity search. Provide these alternative questions separated by newlines.
            Original question: {question}""",
        )

        answer_prompt = ChatPromptTemplate.from_template(
            """Answer the question based ONLY on the following context:
            {context}
            Question: {question}
            """
        )

        return query_expansion_prompt, answer_prompt

    def query(self, question: str, num_results: int = 5) -> Optional[str]:
        """
        Process a query using RAG.

        Args:
            question: The user's question
            num_results: Number of documents to retrieve

        Returns:
            Generated answer or None if failed
        """
        if not question:
            logger.warning("Empty question provided")
            return None

        try:
            logger.info(f"Processing query: {question}")

            # Retrieve relevant documents
            if not self.collection:
                logger.error("Collection not initialized")
                return None

            results = self.collection.query(
                query_texts=[question], n_results=num_results
            )

            if not results or "documents" not in results:
                logger.warning("No results returned from query")
                return "I don't have enough information to answer that question."

            documents = results.get("documents")
            if not documents or not isinstance(documents, list) or len(documents) == 0:
                logger.warning("No documents in results")
                return "I don't have enough information to answer that question."

            retrieved_docs = documents[0]
            if not retrieved_docs:
                logger.warning("No relevant documents found")
                return "I don't have enough information to answer that question."

            context = "\n".join(retrieved_docs)

            if not context:
                logger.warning("No relevant documents found")
                return "I don't have enough information to answer that question."

            # Generate answer using LLM
            if not self.llm:
                logger.error("LLM not initialized")
                return None

            _, answer_prompt = self._get_prompt_templates()

            chain = (
                {"context": lambda _: context, "question": RunnablePassthrough()}
                | answer_prompt
                | self.llm
                | StrOutputParser()
            )

            response = chain.invoke(question)
            logger.info("Query processed successfully")

            return response

        except Exception as e:
            logger.exception(f"Error processing query: {e}")
            return None

    def add_document(
        self, document: str, metadata: Dict[str, Any], doc_id: str
    ) -> bool:
        """
        Add a document to the vector database.

        Args:
            document: The document text
            metadata: Document metadata
            doc_id: Unique document identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.collection:
                logger.error("Collection not initialized")
                return False

            # Get embedding for the document
            from embed import get_embedding

            embedding = get_embedding(document)

            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[document],
                metadatas=[metadata],
                ids=[doc_id],
            )

            logger.info(f"Document {doc_id} added successfully")
            return True

        except Exception as e:
            logger.exception(f"Error adding document {doc_id}: {e}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            if not self.collection:
                logger.error("Collection not initialized")
                return {"error": "Collection not initialized"}

            count = self.collection.count()
            return {
                "document_count": count,
                "collection_name": config.database.collection_name,
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}


# Global service instance
rag_service = RAGService()
