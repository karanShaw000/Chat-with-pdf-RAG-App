import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import Distance, VectorParams
import streamlit as st

load_dotenv()


embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


@st.cache_resource
def get_vector_store() -> QdrantVectorStore:
    COLLECTION_NAME = "Chat_PDF"
    client = QdrantClient(url=os.getenv("DB_URL"), api_key=os.getenv("QDRANT_API_KEY"), timeout=60)

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            hnsw_config=models.HnswConfigDiff(payload_m=16, m=0),
        )

    # Ensure that the 'pdf_id' field is indexed for filtering
    existing_indexes = client.get_collection(COLLECTION_NAME).payload_schema
    if "metadata.pdf_id" not in existing_indexes:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="metadata.pdf_id",
            field_schema=models.KeywordIndexParams(
                type=models.KeywordIndexType.KEYWORD,
                is_tenant=True,
            ),
        )

    vector_store = QdrantVectorStore(
        client=client, embedding=embedding_model, collection_name=COLLECTION_NAME
    )

    return vector_store
