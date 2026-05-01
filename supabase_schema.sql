-- Aday ve Sınav Takip Modülü - Supabase Kurulum SQL
-- Bu script aday verisi yüklemeden sistem iskeletini kurar.
-- Supabase > SQL Editor > New Query içine komple yapıştırıp Run deyin.

create extension if not exists pgcrypto;

-- =========================
-- 1) Yardımcı fonksiyonlar
-- =========================
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- =========================
-- 2) Ana tanım tabloları
-- =========================
create table if not exists public.firmalar (
  id uuid primary key default gen_random_uuid(),
  firma_adi text not null unique,
  aciklama text,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.yeterlilikler (
  id uuid primary key default gen_random_uuid(),
  yeterlilik_kodu text not null unique,
  yeterlilik_adi text not null,
  seviye text,
  revizyon_no text,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.firma_yeterlilikler (
  id uuid primary key default gen_random_uuid(),
  firma_id uuid not null references public.firmalar(id) on delete cascade,
  yeterlilik_id uuid not null references public.yeterlilikler(id) on delete cascade,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(firma_id, yeterlilik_id)
);

create table if not exists public.sinav_gruplari (
  id uuid primary key default gen_random_uuid(),
  grup_adi text not null unique,
  aciklama text,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.sinav_ucretleri (
  id uuid primary key default gen_random_uuid(),
  firma_id uuid references public.firmalar(id) on delete set null,
  yeterlilik_id uuid not null references public.yeterlilikler(id) on delete cascade,
  sinav_grubu_id uuid references public.sinav_gruplari(id) on delete set null,
  ucret_turu text not null default 'ilk_sinav' check (ucret_turu in ('ilk_sinav','tekrar','belge_yenileme','revizyon_gecisi','diger')),
  ucret numeric(12,2) not null default 0,
  para_birimi text not null default 'TRY',
  gecerlilik_baslangic date,
  gecerlilik_bitis date,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.hak_tanimlari (
  id uuid primary key default gen_random_uuid(),
  firma_id uuid references public.firmalar(id) on delete set null,
  yeterlilik_id uuid not null references public.yeterlilikler(id) on delete cascade,
  sinav_grubu_id uuid references public.sinav_gruplari(id) on delete set null,
  hak_adi text not null,
  teorik_hak integer not null default 1,
  performans_hak integer not null default 1,
  ucretsiz_tekrar_hakki integer not null default 0,
  hak_gecerlilik_gun integer,
  aciklama text,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- =========================
-- 3) Aday ve sınav tabloları
-- =========================
create table if not exists public.adaylar (
  id uuid primary key default gen_random_uuid(),
  ad_soyad text not null,
  tc_kimlik_no text,
  telefon text,
  eposta text,
  firma_id uuid references public.firmalar(id) on delete set null,
  notlar text,
  aktif boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint adaylar_tc_unique unique(tc_kimlik_no)
);

create table if not exists public.aday_basvurulari (
  id uuid primary key default gen_random_uuid(),
  aday_id uuid not null references public.adaylar(id) on delete cascade,
  firma_id uuid references public.firmalar(id) on delete set null,
  yeterlilik_id uuid not null references public.yeterlilikler(id) on delete cascade,
  sinav_grubu_id uuid references public.sinav_gruplari(id) on delete set null,
  basvuru_durumu text not null default 'taslak' check (basvuru_durumu in ('taslak','basvuru_alindi','evrak_bekliyor','sinava_hazir','sinava_girdi','belgelendi','iptal')),
  ucret_durumu text not null default 'bekliyor' check (ucret_durumu in ('bekliyor','odendi','muaf','iade','iptal')),
  belge_durumu text not null default 'yok' check (belge_durumu in ('yok','bekliyor','basildi','teslim_edildi','yenileme_gerekli')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.aday_sinav_haklari (
  id uuid primary key default gen_random_uuid(),
  aday_id uuid not null references public.adaylar(id) on delete cascade,
  basvuru_id uuid references public.aday_basvurulari(id) on delete cascade,
  yeterlilik_id uuid not null references public.yeterlilikler(id) on delete cascade,
  teorik_toplam_hak integer not null default 1,
  teorik_kullanilan_hak integer not null default 0,
  performans_toplam_hak integer not null default 1,
  performans_kullanilan_hak integer not null default 0,
  hak_baslangic date default current_date,
  hak_bitis date,
  aciklama text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.sinavlar (
  id uuid primary key default gen_random_uuid(),
  sinav_adi text not null,
  firma_id uuid references public.firmalar(id) on delete set null,
  yeterlilik_id uuid not null references public.yeterlilikler(id) on delete cascade,
  sinav_grubu_id uuid references public.sinav_gruplari(id) on delete set null,
  sinav_tarihi date not null,
  sinav_saati time,
  sinav_yeri text,
  sinav_durumu text not null default 'planlandi' check (sinav_durumu in ('planlandi','tamamlandi','iptal','ertelendi')),
  aciklama text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.sinav_adaylari (
  id uuid primary key default gen_random_uuid(),
  sinav_id uuid not null references public.sinavlar(id) on delete cascade,
  aday_id uuid not null references public.adaylar(id) on delete cascade,
  basvuru_id uuid references public.aday_basvurulari(id) on delete set null,
  teorik_sonuc text default 'bekliyor' check (teorik_sonuc in ('bekliyor','basarili','basarisiz','girmedi','muaf')),
  performans_sonuc text default 'bekliyor' check (performans_sonuc in ('bekliyor','basarili','basarisiz','girmedi','muaf')),
  genel_sonuc text default 'bekliyor' check (genel_sonuc in ('bekliyor','basarili','basarisiz','iptal')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(sinav_id, aday_id)
);

-- =========================
-- 4) Güncelleme triggerları
-- =========================
do $$
declare
  t text;
begin
  foreach t in array array['firmalar','yeterlilikler','firma_yeterlilikler','sinav_gruplari','sinav_ucretleri','hak_tanimlari','adaylar','aday_basvurulari','aday_sinav_haklari','sinavlar','sinav_adaylari'] loop
    execute format('drop trigger if exists trg_%I_updated_at on public.%I', t, t);
    execute format('create trigger trg_%I_updated_at before update on public.%I for each row execute function public.set_updated_at()', t, t);
  end loop;
end $$;

-- =========================
-- 5) Varsayılan firma ve grup verileri
-- =========================
insert into public.firmalar (firma_adi, aciklama) values
('Quaser', 'Varsayılan firma grubu'),
('TCS', 'Varsayılan firma grubu'),
('Belgetürk', 'Varsayılan firma grubu'),
('Kariyer', 'Varsayılan firma grubu'),
('Hakan Yılmaz Grubu', 'Belirsiz ya da ayrı sınıflandırılacak kayıtlar için')
on conflict (firma_adi) do nothing;

insert into public.sinav_gruplari (grup_adi, aciklama) values
('İlk Sınav', 'İlk sınav organizasyonu'),
('Tekrar Sınavı', 'Başarısızlık veya hak kullanımı sonrası tekrar'),
('Belge Yenileme', 'Belge yenileme sınavı/işlemi'),
('Revizyon Geçişi', 'Yeterlilik revizyon geçiş süreci'),
('Diğer', 'Standart dışı gruplama')
on conflict (grup_adi) do nothing;

-- =========================
-- 6) RLS Güvenlik
-- =========================
alter table public.firmalar enable row level security;
alter table public.yeterlilikler enable row level security;
alter table public.firma_yeterlilikler enable row level security;
alter table public.sinav_gruplari enable row level security;
alter table public.sinav_ucretleri enable row level security;
alter table public.hak_tanimlari enable row level security;
alter table public.adaylar enable row level security;
alter table public.aday_basvurulari enable row level security;
alter table public.aday_sinav_haklari enable row level security;
alter table public.sinavlar enable row level security;
alter table public.sinav_adaylari enable row level security;

-- Eski policy varsa temizle
DO $$
DECLARE
  r record;
BEGIN
  FOR r IN
    SELECT schemaname, tablename, policyname
    FROM pg_policies
    WHERE schemaname = 'public'
      AND tablename IN ('firmalar','yeterlilikler','firma_yeterlilikler','sinav_gruplari','sinav_ucretleri','hak_tanimlari','adaylar','aday_basvurulari','aday_sinav_haklari','sinavlar','sinav_adaylari')
  LOOP
    EXECUTE format('drop policy if exists %I on %I.%I', r.policyname, r.schemaname, r.tablename);
  END LOOP;
END $$;

-- Bu iskelette yalnızca Supabase Auth ile giriş yapmış kullanıcılar işlem yapabilir.
-- Anon/public erişim kapalıdır.
create policy "auth read firmalar" on public.firmalar for select to authenticated using (true);
create policy "auth write firmalar" on public.firmalar for all to authenticated using (true) with check (true);

create policy "auth read yeterlilikler" on public.yeterlilikler for select to authenticated using (true);
create policy "auth write yeterlilikler" on public.yeterlilikler for all to authenticated using (true) with check (true);

create policy "auth read firma_yeterlilikler" on public.firma_yeterlilikler for select to authenticated using (true);
create policy "auth write firma_yeterlilikler" on public.firma_yeterlilikler for all to authenticated using (true) with check (true);

create policy "auth read sinav_gruplari" on public.sinav_gruplari for select to authenticated using (true);
create policy "auth write sinav_gruplari" on public.sinav_gruplari for all to authenticated using (true) with check (true);

create policy "auth read sinav_ucretleri" on public.sinav_ucretleri for select to authenticated using (true);
create policy "auth write sinav_ucretleri" on public.sinav_ucretleri for all to authenticated using (true) with check (true);

create policy "auth read hak_tanimlari" on public.hak_tanimlari for select to authenticated using (true);
create policy "auth write hak_tanimlari" on public.hak_tanimlari for all to authenticated using (true) with check (true);

create policy "auth read adaylar" on public.adaylar for select to authenticated using (true);
create policy "auth write adaylar" on public.adaylar for all to authenticated using (true) with check (true);

create policy "auth read aday_basvurulari" on public.aday_basvurulari for select to authenticated using (true);
create policy "auth write aday_basvurulari" on public.aday_basvurulari for all to authenticated using (true) with check (true);

create policy "auth read aday_sinav_haklari" on public.aday_sinav_haklari for select to authenticated using (true);
create policy "auth write aday_sinav_haklari" on public.aday_sinav_haklari for all to authenticated using (true) with check (true);

create policy "auth read sinavlar" on public.sinavlar for select to authenticated using (true);
create policy "auth write sinavlar" on public.sinavlar for all to authenticated using (true) with check (true);

create policy "auth read sinav_adaylari" on public.sinav_adaylari for select to authenticated using (true);
create policy "auth write sinav_adaylari" on public.sinav_adaylari for all to authenticated using (true) with check (true);

-- =========================
-- 7) Kontrol sorguları
-- =========================
select 'Kurulum tamamlandı' as durum;
select firma_adi from public.firmalar order by firma_adi;
select grup_adi from public.sinav_gruplari order by grup_adi;
