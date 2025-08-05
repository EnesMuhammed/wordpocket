WordPocket - Akıllı Çeviri ve Sözlük Uygulaması
WordPocket, kullanıcıların kelimeleri anında çevirebilmesini, kendi çok dilli sözlüklerini oluşturabilmesini ve bu verileri kolayca yönetip dışa aktarabilmesini sağlayan güçlü bir masaüstü uygulamasıdır. Minimal tasarımı, çoklu dil desteği, JSON tabanlı veri saklama özelliği ve PDF olarak dışa aktarma seçenekleri ile dil öğrenenler, çevirmenler ve çok dilli içerik üreten herkes için mükemmel bir araçtır.

🚀 Temel Özellikler
✅ Anında Çeviri
Yazdığınız kelimeler 500ms sonra otomatik olarak çevrilir.

deep-translator veya yedek olarak googletrans kütüphanelerini kullanır.

Çeviri sonuçları hemen görüntülenir ve kolayca kaydedilebilir.

✅ Çok Dilli Destek
Uygulama, 20'den fazla dili destekler: Türkçe, İngilizce, Fransızca, Arapça, Almanca, Japonca, Korece, Çince ve daha fazlası.

Her dil için uygun yazı tipleri otomatik atanır. (Örn. Arapça için NotoSansArabic, Japonca için NotoSansJP)

✅ Kişiselleştirilebilir Dil Ayarları
Kullanıcılar istedikleri kaynak ve hedef dilleri seçebilir.

Birden fazla dil tanımlanabilir, butonlara tıklayarak kolayca geçiş yapılabilir.

✅ Kelime Kaydetme
Çevrilen kelimeler tek tıklama ile JSON dosyasına kaydedilir.

Aynı kelime daha önce varsa üzerine yazılır.

Her dil çifti için ayrı dosya oluşturulur (örnek: dict_EN_TR.json).

✅ Gelişmiş Sözlük Düzenleyici
"📄" butonuna tıklayarak açılan editör penceresinde kelime listeleri düzenlenebilir.

Satır ekleme, silme, kaydetme gibi işlemler desteklenir.

Kaydedilen sözlük verisi PDF olarak dışa aktarılabilir.

✅ PDF Dışa Aktarım
Tablodaki tüm kelimeler, kaynak ve hedef dillerin başlıklarıyla birlikte yüksek kaliteli PDF olarak dışa aktarılır.

Arapça gibi sağdan sola diller için arabic-reshaper ve python-bidi kullanılarak düzgün biçimlendirme sağlanır.

Her dil için uygun font dosyası kullanılarak görsel tutarlılık korunur.

✅ Minimal ve Şık Arayüz
Küçük, yarı saydam ve sabitlenebilir pencere tasarımı.

Başlık çubuğu gizlenebilir ve her zaman üstte kalabilir (overlay özelliği).

Koyu tema ve modern arayüz ile uzun süreli kullanıma uygun.

⚙️ Teknik Detaylar
Görsel Arayüz: Qt tabanlı, PySide6 ile geliştirilmiş.

Çeviri API: deep-translator (varsayılan), googletrans (yedek).

Veri Saklama: Her dil çifti için ayrı JSON dosyası (data/ klasöründe).

PDF Export: reportlab, arabic-reshaper, python-bidi kütüphaneleri ile çok dilli, RTL destekli dışa aktarım.

Font Kullanımı: Her dil için özelleştirilmiş Noto fontları ile uyumlu PDF çıktısı.

💼 Kullanım Senaryoları
Yeni bir dil öğrenen öğrenciler için kişisel sözlük oluşturma.

Çevirmenler için çevrimdışı kelime listesi hazırlama.

Çok dilli ürün geliştiren geliştiriciler için dil verisi yönetimi.

Eğitimciler için PDF çıktısı alarak sınıfta dağıtılabilir materyaller oluşturma.

🧩 Gereksinimler ve Kurulum
Gerekli Python Kütüphaneleri:
bash
Copy
Edit
pip install pyside6 deep-translator reportlab arabic-reshaper python-bidi
Not: deep-translator yerine googletrans da kullanılabilir, ancak önerilen yöntem birincisidir.

Font Dosyaları:
Uygulamanın fonts/ klasörü içinde gerekli NotoSans fontları yer almalıdır. Eğer eksikse Google Fonts üzerinden indirilebilir.

🎯 Öne Çıkanlar
Offline JSON veri yönetimi

PDF çıktılar ile arşivleme veya paylaşım kolaylığı

RTL dillerde kusursuz yazım (Arapça, İbranice vb.)

Kullanıcı dostu, sade arayüz

🔚 Sonuç
WordPocket, sade ama çok işlevli bir sözlük ve çeviri uygulamasıdır. Hem bireysel kullanıcılar hem de profesyoneller için esnek ve özelleştirilebilir yapısıyla öne çıkar. Kullanıcının kendi sözlük deneyimini oluşturmasına olanak tanırken, pratikliği ve hafifliği ile günlük kullanıma uygundur.

Bu metni uygulamanızın websitesi, README dosyası, GitHub tanıtımı veya indirme sayfasında kullanabilirsiniz. Dilerseniz PDF tanıtım broşürü hâline de getirebilirim. Yardımcı olmamı ister misiniz?
