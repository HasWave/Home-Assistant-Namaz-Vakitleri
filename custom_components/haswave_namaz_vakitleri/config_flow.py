"""Config flow for HasWave Namaz Vakitleri integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_API_URL, DEFAULT_CITY
from .api import HasWaveNamazAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("city", default=DEFAULT_CITY): str,
        vol.Optional("district", default=""): str,
        vol.Optional("api_url", default=DEFAULT_API_URL): str,
        vol.Optional("update_interval", default=3600): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = HasWaveNamazAPI(
        api_url=data.get("api_url", DEFAULT_API_URL),
        city=data["city"],
        district=data.get("district", ""),
    )
    
    result = await hass.async_add_executor_job(api.fetch_prayer_times)
    
    if not result or not result.get("success"):
        raise CannotConnect
    
    return {"title": f"Namaz Vakitleri - {data['city']}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HasWave Namaz Vakitleri."""
    
    VERSION = 1
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        
        errors = {}
        
        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)
        
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

