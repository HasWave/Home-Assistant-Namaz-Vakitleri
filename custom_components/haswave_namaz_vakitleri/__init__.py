"""The HasWave Namaz Vakitleri integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .api import HasWaveNamazAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HasWave Namaz Vakitleri from a config entry."""
    
    api = HasWaveNamazAPI(
        api_url=entry.data.get("api_url", "https://api.haswave.com/api/v1/namaz"),
        city=entry.data["city"],
        district=entry.data.get("district", ""),
    )
    
    update_interval = entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL)
    
    async def async_update_data():
        """Fetch data from API."""
        return await hass.async_add_executor_job(api.fetch_prayer_times)
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=update_interval),
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok

