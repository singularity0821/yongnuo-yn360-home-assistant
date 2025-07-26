from homeassistant import config_entries
import voluptuous as vol
from homeassistant.helpers import selector
from homeassistant.core import callback
from homeassistant.components.bluetooth import async_discovered_service_info
from .const import DOMAIN

class YongnuoYn360ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 0

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if "address" not in user_input:
                errors["base"] = "no_devices_found"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({}),
                    errors=errors
                )

            if not async_discovered_service_info(self.hass):
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({}),
                    errors={"base": "no_devices_found"}
                )

            await self.async_set_unique_id(user_input["address"])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"YONGNUO Light ({user_input['address']})",
                data=user_input,
            )

        YONGNUO_SERVICE_UUID = "f000aa60-0451-4000-b000-000000000000"

        devices = {
            info.address: f"{info.name or 'Unknown'} ({info.address})"
            for info in async_discovered_service_info(self.hass)
            if info.advertisement and YONGNUO_SERVICE_UUID in (info.advertisement.service_uuids or [])
        }

        if not devices:
            errors["base"] = "no_devices_found"
            schema = vol.Schema({})
        else:
            schema = vol.Schema({
                vol.Required("address"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[{"label": name, "value": address} for address, name in devices.items()],
                        translation_key="address",
                        mode="dropdown"
                    )
                )
            })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
