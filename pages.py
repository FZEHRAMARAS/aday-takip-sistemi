import pandas as pd
import streamlit as st


def fetch_table(client, table_name: str, order_col: str = "created_at") -> pd.DataFrame:
    try:
        res = client.table(table_name).select("*").order(order_col, desc=True).execute()
        return pd.DataFrame(res.data or [])
    except Exception as exc:
        st.error(f"{table_name} okunamadı: {exc}")
        return pd.DataFrame()


def firmalar_page(client):
    st.header("Firmalar")
    with st.form("firma_form", clear_on_submit=True):
        firma_adi = st.text_input("Firma adı")
        aciklama = st.text_area("Açıklama")
        submitted = st.form_submit_button("Firma ekle")
        if submitted and firma_adi:
            client.table("firmalar").insert({"firma_adi": firma_adi.strip(), "aciklama": aciklama}).execute()
            st.success("Firma eklendi.")
    st.dataframe(fetch_table(client, "firmalar"), use_container_width=True)


def yeterlilikler_page(client):
    st.header("Yeterlilikler")
    with st.form("yeterlilik_form", clear_on_submit=True):
        kod = st.text_input("Yeterlilik kodu")
        ad = st.text_input("Yeterlilik adı")
        seviye = st.text_input("Seviye")
        revizyon_no = st.text_input("Revizyon no")
        submitted = st.form_submit_button("Yeterlilik ekle")
        if submitted and kod and ad:
            client.table("yeterlilikler").insert({
                "yeterlilik_kodu": kod.strip(),
                "yeterlilik_adi": ad.strip(),
                "seviye": seviye.strip() or None,
                "revizyon_no": revizyon_no.strip() or None,
            }).execute()
            st.success("Yeterlilik eklendi.")
    st.dataframe(fetch_table(client, "yeterlilikler"), use_container_width=True)


def eslestirme_page(client):
    st.header("Firma - Yeterlilik Eşleştirme")
    firmalar = fetch_table(client, "firmalar")
    yeterlilikler = fetch_table(client, "yeterlilikler")
    if firmalar.empty or yeterlilikler.empty:
        st.warning("Önce firma ve yeterlilik tanımı ekleyin.")
        return
    firma_map = dict(zip(firmalar["firma_adi"], firmalar["id"]))
    yeterlilik_map = dict(zip(yeterlilikler["yeterlilik_kodu"] + " - " + yeterlilikler["yeterlilik_adi"], yeterlilikler["id"]))
    with st.form("eslestirme_form"):
        firma = st.selectbox("Firma", list(firma_map.keys()))
        yeterlilik = st.selectbox("Yeterlilik", list(yeterlilik_map.keys()))
        submitted = st.form_submit_button("Eşleştir")
        if submitted:
            client.table("firma_yeterlilikler").upsert({
                "firma_id": firma_map[firma],
                "yeterlilik_id": yeterlilik_map[yeterlilik],
                "aktif": True,
            }, on_conflict="firma_id,yeterlilik_id").execute()
            st.success("Eşleştirme kaydedildi.")
    st.dataframe(fetch_table(client, "firma_yeterlilikler"), use_container_width=True)


def gruplar_page(client):
    st.header("Sınav Grupları")
    with st.form("grup_form", clear_on_submit=True):
        grup_adi = st.text_input("Grup adı")
        aciklama = st.text_area("Açıklama")
        submitted = st.form_submit_button("Grup ekle")
        if submitted and grup_adi:
            client.table("sinav_gruplari").insert({"grup_adi": grup_adi.strip(), "aciklama": aciklama}).execute()
            st.success("Sınav grubu eklendi.")
    st.dataframe(fetch_table(client, "sinav_gruplari"), use_container_width=True)


