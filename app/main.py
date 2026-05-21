from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional, List
from fastapi.responses import JSONResponse
from app.chatbot.chatbot_ai import chatbot_response

import shutil
import os
import uuid
import bcrypt
import pymysql

from database import engine


def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="disdukcapil_ta",
        cursorclass=pymysql.cursors.DictCursor
    )


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret123")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

def format_detail_pengajuan(value: str) -> str:
    mapping = {
        "anggota": "Perubahan Anggota Keluarga",
        "alamat": "Perubahan Domisili/Alamat",
        "lainnya": "Perubahan Lainnya",
        "tidak_sekolah": "Tidak/Belum Sekolah",
        "belum_tamat_sd": "Belum Tamat SD/Sederajat",
        "tamat_sd": "Tamat SD/Sederajat",
        "sltp": "SLTP/Sederajat",
        "slta": "SLTA/Sederajat",
        "diploma_1_2": "Diploma I/II",
        "diploma_3": "Akademi/Diploma III/Sarjana Muda",
        "s1": "Diploma IV/Strata I",
        "s2": "Strata II"
    }
    return mapping.get(value, value or "-")

templates.env.filters["format_detail_pengajuan"] = format_detail_pengajuan



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": request.session.get("user")
        }
    )


@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chatbot.html",
        context={
            "user": request.session.get("user")
        }
    )


@app.get("/pengajuan", response_class=HTMLResponse)
async def pengajuan(request: Request):
    user = request.session.get("user")

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login_required.html",
            context={
                "user": request.session.get("user")
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="pengajuan.html",
        context={
            "user": user
        }
    )


@app.get("/pengajuan-kk", response_class=HTMLResponse)
async def pengajuan_kk(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="form_kk.html",
        context={
            "user": request.session.get("user")
        }
    )


@app.post("/pengajuan-kk")
async def submit_kk(
    request: Request,
    jenis_pengajuan: str = Form(...),
    catatan: str = Form(None),
    file_upload: List[UploadFile] = File(None)
):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                INSERT INTO pengajuan
                (
                    nik,
                    jenis_layanan,
                    detail_pengajuan,
                    nama,
                    status,
                    catatan_user
                )
                VALUES
                (
                    :nik,
                    :jenis_layanan,
                    :detail_pengajuan,
                    :nama,
                    :status,
                    :catatan_user
                )
            """),
            {
                "nik": user["nik"],
                "jenis_layanan": "Perubahan KK",
                "detail_pengajuan": jenis_pengajuan,
                "nama": user["nama"],
                "status": "Menunggu Verifikasi",
                "catatan_user": catatan
            }
        )

        conn.commit()

        pengajuan_id = result.lastrowid
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        if file_upload:
            for file in file_upload:
                if file.filename != "":
                    filename = f"{uuid.uuid4()}_{file.filename}"
                    file_path = os.path.join(upload_folder, filename)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    conn.execute(
                        text("""
                            INSERT INTO dokumen_pengajuan
                            (
                                pengajuan_id,
                                nama_file
                            )
                            VALUES
                            (
                                :pengajuan_id,
                                :nama_file
                            )
                        """),
                        {
                            "pengajuan_id": pengajuan_id,
                            "nama_file": filename
                        }
                    )

        conn.commit()

    return RedirectResponse("/dashboard", status_code=303)

@app.get("/pengajuan-pendidikan", response_class=HTMLResponse)
async def pengajuan_pendidikan(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="form_pendidikan.html",
        context={
            "user": request.session.get("user")
        }
    )


@app.post("/pengajuan-pendidikan")
async def submit_pendidikan(
    request: Request,
    nik: str = Form(...),
    nama: str = Form(...),
    pendidikan_lama: str = Form(...),
    pendidikan_baru: str = Form(...),
    catatan: str = Form(None),
    file_upload: List[UploadFile] = File(None)
):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                INSERT INTO pengajuan
                (
                    nik,
                    jenis_layanan,
                    detail_pengajuan,
                    nama,
                    pendidikan_lama,
                    status,
                    catatan_user
                )
                VALUES
                (
                    :nik,
                    :jenis_layanan,
                    :detail_pengajuan,
                    :nama,
                    :pendidikan_lama,
                    :status,
                    :catatan_user
                )
            """),
            {
                "nik": nik,
                "jenis_layanan": "Perubahan Status Pendidikan",
                "detail_pengajuan": pendidikan_baru,
                "nama": nama,
                "pendidikan_lama": pendidikan_lama,
                "status": "Menunggu Verifikasi",
                "catatan_user": catatan
            }
        )

        conn.commit()

        pengajuan_id = result.lastrowid
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        if file_upload:
            for file in file_upload:
                if file.filename != "":
                    filename = f"{uuid.uuid4()}_{file.filename}"
                    file_path = os.path.join(upload_folder, filename)

                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    conn.execute(
                        text("""
                            INSERT INTO dokumen_pengajuan
                            (
                                pengajuan_id,
                                nama_file
                            )
                            VALUES
                            (
                                :pengajuan_id,
                                :nama_file
                            )
                        """),
                        {
                            "pengajuan_id": pengajuan_id,
                            "nama_file": filename
                        }
                    )

        conn.commit()

    return RedirectResponse("/dashboard", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "user": request.session.get("user"),
            "error": error
        }
    )


