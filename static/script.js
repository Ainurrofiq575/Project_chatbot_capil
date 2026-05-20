// Kirim pesan saat tombol diklik
function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBody = document.getElementById("chatBody");

    const message = input.value.trim();
    if (message === "") return;

    // User message
    const userDiv = document.createElement("div");
    userDiv.classList.add("user-message");
    userDiv.textContent = message;
    chatBody.appendChild(userDiv);

    // Bot reply
    const botDiv = document.createElement("div");
    botDiv.classList.add("bot-message");

    if (message.toLowerCase().includes("kk")) {
        botDiv.textContent = "Untuk cetak ulang KK, silakan membawa KK lama dan KTP ke kantor Disdukcapil.";
    } 
    else if (message.toLowerCase().includes("golongan darah")) {
        botDiv.textContent = "Untuk ubah golongan darah, sertakan surat keterangan medis resmi.";
    } 
    else {
        botDiv.textContent = "Terima kasih atas pertanyaan Anda. Silakan hubungi kantor Disdukcapil untuk informasi lebih lanjut.";
    }

    setTimeout(() => {
        chatBody.appendChild(botDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }, 500);

    input.value = "";
}


// ==========================
// ENTER KEY SUPPORT
// ==========================
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("userInput");

    if (input) {
        input.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    }
});

// ==========================
// HAMBURGER MENU
// ==========================
document.addEventListener("DOMContentLoaded", function () {

    const hamburger = document.getElementById("hamburger");
    const navMenu = document.querySelector(".nav-menu");

    if (hamburger) {
        hamburger.addEventListener("click", function () {
            navMenu.classList.toggle("active");
        });
    }

});

// popup chatbot
function closePopup() {
    document.getElementById("popupTutorial").style.display = "none";
}

// otomatis muncul saat halaman dibuka
window.onload = function() {
    const popup = document.getElementById("popupTutorial");
    if (popup) {
        popup.style.display = "flex";
    }
};


// pengajuan
function toggleForm(id) {
    const form = document.getElementById(id);

    if (form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

// dropdown nama
function toggleDropdown() {
    const menu = document.getElementById("dropdownMenu");
    menu.style.display = menu.style.display === "flex" ? "none" : "flex";
}

// klik luar = tutup
window.onclick = function(e) {
    if (!e.target.matches('.user-btn')) {
        const menu = document.getElementById("dropdownMenu");
        if (menu) menu.style.display = "none";
    }
}

// tampilan riwayat pengajuan
function openDetail(button)
{
    const item =
        JSON.parse(button.dataset.item);

    document.getElementById("modalDetail").style.display =
        "flex";

    document.getElementById("dLayanan").innerText =
        item.jenis_layanan;

    document.getElementById("dNik").innerText =
        item.nik;

    document.getElementById("dNama").innerText =
        item.nama || "-";

    document.getElementById("dTanggal").innerText =
        item.tanggal_pengajuan;

    document.getElementById("modalStatus").innerText =
        item.status;

    // =========================
    // DOKUMEN USER
    // =========================
    let htmlDokumen = "";

    if (item.dokumen && item.dokumen.length > 0)
    {
        item.dokumen.forEach(file => {

            htmlDokumen += `
                <a
                    href="/static/uploads/${file.nama_file}"
                    target="_blank"
                    class="file-btn"
                    style="display:block; margin-bottom:10px;"
                >
                    📄 ${file.nama_file}
                </a>
            `;
        });

        document.getElementById("dokumenUserList")
            .innerHTML = htmlDokumen;

        document.getElementById("boxUser")
            .style.display = "block";

    }
    else
    {
        document.getElementById("boxUser")
            .style.display = "none";
    }

    // =========================
    // CATATAN USER
    // =========================
    document.getElementById("catatanUser").innerText =
        item.catatan_user || "-";

    // =========================
    // CATATAN ADMIN
    // =========================
    document.getElementById("catatanAdmin").innerText =
        item.catatan_admin || "Belum ada balasan admin";

    document.getElementById("boxCatatan")
        .style.display = "block";

    // =========================
    // FILE ADMIN
    // =========================
    const linkAdmin =
        document.getElementById("linkAdmin");

    document.getElementById("boxAdmin")
        .style.display = "block";

if (
    item.file_balasan &&
    item.file_balasan !== "None" &&
    item.file_balasan !== ""
)
{
    // ADA FILE
    linkAdmin.href =
        "/static/uploads/" + item.file_balasan;

    linkAdmin.style.pointerEvents = "auto";

    linkAdmin.style.opacity = "1";

    linkAdmin.style.background =
        "#2563eb";

    linkAdmin.innerText =
        "📄 Lihat Dokumen";

}
else
{
    // TIDAK ADA FILE
    linkAdmin.href = "#";

    linkAdmin.style.pointerEvents =
        "none";

    linkAdmin.style.opacity =
        "0.5";

    linkAdmin.style.background =
        "#9ca3af";

    linkAdmin.innerText =
        "Belum Ada Dokumen";
}

    // =========================
    // INFO STATUS
    // =========================
    let info = "";

    if (item.status === "Menunggu Verifikasi") {

        info =
            "Pengajuan Anda sedang menunggu verifikasi admin.";

    } else if (item.status === "Diproses") {

        info =
            "Pengajuan Anda sedang diproses oleh admin.";

    } else if (item.status === "Disetujui") {

        info =
            "Pengajuan Anda telah disetujui.";

    } else if (item.status === "Ditolak") {

        info =
            "Pengajuan Anda ditolak.";
    }

    document.getElementById("infoStatus").innerText =
        info;
}

// close modal
function closeDetail() {

    document.getElementById("modalDetail").style.display =
        "none";

    document.getElementById("linkUser").href = "#";
    document.getElementById("linkAdmin").href = "#";

    // reset semua box
    document.getElementById("boxUser").style.display =
        "none";

    document.getElementById("boxAdmin").style.display =
        "none";

    document.getElementById("boxCatatan").style.display =
        "none";
}

// admin proses
function openProsesModal(id) {

    document.getElementById("modalProses").style.display =
        "flex";

    // set form action dinamis
    document.getElementById("formProses").action =
        "/admin/proses/" + id;
}

function closeProsesModal() {

    document.getElementById("modalProses").style.display =
        "none";
}


// show password
function togglePassword() {
    const input = document.getElementById("password");
    const iconShow = document.getElementById("iconShow");
    const iconHide = document.getElementById("iconHide");

    if (input.type === "password") {
        input.type = "text";
        iconShow.style.display = "none";
        iconHide.style.display = "block";
    } else {
        input.type = "password";
        iconShow.style.display = "block";
        iconHide.style.display = "none";
    }
}

// show confirm password
function toggleConfirmPassword() {
    const input = document.getElementById("confirm_password");
    const iconShow = document.getElementById("iconShowConfirm");
    const iconHide = document.getElementById("iconHideConfirm");

    if (input.type === "password") {
        input.type = "text";
        iconShow.style.display = "none";
        iconHide.style.display = "block";
    } else {
        input.type = "password";
        iconShow.style.display = "block";
        iconHide.style.display = "none";
    }
}