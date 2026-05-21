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
fetch("/api/chatbot", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        message: message
    })
})
.then(response => response.json())
.then(data => {
    const botDiv = document.createElement("div");
    botDiv.classList.add("bot-message");
    botDiv.textContent = data.reply;

    chatBody.appendChild(botDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
})
.catch(error => {
    const botDiv = document.createElement("div");
    botDiv.classList.add("bot-message");
    botDiv.textContent = "Maaf, chatbot sedang mengalami gangguan.";

    chatBody.appendChild(botDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
});


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

    // Popular suggestions interaction
    const suggestions = document.querySelectorAll(".chat-suggestions span");
    suggestions.forEach(span => {
        span.addEventListener("click", function () {
            if (input) {
                input.value = this.innerText;
                sendMessage();
            }
        });
    });
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

    // Pemetaan detail pengajuan ke teks yang mudah dipahami
    const mapDetail = {
        'anggota': 'Perubahan Anggota Keluarga',
        'alamat': 'Perubahan Domisili/Alamat',
        'lainnya': 'Perubahan Lainnya',
        'tidak_sekolah': 'Tidak/Belum Sekolah',
        'belum_tamat_sd': 'Belum Tamat SD/Sederajat',
        'tamat_sd': 'Tamat SD/Sederajat',
        'sltp': 'SLTP/Sederajat',
        'slta': 'SLTA/Sederajat',
        'diploma_1_2': 'Diploma I/II',
        'diploma_3': 'Akademi/Diploma III/Sarjana Muda',
        's1': 'Diploma IV/Strata I',
        's2': 'Strata II'
    };

    const detailVal = item.detail_pengajuan;
    const boxDetail = document.getElementById("boxDetailPengajuan");
    if (detailVal) {
        document.getElementById("dDetailPengajuan").innerText = mapDetail[detailVal] || detailVal;
        if (boxDetail) boxDetail.style.display = "block";
    } else {
        if (boxDetail) boxDetail.style.display = "none";
    }

    document.getElementById("dNik").innerText =
        item.nik;

    document.getElementById("dNama").innerText =
        item.nama || "-";

    document.getElementById("dTanggal").innerText =
        item.tanggal_pengajuan;


    const modalStatus = document.getElementById("modalStatus");
    modalStatus.innerText = item.status;
    modalStatus.className = "status-box status-" + item.status.toLowerCase().replace(/\s+/g, "-");

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

    const infoStatus = document.getElementById("infoStatus");
    infoStatus.innerText = info;
    infoStatus.className = "info-box info-" + item.status.toLowerCase().replace(/\s+/g, "-");
}

// close modal
function closeDetail() {

    document.getElementById("modalDetail").style.display =
        "none";

    // reset semua box
    const boxDetail = document.getElementById("boxDetailPengajuan");
    if (boxDetail) boxDetail.style.display = "none";

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

// ==========================
// QUICK QUESTION
// ==========================
function setQuestion(text) {

    document.getElementById("userInput").value =
        text;

    sendMessage();
}

// ==========================
// COLLAPSE/TOGGLE SYARAT
// ==========================
function toggleSyarat(btn, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const isCollapsed = container.classList.toggle('collapsed');

    if (isCollapsed) {
        btn.innerHTML = 'Baca Selengkapnya <span>▼</span>';
        btn.classList.remove('expanded');
    } else {
        btn.innerHTML = 'Sembunyikan <span>▼</span>';
        btn.classList.add('expanded');
    }
}

// ==========================
// THEME TOGGLE LOGIC
// ==========================
document.addEventListener("DOMContentLoaded", function () {
    const themeToggleBtn = document.getElementById("themeToggle");
    const themeToggleMobileBtn = document.getElementById("themeToggleMobile");

    function updateThemeUI(theme) {
        const themeText = document.querySelector(".theme-text");
        if (themeText) {
            themeText.textContent = theme === "dark" ? "Mode Terang" : "Mode Gelap";
        }
    }

    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateThemeUI(newTheme);
    }

    // Initialize UI Text based on active theme
    const activeTheme = document.documentElement.getAttribute("data-theme") || "light";
    updateThemeUI(activeTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", toggleTheme);
    }
    if (themeToggleMobileBtn) {
        themeToggleMobileBtn.addEventListener("click", toggleTheme);
    }
});