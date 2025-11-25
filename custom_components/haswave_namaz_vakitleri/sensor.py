"""Sensor platform for HasWave Namaz Vakitleri."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    SENSOR_IMSAK,
    SENSOR_GUNES,
    SENSOR_OGLE,
    SENSOR_IKINDI,
    SENSOR_AKSAM,
    SENSOR_YATSI,
    SENSOR_TARIH,
)

SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    SENSOR_IMSAK: SensorEntityDescription(
        key=SENSOR_IMSAK,
        name="İmsak",
        icon="mdi:weather-night",
        device_class="timestamp",
    ),
    SENSOR_GUNES: SensorEntityDescription(
        key=SENSOR_GUNES,
        name="Güneş",
        icon="mdi:weather-sunny",
        device_class="timestamp",
    ),
    SENSOR_OGLE: SensorEntityDescription(
        key=SENSOR_OGLE,
        name="Öğle",
        icon="mdi:weather-sunset-up",
        device_class="timestamp",
    ),
    SENSOR_IKINDI: SensorEntityDescription(
        key=SENSOR_IKINDI,
        name="İkindi",
        icon="mdi:weather-sunset",
        device_class="timestamp",
    ),
    SENSOR_AKSAM: SensorEntityDescription(
        key=SENSOR_AKSAM,
        name="Akşam",
        icon="mdi:weather-sunset-down",
        device_class="timestamp",
    ),
    SENSOR_YATSI: SensorEntityDescription(
        key=SENSOR_YATSI,
        name="Yatsı",
        icon="mdi:weather-night",
        device_class="timestamp",
    ),
    SENSOR_TARIH: SensorEntityDescription(
        key=SENSOR_TARIH,
        name="Tarih",
        icon="mdi:calendar",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    entities = []
    for key, description in SENSOR_DESCRIPTIONS.items():
        entities.append(HasWaveNamazSensor(coordinator, description, key))
    
    async_add_entities(entities)


class HasWaveNamazSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HasWave Namaz Vakitleri sensor."""
    
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        sensor_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._sensor_key = sensor_key
        self._attr_unique_id = f"{DOMAIN}_{sensor_key}"
        self._attr_name = f"Namaz Vakti - {description.name}"
    
    @property
    def native_value(self) -> datetime | str | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            _LOGGER.debug(f"Sensor {self._sensor_key}: Coordinator data is None")
            return None
        
        if self._sensor_key == SENSOR_TARIH:
            value = self.coordinator.data.get("tarih")
            _LOGGER.debug(f"Sensor {self._sensor_key}: Tarih = {value}")
            return value
        
        vakitler = self.coordinator.data.get("vakitler", {})
        if not vakitler:
            _LOGGER.warning(f"Sensor {self._sensor_key}: Vakitler boş. Data: {self.coordinator.data}")
            return None
        
        time_str = vakitler.get(self._sensor_key)
        if not time_str:
            _LOGGER.warning(f"Sensor {self._sensor_key}: Zaman bulunamadı. Vakitler keys: {list(vakitler.keys())}")
            return None
        
        # Tarih ve saati birleştirerek datetime oluştur
        tarih_str = self.coordinator.data.get("tarih", "")
        if not tarih_str:
            _LOGGER.warning(f"Sensor {self._sensor_key}: Tarih bulunamadı")
            return None
        
        try:
            # Tarih formatı: "2025-11-25", "25.11.2025" veya "25 Nov 2025" olabilir
            tarih_obj = None
            tarih_formats = [
                "%d %b %Y",      # "25 Nov 2025"
                "%d.%m.%Y",       # "25.11.2025"
                "%Y-%m-%d",      # "2025-11-25"
            ]
            
            for fmt in tarih_formats:
                try:
                    tarih_obj = datetime.strptime(tarih_str, fmt)
                    break
                except ValueError:
                    continue
            
            if tarih_obj is None:
                raise ValueError(f"Tarih formatı tanınmadı: {tarih_str}")
            
            # Zaman formatı: "06:16" veya "06:16:00" olabilir
            if len(time_str.split(":")) == 2:
                # "06:16" formatı
                saat_obj = datetime.strptime(time_str, "%H:%M").time()
            else:
                # "06:16:00" formatı
                saat_obj = datetime.strptime(time_str, "%H:%M:%S").time()
            
            # Tarih ve saati birleştir
            datetime_obj = datetime.combine(tarih_obj.date(), saat_obj)
            _LOGGER.debug(f"Sensor {self._sensor_key}: {time_str} -> {datetime_obj}")
            return datetime_obj
            
        except ValueError as e:
            _LOGGER.error(f"Sensor {self._sensor_key}: Zaman parse hatası - Tarih: {tarih_str}, Zaman: {time_str}, Hata: {e}")
            return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
        
        if self._sensor_key == SENSOR_TARIH:
            return {
                "sehir": self.coordinator.data.get("sehir", ""),
                "ilce": self.coordinator.data.get("ilce", ""),
            }
        
        return {}

