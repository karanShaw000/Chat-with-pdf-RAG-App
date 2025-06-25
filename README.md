# 💬 Chat with Your PDF — RAG Application

This is a lightweight RAG (Retrieval-Augmented Generation) application built using:

[Deployed Link](https://chat-with-pdf-rag-app.streamlit.app/)

- [Streamlit](https://streamlit.io/) for the UI
- [Google Gemini](https://ai.google.dev/)
- [Qdrant](https://qdrant.tech/) as the vector database
- [Google Generative AI Embeddings](https://ai.google.dev/docs/embedding)


---

## 🚀 Features

- Upload any PDF and index it
- Ask questions and get contextual answers
- See page references from the original document
- Storing the embedding in vectorDB by batching.

---

## 📦 Requirements

- Python 3.9+
- A [Qdrant Cloud](https://qdrant.tech/) instance (or local Qdrant)
- Google Gemini API Key
- [Streamlit](https://streamlit.io/)

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
DB_URL=https://your-qdrant-cloud-instance.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
````

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/karanShaw000/Chat-with-pdf-RAG-App.git
cd chat-with-pdf-RAG-App

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🧠 Run the App Locally

```bash
streamlit run main.py
```

Upload your PDF, let it index, and start chatting with it!

---

## 🐳 Optional: Running Qdrant Locally (for development)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Update your `.env`:

```env
DB_URL=http://localhost:6333
QDRANT_API_KEY=
```

---

## ⚠️ Common Issues

* **Field not indexed**: Ensure the `"pdf_id"` metadata is indexed before querying with a filter.

---

## 📤 Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo
4. Set environment variables in the "Secrets" section
5. Deploy!


