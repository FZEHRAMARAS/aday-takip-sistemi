import pandas as pd


def template_yeterlilikler():
    return pd.DataFrame([
        {"yeterlilik_kodu": "", "yeterlilik_adi": "", "seviye": "", "revizyon_no": "", "aktif": True}
    ])


def template_ucretler():
    return pd.DataFrame([
        {"firma_adi": "Quaser", "yeterlilik_kodu": "", "sinav_grubu": "İlk Sınav", "ucret_turu": "ilk_sinav", "ucret": 0, "para_birimi": "TRY"}
    ])


def template_haklar():
    return pd.DataFrame([
        {"firma_adi": "Quaser", "yeterlilik_kodu": "", "sinav_grubu": "İlk Sınav", "hak_adi": "Standart Hak", "teorik_hak": 1, "performans_hak": 1, "ucretsiz_tekrar_hakki": 0, "hak_gecerlilik_gun": ""}
    ])
