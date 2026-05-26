# 🎙 Milyona Giden Yol — Telegram Bot

Türkçe "Kim Milyoner Olmak İster?" formatında Telegram oyun botu.  
10 soruyu doğru cevaplayarak **1.000.000 TL** kazanın!

---

## 📁 Proje Yapısı

```
milyona_giden_yol/
├── main.py              # Bot giriş noktası
├── config.py            # Ayarlar ve sabitler
├── database.py          # SQLite async veritabanı işlemleri
├── game_logic.py        # Oyun mantığı ve mesaj şablonları
├── keyboards.py         # Telegram klavyeleri
├── questions.py         # 100 soruluk soru bankası
├── handlers/
│   ├── __init__.py
│   ├── start.py         # /start, /help, /rules
│   ├── game.py          # Oyun akışı, zamanlayıcı
│   └── profile.py       # /profile, /top
├── .env.example         # Örnek ortam değişkenleri
├── requirements.txt
└── README.md
```

---

## 🚀 Kurulum ve Çalıştırma

### 1. Depoyu klonlayın / klasörü açın

```bash
cd milyona_giden_yol
```

### 2. Sanal ortam oluşturun (önerilen)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. `.env` dosyasını oluşturun

```bash
cp .env.example .env
```

`.env` dosyasını açın ve `BOT_TOKEN` değerini doldurun:

```
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

> Token almak için [@BotFather](https://t.me/BotFather) ile konuşun.

### 5. Botu çalıştırın

```bash
python main.py
```

---

## 🤖 Bot Komutları

| Komut       | Açıklama                  |
|-------------|---------------------------|
| `/start`    | Ana menüyü aç             |
| `/play`     | Yeni oyun başlat          |
| `/rules`    | Oyun kurallarını görüntüle|
| `/profile`  | Kişisel istatistikler     |
| `/top`      | Liderlik tablosu (İlk 10) |
| `/help`     | Komut listesi             |

---

## 🎮 Oyun Özellikleri

- 100 soruluk banka, 10 kategoride (her oyunda 10 rastgele soru)
- Şıklar her oyunda karıştırılır
- 60 saniyelik soru süresi + otomatik zamanlayıcı
- 🧠 **50/50 joker** — oyun başına 1 kez
- 💰 **Kazancı al** — istediğiniz zaman güvenli çıkış
- Tam istatistik takibi (toplam oyun, en iyi ödül, toplam kazanç)
- Liderlik tablosu

## 💰 Ödül Basamakları

| Soru | Ödül         |
|------|--------------|
| 1    | 500 TL       |
| 2    | 1.000 TL     |
| 3    | 2.500 TL     |
| 4    | 5.000 TL     |
| 5    | 10.000 TL    |
| 6    | 25.000 TL    |
| 7    | 50.000 TL    |
| 8    | 100.000 TL   |
| 9    | 250.000 TL   |
| 10   | 1.000.000 TL |

---

## ☁️ Railway'e Deploy

### Yöntem 1 — GitHub üzerinden (önerilen)

1. Projeyi GitHub'a push edin:
   ```bash
   git init
   git add .
   git commit -m "initial commit"
   git remote add origin https://github.com/KULLANICI/milyona-giden-yol.git
   git push -u origin main
   ```

2. [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo** seçin.

3. Repoyu seçin — Railway `Dockerfile` dosyasını otomatik algılar ve build başlar.

4. **Variables** sekmesine gidin ve ekleyin:
   ```
   BOT_TOKEN = 123456:ABC...
   DB_PATH   = /app/data/game.db
   ```

5. **Deploy** — birkaç dakika içinde bot çalışır.

> **Not:** Railway'de SQLite dosyası pod yeniden başladığında sıfırlanabilir.  
> Kalıcı veri için Railway'in **Volume** özelliğini kullanın:  
> Service → **Volumes** → `/app/data` dizinini mount edin.

### Yöntem 2 — Railway CLI

```bash
# CLI kur
npm install -g @railway/cli

# Giriş yap
railway login

# Proje oluştur ve deploy et
railway init
railway up

# Ortam değişkenlerini ayarla
railway variables set BOT_TOKEN=123456:ABC...
railway variables set DB_PATH=/app/data/game.db
```

---

SQLite (`game.db`) otomatik oluşturulur. Tablolar:

- **users** — kullanıcı bilgileri ve istatistikler
- **games** — her oyunun durumu ve soruları
- **results** — tamamlanan oyun sonuçları

---

## 📦 Bağımlılıklar

```
aiogram==3.7.0
aiosqlite==0.20.0
python-dotenv==1.0.1
```
