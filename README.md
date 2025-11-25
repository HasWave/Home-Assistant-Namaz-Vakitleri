# 🕌 HasWave Namaz Vakitleri

Home Assistant entegrasyonu ile il ve ilçe bazlı namaz vakitlerini takip edin.

## 📋 Özellikler

* 🕌 **Namaz Vakitleri** - İl ve ilçe bazlı güncel namaz vakitleri
* ⏰ **Sonraki Vakit** - Bir sonraki namaz vaktini ve kalan süreyi gösterir
* 🔄 **Otomatik Güncelleme** - Belirli aralıklarla otomatik veri güncelleme
* 📅 **Hicri Tarih** - Hicri takvim bilgisi

## 🚀 Kurulum

### HACS ile Kurulum

1. HACS → Integrations → Custom repositories
2. Repository URL: `https://github.com/HasWave/Home-Assistant-Namaz-Vakitleri`
3. Category: Integration
4. Add butonuna tıklayın
5. HACS → Integrations → HasWave Namaz Vakitleri'ni bulun ve yükleyin

### Manuel Kurulum

1. Bu repository'yi klonlayın veya indirin
2. `custom_components` klasörünü Home Assistant'ın `config` klasörüne kopyalayın
3. Home Assistant'ı yeniden başlatın
4. Settings → Devices & Services → Add Integration
5. "HasWave Namaz Vakitleri" arayın ve ekleyin

## ⚙️ Yapılandırma

Integration eklerken şu bilgileri girmeniz gerekecek:

- **İl**: Büyük harf ile il adı (örn: İSTANBUL, ANKARA)
- **İlçe**: Opsiyonel, büyük harf ile ilçe adı
- **API URL**: Varsayılan: `https://api.haswave.com/api/v1/namaz`
- **Güncelleme Aralığı**: Saniye cinsinden (varsayılan: 3600)

## 📊 Sensor'lar

Entegrasyon aşağıdaki sensor'ları oluşturur:

- `sensor.namaz_imsak` - İmsak vakti
- `sensor.namaz_gunes` - Güneş vakti
- `sensor.namaz_ogle` - Öğle vakti
- `sensor.namaz_ikindi` - İkindi vakti
- `sensor.namaz_aksam` - Akşam vakti
- `sensor.namaz_yatsi` - Yatsı vakti
- `sensor.namaz_tarih` - Namaz vakitleri tarihi

## 📖 Daha Fazla Bilgi

Detaylı dokümantasyon için: [GitHub Repository](https://github.com/HasWave/Home-Assistant-Namaz-Vakitleri)

## 👨‍💻 Geliştirici

**HasWave**

🌐 [HasWave](https://haswave.com) | 📱 [Telegram](https://t.me/HasWave) | 📦 [GitHub](https://github.com/HasWave)

