from google.genai import types
from qdrant_client.http import models
import streamlit as st
from google import genai

from setup import get_vector_store


def chat_ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.subheader("Your PDF is Now Chat-Able!", divider="green")
    if st.button("Reset"):
        st.session_state.indexed = False
        st.session_state.messages = []
        st.session_state.pdf_id = ""
        st.session_state.is_indexing = False 
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if query := st.chat_input("Ask question to the PDF"):
        with st.chat_message("user"):
            st.session_state.messages.append({"role": "user", "content": query})
            st.markdown(query)

        with st.chat_message("assistant"):
            try:
                placeholder = st.empty()
                full_response = ""
                stream = chat_logic(query, st.session_state.pdf_id)
                for chunk in stream:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(f"{full_response} ▌")

                placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            except Exception as e:
                st.error(str(e))


def chat_logic(query, pdf_id):
    try:
        vector_store = get_vector_store()
        query_result = vector_store.similarity_search(
            query=query,
            filter=models.Filter(
                should=[
                    models.FieldCondition(
                        key="metadata.pdf_id",
                        match=models.MatchValue(value=pdf_id),
                    ),
                ]
            ),
        )


        context = "\n\n\n".join(
            [
                f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}"
                for result in query_result
            ]
        )


        SYSTEM_PROMPT = f"""
                You are a helpfull AI Assistant who answers user query based on the available
                context retrieved from a PDF file along with page_contents and page number.

                You can also summarise the context.

                Rules:
                    1. Answer the user's question **only** using the context.
                    2. If the answer is found in the context, mention the page number where it appears.
                    3. If the answer is not found, respond politely that the PDF does not contain information about that question.

                    Do NOT make up information. Always refer to the content and the page number.

                Context:
                {context}
        """

        client = genai.Client()
        stream = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=query,
        )
        return stream

    except Exception as e:
        raise Exception(f"Somthing went wrong: {str(e)}")
