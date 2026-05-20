// // Kirim pesan saat tombol diklik
// function sendMessage() {
//     const input = document.getElementById("userInput");
//     const chatBody = document.getElementById("chatBody");

//     const message = input.value.trim();
//     if (message === "") return;

//     // User message
//     const userDiv = document.createElement("div");
//     userDiv.classList.add("user-message");
//     userDiv.textContent = message;
//     chatBody.appendChild(userDiv);

//     // Bot reply
//     const botDiv = document.createElement("div");
//     botDiv.classList.add("bot-message");

//     if (message.toLowerCase().includes("kk")) {
//         botDiv.textContent = "Untuk cetak ulang KK, silakan membawa KK lama dan KTP ke kantor Disdukcapil.";
//     } 
//     else if (message.toLowerCase().includes("golongan darah")) {
//         botDiv.textContent = "Untuk ubah golongan darah, sertakan surat keterangan medis resmi.";
//     } 
//     else {
//         botDiv.textContent = "Terima kasih atas pertanyaan Anda. Silakan hubungi kantor Disdukcapil untuk informasi lebih lanjut.";
//     }

//     setTimeout(() => {
//         chatBody.appendChild(botDiv);
//         chatBody.scrollTop = chatBody.scrollHeight;
//     }, 500);

//     input.value = "";
// }


// // ==========================
// // ENTER KEY SUPPORT
// // ==========================
// document.addEventListener("DOMContentLoaded", function () {
//     const input = document.getElementById("userInput");

//     if (input) {
//         input.addEventListener("keypress", function (event) {
//             if (event.key === "Enter") {
//                 event.preventDefault();
//                 sendMessage();
//             }
//         });
//     }
// });

// // ==========================
// // HAMBURGER MENU
// // ==========================
// document.addEventListener("DOMContentLoaded", function () {

//     const hamburger = document.getElementById("hamburger");
//     const navMenu = document.querySelector(".nav-menu");

//     if (hamburger) {
//         hamburger.addEventListener("click", function () {
//             navMenu.classList.toggle("active");
//         });
//     }

// });

// // popup chatbot
// function closePopup() {
//     document.getElementById("popupTutorial").style.display = "none";
// }

// // otomatis muncul saat halaman dibuka
// window.onload = function() {
//     const popup = document.getElementById("popupTutorial");
//     if (popup) {
//         popup.style.display = "flex";
//     }
// };


// // pengajuan
// function toggleForm(id) {
//     const form = document.getElementById(id);

//     if (form.style.display === "block") {
//         form.style.display = "none";
//     } else {
//         form.style.display = "block";
//     }
// }