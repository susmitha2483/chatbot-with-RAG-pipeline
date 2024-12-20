from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from text_to_doc import get_doc_chunks
from web_crawler import get_data_from_website
from prompt import get_prompt
from langchain.chains import ConversationalRetrievalChain

# 1. Get Chroma Client - Initialize and return Chroma vector store
def get_chroma_client():
    embedding_function = OpenAIEmbeddings()
    return Chroma(
        collection_name="website_data",
        embedding_function=embedding_function,
        persist_directory="data/chroma"
    )

# 2. Store Docs - Scrape website content, split into chunks, and store in Chroma
def store_docs(url):
    text, metadata = get_data_from_website(url)
    docs = get_doc_chunks(text, metadata)
    vector_store = get_chroma_client()
    vector_store.add_documents(docs)
    vector_store.persist()

# 3. Make Chain - Create a ConversationalRetrievalChain for handling queries
def make_chain():
    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0, verbose=True)
    vector_store = get_chroma_client()
    prompt = get_prompt()
    retriever = vector_store.as_retriever(search_type="mmr", verbose=True)

    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs=dict(prompt=prompt),
        verbose=True,
        rephrase_question=False,
    )
    return chain

# 4. Get Response - Generate a response using the RAG pipeline
def get_response(question, organization_name, organization_info, contact_info):
    chat_history = ""
    chain = make_chain()
    response = chain({
        "question": question,
        "chat_history": chat_history,
        "organization_name": organization_name,
        "contact_info": contact_info,
        "organization_info": organization_info
    })
    return response['answer']