def ucretler_page(client):
    st.header("Sınav Ücretleri")
    firmalar = fetch_table(client, "firmalar")
    yeterlilikler = fetch_table(client, "yeterlilikler")
    gruplar = fetch_table(client, "sinav_gruplari")
    if yeterlilikler.empty:
        st.warning("Önce yeterlilik ekleyin.")
        return
    firma_options = ["Genel"] + firmalar["firma_adi"].tolist() if not firmalar.empty else ["Genel"]
    firma_map = dict(zip(firmalar.get("firma_adi", []), firmalar.get("id", []))) if not firmalar.empty else {}
    yeterlilik_map = dict(zip(yeterlilikler["yeterlilik_kodu"] + " - " + yeterlilikler["yeterlilik_adi"], yeterlilikler["id"]))
    grup_map = dict(zip(gruplar["grup_adi"], gruplar["id"])) if not gruplar.empty else {}
    with st.form("ucret_form"):
        firma = st.selectbox("Firma", firma_options)
        yeterlilik = st.selectbox("Yeterlilik", list(yeterlilik_map.keys()))
        grup = st.selectbox("Sınav grubu", ["Yok"] + list(grup_map.keys()))
        ucret_turu = st.selectbox("Ücret türü", ["ilk_sinav", "tekrar", "belge_yenileme", "revizyon_gecisi", "diger"])
        ucret = st.number_input("Ücret", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Ücret kaydet")
        if submitted:
            client.table("sinav_ucretleri").insert({
                "firma_id": None if firma == "Genel" else firma_map[firma],
                "yeterlilik_id": yeterlilik_map[yeterlilik],
                "sinav_grubu_id": None if grup == "Yok" else grup_map[grup],
                "ucret_turu": ucret_turu,
                "ucret": ucret,
                "para_birimi": "TRY",
            }).execute()
            st.success("Ücret kaydedildi.")
    st.dataframe(fetch_table(client, "sinav_ucretleri"), use_container_width=True)


def haklar_page(client):
    st.header("Hak Tanımları")
    firmalar = fetch_table(client, "firmalar")
    yeterlilikler = fetch_table(client, "yeterlilikler")
    gruplar = fetch_table(client, "sinav_gruplari")
    if yeterlilikler.empty:
        st.warning("Önce yeterlilik ekleyin.")
        return
    firma_options = ["Genel"] + firmalar["firma_adi"].tolist() if not firmalar.empty else ["Genel"]
    firma_map = dict(zip(firmalar.get("firma_adi", []), firmalar.get("id", []))) if not firmalar.empty else {}
    yeterlilik_map = dict(zip(yeterlilikler["yeterlilik_kodu"] + " - " + yeterlilikler["yeterlilik_adi"], yeterlilikler["id"]))
    grup_map = dict(zip(gruplar["grup_adi"], gruplar["id"])) if not gruplar.empty else {}
    with st.form("hak_form"):
        firma = st.selectbox("Firma", firma_options)
        yeterlilik = st.selectbox("Yeterlilik", list(yeterlilik_map.keys()))
        grup = st.selectbox("Sınav grubu", ["Yok"] + list(grup_map.keys()))
        hak_adi = st.text_input("Hak adı", value="Standart Hak")
        teorik_hak = st.number_input("Teorik hak", min_value=0, value=1, step=1)
        performans_hak = st.number_input("Performans hak", min_value=0, value=1, step=1)
        ucretsiz_tekrar = st.number_input("Ücretsiz tekrar hakkı", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Hak kaydet")
        if submitted and hak_adi:
            client.table("hak_tanimlari").insert({
                "firma_id": None if firma == "Genel" else firma_map[firma],
                "yeterlilik_id": yeterlilik_map[yeterlilik],
                "sinav_grubu_id": None if grup == "Yok" else grup_map[grup],
                "hak_adi": hak_adi,
                "teorik_hak": teorik_hak,
                "performans_hak": performans_hak,
                "ucretsiz_tekrar_hakki": ucretsiz_tekrar,
            }).execute()
            st.success("Hak tanımı kaydedildi.")
    st.dataframe(fetch_table(client, "hak_tanimlari"), use_container_width=True)


def sinavlar_page(client):
    st.header("Sınavlar")
    firmalar = fetch_table(client, "firmalar")
    yeterlilikler = fetch_table(client, "yeterlilikler")
    gruplar = fetch_table(client, "sinav_gruplari")
    if yeterlilikler.empty:
        st.warning("Önce yeterlilik ekleyin.")
        return
    firma_map = dict(zip(firmalar["firma_adi"], firmalar["id"])) if not firmalar.empty else {}
    yeterlilik_map = dict(zip(yeterlilikler["yeterlilik_kodu"] + " - " + yeterlilikler["yeterlilik_adi"], yeterlilikler["id"]))
    grup_map = dict(zip(gruplar["grup_adi"], gruplar["id"])) if not gruplar.empty else {}
    with st.form("sinav_form"):
        sinav_adi = st.text_input("Sınav adı")
        firma = st.selectbox("Firma", list(firma_map.keys()) if firma_map else ["Yok"])
        yeterlilik = st.selectbox("Yeterlilik", list(yeterlilik_map.keys()))
        grup = st.selectbox("Sınav grubu", ["Yok"] + list(grup_map.keys()))
        tarih = st.date_input("Sınav tarihi")
        yer = st.text_input("Sınav yeri")
        submitted = st.form_submit_button("Sınav oluştur")
        if submitted and sinav_adi:
            client.table("sinavlar").insert({
                "sinav_adi": sinav_adi,
                "firma_id": None if firma == "Yok" else firma_map[firma],
                "yeterlilik_id": yeterlilik_map[yeterlilik],
                "sinav_grubu_id": None if grup == "Yok" else grup_map[grup],
                "sinav_tarihi": str(tarih),
                "sinav_yeri": yer,
            }).execute()
            st.success("Sınav oluşturuldu.")
    st.dataframe(fetch_table(client, "sinavlar"), use_container_width=True)


def adaylar_locked_page(client):
    st.header("Adaylar")
    st.warning("Aday veri yükleme bu aşamada kapalıdır. Tablo ve RLS güvenliği hazır; import işlemi sonraki aşamada açılacak.")
    df = fetch_table(client, "adaylar")
    if df.empty:
        st.info("Aday kaydı yok. Bu beklenen durum.")
    else:
        st.dataframe(df, use_container_width=True)
