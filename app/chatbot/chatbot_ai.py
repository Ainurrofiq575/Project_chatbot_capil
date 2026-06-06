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
# UTILS: FORMAT REQUIREMENTS AS LIST
# =========================
def format_requirements(text):
    # Check if the text matches requirement patterns and has commas
    requirement_starters = ("fotokopi", "surat", "kutipan", "paspor", "keputusan", "salinan", "dokumen")
    if not (text.strip().lower().startswith(requirement_starters) and "," in text):
        return text

    clean_text = text.strip()
    if clean_text.endswith("."):
        clean_text = clean_text[:-1]

    # Normalize separators into a single temporary splitter
    normalized = clean_text
    normalized = normalized.replace(", serta ", "|||")
    normalized = normalized.replace(", dan ", "|||")
    normalized = normalized.replace(", ", "|||")
    
    raw_items = normalized.split("|||")
    items = []
    for item in raw_items:
        item = item.strip()
        if not item:
            continue
            
        # Clean up leading conjunctions
        if item.lower().startswith("serta "):
            item = item[6:]
        elif item.lower().startswith("dan "):
            item = item[4:]
            
        if item:
            # Capitalize the first letter of each item
            item = item[0].upper() + item[1:]
            items.append(item)
            
    if len(items) <= 1:
        return text
        
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))


# =========================
# CHATBOT RESPONSE
# =========================
def chatbot_response(question):

    allowed_keywords = [
        "ktp", "kk", "kartu keluarga", "kia",
        "akta", "kelahiran", "kematian",
        "pindah", "datang",
        "perkawinan", "perceraian",
        "pengakuan anak", "pengesahan anak",
        "perubahan nama",
        "dokumen", "hilang", "rusak",
        "disdukcapil", "kependudukan",
        "syarat", "persyaratan", "prosedur", "cara"
    ]

    question_lower = question.lower()

    if not any(keyword in question_lower for keyword in allowed_keywords):
        return (
            "Maaf, saya hanya dapat menjawab pertanyaan "
            "seputar layanan administrasi kependudukan Disdukcapil. "
            "Silakan ketik 'menu' untuk melihat daftar layanan."
        )

    embedding = model.encode([question])
    embedding = np.array(embedding, dtype=np.float32)

    D, I = index.search(embedding, k=1)

    idx = int(I[0][0])
    distance = float(D[0][0])

    if distance > 1.5:
        return (
            "Maaf, informasi tersebut belum tersedia di dataset chatbot. "
            "Silakan ketik 'menu' untuk melihat layanan yang tersedia."
        )

    return data["answers"][idx]
    return format_requirements(ans)