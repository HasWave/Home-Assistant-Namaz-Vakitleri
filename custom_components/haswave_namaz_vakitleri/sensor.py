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
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    SENSOR_IMSAK,
    SENSOR_GUNES,
    SENSOR_OGLE,
    SENSOR_IKINDI,
    SENSOR_AKSAM,
    SENSOR_YATSI,
)

SENSOR_DESCRIPTIONS: dict[str, SensorEntityDescription] = {
    SENSOR_IMSAK: SensorEntityDescription(
        key=SENSOR_IMSAK,
        name="İmsak",
        icon="mdi:weather-night",
    ),
    SENSOR_GUNES: SensorEntityDescription(
        key=SENSOR_GUNES,
        name="Güneş",
        icon="mdi:weather-sunny",
    ),
    SENSOR_OGLE: SensorEntityDescription(
        key=SENSOR_OGLE,
        name="Öğle",
        icon="mdi:weather-sunset-up",
    ),
    SENSOR_IKINDI: SensorEntityDescription(
        key=SENSOR_IKINDI,
        name="İkindi",
        icon="mdi:weather-sunset",
    ),
    SENSOR_AKSAM: SensorEntityDescription(
        key=SENSOR_AKSAM,
        name="Akşam",
        icon="mdi:weather-sunset-down",
    ),
    SENSOR_YATSI: SensorEntityDescription(
        key=SENSOR_YATSI,
        name="Yatsı",
        icon="mdi:weather-night",
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
        entities.append(HasWaveNamazSensor(hass, coordinator, description, key))
    
    async_add_entities(entities)


class HasWaveNamazSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HasWave Namaz Vakitleri sensor."""
    
    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        sensor_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._hass = hass
        self.entity_description = description
        self._sensor_key = sensor_key
        # Entity ID'yi namaz_vakti_* formatında oluştur
        self._attr_unique_id = f"namaz_vakti_{sensor_key}"
        self._attr_name = f"Namaz Vakti - {description.name}"
    
    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            _LOGGER.debug(f"Sensor {self._sensor_key}: Coordinator data is None")
            return None
        
        vakitler = self.coordinator.data.get("vakitler", {})
        if not vakitler:
            _LOGGER.warning(f"Sensor {self._sensor_key}: Vakitler boş. Data: {self.coordinator.data}")
            return None
        
        time_str = vakitler.get(self._sensor_key)
        if not time_str:
            _LOGGER.warning(f"Sensor {self._sensor_key}: Zaman bulunamadı. Vakitler keys: {list(vakitler.keys())}")
            return None
        
        # Sadece saat formatını döndür (örn: "06:16")
        # Timestamp yerine string olarak gösterilecek
        _LOGGER.debug(f"Sensor {self._sensor_key}: {time_str}")
        return time_str
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
        
        # Tüm sensor'lara il/ilçe bilgilerini ekle
        attributes = {
            "sehir": self.coordinator.data.get("sehir", ""),
            "ilce": self.coordinator.data.get("ilce", ""),
            "tarih": self.coordinator.data.get("tarih", ""),
        }
        
        return attributes

