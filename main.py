import uuid
import streamlit as st
from pathlib import Path
from indexing import index
from tempfile import NamedTemporaryFile
from chat import chat_ui


def main():
    st.set_page_config(
        page_title="Basic RAG Application",
        page_icon="📄",
        layout="centered",
    )
    st.title("💬 Chat With Your PDF")

    if "indexed" not in st.session_state:
        st.session_state.indexed = False

    if "is_indexing" not in st.session_state:
        st.session_state.is_indexing = False

    if "pdf_id" not in st.session_state:
        st.session_state.pdf_id = ""


    if "upload_key" not in st.session_state:
        st.session_state.upload_key = "uploader_1"

    def reset_uploader():
        st.session_state.upload_key = (
            f"uploader_{st.session_state.upload_key[-1]}_reset"
        )

    if not st.session_state.indexed:
        st.subheader("Let's Get Your PDF Ready for Chat!", divider="green")
        user_pdf = st.file_uploader(
            "Upload your pdf",
            type="pdf",
            accept_multiple_files=False,
            key=st.session_state.upload_key,
            disabled=st.session_state.is_indexing
        )

        if st.button("Start Indexing", disabled=st.session_state.is_indexing):
            if not user_pdf:
                st.error("PDF is required")
                reset_uploader()
            else:
                st.session_state.is_indexing = True  # Disable UI elements
                with NamedTemporaryFile(prefix=user_pdf.name, suffix=".pdf") as f:
                    f.write(user_pdf.getvalue())
                    temp_path = Path(f.name)
                    st.write(temp_path)

                    with st.empty():
                        indexing_bar = st.progress(0, text=None)

                        def progress_updater(number, message):
                            indexing_bar.progress(number, text=message)

                        try:
                            st.session_state.pdf_id = f"{uuid.uuid4()}-{user_pdf.name}"
                            index(temp_path, st.session_state.pdf_id, progress_updater)
                            st.session_state.indexed = True
                            st.rerun()
                        except Exception as e:
                            st.error(e)
    else:
        chat_ui()


if __name__ == "__main__":
    main()
