"""
Oyunun soru bankası — 100 soru, 10 kategori, kategori başına 10 soru.
Her soru: category, question, options (4 şık), correct (doğru cevap metni).
"""

QUESTIONS: list[dict] = [
    # ── 1. Genel Kültür ─────────────────────────────────────────────────
    {
        "category": "Genel Kültür",
        "question": "Türkiye'nin başkenti neresidir?",
        "options": ["İstanbul", "Ankara", "İzmir", "Bursa"],
        "correct": "Ankara",
    },
    {
        "category": "Genel Kültür",
        "question": "Dünyanın en büyük okyanusu hangisidir?",
        "options": ["Atlas", "Hint", "Pasifik", "Arktik"],
        "correct": "Pasifik",
    },
    {
        "category": "Genel Kültür",
        "question": "Bir yılda kaç ay vardır?",
        "options": ["10", "11", "12", "13"],
        "correct": "12",
    },
    {
        "category": "Genel Kültür",
        "question": "İnsan vücudunda kaç kalp vardır?",
        "options": ["1", "2", "3", "4"],
        "correct": "1",
    },
    {
        "category": "Genel Kültür",
        "question": "Güneş hangi yönden doğar?",
        "options": ["Batı", "Kuzey", "Doğu", "Güney"],
        "correct": "Doğu",
    },
    {
        "category": "Genel Kültür",
        "question": "Türkiye'nin para birimi nedir?",
        "options": ["Euro", "Dolar", "Lira", "Sterlin"],
        "correct": "Lira",
    },
    {
        "category": "Genel Kültür",
        "question": "Haftada kaç gün vardır?",
        "options": ["5", "6", "7", "8"],
        "correct": "7",
    },
    {
        "category": "Genel Kültür",
        "question": "En uzun gün hangi mevsimdedir?",
        "options": ["İlkbahar", "Yaz", "Sonbahar", "Kış"],
        "correct": "Yaz",
    },
    {
        "category": "Genel Kültür",
        "question": "Su kaç derecede donar?",
        "options": ["0", "50", "100", "150"],
        "correct": "0",
    },
    {
        "category": "Genel Kültür",
        "question": "Dünyamız hangi gezegendir?",
        "options": ["Mars", "Venüs", "Dünya", "Jüpiter"],
        "correct": "Dünya",
    },

    # ── 2. Spor ─────────────────────────────────────────────────────────
    {
        "category": "Spor",
        "question": "Futbolda bir takım kaç oyuncudan oluşur?",
        "options": ["9", "10", "11", "12"],
        "correct": "11",
    },
    {
        "category": "Spor",
        "question": "Basketbolda potaya atılan en değerli şut kaç sayıdır?",
        "options": ["1", "2", "3", "4"],
        "correct": "3",
    },
    {
        "category": "Spor",
        "question": "Cristiano Ronaldo hangi sporla tanınır?",
        "options": ["Basketbol", "Futbol", "Tenis", "Voleybol"],
        "correct": "Futbol",
    },
    {
        "category": "Spor",
        "question": "Wimbledon hangi spor dalıdır?",
        "options": ["Golf", "Futbol", "Tenis", "Yüzme"],
        "correct": "Tenis",
    },
    {
        "category": "Spor",
        "question": "Galatasaray'ın renkleri nelerdir?",
        "options": ["Mavi-Beyaz", "Sarı-Kırmızı", "Siyah-Beyaz", "Yeşil-Sarı"],
        "correct": "Sarı-Kırmızı",
    },
    {
        "category": "Spor",
        "question": "Olimpiyatlar kaç yılda bir yapılır?",
        "options": ["2", "3", "4", "5"],
        "correct": "4",
    },
    {
        "category": "Spor",
        "question": "Basketbolda topu sektirmeye ne denir?",
        "options": ["Pas", "Dripling", "Şut", "Faul"],
        "correct": "Dripling",
    },
    {
        "category": "Spor",
        "question": "Lionel Messi hangi ülkedendir?",
        "options": ["Brezilya", "İspanya", "Arjantin", "Fransa"],
        "correct": "Arjantin",
    },
    {
        "category": "Spor",
        "question": "Fenerbahçe hangi şehrin takımıdır?",
        "options": ["Ankara", "İstanbul", "İzmir", "Antalya"],
        "correct": "İstanbul",
    },
    {
        "category": "Spor",
        "question": "Bir futbol maçında kırmızı kart alan oyuncu ne olur?",
        "options": ["Devam eder", "Dinlenir", "Oyundan atılır", "Kaleci olur"],
        "correct": "Oyundan atılır",
    },

    # ── 3. Sinema ve Diziler ─────────────────────────────────────────────
    {
        "category": "Sinema ve Diziler",
        "question": "Harry Potter hangi okula gider?",
        "options": ["Oxford", "Hogwarts", "Harvard", "Stanford"],
        "correct": "Hogwarts",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Titanic filmi hangi olayla ilgilidir?",
        "options": ["Yangın", "Deprem", "Gemi kazası", "Savaş"],
        "correct": "Gemi kazası",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Batman hangi şehri korur?",
        "options": ["Metropolis", "Gotham", "New York", "Chicago"],
        "correct": "Gotham",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Spider-Man'in gerçek adı nedir?",
        "options": ["Tony Stark", "Peter Parker", "Bruce Wayne", "Clark Kent"],
        "correct": "Peter Parker",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Frozen filmindeki prensesin adı nedir?",
        "options": ["Anna", "Bella", "Sofia", "Mia"],
        "correct": "Anna",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Joker hangi karakterin düşmanıdır?",
        "options": ["Superman", "Batman", "Hulk", "Thor"],
        "correct": "Batman",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Simba hangi filmdedir?",
        "options": ["Shrek", "Aslan Kral", "Cars", "Nemo"],
        "correct": "Aslan Kral",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Netflix nedir?",
        "options": ["Oyun konsolu", "Yayın platformu", "Telefon markası", "Gazete"],
        "correct": "Yayın platformu",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Avengers takımının lideri kimdir?",
        "options": ["Hulk", "Iron Man", "Captain America", "Thor"],
        "correct": "Captain America",
    },
    {
        "category": "Sinema ve Diziler",
        "question": "Elsa hangi güçlere sahiptir?",
        "options": ["Ateş", "Su", "Buz", "Toprak"],
        "correct": "Buz",
    },

    # ── 4. Müzik ─────────────────────────────────────────────────────────
    {
        "category": "Müzik",
        "question": "Piyano kaç tuştan oluşur?",
        "options": ["44", "66", "88", "100"],
        "correct": "88",
    },
    {
        "category": "Müzik",
        "question": "Gitar hangi tür enstrümandır?",
        "options": ["Nefesli", "Yaylı", "Telli", "Vurmalı"],
        "correct": "Telli",
    },
    {
        "category": "Müzik",
        "question": "Mikrofon ne için kullanılır?",
        "options": ["Yemek yapmak", "Ses yükseltmek", "Yazı yazmak", "Oyun oynamak"],
        "correct": "Ses yükseltmek",
    },
    {
        "category": "Müzik",
        "question": "Spotify nedir?",
        "options": ["Film sitesi", "Müzik platformu", "Banka", "Oyun"],
        "correct": "Müzik platformu",
    },
    {
        "category": "Müzik",
        "question": "DJ ne yapar?",
        "options": ["Yemek pişirir", "Müzik çalar", "Resim yapar", "Araba kullanır"],
        "correct": "Müzik çalar",
    },
    {
        "category": "Müzik",
        "question": "En yüksek erkek sesine ne denir?",
        "options": ["Bas", "Tenor", "Alto", "Bariton"],
        "correct": "Tenor",
    },
    {
        "category": "Müzik",
        "question": "Kulaklık ne için kullanılır?",
        "options": ["Müzik dinlemek", "Yazı yazmak", "Fotoğraf çekmek", "Uyku"],
        "correct": "Müzik dinlemek",
    },
    {
        "category": "Müzik",
        "question": "Konserde sanatçı ne yapar?",
        "options": ["Spor yapar", "Şarkı söyler", "Yemek yer", "Kitap okur"],
        "correct": "Şarkı söyler",
    },
    {
        "category": "Müzik",
        "question": "Davul hangi gruba girer?",
        "options": ["Telli", "Nefesli", "Vurmalı", "Elektronik"],
        "correct": "Vurmalı",
    },
    {
        "category": "Müzik",
        "question": "Nota neyi gösterir?",
        "options": ["Renk", "Ses", "Hava", "Tat"],
        "correct": "Ses",
    },

    # ── 5. Teknoloji ──────────────────────────────────────────────────────
    {
        "category": "Teknoloji",
        "question": "Bilgisayarın beyni nedir?",
        "options": ["Ekran", "İşlemci", "Klavye", "Fare"],
        "correct": "İşlemci",
    },
    {
        "category": "Teknoloji",
        "question": "İnternete bağlanmak için hangisi gerekir?",
        "options": ["Wi-Fi", "Buzdolabı", "Televizyon", "Mikrofon"],
        "correct": "Wi-Fi",
    },
    {
        "category": "Teknoloji",
        "question": "USB ne için kullanılır?",
        "options": ["Veri taşımak", "Yemek yapmak", "Müzik söylemek", "Spor yapmak"],
        "correct": "Veri taşımak",
    },
    {
        "category": "Teknoloji",
        "question": "Akıllı telefonla ne yapılabilir?",
        "options": ["Arama yapmak", "Uçmak", "Yüzmek", "Boya yapmak"],
        "correct": "Arama yapmak",
    },
    {
        "category": "Teknoloji",
        "question": "Google nedir?",
        "options": ["Arama motoru", "Oyun", "Market", "Araba"],
        "correct": "Arama motoru",
    },
    {
        "category": "Teknoloji",
        "question": "Klavyede harfler nerede bulunur?",
        "options": ["Ekranda", "Tuşlarda", "Masada", "Farede"],
        "correct": "Tuşlarda",
    },
    {
        "category": "Teknoloji",
        "question": "Şifre neden kullanılır?",
        "options": ["Güvenlik için", "Yemek için", "Spor için", "Temizlik için"],
        "correct": "Güvenlik için",
    },
    {
        "category": "Teknoloji",
        "question": "Bluetooth ne işe yarar?",
        "options": ["Kablosuz bağlantı", "Yemek pişirme", "Fotoğraf basma", "Oyun çizme"],
        "correct": "Kablosuz bağlantı",
    },
    {
        "category": "Teknoloji",
        "question": "Tablet nedir?",
        "options": ["Elektronik cihaz", "Meyve", "Araba", "Ayakkabı"],
        "correct": "Elektronik cihaz",
    },
    {
        "category": "Teknoloji",
        "question": "Sosyal medya nedir?",
        "options": ["İletişim platformu", "Yemek türü", "Spor dalı", "Film stüdyosu"],
        "correct": "İletişim platformu",
    },

    # ── 6. Hayvanlar ─────────────────────────────────────────────────────
    {
        "category": "Hayvanlar",
        "question": "En hızlı kara hayvanı hangisidir?",
        "options": ["Aslan", "Çita", "Fil", "Zebra"],
        "correct": "Çita",
    },
    {
        "category": "Hayvanlar",
        "question": "Balıklar nerede yaşar?",
        "options": ["Gökyüzü", "Su", "Çöl", "Orman"],
        "correct": "Su",
    },
    {
        "category": "Hayvanlar",
        "question": "Penguenler uçar mı?",
        "options": ["Evet", "Hayır", "Bazen", "Yazın"],
        "correct": "Hayır",
    },
    {
        "category": "Hayvanlar",
        "question": "Aslan hangi hayvan olarak bilinir?",
        "options": ["Ormanın kralı", "Denizin kralı", "Çölün kralı", "Gökyüzünün kralı"],
        "correct": "Ormanın kralı",
    },
    {
        "category": "Hayvanlar",
        "question": "Arılar ne üretir?",
        "options": ["Süt", "Bal", "Peynir", "Çikolata"],
        "correct": "Bal",
    },
    {
        "category": "Hayvanlar",
        "question": "Zürafa neden uzundur?",
        "options": ["Uzun boynu vardır", "Kanatları vardır", "Hızlı koşar", "Yüzer"],
        "correct": "Uzun boynu vardır",
    },
    {
        "category": "Hayvanlar",
        "question": "Hangi hayvan havlar?",
        "options": ["Kedi", "Köpek", "Kuş", "Balık"],
        "correct": "Köpek",
    },
    {
        "category": "Hayvanlar",
        "question": "Filin burnuna ne denir?",
        "options": ["Kuyruk", "Hortum", "Pençe", "Gaga"],
        "correct": "Hortum",
    },
    {
        "category": "Hayvanlar",
        "question": "Tavuk ne yumurtlar?",
        "options": ["Altın", "Yumurta", "Taş", "Süt"],
        "correct": "Yumurta",
    },
    {
        "category": "Hayvanlar",
        "question": "Kedi hangi sesi çıkarır?",
        "options": ["Möö", "Miyav", "Hav hav", "Vak vak"],
        "correct": "Miyav",
    },

    # ── 7. Yemek ─────────────────────────────────────────────────────────
    {
        "category": "Yemek",
        "question": "Pizza hangi ülkeye aittir?",
        "options": ["Türkiye", "İtalya", "Fransa", "Almanya"],
        "correct": "İtalya",
    },
    {
        "category": "Yemek",
        "question": "Çayın rengi genellikle nedir?",
        "options": ["Mavi", "Kırmızı", "Yeşil", "Beyaz"],
        "correct": "Kırmızı",
    },
    {
        "category": "Yemek",
        "question": "Patates kızartması neyle yapılır?",
        "options": ["Domates", "Patates", "Soğan", "Havuç"],
        "correct": "Patates",
    },
    {
        "category": "Yemek",
        "question": "Hamburgerin içinde genelde ne bulunur?",
        "options": ["Köfte", "Balık", "Elma", "Çikolata"],
        "correct": "Köfte",
    },
    {
        "category": "Yemek",
        "question": "Dondurma sıcak mı yenir?",
        "options": ["Evet", "Hayır", "Bazen", "Fırında"],
        "correct": "Hayır",
    },
    {
        "category": "Yemek",
        "question": "Kahvaltıda hangisi yenir?",
        "options": ["Çorba", "Zeytin", "Makarna", "Pizza"],
        "correct": "Zeytin",
    },
    {
        "category": "Yemek",
        "question": "Makarna hangi ülkede meşhurdur?",
        "options": ["İtalya", "Japonya", "Kanada", "Mısır"],
        "correct": "İtalya",
    },
    {
        "category": "Yemek",
        "question": "Limonun tadı nasıldır?",
        "options": ["Tatlı", "Ekşi", "Tuzlu", "Acı"],
        "correct": "Ekşi",
    },
    {
        "category": "Yemek",
        "question": "Suşi hangi ülkeye aittir?",
        "options": ["Çin", "Japonya", "Türkiye", "İspanya"],
        "correct": "Japonya",
    },
    {
        "category": "Yemek",
        "question": "Ekmek genellikle neyden yapılır?",
        "options": ["Un", "Şeker", "Tuz", "Yağ"],
        "correct": "Un",
    },

    # ── 8. Coğrafya ───────────────────────────────────────────────────────
    {
        "category": "Coğrafya",
        "question": "Türkiye hangi kıtadadır?",
        "options": ["Avrupa ve Asya", "Afrika", "Amerika", "Avustralya"],
        "correct": "Avrupa ve Asya",
    },
    {
        "category": "Coğrafya",
        "question": "Nil Nehri hangi kıtadadır?",
        "options": ["Avrupa", "Afrika", "Asya", "Amerika"],
        "correct": "Afrika",
    },
    {
        "category": "Coğrafya",
        "question": "En büyük çöl hangisidir?",
        "options": ["Gobi", "Sahra", "Atacama", "Karakum"],
        "correct": "Sahra",
    },
    {
        "category": "Coğrafya",
        "question": "Everest Dağı hangi sıradağlardadır?",
        "options": ["Alpler", "Himalayalar", "Toroslar", "Andlar"],
        "correct": "Himalayalar",
    },
    {
        "category": "Coğrafya",
        "question": "Paris hangi ülkenin başkentidir?",
        "options": ["Almanya", "Fransa", "İtalya", "İngiltere"],
        "correct": "Fransa",
    },
    {
        "category": "Coğrafya",
        "question": "Japonya hangi kıtadadır?",
        "options": ["Avrupa", "Asya", "Afrika", "Amerika"],
        "correct": "Asya",
    },
    {
        "category": "Coğrafya",
        "question": "Akdeniz'in suyu nasıldır?",
        "options": ["Tatlı", "Tuzlu", "Acı", "Soğuk"],
        "correct": "Tuzlu",
    },
    {
        "category": "Coğrafya",
        "question": "Türkiye'nin en kalabalık şehri hangisidir?",
        "options": ["Ankara", "İzmir", "İstanbul", "Bursa"],
        "correct": "İstanbul",
    },
    {
        "category": "Coğrafya",
        "question": "Hangi ülke piramitleriyle ünlüdür?",
        "options": ["Mısır", "Kanada", "Rusya", "Norveç"],
        "correct": "Mısır",
    },
    {
        "category": "Coğrafya",
        "question": "Dünya'nın uydusu hangisidir?",
        "options": ["Mars", "Ay", "Venüs", "Jüpiter"],
        "correct": "Ay",
    },

    # ── 9. Bilim ─────────────────────────────────────────────────────────
    {
        "category": "Bilim",
        "question": "İnsanlar hangi gazı solur?",
        "options": ["Oksijen", "Karbon", "Hidrojen", "Azot"],
        "correct": "Oksijen",
    },
    {
        "category": "Bilim",
        "question": "Suyun kimyasal formülü nedir?",
        "options": ["CO2", "H2O", "O2", "NaCl"],
        "correct": "H2O",
    },
    {
        "category": "Bilim",
        "question": "Dünya Güneş'in etrafında kaç günde döner?",
        "options": ["30", "100", "365", "700"],
        "correct": "365",
    },
    {
        "category": "Bilim",
        "question": "Yer çekimini kim bulmuştur?",
        "options": ["Einstein", "Newton", "Tesla", "Edison"],
        "correct": "Newton",
    },
    {
        "category": "Bilim",
        "question": "İnsan vücudunda en sert madde nedir?",
        "options": ["Kemik", "Diş minesi", "Tırnak", "Saç"],
        "correct": "Diş minesi",
    },
    {
        "category": "Bilim",
        "question": "Elektrik çarpabilir mi?",
        "options": ["Evet", "Hayır", "Bazen", "Sadece yazın"],
        "correct": "Evet",
    },
    {
        "category": "Bilim",
        "question": "Hangi gezegen kırmızı gezegen olarak bilinir?",
        "options": ["Dünya", "Mars", "Satürn", "Uranüs"],
        "correct": "Mars",
    },
    {
        "category": "Bilim",
        "question": "Güneş bir nedir?",
        "options": ["Gezegen", "Yıldız", "Uydu", "Meteor"],
        "correct": "Yıldız",
    },
    {
        "category": "Bilim",
        "question": "Buz eriyince ne olur?",
        "options": ["Ateş", "Su", "Taş", "Kum"],
        "correct": "Su",
    },
    {
        "category": "Bilim",
        "question": "İnsan vücudunda kaç göz vardır?",
        "options": ["1", "2", "3", "4"],
        "correct": "2",
    },

    # ── 10. Tarih ────────────────────────────────────────────────────────
    {
        "category": "Tarih",
        "question": "Türkiye Cumhuriyeti'nin kurucusu kimdir?",
        "options": [
            "Fatih Sultan Mehmet",
            "Mustafa Kemal Atatürk",
            "Yavuz Sultan Selim",
            "Kanuni Sultan Süleyman",
        ],
        "correct": "Mustafa Kemal Atatürk",
    },
    {
        "category": "Tarih",
        "question": "İstanbul'un eski adı nedir?",
        "options": ["Roma", "Konstantinopolis", "Atina", "Selanik"],
        "correct": "Konstantinopolis",
    },
    {
        "category": "Tarih",
        "question": "İlk insan Ay'a ne zaman çıktı?",
        "options": ["1950", "1969", "1980", "1999"],
        "correct": "1969",
    },
    {
        "category": "Tarih",
        "question": "Osmanlı İmparatorluğu'nun başkenti hangisiydi?",
        "options": ["Ankara", "İstanbul", "Bursa", "İzmir"],
        "correct": "İstanbul",
    },
    {
        "category": "Tarih",
        "question": "Piramitler hangi uygarlığa aittir?",
        "options": ["Roma", "Mısır", "Yunan", "Pers"],
        "correct": "Mısır",
    },
    {
        "category": "Tarih",
        "question": "Fatih Sultan Mehmet hangi şehri fethetti?",
        "options": ["Roma", "İstanbul", "Paris", "Londra"],
        "correct": "İstanbul",
    },
    {
        "category": "Tarih",
        "question": "Cumhuriyet Bayramı hangi tarihtedir?",
        "options": ["19 Mayıs", "23 Nisan", "29 Ekim", "30 Ağustos"],
        "correct": "29 Ekim",
    },
    {
        "category": "Tarih",
        "question": "Türkiye kaç yılında kuruldu?",
        "options": ["1920", "1923", "1938", "1950"],
        "correct": "1923",
    },
    {
        "category": "Tarih",
        "question": "İlk dünya savaşı kaç yılında başladı?",
        "options": ["1914", "1920", "1939", "1945"],
        "correct": "1914",
    },
    {
        "category": "Tarih",
        "question": "Atatürk'ün doğduğu şehir hangisidir?",
        "options": ["Ankara", "Selanik", "İstanbul", "İzmir"],
        "correct": "Selanik",
    },
]
