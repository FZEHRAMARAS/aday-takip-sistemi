import streamlit as st
from db import get_client, sign_in
from pages import (
    adaylar_locked_page,
    eslestirme_page,
    firmalar_page,
    gruplar_page,
    haklar_page,
    sinavlar_page,
    ucretler_page,
    yeterlilikler_page,
)

st.set_page_config(page_title="Aday ve Sınav Takip", layout="wide")
st.title("Aday ve Sınav Takip Modülü")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.subheader("Giriş")
    if not st.session_state.logged_in:
        email = st.text_input("E-posta")
        password = st.text_input("Şifre", type="password")
        if st.button("Giriş yap"):
            try:
                sign_in(email, password)
                st.session_state.logged_in = True
                st.success("Giriş başarılı.")
                st.rerun()
            except Exception as exc:
                st.error(f"Giriş yapılamadı: {exc}")
    else:
        st.success("Oturum açık")
        if st.button("Çıkış"):
            st.session_state.logged_in = False
            st.rerun()

if not st.session_state.logged_in:
    st.info("Devam etmek için Supabase Auth kullanıcınızla giriş yapın.")
    st.stop()

client = get_client()

page = st.sidebar.radio(
    "Modül seç",
    [
        "Firmalar",
        "Yeterlilikler",
        "Firma-Yeterlilik Eşleştirme",
        "Sınav Grupları",
        "Sınav Ücretleri",
        "Hak Tanımları",
        "Sınavlar",
        "Adaylar - Kapalı",
    ],
)

if page == "Firmalar":
    firmalar_page(client)
elif page == "Yeterlilikler":
    yeterlilikler_page(client)
elif page == "Firma-Yeterlilik Eşleştirme":
    eslestirme_page(client)
elif page == "Sınav Grupları":
    gruplar_page(client)
elif page == "Sınav Ücretleri":
    ucretler_page(client)
elif page == "Hak Tanımları":
    haklar_page(client)
elif page == "Sınavlar":
    sinavlar_page(client)
elif page == "Adaylar - Kapalı":
    adaylar_locked_page(client)