@app.post("/login")
async def process_login(
    request: Request,
    nik: str = Form(...),
    password: str = Form(...)
):
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT * FROM users WHERE nik = :nik"),
            {"nik": nik}
        ).fetchone()

    if user and bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        request.session["user"] = {
            "id": user.id,
            "nik": user.nik,
            "nama": user.nama,
            "email": user.email,
            "role": user.role,
            "foto_profile": user.foto_profile
        }

        if user.role == "admin":
            return RedirectResponse("/admin", status_code=303)

        return RedirectResponse("/dashboard", status_code=303)

    return RedirectResponse("/login?error=NIK atau Password salah!", status_code=303)


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "user": request.session.get("user"),
            "error": error
        }
    )


@app.post("/register")
async def process_register(
    nik: str = Form(...),
    nama: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    print("REGISTER MASUK")
    print("NIK:", nik)
    print("NAMA:", nama)
    print("EMAIL:", email)
    print("PASSWORD SAMA:", password == confirm_password)

    if password != confirm_password:
        print("PASSWORD TIDAK SAMA")
        return RedirectResponse("/register?error=Konfirmasi password tidak cocok!", status_code=303)

    with engine.connect() as conn:
        check_user = conn.execute(
            text("SELECT * FROM users WHERE nik = :nik OR email = :email"),
            {
                "nik": nik,
                "email": email
            }
        ).fetchone()

        if check_user:
            print("USER SUDAH ADA")
            return RedirectResponse("/register?error=NIK atau Email sudah terdaftar!", status_code=303)


        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        conn.execute(
            text("""
                INSERT INTO users
                (
                    nik,
                    nama,
                    email,
                    password
                )
                VALUES
                (
                    :nik,
                    :nama,
                    :email,
                    :password
                )
            """),
            {
                "nik": nik,
                "nama": nama,
                "email": email,
                "password": hashed.decode("utf-8")
            }
        )

        conn.commit()

        print("REGISTER BERHASIL MASUK DATABASE")

    return RedirectResponse("/login", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    if user["role"] == "admin":
        return RedirectResponse("/admin", status_code=303)

    with engine.connect() as conn:
        data = conn.execute(
            text("""
                SELECT *
                FROM pengajuan
                WHERE nik = :nik
                ORDER BY id DESC
            """),
            {
                "nik": user["nik"]
            }
        ).mappings().all()

        data = [dict(row) for row in data]

        for item in data:
            if item["tanggal_pengajuan"]:
                item["tanggal_pengajuan"] = item["tanggal_pengajuan"].strftime(
                    "%d-%m-%Y %H:%M"
                )

            dokumen = conn.execute(
                text("""
                    SELECT *
                    FROM dokumen_pengajuan
                    WHERE pengajuan_id = :id
                """),
                {
                    "id": item["id"]
                }
            ).mappings().all()

            item["dokumen"] = [dict(d) for d in dokumen]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "pengajuan": data
        }
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    with engine.connect() as conn:
        data = conn.execute(
            text("""
                SELECT *
                FROM pengajuan
                ORDER BY tanggal_pengajuan DESC
            """)
        ).fetchall()

    total = len(data)

    menunggu = len([
        d for d in data
        if d.status == "Menunggu Verifikasi"
    ])

    disetujui = len([
        d for d in data
        if d.status == "Disetujui"
    ])

    ditolak = len([
        d for d in data
        if d.status == "Ditolak"
    ])

    layanan_count = {}

    for d in data:
        if d.detail_pengajuan:
            layanan = f"{d.jenis_layanan} ({d.detail_pengajuan})"
        else:
            layanan = d.jenis_layanan

        layanan_count[layanan] = layanan_count.get(layanan, 0) + 1

    status_count = {
        "Menunggu Verifikasi": menunggu,
        "Disetujui": disetujui,
        "Ditolak": ditolak
    }

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "user": user,
            "pengajuan": data,
            "total": total,
            "menunggu": menunggu,
            "disetujui": disetujui,
            "ditolak": ditolak,
            "layanan_labels": list(layanan_count.keys()),
            "layanan_values": list(layanan_count.values()),
            "status_labels": list(status_count.keys()),
            "status_values": list(status_count.values())
        }
    )


