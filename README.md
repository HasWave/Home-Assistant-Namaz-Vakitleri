# 🕌 HasWave Namaz Vakitleri

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**İl ve ilçe bazlı namaz vakitlerini Home Assistant'a sensor olarak ekler**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=HasWave&repository=HACS-Namaz-Vakitleri&category=Integration)

</div>

---

## 📋 Özellikler

* 🕌 **Namaz Vakitleri** - İl ve ilçe bazlı güncel namaz vakitleri
* ✅ **Config Flow** - Kolay kurulum ve yapılandırma
* ⏰ **Sonraki Vakit** - Bir sonraki namaz vaktini ve kalan süreyi gösterir
* 🔄 **Otomatik Güncelleme** - Belirli aralıklarla otomatik veri güncelleme
* 📅 **Hicri Tarih** - Hicri takvim bilgisi
* 📊 **Statistics** - Home Assistant statistics sayfasında görünür

## 🚀 Hızlı Başlangıç

### 1️⃣ HACS ile Kurulum

1. Home Assistant → **HACS** → **Integrations**
2. Sağ üstteki **⋮** menüsünden **Custom repositories** seçin
3. Repository URL: `https://github.com/HasWave/HACS-Namaz-Vakitleri`
4. Category: **Integration** seçin
5. **Add** butonuna tıklayın
6. HACS → Integrations → **HasWave Namaz Vakitleri**'ni bulun
7. **Download** butonuna tıklayın
8. Home Assistant'ı yeniden başlatın

### 2️⃣ Manuel Kurulum

1. Bu repository'yi klonlayın veya indirin
2. `custom_components/haswave_namaz_vakitleri` klasörünü Home Assistant'ın `config/custom_components/` klasörüne kopyalayın
3. Home Assistant'ı yeniden başlatın

### 3️⃣ Integration Ekleme

1. Home Assistant → **Settings** → **Devices & Services**
2. Sağ alttaki **+ ADD INTEGRATION** butonuna tıklayın
3. **HasWave Namaz Vakitleri** arayın ve seçin
4. Yapılandırma formunu doldurun:
   - **İl**: Büyük harf ile il adı (örn: `İSTANBUL`, `ANKARA`, `İZMİR`)
   - **İlçe**: Opsiyonel, büyük harf ile ilçe adı (örn: `KADIKÖY`, `ÇANKAYA`)
   - **API URL**: Varsayılan: `https://api.haswave.com/api/v1/namaz`
   - **Güncelleme Aralığı**: Saniye cinsinden (varsayılan: 3600 = 1 saat)
5. **Submit** butonuna tıklayın

**✅ Sensor'lar Otomatik Oluşturulur:** Integration eklendiğinde sensor'lar direkt Home Assistant'a eklenir. Hiçbir ek kurulum gerekmez!

## 📖 Kullanım

### Home Assistant Sensor'ları

Integration otomatik olarak şu sensor'ları oluşturur:

#### `sensor.namaz_imsak`
İmsak vakti (timestamp formatında)

#### `sensor.namaz_gunes`
Güneş vakti (timestamp formatında)

#### `sensor.namaz_ogle`
Öğle vakti (timestamp formatında)

#### `sensor.namaz_ikindi`
İkindi vakti (timestamp formatında)

#### `sensor.namaz_aksam`
Akşam vakti (timestamp formatında)

#### `sensor.namaz_yatsi`
Yatsı vakti (timestamp formatında)

#### `sensor.namaz_imsak_minutes`
İmsak vakti (dakika cinsinden, statistics için)

#### `sensor.namaz_gunes_minutes`
Güneş vakti (dakika cinsinden, statistics için)

#### `sensor.namaz_ogle_minutes`
Öğle vakti (dakika cinsinden, statistics için)

#### `sensor.namaz_ikindi_minutes`
İkindi vakti (dakika cinsinden, statistics için)

#### `sensor.namaz_aksam_minutes`
Akşam vakti (dakika cinsinden, statistics için)

#### `sensor.namaz_yatsi_minutes`
Yatsı vakti (dakika cinsinden, statistics için)

#### `sensor.namaz_sonraki_vakit`
Sonraki namaz vakti (attributes içinde kalan süre bilgisi)

#### `sensor.namaz_sonraki_vakit_kalan_dakika`
Sonraki namaz vaktine kalan dakika (statistics için)

