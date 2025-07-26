import asyncio
import struct
import logging
from bleak import BleakClient
from homeassistant.components.bluetooth import (
    async_ble_device_from_address,
    async_discovered_service_info,
)
from homeassistant.core import HomeAssistant

CHARACTERISTIC_UUID = "f000aa61-0451-4000-b000-000000000000"
_LOGGER = logging.getLogger(__name__)

class YongnuoYn360Device:
    def __init__(self, hass: HomeAssistant, address: str):
        self.hass = hass
        self.address = address

    async def connect_and_send(self, data: bytes):
        _LOGGER.debug("Attempting to connect to %s", self.address)

        ble_device = async_ble_device_from_address(self.hass, self.address, connectable=True)
        if not ble_device:
            _LOGGER.debug("No BLE device resolved via async_ble_device_from_address")
            _LOGGER.debug("Currently known devices:")
            for info in async_discovered_service_info(self.hass):
                _LOGGER.debug("- %s (%s) connectable=%s", info.name, info.address, info.connectable)
            for info in async_discovered_service_info(self.hass):
                if info.address == self.address:
                    ble_device = info.device
                    _LOGGER.info("Resolved device from fallback discovery: %s", ble_device)
                    break

        if not ble_device:
            raise RuntimeError(f"BLE device {self.address} not found or not connectable")

        for attempt in range(5):
            try:
                async with BleakClient(ble_device) as client:
                    await client.write_gatt_char(CHARACTERISTIC_UUID, data)
                    return
            except Exception as e:
                delay = min(2 ** attempt, 10)
                _LOGGER.warning("Connection attempt %d failed: %s (retrying in %ds)", attempt + 1, e, delay)
                await asyncio.sleep(delay)

        raise RuntimeError(f"Failed to connect to {self.address} after multiple attempts")

    async def set_color(self, r: int, g: int, b: int, brightness: int):
        r = min(max(int(r * (brightness / 100)), 0), 255)
        g = min(max(int(g * (brightness / 100)), 0), 255)
        b = min(max(int(b * (brightness / 100)), 0), 255)
        packet = struct.pack(">BBBBBB", 0xAE, 0xA1, r, g, b, 0x56)
        _LOGGER.debug("Sending set_color packet: %s", packet.hex())
        await self.connect_and_send(packet)

    async def turn_off(self):
        packet = struct.pack(">BBBBBB", 0xAE, 0xA3, 0x00, 0x00, 0x00, 0x56)
        _LOGGER.debug("Sending power_off packet: %s", packet.hex())
        await self.connect_and_send(packet)
