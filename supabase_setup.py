import os
from supabase import create_client, Client

# Bağlantı Bilgileri
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SERVICE_ROLE_KEY" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def iskelet_kurulumu():
    print("--- Proaktif Belgelendirme Sistem İskeleti Kuruluyor ---")

    # 1. Firmalar (Talep edilen tam liste)
    firmalar = [
        {"ad": "TCS"},
        {"ad": "Quaser"},
        {"ad": "Belgetek"},
        {"ad": "Kariyer"},
        {"ad": "Hakan Yılmaz Grubu"},
        {"ad": "Seçkin"},
        {"ad": "MYK"}
    ]
    
    try:
        supabase.table("firmalar").insert(firmalar).execute()
        print(f"✓ Firmalar yüklendi: {len(firmalar)} adet")
    except Exception as e:
        print(f"X Firma hatası: {e}")

    # 2. Fiyat Grupları (Hakan Yılmaz Grubu kuralı dahil)
    fiyat_tanimlari = [
        {"tanim": "Standart Başvuru Ücreti", "tutar": 0, "grup": "Genel"},
        {"tanim": "Bilinmeyen Fiyat Kalemi", "tutar": 0, "grup": "Hakan Yılmaz Grubu"}
    ]
    
    try:
        supabase.table("fiyatlar").insert(fiyat_tanimlari).execute()
        print("✓ Fiyat iskeleti oluşturuldu.")
    except Exception as e:
        print(f"X Fiyat hatası: {e}")

    # 3. Sistem Ayarları
    ayarlar = [
        {"anahtar": "odeme_durumlari", "deger": ["Beklemede", "Ödendi", "İptal"]},
        {"anahtar": "sinav_durumlari", "deger": ["Planlandı", "Tamamlandı", "Ertelendi"]}
    ]
    
    try:
        supabase.table("ayarlar").insert(ayarlar).execute()
        print("✓ Sistem ayarları yüklendi.")
    except Exception as e:
        print(f"X Ayar hatası: {e}")

    print("\n--- Kurulum Tamamlandı ---")

if __name__ == "__main__":
    iskelet_kurulumu()