#### `sensor.namaz_tarih`
Namaz vakitleri tarihi (attributes içinde şehir, ilçe, hicri tarih)

### Dashboard Kartı

Lovelace UI'da kart ekleyin:

```yaml
type: entities
title: Namaz Vakitleri
entities:
  - entity: sensor.namaz_imsak
    name: İmsak
    icon: mdi:weather-night
  - entity: sensor.namaz_gunes
    name: Güneş
    icon: mdi:weather-sunny
  - entity: sensor.namaz_ogle
    name: Öğle
    icon: mdi:weather-sunny
  - entity: sensor.namaz_ikindi
    name: İkindi
    icon: mdi:weather-sunset
  - entity: sensor.namaz_aksam
    name: Akşam
    icon: mdi:weather-sunset-down
  - entity: sensor.namaz_yatsi
    name: Yatsı
    icon: mdi:weather-night
  - entity: sensor.namaz_sonraki_vakit
    name: Sonraki Vakit
    icon: mdi:clock-alert
```

### Otomasyon Örneği

Namaz vakti geldiğinde bildirim gönderme:

```yaml
automation:
  - alias: "Namaz Vakti Bildirimi"
    trigger:
      - platform: time
        at: "{{ states('sensor.namaz_ogle') }}"
      - platform: time
        at: "{{ states('sensor.namaz_ikindi') }}"
      - platform: time
        at: "{{ states('sensor.namaz_aksam') }}"
      - platform: time
        at: "{{ states('sensor.namaz_yatsi') }}"
    action:
      - service: notify.mobile_app
        data:
          title: "🕌 Namaz Vakti"
          message: "{{ trigger.platform }} vakti geldi!"
          data:
            priority: high
```

### Sonraki Vakit Bildirimi

Sonraki namaz vaktine kalan süreye göre bildirim:

```yaml
automation:
  - alias: "Namaz Vakti Hatırlatıcı"
    trigger:
      - platform: time_pattern
        minutes: "/5"  # Her 5 dakikada bir kontrol et
    condition:
      condition: template
      value_template: "{{ states('sensor.namaz_sonraki_vakit_kalan_dakika') | int <= 10 }}"
    action:
      - service: notify.mobile_app
        data:
          title: "🕌 Namaz Vakti Yaklaşıyor"
          message: >
            {{ state_attr('sensor.namaz_sonraki_vakit', 'name') }} vakti
            {{ states('sensor.namaz_sonraki_vakit_kalan_dakika') }} dakika sonra!
```

## 🔧 Gelişmiş Kullanım

### İlçe Belirtme

Daha doğru vakitler için ilçe belirtebilirsiniz. Integration ayarlarından ilçe bilgisini güncelleyebilirsiniz.

### Performans Optimizasyonu

* **Güncelleme Aralığı** değerini artırarak API çağrı sayısını azaltabilirsiniz (namaz vakitleri günlük değiştiği için 1 saat yeterlidir)

### Sorun Giderme

#### Sensor'lar Görünmüyor

* Integration'ın eklendiğini kontrol edin: **Settings** → **Devices & Services**
* Home Assistant'ı yeniden başlatın
* Sensor'ları **Settings** → **Devices & Services** → **Entities** bölümünden kontrol edin
* Logları kontrol edin: **Settings** → **System** → **Logs**

#### API Hatası

* İnternet bağlantınızı kontrol edin
* API URL ayarının doğru olduğundan emin olun
* İl ve ilçe değerlerinin büyük harf olduğundan emin olun
* Logları kontrol edin

#### Integration Ekleme Hatası

* HACS üzerinden doğru şekilde yüklendiğinden emin olun
* Home Assistant'ı yeniden başlatın
* `custom_components` klasörünün doğru konumda olduğundan emin olun

## 📁 Dosya Yapısı

```
HACS-Namaz-Vakitleri/
├── custom_components/
│   └── haswave_namaz_vakitleri/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── api.py
│       ├── sensor.py
│       └── config_flow.py
├── hacs.json
└── README.md
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**HasWave**

🌐 [HasWave](https://haswave.com) | 📱 [Telegram](https://t.me/HasWave) | 📦 [GitHub](https://github.com/HasWave)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

Made with ❤️ by HasWave