@app.post("/admin/proses/{id}")
async def proses_pengajuan(
    request: Request,
    id: int,
    status: str = Form(...),
    catatan: str = Form(None),
    file_admin: UploadFile = File(None)
):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    filename = None

    if file_admin and file_admin.filename != "":
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{uuid.uuid4()}_{file_admin.filename}"
        file_path = os.path.join(upload_folder, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file_admin.file, buffer)

    with engine.connect() as conn:
        if filename:
            conn.execute(
                text("""
                    UPDATE pengajuan
                    SET status = :status,
                        catatan_admin = :catatan,
                        file_balasan = :file_admin
                    WHERE id = :id
                """),
                {
                    "status": status,
                    "catatan": catatan,
                    "file_admin": filename,
                    "id": id
                }
            )
        else:
            conn.execute(
                text("""
                    UPDATE pengajuan
                    SET status = :status,
                        catatan_admin = :catatan
                    WHERE id = :id
                """),
                {
                    "status": status,
                    "catatan": catatan,
                    "id": id
                }
            )

        conn.commit()

    return RedirectResponse("/admin", status_code=303)


@app.get("/admin/detail/{id}", response_class=HTMLResponse)
async def admin_detail(id: int, request: Request):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    if user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    with engine.connect() as conn:
        data = conn.execute(
            text("""
                SELECT *
                FROM pengajuan
                WHERE id = :id
            """),
            {
                "id": id
            }
        ).mappings().first()

        if not data:
            return HTMLResponse("Data tidak ditemukan", status_code=404)

        dokumen = conn.execute(
            text("""
                SELECT *
                FROM dokumen_pengajuan
                WHERE pengajuan_id = :id
            """),
            {
                "id": id
            }
        ).mappings().all()

        data = dict(data)
        data["dokumen"] = [dict(d) for d in dokumen]

    return templates.TemplateResponse(
        request=request,
        name="admin_detail.html",
        context={
            "user": user,
            "item": data
        }
    )


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/edit-profile", response_class=HTMLResponse)
async def edit_profile_page(request: Request):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit_profile.html",
        context={
            "user": user
        }
    )


@app.post("/edit-profile")
async def update_profile(
    request: Request,
    nama: str = Form(...),
    email: str = Form(...),
    foto_profile: UploadFile = File(None)
):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    filename = user.get("foto_profile")

    if foto_profile and foto_profile.filename != "":
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{uuid.uuid4()}_{foto_profile.filename}"
        file_path = os.path.join(upload_folder, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto_profile.file, buffer)

    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE users
                SET nama = :nama,
                    email = :email,
                    foto_profile = :foto
                WHERE id = :id
            """),
            {
                "nama": nama,
                "email": email,
                "foto": filename,
                "id": user["id"]
            }
        )

        conn.commit()

    request.session["user"]["nama"] = nama
    request.session["user"]["email"] = email
    request.session["user"]["foto_profile"] = filename

    return RedirectResponse("/dashboard", status_code=303)


@app.get("/admin/riwayat", response_class=HTMLResponse)
async def admin_riwayat(
    request: Request,
    bulan: str = None,
    tahun: str = None
):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    query = """
        SELECT *
        FROM pengajuan
        WHERE 1=1
    """

    params = {}

    if bulan and bulan != "":
        query += " AND MONTH(tanggal_pengajuan) = :bulan"
        params["bulan"] = int(bulan)

    if tahun and tahun != "":
        query += " AND YEAR(tanggal_pengajuan) = :tahun"
        params["tahun"] = int(tahun)

    query += " ORDER BY tanggal_pengajuan DESC"

    with engine.connect() as conn:
        data = conn.execute(text(query), params).fetchall()

    return templates.TemplateResponse(
        request=request,
        name="admin_riwayat.html",
        context={
            "user": user,
            "pengajuan": data,
            "bulan_selected": bulan,
            "tahun_selected": tahun
        }
    )


@app.get("/admin/pengajuan", response_class=HTMLResponse)
async def admin_pengajuan(
    request: Request,
    status: str = "Semua",
    nik: str = None
):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    query = """
        SELECT *
        FROM pengajuan
        WHERE 1=1
    """

    params = {}

    if status != "Semua":
        query += " AND status = :status"
        params["status"] = status

    if nik and nik.strip() != "":
        query += " AND nik LIKE :nik"
        params["nik"] = f"%{nik}%"

    query += " ORDER BY tanggal_pengajuan DESC"

    with engine.connect() as conn:
        data = conn.execute(text(query), params).fetchall()

    return templates.TemplateResponse(
        request=request,
        name="admin_pengajuan.html",
        context={
            "user": user,
            "pengajuan": data,
            "selected_status": status,
            "nik_selected": nik
        }
    )


@app.get("/admin/laporan", response_class=HTMLResponse)
async def cetak_laporan(
    request: Request,
    bulan: Optional[str] = None,
    tahun: Optional[str] = None
):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    query = """
        SELECT *
        FROM pengajuan
        WHERE 1=1
    """

    params = {}

    if bulan and bulan != "":
        query += " AND MONTH(tanggal_pengajuan) = :bulan"
        params["bulan"] = int(bulan)

    if tahun and tahun != "":
        query += " AND YEAR(tanggal_pengajuan) = :tahun"
        params["tahun"] = int(tahun)

    query += " ORDER BY tanggal_pengajuan DESC"

    with engine.connect() as conn:
        data = conn.execute(text(query), params).fetchall()

    return templates.TemplateResponse(
        request=request,
        name="laporan_pengajuan.html",
        context={
            "user": user,
            "pengajuan": data,
            "bulan": bulan,
            "tahun": tahun
        }
    )


@app.get("/layanan", response_class=HTMLResponse)
async def layanan_page(request: Request):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM layanan")
    layanan = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="layanan.html",
        context={
            "layanan": layanan,
            "user": request.session.get("user")
        }
    )


@app.get("/admin/layanan", response_class=HTMLResponse)
def admin_layanan(request: Request):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM layanan
        ORDER BY id DESC
    """)

    layanan = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="admin_layanan.html",
        context={
            "user": user,
            "layanan": layanan
        }
    )


