# Aday ve Sınav Takip Modülü

Bu paket aday verisini yüklemeden önce sistem iskeletini kurmak için hazırlanmıştır.

## İçindekiler

- `supabase_schema.sql`: Supabase tabloları, RLS güvenliği, varsayılan firma/grup kayıtları
- `app/`: Streamlit tabanlı basit yönetim paneli
- `.env.example`: Supabase bağlantı değişkenleri
- `requirements.txt`: Python bağımlılıkları

## Kurulum

### 1. Supabase SQL kurulumu

Supabase panelinde:

1. SQL Editor açın.
2. `supabase_schema.sql` içeriğini komple yapıştırın.
3. Run deyin.

Kurulum sonrası varsayılan firmalar oluşur:

- Quaser
- TCS
- Belgetürk
- Kariyer
- Hakan Yılmaz Grubu

### 2. Supabase Auth kullanıcısı oluşturma

Supabase > Authentication > Users alanından kullanıcı oluşturun.

RLS açık olduğu için giriş yapmadan veriler görünmez.

### 3. Python uygulamasını çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` dosyasına Supabase URL ve anon key değerlerinizi yazın.

Sonra:

```bash
streamlit run app/main.py
```

## Önemli güvenlik notu

Service Role Key bu projeye yazılmamalıdır. GitHub'a asla yüklenmemelidir. Uygulama yalnızca anon key + Supabase Auth ile çalışacak şekilde hazırlanmıştır.

## İlk aşamada aday verisi yüklenmez

Bu paket iskeleti kurar. Aday import işlemi ayrıca kontrollü biçimde açılır.
