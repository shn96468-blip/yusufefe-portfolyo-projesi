import streamlit as st
import time

# --- OTURUM DURUMU (SESSION STATE) BAŞLANGIÇ AYARLARI ---
ADMIN_PASSWORD = "123"
MOCK_USERS = [
    {"username": "ali", "email": "ali@mail.com", "password_hash": "a123"},
    {"username": "ayse", "email": "ayse@mail.com", "password_hash": "a456"},
]

# Temel Durumlar
if 'admin_mode' not in st.session_state:
    st.session_state['admin_mode'] = False
if 'user_logged_in' not in st.session_state:
    st.session_state['user_logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'app_color' not in st.session_state:
    st.session_state['app_color'] = '#FF4B4B' # Portfolyo için Varsayılan Vurgu Rengi
if 'secilen_sayfa' not in st.session_state:
    st.session_state['secilen_sayfa'] = "Hakkımda" 

# Müzik Kontrol Durumları (Varsayılan: AÇIK)
if 'music_enabled' not in st.session_state:
    st.session_state['music_enabled'] = True 
if 'music_url' not in st.session_state:
    st.session_state['music_url'] = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
if 'music_volume' not in st.session_state:
    st.session_state['music_volume'] = 0.5 

# UI Kontrol Durumları
if 'show_admin_login' not in st.session_state:
    st.session_state['show_admin_login'] = False
if 'show_user_login' not in st.session_state:
    st.session_state['show_user_login'] = False
if 'show_user_register' not in st.session_state:
    st.session_state['show_user_register'] = False

# Sistem İzin Durumları (Varsayılan: HEP AÇIK)
if 'registration_allowed' not in st.session_state:
    st.session_state['registration_allowed'] = True
if 'user_login_allowed' not in st.session_state:
    st.session_state['user_login_allowed'] = True

# Chat Geçmişi
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Duyuru Durumları
if 'announcement' not in st.session_state:
    st.session_state['announcement'] = "🚀 Hoş geldiniz! Portfolyomdaki projeleri keşfedin."
if 'announcement_color' not in st.session_state:
    st.session_state['announcement_color'] = 'success'


# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Yusuf Efe Şahin | Portfolyo",
    layout="wide",
    page_icon="💼" 
)

# --- PORTFOLYO İÇERİK FONKSİYONU ---
def get_portfolyo_bilgisi(baslik):
    if baslik == "Hakkımda":
        return ("Merhaba, ben Yusuf Efe Şahin. Bu kişisel portfolyo sayfamda, teknoloji, yazılım ve tasarım alanındaki çalışmalarımı sergiliyorum. Yaratıcı projeler geliştirmeye ve sürekli öğrenmeye odaklıyım.", "👨‍💻")
    elif baslik == "Projelerim":
        return ("Yaptığım bazı öne çıkan projeler ve kullandığım teknolojiler aşağıdadır:\n\n* **Portfolyo Sitesi (Streamlit/Python):** Yönetici ve üye panelli kişisel site.\n* **Eğitim Robotu (Eski Proje):** Ders kartları ve AI simülasyonu içeren deneme uygulaması.\n* **Tasarım:** Photoshop/Illustrator ile minimalist görsel tasarımlar.", "💡")
    elif baslik == "İletişim":
        return ("Bana ulaşmak için aşağıdaki formu kullanabilir veya sosyal medya hesaplarımdan yazabilirsiniz.\n\n* **E-posta:** yusuf_efe_sahin@mail.com (Simülasyon)\n* **LinkedIn:** /yusufefesahin (Simülasyon)", "📧")
    return ("İçerik Bulunamadı.", "❓")


# --- GİRİŞ / ÇIKIŞ VE KONTROL FONKSİYONLARI ---

