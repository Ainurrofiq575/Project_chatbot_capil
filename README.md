# 🤖 Chatbot Disdukcapil & Sistem Pengajuan Layanan Kependudukan

Aplikasi web modern berbasis **FastAPI** yang mengintegrasikan sistem administrasi pengajuan layanan kependudukan (Dinas Kependudukan dan Pencatatan Sipil) dengan **Chatbot AI** menggunakan metode **RAG (Retrieval-Augmented Generation)** berbasis **FAISS** dan **SentenceTransformers**.

Aplikasi ini memudahkan masyarakat untuk mengajukan dokumen kependudukan seperti perubahan Kartu Keluarga (KK) dan status pendidikan secara online, sekaligus mendapatkan jawaban instan dari Chatbot AI mengenai persyaratan kependudukan secara akurat.

---

## ✨ Fitur Utama

### 👤 Fitur User (Masyarakat)
- **Chatbot AI Interaktif (RAG)**: Chatbot cerdas yang dapat menjawab pertanyaan seputar layanan Disdukcapil. Pencarian jawaban cepat menggunakan model embedding `all-MiniLM-L6-v2` dan indeks **FAISS** yang di-host di Hugging Face.
- **Pengajuan Layanan Online**:
  - **Perubahan Kartu Keluarga (KK)**: Penambahan anggota keluarga, perubahan alamat, dll.
  - **Perubahan Status Pendidikan**: Sinkronisasi tingkat pendidikan terakhir di database kependudukan.
  - **Upload Dokumen**: Mendukung unggahan banyak dokumen bukti (multi-file upload) dengan nama file yang aman (UUID).
- **Dashboard Pengguna**: Melacak status pengajuan secara real-time (*Menunggu Verifikasi*, *Disetujui*, atau *Ditolak*), serta melihat pesan balasan dan file dokumen yang dikirim oleh Admin.
- **Kelola Profil**: Mengubah nama, email, dan mengunggah foto profil kustom.
- **Keamanan Akun**: Registrasi dan login aman menggunakan enkripsi password satu arah berbasis **Bcrypt**.

