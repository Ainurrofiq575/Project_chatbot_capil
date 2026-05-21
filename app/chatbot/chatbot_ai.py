import pickle
import requests
# pyrefly: ignore [missing-import]
import faiss
import numpy as np
import tempfile

from sentence_transformers import SentenceTransformer

# =========================
# LINK HUGGING FACE
# =========================
PKL_URL = (
    "https://huggingface.co/"
    "Ainrrofiq/chatbot-disdukcapil/"
    "resolve/main/disdukcapil_data.pkl"
)

FAISS_URL = (
    "https://huggingface.co/"
    "Ainrrofiq/chatbot-disdukcapil/"
    "resolve/main/disdukcapil_index.faiss"
)

# =========================
# LOAD MODEL
# =========================
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================
# LOAD DATA PKL
# =========================
print("Loading PKL...")

pkl_response = requests.get(PKL_URL)

data = pickle.loads(
    pkl_response.content
)

# =========================
# LOAD FAISS
# =========================
print("Loading FAISS...")

faiss_response = requests.get(
    FAISS_URL
)

# buat file sementara
with tempfile.NamedTemporaryFile(
    delete=False
) as tmp:

    tmp.write(
        faiss_response.content
    )

    temp_path = tmp.name

# load faiss
index = faiss.read_index(
    temp_path
)

# =========================
# CHATBOT RESPONSE
# =========================
def chatbot_response(question):

    embedding = model.encode([question])
    embedding = np.array(embedding, dtype=np.float32)

    D, I = index.search(embedding, k=1)

    idx = int(I[0][0])
    distance = float(D[0][0])

    if distance > 2.0:
        return "Maaf, saya belum menemukan informasi yang sesuai."

    return data["answers"][idx]