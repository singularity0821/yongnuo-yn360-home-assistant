from .const import DOMAIN

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, config_entry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    await hass.config_entries.async_forward_entry_setups(config_entry, ["light"])
    return True

async def async_unload_entry(hass, config_entry):
    return await hass.config_entries.async_unload_platforms(config_entry, ["light"])
