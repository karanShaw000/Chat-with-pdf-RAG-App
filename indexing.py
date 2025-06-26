import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from setup import get_vector_store




load_dotenv()


def index(pdf_path, pdf_id, progress_setter):
    try:
        if progress_setter:
            progress_setter(20, "Loading the PDF ...")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()


        if progress_setter:
            progress_setter(40, "Splitting into Chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=400
        )

        split_docs = text_splitter.split_documents(documents=docs)

        for doc in split_docs:
            doc.metadata["pdf_id"] = pdf_id

        if progress_setter:
            vector_store = get_vector_store()
            batch_size = 10
            total_batches = (len(split_docs) + batch_size - 1)
            for idx, i in enumerate(range(0, len(split_docs), batch_size)):
                chunk = split_docs[i : i + batch_size]
                vector_store.add_documents(chunk)
                progress = 60 + int((idx / total_batches) * 40) # From 60 to 100
                progress_setter(progress, f"Storing embeddings...({idx}/{total_batches} batches)")
                time.sleep(3) # Throting for limit the gemini request

        if progress_setter:
            progress_setter(100, "Indexing Done!!!")
    except Exception as e:
        raise Exception(f"Something went wrong during Ingestion!!--{str(e)}")
