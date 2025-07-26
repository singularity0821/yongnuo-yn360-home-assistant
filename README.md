# YONGNUO YN360 LED video light custom component for Home Assistant

Control your YN360 LED video lights directly from Home Assistant.

The YN360 is a Bluetooth LE device, thus it is necessary to be in proximity of a Bluetooth radio attached to Home Assistant (either directly or by ESP32 Bluetooth proxy).

## Installation
Copy contents of custom_components/yongnuo_yn360/ to custom_components/yongnuo_yn360/ in your Home Assistant config folder.

## Installation using HACS
HACS is a community store for Home Assistant. Add this repository to HACS and install "YONGNUO YN360 LED video light" from there.

## Features

- Power on/off
- RGB color control
- Full config flow with auto-discovery

The device is not paired to your Home Assistant instance but instead each command that is sent to it will open a new connection.

## Requirements

- Bluetooth is available in Home Assistant instance (either directly or by proxy)
- Home Assistant 2025.7+

## Acknowledgments

This integration is heavily inspired by and based on the original [Lantern](https://github.com/kenkeiter/lantern) project by @kenkeiter, which reverse-engineered the Bluetooth protocol used by YONGNUO LED lights.