### 👑 Fitur Admin (Petugas)
- **Dashboard Statistik**: Visualisasi data statistik pengajuan menggunakan grafik interaktif (distribusi status dan jenis layanan).
- **Pemrosesan Pengajuan**: Petugas dapat menyetujui atau menolak pengajuan, menyertakan catatan, dan mengunggah dokumen balasan/hasil layanan (misalnya KK baru dalam format PDF/Gambar).
- **Riwayat & Filter**: Menyaring data pengajuan berdasarkan NIK pemohon, status verifikasi, serta bulan & tahun pengajuan.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+ dengan [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM & Driver**: [SQLAlchemy](https://www.sqlalchemy.org/) & [PyMySQL](https://pymysql.readthedocs.io/)
- **Vector Search / AI**: [FAISS (Facebook AI Similarity Search)](https://github.com/facebookresearch/faiss) & [SentenceTransformers](https://www.sbert.net/)
- **Database Utama**: MySQL / MariaDB
- **Frontend**: HTML5, Vanilla CSS (Custom sleek dark/light components), JavaScript, & Jinja2 Templates
- **Data Hosting (Model AI)**: Hugging Face (untuk index `.faiss` dan model data `.pkl`)

---

## 📋 Prasyarat Sistem

Sebelum menjalankan aplikasi, pastikan komputer Anda telah terpasang:
1. **Python 3.10** atau versi di atasnya.
2. **MySQL Server** (bisa menggunakan XAMPP, Laragon, Docker, atau MySQL Installer resmi).
3. Koneksi internet (dibutuhkan pada saat pertama kali menjalankan chatbot untuk mendownload model embeddings dari Hugging Face secara otomatis).

---

## 🚀 Panduan Instalasi & Menjalankan Project

Ikuti langkah-langkah di bawah ini untuk menjalankan project ini di komputer lokal Anda:

### 1. Clone Repository
Pertama, clone project ini ke penyimpanan lokal Anda:
```bash
git clone <URL_REPOSITORY_ANDA>
cd chatbotdisdukcapil
```

### 2. Buat & Aktifkan Virtual Environment
Sangat disarankan menggunakan virtual environment agar dependensi project tidak bentrok dengan pustaka global komputer Anda.

**Untuk Windows (CMD / PowerShell):**
```powershell
# Membuat virtual environment
python -m venv venv

# Mengaktifkan venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Mengaktifkan venv (Command Prompt)
.\venv\Scripts\activate.bat
```

**Untuk Linux / macOS:**
```bash
# Membuat virtual environment
python3 -m venv venv

# Mengaktifkan venv
source venv/bin/activate
```

### 3. Instal Dependensi Python
Instal semua modul yang diperlukan dengan menggunakan file `requirements.txt` yang sudah disediakan:
```bash
pip install -r requirements.txt
```

> [!NOTE]
> Proses instalasi `sentence-transformers` mungkin memerlukan waktu beberapa menit karena akan mengunduh dependensi PyTorch.

### 4. Setup Database MySQL
1. Jalankan MySQL Server Anda (misal: jalankan Apache & MySQL di XAMPP).
2. Buka tool database client Anda (phpMyAdmin, DBeaver, HeidiSQL, dll).
3. Buat database baru bernama `disdukcapil_ta`:
   ```sql
   CREATE DATABASE disdukcapil_ta;
   ```
4. Jalankan struktur query SQL berikut untuk membuat tabel-tabel yang diperlukan:

```sql
USE disdukcapil_ta;

-- 1. Tabel Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nik VARCHAR(50) UNIQUE NOT NULL,
    nama VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    foto_profile VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Tabel Pengajuan Layanan
CREATE TABLE IF NOT EXISTS pengajuan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nik VARCHAR(50) NOT NULL,
    nama VARCHAR(255) NOT NULL,
    jenis_layanan VARCHAR(100) NOT NULL,
    detail_pengajuan VARCHAR(255) DEFAULT NULL,
    pendidikan_lama VARCHAR(100) DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'Menunggu Verifikasi',
    catatan_user TEXT DEFAULT NULL,
    catatan_admin TEXT DEFAULT NULL,
    file_balasan VARCHAR(255) DEFAULT NULL,
    tanggal_pengajuan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nik) REFERENCES users(nik) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Tabel Dokumen Persyaratan Pengajuan
CREATE TABLE IF NOT EXISTS dokumen_pengajuan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pengajuan_id INT NOT NULL,
    nama_file VARCHAR(255) NOT NULL,
    FOREIGN KEY (pengajuan_id) REFERENCES pengajuan(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 5. Konfigurasi Koneksi Database
Secara default, koneksi database diatur pada file `database.py` dan `app/main.py`. 
Jika Anda menggunakan username/password database MySQL yang berbeda dari default (User: `root`, Password: `""`), silakan sesuaikan variabel di dalam **`database.py`**:
```python
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "disdukcapil_ta"
```
Dan sesuaikan juga fungsi `get_db()` di dalam **`app/main.py`** baris 20-27:
```python
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="disdukcapil_ta",
        cursorclass=pymysql.cursors.DictCursor
    )
```

### 6. Menjalankan Migrasi Password (Opsional)
Jika Anda mengimpor data user mentah yang password-nya belum terenkripsi (masih berupa plain text), Anda dapat menjalankan skrip migrasi password untuk mengenkripsinya ke dalam Bcrypt:
```bash
python migrate_password.py
```

### 7. Membuat Akun Admin
Untuk masuk ke sistem admin (`/admin`), Anda perlu mengubah kolom `role` menjadi `admin` pada database secara manual melalui tool database client Anda setelah Anda berhasil mendaftar (register) melalui website.
```sql
UPDATE users SET role = 'admin' WHERE email = 'email_admin_anda@example.com';
```

---

## 🖥️ Cara Menjalankan Aplikasi

### Menjalankan Server Web (FastAPI)
Untuk menjalankan aplikasi web di mode development (dengan fitur auto-reload), jalankan perintah berikut:
```bash
uvicorn app.main:app --reload
```
Setelah server berjalan, Anda dapat membuka aplikasi melalui browser Anda di alamat:
- **Aplikasi Web**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Dokumentasi API Otomatis (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Menguji Chatbot AI di Terminal
Anda juga dapat menguji kecerdasan respon chatbot AI secara langsung di terminal Anda tanpa harus membuka website dengan menjalankan perintah:
```bash
python test_chatbot.py
```

---

## 📁 Struktur Direktori Project
```text
chatbotdisdukcapil/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Endpoint utama web & API FastAPI
│   │
│   ├── chatbot/
│   │   ├── __init__.py
│   │   └── chatbot_ai.py       # Logika chatbot RAG (FAISS + SentenceTransformers)
│   │
│   └── templates/              # File HTML (Jinja2)
│       ├── base.html           # Layout dasar website
│       ├── index.html          # Halaman beranda
│       ├── chatbot.html        # Halaman chatbot AI
│       ├── login.html          # Halaman masuk
│       ├── register.html       # Halaman daftar
│       ├── dashboard.html      # Halaman dashboard user
│       ├── admin_dashboard.html# Dashboard utama admin
│       └── ...
│
├── static/                     # Aset statis website
│   ├── css/                    # File stylesheet CSS kustom
│   ├── images/                 # Gambar & ikon
│   ├── uploads/                # Berkas dokumen unggahan user & admin
│   ├── script.js               # Logika frontend
│   └── style.css               # Gaya styling visual utama
│
├── database.py                 # Konfigurasi SQLAlchemy
├── migrate_password.py         # Skrip enkripsi password migrasi
├── test_chatbot.py             # CLI test tool untuk Chatbot AI
├── requirements.txt            # Daftar pustaka & dependensi project
└── README.md                   # Panduan dokumentasi project (File ini)
```

---

## ⚠️ Troubleshooting Umum
1. **Error `ModuleNotFoundError: No module named 'faiss'`**:
   Pastikan Anda menginstal `faiss-cpu` di sistem operasi Anda. Windows terkadang membutuhkan versi Python modern dan tools C++ terpasang.
2. **Error database `pymysql.err.OperationalError`**:
   Pastikan database server MySQL Anda dalam keadaan aktif dan kredensial (host, username, password) di file `database.py` serta `app/main.py` sudah sesuai dengan pengaturan lokal Anda.
3. **Download Model Lambat**:
   Pada run pertama, program akan mendownload model `all-MiniLM-L6-v2` dari Hugging Face (sekitar ~90MB) serta mengambil data FAISS. Proses ini otomatis berjalan sekali saja di awal, run berikutnya akan sangat cepat karena menggunakan local cache.
