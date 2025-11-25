"""API client for HasWave Namaz Vakitleri."""
from __future__ import annotations

import logging
from typing import Any
import requests

_LOGGER = logging.getLogger(__name__)


class HasWaveNamazAPI:
    """API client for HasWave Namaz Vakitleri."""
    
    def __init__(self, api_url: str, city: str, district: str = "") -> None:
        """Initialize the API client."""
        self.api_url = api_url
        self.city = city
        self.district = district
    
    def fetch_prayer_times(self) -> dict[str, Any] | None:
        """Fetch prayer times from the API."""
        try:
            params = {"il": self.city}
            if self.district:
                params["ilce"] = self.district
            
            _LOGGER.debug(f"API isteği: {self.api_url} - Params: {params}")
            response = requests.get(self.api_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                _LOGGER.debug(f"API yanıtı: {data}")
                if data.get("success"):
                    _LOGGER.info(f"Namaz vakitleri başarıyla alındı: {data.get('vakitler', {})}")
                    return data
                else:
                    _LOGGER.error(f"API hatası: {data.get('error', 'Bilinmeyen hata')}")
            else:
                _LOGGER.error(f"HTTP hatası: {response.status_code} - {response.text}")
                
        except Exception as e:
            _LOGGER.error(f"API bağlantı hatası: {e}", exc_info=True)
        
        return None