@app.get("/admin/layanan/hapus/{id}")
def hapus_layanan(request: Request, id: int):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM layanan WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/admin/layanan", status_code=303)


@app.get("/admin/layanan/edit/{id}", response_class=HTMLResponse)
def edit_layanan(request: Request, id: int):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM layanan WHERE id=%s",
        (id,)
    )

    layanan = cursor.fetchone()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="edit_layanan.html",
        context={
            "user": user,
            "layanan": layanan
        }
    )


@app.post("/admin/layanan/update/{id}")
def update_layanan(
    request: Request,
    id: int,
    judul: str = Form(...),
    waktu_proses: str = Form(...),
    deskripsi: str = Form(...)
):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE layanan
        SET judul=%s,
            waktu_proses=%s,
            deskripsi=%s
        WHERE id=%s
        """,
        (
            judul,
            waktu_proses,
            deskripsi,
            id
        )
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/admin/layanan", status_code=303)


@app.get("/admin/layanan/tambah", response_class=HTMLResponse)
def tambah_layanan_page(request: Request):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="tambah_layanan.html",
        context={
            "user": user
        }
    )


@app.post("/admin/layanan/tambah")
async def tambah_layanan_process(request: Request):
    user = request.session.get("user")

    if not user or user["role"] != "admin":
        return RedirectResponse("/dashboard", status_code=303)

    form = await request.form()

    judul = form.get("judul")
    waktu = form.get("waktu_proses")
    deskripsi = form.get("deskripsi")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO layanan
        (
            judul,
            waktu_proses,
            deskripsi
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
        """,
        (
            judul,
            waktu,
            deskripsi
        )
    )

    conn.commit()
    conn.close()

    return RedirectResponse("/admin/layanan", status_code=303)


print("Database berhasil terhubung")

# CHATBOT
@app.post("/api/chatbot")
async def api_chatbot(request: Request):

    body = await request.json()
    message = body.get("message", "").strip()

    if not message:
        return JSONResponse({
            "reply": "Silakan ketik pertanyaan terlebih dahulu."
        })

    menu = {
        "1": "Apa saja persyaratan membuat KTP baru?",
        "2": "Apa saja persyaratan Kartu Keluarga?",
        "3": "Apa saja persyaratan Akta Kelahiran?",
        "4": "Apa saja persyaratan Akta Kematian?",
        "5": "Apa saja persyaratan perubahan status pendidikan?",
        "6": "Apa saja persyaratan pindah datang?",
        "7": "Apa saja layanan Disdukcapil?"
    }


    if message in menu:
        message = menu[message]

    reply = chatbot_response(message)

    return JSONResponse({
        "reply": reply
    })