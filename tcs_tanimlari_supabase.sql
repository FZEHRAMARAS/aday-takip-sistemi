-- 1. Aday tablolarını kapalı tut (RLS Aktif)
ALTER TABLE adaylar ENABLE ROW LEVEL SECURITY;
ALTER TABLE basvurular ENABLE ROW LEVEL SECURITY;
ALTER TABLE takvim ENABLE ROW LEVEL SECURITY;

-- 2. Tanım tablolarını açık bırak (RLS Pasif)
ALTER TABLE firmalar DISABLE ROW LEVEL SECURITY;
ALTER TABLE belgeler DISABLE ROW LEVEL SECURITY;
ALTER TABLE yeterlilikler DISABLE ROW LEVEL SECURITY;
ALTER TABLE fiyatlar DISABLE ROW LEVEL SECURITY;

-- 3. Firmalar Veri Girişi
INSERT INTO firmalar (ad) VALUES 
('TCS'),
('Quaser'),
('Belgetek'),
('Kariyer'),
('Hakan Yılmaz Grubu'),
('Seçkin'),
('MYK');

-- 4. Temel İskelet (Boş tabloların oluşturulması varsayılmıştır)
-- Bu bölüm tablo yapılarınızın hazır olduğunu varsayar.
