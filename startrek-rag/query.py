import os
import logging
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from db_config import get_collection

# Configure logging
logger = logging.getLogger(__name__)

LLM_MODEL = os.getenv('LLM_MODEL', 'mistral')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')

logger.info(f"Initializing query module with LLM_MODEL={LLM_MODEL}, OLLAMA_HOST={OLLAMA_HOST}")

# Function to get the prompt templates for generating alternative questions and answering based on context
def get_prompt():
    logger.debug("Getting prompt templates")
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    logger.debug("Prompt templates created successfully")
    return QUERY_PROMPT, prompt

# Main function to handle the query process
def query(input):
    if input:
        try:
            logger.info(f"Initializing Ollama client with model={LLM_MODEL}, base_url=http://{OLLAMA_HOST}:11434")
            # Initialize the language model with the specified model name and host
            llm = ChatOllama(model=LLM_MODEL, base_url=f"http://{OLLAMA_HOST}:11434")
            logger.debug("Ollama client initialized successfully")

            # Get the vector database collection
            logger.debug("Getting vector database collection")
            collection = get_collection()
            logger.debug("Vector database collection retrieved successfully")

            # Get the prompt templates
            QUERY_PROMPT, prompt = get_prompt()

            # Use the native ChromaDB client to query the collection
            logger.debug("Querying the collection using native ChromaDB client")
            results = collection.query(
                query_texts=[input],
                n_results=5
            )
            logger.debug(f"Query results: {results}")

            # Extract the retrieved documents from the results
            retrieved_docs = results.get('documents', [[]])[0]
            context = "\n".join(retrieved_docs)

            # Define the processing chain to generate the answer and parse the output
            logger.debug("Setting up processing chain")
            chain = (
                {"context": lambda _: context, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            logger.debug("Processing chain set up successfully")

            logger.info("Invoking chain with input")
            response = chain.invoke(input)
            logger.info("Chain invocation completed successfully")
            logger.debug(f"Response: {response}")

            return response
        except Exception as e:
            logger.exception("Error in query processing")
            raise

    return None