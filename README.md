# Edebiyat Matik
Edebiyat Matik – 80mm Barkod Yazıcı için Edebi Eser Yazdırma Sistemi

Edebiyat Matik; TXT dosyalarındaki Edebi Eserleri 80mm barkod / POS yazıcılar için optimize ederek,
Türkçe karakter sorunu olmadan, taşma yapmadan ve estetik bir düzenle yazdıran Python tabanlı bir uygulamadır.

Bu proje özellikle:

Kiosk sistemleri

POS yazıcı ile metin çıktısı alınması gereken uygulamalar

için tasarlanmıştır.

✨ Özellikler

✔ Türkçe karakter desteği (ç, ğ, ı, İ, ö, ş, ü sorunsuz)
✔ 80mm kağıda tam uyumlu çıktı
✔ Satır başına boşluklar dahil tam 60 karakter
✔ Yazıyı resme çevirerek yazdırma (ESC/POS encoding sorunları yok)
✔ Eser başlığı büyük puntolu ve ortalanmış
✔ Gövde metni farklı font ile yazdırma
✔ Eser bitiminde otomatik ayraç çizgisi
✔ Metin uzunluğu ne olursa olsun yazıcıdan eksiksiz çıkar
✔ Windows üzerinde kurulu olan barkod yazıcıyı kullanır (Aclas dahil)

🖨️ Desteklenen Yazıcılar

Aclas barkod / POS yazıcılar

Windows’ta normal yazdırma test sayfası alabilen tüm 80mm POS yazıcılar

Not: Yazıcı ESC/POS ile değil, Windows yazdırma altyapısı üzerinden çalışır.

🛠️ Kullanılan Teknolojiler

Python 3.10+

Pillow (PIL)

pywin32

Windows Print API

📂 Proje Yapısı
EdebiyatMatik/
│
├─ main.py
├─ print_temp.png
├─ siirler/
│   ├─ ornek_siir.txt
│   └─ ...
├─ venv/
└─ README.md

⚙️ Kurulum
1️⃣ Python kurulumu

Python 3.11 veya üstü gereklidir.

2️⃣ Sanal ortam (önerilir)
python -m venv venv
venv\Scripts\activate

3️⃣ Gerekli paketler
pip install PyQt5
pip install pillow pywin32

📝 TXT Dosya Formatı

TXT dosyalarının yapısı çok önemlidir:

ESER BAŞLIĞI
Birinci satır
İkinci satır
Üçüncü satır
...


İlk satır: Edebi Eser başlığı (büyük puntolu basılır)

Diğer satırlar: Gövde metni

🧠 Çalışma Mantığı

TXT dosyası okunur

Başlık ve gövde ayrılır

Gövde metni 60 karakterlik satırlara bölünür

Metin 80mm genişliğe uygun bir görsele dönüştürülür

Görsel Windows yazıcıya gönderilir

Yazıcı çıktıyı basar ve kağıdı düzgün şekilde keser

Bu yöntem sayesinde:

Türkçe karakter sorunu tamamen ortadan kalkar

Satır taşmaları yaşanmaz

Yazıcı modeline bağımlılık azalır

🖨️ Yazdırma Fonksiyonu (Özet)
def print_txt_as_image(file_path):
    img = "print_temp.png"
    text_to_image_80mm(file_path, img)
    print_image(img)


Bu fonksiyon çağrıldığında:

TXT → Resim

Resim → Yazıcı

İşlem otomatik tamamlanır

🎯 Neden Metni Resme Dönüştürüyoruz?

ESC/POS yazıcılarda:

Türkçe karakter setleri sorunlu

Satır genişliği üreticiye göre değişiyor

Font kontrolü sınırlı

➡ Resim tabanlı yazdırma, tüm bu sorunları kökten çözer.

🚀 Geliştirme Fikirleri

Kıta arası otomatik boşluk

Otomatik kağıt kesme optimizasyonu

Dokunmatik kiosk entegrasyonu

⚠️ Bilinen Sınırlamalar

Sadece Windows desteklenir

Yazıcı Windows’a tanıtılmış olmalıdır

Yazıcı sürücüsü düzgün çalışmalıdır

