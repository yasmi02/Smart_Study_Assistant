- Akıllı Öğrenme Asistanı, kullanıcıların öğrenmek istedikleri konular hakkında yapay zeka destekli öneriler sunan bir web uygulamasıdır. Machine Learning algoritmaları kullanarak, kullanıcının sorgusuna en uygun öğrenme kaynaklarını ve konuları önerir.

- Sample_topics.jason'daki linkleri google'dan ve youtube'dan aldım. Keyword'leri de ona göre belirledim.

- Text_Proccessor kısmında İngilizce ve Türkçe harmonisi kurmaya uğraştım. Site Türkçe ağırlıklı, ama İngilizce keyword aratarak da kaynak bulabilirsin.

- Konu Keşfi kısmındaki konu isimlerini Arı Bilgi'nin ana sayfasından esinlendim, biraz da kendim kattım ve yeni konular ekledim.

- Kullanıcı Adı kısmında bir üyelik sistemine ihtiyaç yok. 'Misafir' yerine istediğin adı girdiğin zaman sisteme girilmiş oluyor. Streak sistemi ise aynı, üyeliğe ihtiyaç yok. Bilgisayarından girdiğin an saymaya başlamış oluyor.

## Sitenin amacı? ##

Öğrenme sürecini kişiselleştirmek
Doğru kaynaklara hızlıca ulaşmayı sağlamak
Öğrenme motivasyonunu artırmak (streak sistemi)
Öğrenme istatistiklerini görselleştirmek

## Özellikler ## 

**Akıllı Öneri Sistemi**

TF-IDF + Cosine Similarity ile konu önerileri
19 farklı teknoloji konusu
Zorluk seviyesine göre (Başlangıç, Orta, İleri) kaynak önerileri


**Kapsamlı Kaynak Veritabanı**


**İstatistik ve Analiz**

Öğrenme geçmişi takibi
Görsel grafikler ve analizler
En çok aranan konular
Zaman çizelgesi grafikleri
Kelime sıklığı analizi

**Motivasyon Sistemi**

Streak sistemi: öğrenme günlerini takip et

**Konu Keşfi**

Tüm konuları keşfet
Her konu için detaylı bilgi ve kaynaklar
İlgili konular önerisi (bu percentage ile işliyor)

**Veri Yönetimi**

SQLite veritabanı
Sorgu geçmişi kaydetme
CSV export özelliği
Kullanıcı takibi

## Nasıl Kurulur? ##

- Bu siteyi Streamlit ile kurdum, yani başlatmak için Terminal'e "streamlit run app.py" bashlenmesi gerekecek.

- Site kurulumu için Terminal'e "pip install -r requirements.txt" bashlemen gerek.
