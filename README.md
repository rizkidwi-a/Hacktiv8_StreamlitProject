# 🤖 Hacktiv8 Streamlit Chatbot

Aplikasi chatbot interaktif berbasis **Streamlit** yang menggunakan **LangGraph** dan **Google Gemini AI** sebagai backend percakapan. Proyek ini dibuat sebagai bagian dari program Hacktiv8.

---

## 📋 Daftar Isi

- [Fitur](#-fitur)
- [Tech Stack](#-tech-stack)
- [Struktur Folder](#-struktur-folder)
- [Prasyarat](#-prasyarat)
- [Instalasi & Setup](#-instalasi--setup)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Penjelasan File](#-penjelasan-file)
- [Screenshot](#-screenshot)

---

## ✨ Fitur

- 💬 Chat interaktif dengan AI (Google Gemini 1.5 Flash)
- 🔄 Streaming response secara real-time
- 🧵 Multi-thread chat — buat percakapan baru tanpa kehilangan riwayat
- 📜 Riwayat chat tersimpan di sidebar dan dapat dimuat kembali
- 🧠 Memory persistence menggunakan LangGraph MemorySaver

---

## 🛠 Tech Stack

| Teknologi | Keterangan |
|---|---|
| **Python 3.14** | Bahasa pemrograman utama |
| **Streamlit** | Framework UI untuk web app |
| **LangGraph** | Orkestrasi workflow LLM berbasis graph |
| **LangChain** | Core library untuk integrasi LLM |
| **Google Gemini 1.5 Flash** | Model LLM dari Google |
| **python-dotenv** | Manajemen environment variable |

---

## 📁 Struktur Folder

```
Hacktiv8_StreamlitProject/
├── .env                # Environment variable (API key)
├── .git/               # Git repository
├── app.py              # Backend — LangGraph workflow & konfigurasi LLM
├── st.py               # Frontend — Streamlit chatbot UI
├── venv/               # Python virtual environment
└── README.md           # Dokumentasi proyek (file ini)
```

---

## 📌 Prasyarat

Sebelum memulai, pastikan kamu sudah memiliki:

1. **Python 3.10+** terinstal di komputer ([Download Python](https://www.python.org/downloads/))
2. **Google API Key** untuk mengakses Gemini AI ([Dapatkan di sini](https://aistudio.google.com/apikey))
3. **Git** (opsional, untuk clone repository)

---

## 🚀 Instalasi & Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/username/Hacktiv8_StreamlitProject.git
cd Hacktiv8_StreamlitProject
```

> Atau download ZIP dan extract ke folder yang diinginkan.

### Step 2: Buat Virtual Environment

```bash
python -m venv venv
```

### Step 3: Aktifkan Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install streamlit langgraph langchain-google-genai langchain-core python-dotenv
```

### Step 5: Konfigurasi API Key

Buka file `.env` di root folder proyek, lalu isi dengan API key milikmu:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> ⚠️ **Penting:** Jangan pernah membagikan API key ke publik atau meng-commit file `.env` ke repository.

---

## ▶️ Menjalankan Aplikasi

Pastikan virtual environment sudah aktif, lalu jalankan:

```bash
streamlit run st.py
```

Aplikasi akan terbuka otomatis di browser pada alamat:

```
http://localhost:8501
```

---

## 📖 Penjelasan File

### `app.py` — Backend Workflow

File ini berisi konfigurasi backend chatbot:

1. **Load environment variable** — Membaca `GOOGLE_API_KEY` dari file `.env`
2. **Inisialisasi LLM** — Menggunakan `ChatGoogleGenerativeAI` dengan model `gemini-1.5-flash`
3. **Definisi Graph Node** — Fungsi `chatbot_node()` yang mengirim pesan ke LLM dan mengembalikan response
4. **Build & Compile Graph** — Membuat workflow LangGraph sederhana: `START → chatbot → END`
5. **Memory Checkpointer** — Menggunakan `MemorySaver` agar riwayat percakapan per-thread tersimpan di memori

```
START ──► chatbot_node (Gemini AI) ──► END
```

### `st.py` — Frontend Streamlit UI

File ini berisi antarmuka pengguna chatbot:

1. **Import workflow** — Mengimpor `workflow` dari `app.py`
2. **Thread management** — Setiap percakapan memiliki `thread_id` unik (UUID)
3. **Sidebar** — Menampilkan tombol "New Chat" dan daftar riwayat thread
4. **Chat display** — Menampilkan seluruh riwayat pesan (user & assistant)
5. **Streaming response** — Menggunakan `workflow.stream()` dan `st.write_stream()` untuk menampilkan respons AI secara real-time
6. **Session state** — Menyimpan `messages_history`, `thread_id`, dan `chat_threads` di `st.session_state`

### `.env` — Environment Variable

Menyimpan konfigurasi sensitif berupa API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## 🖼 Screenshot

> Jalankan aplikasi untuk melihat tampilan chatbot di browser.

---

## 📝 Catatan Tambahan

- Riwayat chat disimpan **di memori** (in-memory), sehingga akan hilang saat aplikasi di-restart.
- Pastikan koneksi internet aktif karena aplikasi membutuhkan akses ke Google Gemini API.
- Jika terjadi error terkait API key, pastikan file `.env` sudah terisi dengan benar.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran di program **Hacktiv8**.
