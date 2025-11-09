import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Muat variabel lingkungan (API Key) dari file .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# --- System Prompt (Parameter Kreatif) ---
# Ini adalah instruksi "rahasia" yang mendefinisikan kepribadian 
# dan tugas chatbot Anda.
SYSTEM_PROMPT = """
Kamu adalah "ResepKreatif", seorang asisten koki AI yang ramah, suportif, dan sangat kreatif.
Gaya bicaramu santai dan mendorong, seperti seorang sahabat.
Tugas utamamu adalah membantu pengguna membuat resep masakan dari bahan-bahan yang mereka sebutkan.

Aturan Penting:
1.  SELALU tanyakan bahan apa saja yang dimiliki pengguna terlebih dahulu.
2.  Jika pengguna hanya memberi sedikit bahan (misal: "cuma punya telur dan nasi"), berikan resep yang simpel tapi kreatif (misal: "Nasi Goreng Telur Keju lezat" atau "Omelet Nasi ala Jepang").
3.  Berikan resep dalam format yang jelas: Judul Resep, Bahan-Bahan, dan Langkah-Langkah.
4.  Jika pengguna bertanya di luar topik memasak (misal: "cuaca hari ini"), jawab dengan sopan bahwa kamu adalah asisten koki dan tidak bisa menjawab itu, lalu tawarkan bantuan resep lagi.
5.  (Fitur Memori): Jika pengguna menyebutkan preferensi (misal: "aku vegetarian" atau "nggak suka pedas"), ingat itu untuk sisa percakapan.
"""

# Inisialisasi model Gemini
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Fungsi untuk Inisialisasi Chat ---
def initialize_chat():
    # Mulai chat baru dengan system prompt
    chat = model.start_chat(history=[
        {"role": "user", "parts": [SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Halo! Aku ResepKreatif, asisten kokimu. 🍳 Siap masak apa kita hari ini? Coba sebutkan bahan-bahan yang kamu punya di kulkas!"]}
    ])
    return chat

# --- Tampilan Utama Streamlit ---
st.set_page_config(page_title="ResepKreatif", page_icon="🍳")
st.title("🍳 Asisten Koki 'ResepKreatif'")
st.caption("Bingung masak apa? Beri tahu aku bahan-bahanmu!")

# --- Logika Chat & Memori ---
# Gunakan st.session_state untuk menyimpan riwayat chat
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = initialize_chat()

# Tampilkan riwayat chat (skip pesan sistem pertama)
for message in st.session_state.chat_session.history[1:]:
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# Input dari pengguna
user_prompt = st.chat_input("Aku punya telur, nasi, dan sedikit kecap...")

if user_prompt:
    # Tampilkan pesan pengguna di UI
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Kirim pesan pengguna ke Gemini
    response = st.session_state.chat_session.send_message(user_prompt)
    
    # Tampilkan respons dari Gemini
    with st.chat_message("model"):
        st.markdown(response.text)