def user_login(username, password):
    if not st.session_state['user_login_allowed']:
        st.error("Üye girişi şu anda bakımdadır.")
        return
    for user in MOCK_USERS:
        if user["username"] == username and user["password_hash"] == password:
            st.session_state['user_logged_in'] = True
            st.session_state['current_user'] = username
            st.session_state['show_user_login'] = False
            st.success(f"Hoş geldiniz, {username.upper()}!")
            time.sleep(1)
            st.rerun()
            return
    # Simülasyon Girişi
    if len(username) > 0 and len(password) > 0:
         st.session_state['user_logged_in'] = True
         st.session_state['current_user'] = username
         st.session_state['show_user_login'] = False
         st.success(f"Hoş geldiniz, {username.upper()}! (Simülasyon Girişi Başarılı)")
         time.sleep(1)
         st.rerun()
    else:
        st.error("Kullanıcı adı veya şifre yanlış. (Demo: ali/a123)")

def user_logout():
    st.session_state['user_logged_in'] = False
    st.session_state['current_user'] = None
    st.rerun()

# Hata alınan fonksiyon burasıydı, düzeltildi.
def forgot_password_simulation(email_or_username, is_admin=False):
    st.sidebar.warning("Sistem simülasyon modunda olduğundan, şifre sıfırlama kodu e-posta adresinize gönderilmiş gibi yapıldı.")
    time.sleep(1)
    if is_admin:
        st.sidebar.success(f" Yönetici Şifresi sıfırlama maili 'admin@portfolyo.com' adresine gönderildi.")
    else:
        # SyntaxError burada düzeltildi: f-string doğru kapatıldı.
        st.sidebar.success(f" Kullanıcı şifresi sıfırlama kodu '{email_or_username}@mail.com' adresine gönderildi.")


def metin_oku(text):
    clean_text = text.replace('"', '').replace('\n', ' ')
    js_code = f"""
    <script>
        var utterance = new SpeechSynthesisUtterance("{clean_text}");
        window.speechSynthesis.speak(utterance);
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)


# --- MÜZİK ÇALMA MANTIĞI ---
if st.session_state['music_enabled'] and st.session_state['music_url']:
    # SES SEVİYESİ KAYDIRICISI DESTEĞİ İÇİN HTML ATTR KULLANIMI
    st.audio(
        st.session_state['music_url'], 
        format="audio/mp3", 
        start_time=0, 
        loop=True,
        # Streamlit HTML attribute'ü ile ses seviyesi kontrolü
        html_attrs={"autoplay": "autoplay", "volume": st.session_state['music_volume']} 
    )

# --- CHAT BOT MANTIĞI (BASİT SİMÜLASYON) ---
def general_chat_portfolyo(mesaj):
    mesaj_lower = mesaj.lower().strip()
    basit_cevaplar = {"merhaba": "Selam, Portfolyo sitesine hoş geldin!", "nasılsın": "Çok iyi çalışıyorum, teşekkürler!", "proje": "Projelerim sayfasına göz atmak ister misin?", "hata": "Hata bildirimleri için Yorum alanını kullanabilirsin."}
    
    for kelime, cevap in basit_cevaplar.items():
        if kelime in mesaj_lower:
            return f"🤖 (Kanka): {cevap}"
    return f"🤖 (Kanka): Anladım. Ben Yusuf Efe Şahin'in AI asistanıyım. Projeleri merak ediyorsan, kartlardan birini seçebilirsin."


# --- BAŞLIK VE CSS AYARLARI ---
st.markdown(f'<style>h1, h2, h3, h4, h5, h6 {{color: #FFFFFF;}}</style>', unsafe_allow_html=True)
st.title(f"💼 Yusuf Efe Şahin Portfolyo")

# --- ÖĞRENCİ/ZİYARETÇİ MODU (Admin değilse) ---
if not st.session_state['admin_mode']:

    # --- SES KONTROLLERİ (Ana Sayfa) ---
    col_kapat, col_ac, col_volume_slider = st.columns([1, 1, 6]) 

    if st.session_state['music_enabled']:
        with col_kapat:
            if st.button("🔊 Kapat", key="btn_kapat_ses", use_container_width=True):
                st.session_state['music_enabled'] = False
                st.rerun()
        with col_volume_slider:
            # Ses seviyesi kaydırıcısı
