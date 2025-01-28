
// Cek apakah halaman diakses dari localhost atau domain tertentu
document.addEventListener("DOMContentLoaded", function() {
    const allowedDomains = ["localhost", "127.0.0.1", "example.com", "yourwebsite.com"]; // Tambahkan localhost
    const currentHost = window.location.hostname;

    if (window.location.protocol === "file:") {
        document.body.innerHTML = "<h1>Akses Ditolak</h1><p>Halaman ini tidak bisa dibuka secara lokal.</p>";
    } else if (!allowedDomains.includes(currentHost)) {
        document.body.innerHTML = "<h1>Akses Ditolak</h1><p>Domain ini tidak diizinkan.</p>";
    }
});

document.getElementById("start-test").addEventListener("click", function() {
    logMessage("🚀 Test started...");
});

document.getElementById("stop-test").addEventListener("click", function() {
    logMessage("🛑 Test stopped.");
});

function logMessage(message) {
    const logContainer = document.getElementById("logs");
    const newLog = document.createElement("p");
    newLog.textContent = message;
    logContainer.appendChild(newLog);
}
