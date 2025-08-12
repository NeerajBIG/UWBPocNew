from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

import os
import tempfile
import uuid
import pandas as pd
import re

def clean_filename(filename):
    # Regular expression to find "(number)" pattern
    new_filename = re.sub(r'\s\(\d+\)', '', filename)
    new_filename = new_filename.replace(" ", "")
    return new_filename

def get_pdf_text(uploaded_file):
    temp_file = ""
    try:
        # Read file content
        #input_file = uploaded_file.read()

        input_file = uploaded_file

        # Create a temporary file (PyPDFLoader requires a file path to read the PDF,
        # it can't work directly with file-like objects or byte streams that we get from Streamlit's uploaded_file)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(input_file)
        temp_file.close()

        # load PDF document
        loader = PyPDFLoader(temp_file.name)
        documents = loader.load()

        return documents

    finally:
        # Ensure the temporary file is deleted when we're done with it
        os.unlink(temp_file.name)

def split_document(documents, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap,
                                                   length_function=len,
                                                   separators=["\n\n", "\n", " "])

    return text_splitter.split_documents(documents)

def get_embedding_function(api_key):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=api_key
    )
    return embeddings

def create_vectorstore(chunks, embedding_function, file_name, vector_store_path="db"):
    # Create a list of unique ids for each document based on the content
    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in chunks]

    # Ensure that only unique docs with unique ids are kept
    unique_ids = set()
    unique_chunks = []

    unique_chunks = []
    for chunk, id in zip(chunks, ids):
        if id not in unique_ids:
            unique_ids.add(id)
            unique_chunks.append(chunk)

            # Create a new Chroma database from the documents
    vectorstore = Chroma.from_documents(documents=unique_chunks,
                                        collection_name=clean_filename(file_name),
                                        embedding=embedding_function,
                                        ids=list(unique_ids),
                                        persist_directory=vector_store_path)
    vectorstore.persist()

    return vectorstore

def create_vectorstore_from_texts(documents, api_key, file_name):
    # Step 2 split the documents
    docs = split_document(documents, chunk_size=1000, chunk_overlap=200)

    # Step 3 define embedding function
    embedding_function = get_embedding_function(api_key)

    # Step 4 create a vector store
    vectorstore = create_vectorstore(docs, embedding_function, file_name)

    return vectorstore

def load_vectorstore(file_name, api_key, vectorstore_path="db"):
    embedding_function = get_embedding_function(api_key)
    return Chroma(persist_directory=vectorstore_path,
                  embedding_function=embedding_function,
                  collection_name=clean_filename(file_name))


# Prompt template
PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer
the question. Answer by reading content from the file. Do not assume anything.
If you don't know the answer, say that you
don't know. DON'T MAKE UP ANYTHING.

{context}
---
Answer the question based on the above context: {question}
"""


class AnswerWithSources(BaseModel):
    """An answer to the question, with sources and reasoning."""
    answer: str = Field(description="Answer to question")
    sources: str = Field(description="Full direct text chunk from the context used to answer the question")
    reasoning: str = Field(description="Explain the reasoning of the answer based on the sources")


class ExtractedInfoWithSources(BaseModel):
    Report_Title: AnswerWithSources
    Report_Summary: AnswerWithSources
    Report_Date: AnswerWithSources
    Test_Results_Overview: AnswerWithSources
    Test_Results_Count_Passed: AnswerWithSources
    Test_Results_Count_Failed: AnswerWithSources


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def query_document(vectorstore, query, api_key):
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

    retriever = vectorstore.as_retriever(search_type="similarity")

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | llm.with_structured_output(ExtractedInfoWithSources, strict=True)
    )

    structured_response = rag_chain.invoke(query)
    df = pd.DataFrame([structured_response.dict()])

    # Transforming into a table with two rows: 'answer' and 'source'
    answer_row = []
    source_row = []
    reasoning_row = []

    for col in df.columns:
        answer_row.append(df[col][0]['answer'])
        source_row.append(df[col][0]['sources'])
        reasoning_row.append(df[col][0]['reasoning'])

    # Create new dataframe with two rows: 'answer' and 'source'
    structured_response_df = pd.DataFrame([answer_row, source_row, reasoning_row], columns=df.columns,
                                          index=['answer', 'source', 'reasoning'])

    return structured_response_df.T