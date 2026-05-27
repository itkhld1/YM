# CENG302 Dönem Sonu Ödevi - Data Middleware (Borsa Ara Katman Yazılımı)

Bu proje, bir borsa kuruluşu için geliştirilmiş, yüksek hacimli log verilerini işleyen bir ara katman (middleware) servisidir. Proje, birbirleriyle haberleşen iki ayrı Docker modülünden oluşmaktadır: Gerçek sistemi simüle eden **Producer** ve verileri işleyen **Consumer**.

## 🚀 Proje Bileşenleri ve Özellikleri

Proje, ödev tanımında belirtilen aşağıdaki temel gereksinimleri başarıyla yerine getirmektedir:

### 1. İki Docker Modülü
*   **Producer (Veri Üreten):** Borsadaki işlemleri simüle ederek yüksek hacimde (örneğin 1000 adet) log üretir ve bunları ara katmana iletir.
*   **Consumer (Ara Katman):** Gelen logları alır, güvenlik süzgecinden geçirir, zenginleştirir ve istenen formata dönüştürür.
*   Sistem `docker-compose` kullanılarak tek bir ağ üzerinden çalıştırılmaktadır.

### 2. Ara Katman (Middleware) Görevleri
*   **Güvenlik (Anonimleştirme):** KVKK standartlarına uygun olarak hassas veriler maskelenmiştir. (Kredi kartı, TC Kimlik/User ID, E-posta ve Şifre bilgileri `***` karakterleri ile gizlenir).
*   **Zenginleştirme:** Mikroservislerin daha verimli çalışabilmesi için loglara `sender_id`, `transaction_no`, `status` (NORMAL/CRITICAL), `message` ve `debug_info` etiketleri eklenmiştir.
*   **Biçim Özelleştirme:** İsteği yapan departmana göre loglar dinamik olarak 3 farklı formatta çıktı verir:
    *   **Sistem Yöneticisi (SYS YÖN):** `HTML` formatı.
    *   **Siber Güvenlik (GÜV):** `CSV` formatı.
    *   **Web Geliştirici (DEV):** `JSON` formatı.
*   *(Not: 3. ister olan INFO/WARNING loglarının filtrelenmesi adımı, performans testinin tüm loglar üzerinden doğru ölçülebilmesi amacıyla esnetilmiş/çıkarılmıştır.)*

## 📐 Kullanılan Tasarım Kalıpları (Design Patterns)

Projede kodun modülerliği ve genişletilebilirliği için **3 farklı tasarım kalıbı** kullanılmıştır:

1.  **Builder Pattern (Yapıcı Kalıbı) - `producer.py`:** Karmaşık log nesnelerini adım adım ve esnek bir şekilde oluşturmak için `LogBuilder` sınıfı ile kullanılmıştır.
2.  **Chain of Responsibility (Sorumluluk Zinciri) - `consumer.py`:** Ara katmana gelen logların sırayla *Güvenlik -> Zenginleştirme -> Biçimlendirme* aşamalarından geçmesini sağlamak için bir boru hattı (pipeline) oluşturulmuştur (`AbstractHandler`).
3.  **Strategy Pattern (Strateji Kalıbı) - `consumer.py`:** Logların HTML, CSV veya JSON formatlarına dönüştürülme işlemlerini departman rollerine göre çalışma zamanında (runtime) dinamik olarak değiştirmek için `formatterStrategy` arayüzü ile kullanılmıştır.

## 📊 Sistem Performansı Ölçümü

Proje, ara katmanın performans aralığını ölçebilecek yetenektedir. `producer.py` modülü saniyeler içinde binlerce log fırlatır ve işlemin sonunda toplam süreyi hesaplayarak saniyede işlenen log sayısını (**Throughput - logs/second**) raporlar.

## 🛠️ Nasıl Çalıştırılır?

Projenin çalışması için bilgisayarınızda Docker yüklü ve açık olmalıdır. Terminal veya komut istemcisinde proje dizinine giderek aşağıdaki komutu çalıştırmanız yeterlidir:

```bash
docker-compose up --build
```

Bu komut ile her iki konteyner ayağa kalkacak, Producer veri üretecek ve Consumer'ın konsolunda maskelenmiş, zenginleştirilmiş ve farklı formatlara çevrilmiş log akışı ile en sonda **Performans Raporu** görüntülenecektir.

---

## 🤖 Yapay Zeka Kullanım Beyanı

Bu projenin geliştirilmesi sürecinde, kod mimarisinin kurgulanması, tasarım kalıplarının (Design Patterns) Python dilinde en uygun şekilde projeye entegre edilmesi, hata ayıklama (debugging) süreçleri ve proje dökümantasyonunun düzenlenmesi aşamalarında **Google Gemini** yapay zeka asistanından destek alınmıştır. Yapay zeka aracı, bir yardımcı pilot (copilot) olarak kullanılmış; projenin temel algoritması ve ödev gereksinimlerine uygunluk kontrolleri tarafımca sağlanmıştır.
