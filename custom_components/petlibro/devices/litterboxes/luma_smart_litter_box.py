"""Luma Smart Litter Box (PLLB001)"""
import aiohttp

from ...api import make_api_call
from aiohttp import ClientSession, ClientError
from ...exceptions import PetLibroAPIError
from ..device import Device
from typing import cast
from logging import getLogger

_LOGGER = getLogger(__name__)


class LumaSmartLitterBox(Device):
    """Represents the Luma Smart Litter Box device (PLLB001)."""

    async def refresh(self):
        """Refresh the device data from the API."""
        try:
            await super().refresh()  # Call the refresh method from the parent class (Device)

            # Fetch real info from the API
            real_info = await self.api.device_real_info(self.serial)
            data_real_info = await self.api.device_data_real_info(self.serial)
            attribute_settings = await self.api.device_attribute_settings(self.serial)
            get_upgrade = await self.api.get_device_upgrade(self.serial)

            # Update internal data with fetched API data
            self.update_data({
                "realInfo": real_info or {},
                "dataRealInfo": data_real_info or {},
                "getAttributeSetting": attribute_settings or {},
                "getUpgrade": get_upgrade or {},
            })
        except PetLibroAPIError as err:
            _LOGGER.error(f"Error refreshing data for LumaSmartLitterBox: {err}")

    @property
    def available(self) -> bool:
        """Return if the device is available."""
        _LOGGER.debug(f"Device {self.name} availability: {self.online}")
        return self.online if hasattr(self, 'online') else True

    @property
    def device_sn(self) -> str:
        """Return the device serial number."""
        return self._data.get("realInfo", {}).get("deviceSn", "unknown")

    @property
    def wifi_ssid(self) -> str:
        """Return the Wi-Fi SSID of the device."""
        return self._data.get("realInfo", {}).get("wifiSsid", "unknown")

    @property
    def online(self) -> bool:
        """Return the online status of the litter box."""
        return bool(self._data.get("realInfo", {}).get("online", False))

    @property
    def wifi_rssi(self) -> int:
        """Get the Wi-Fi signal strength."""
        return self._data.get("realInfo", {}).get("wifiRssi", -100)

    @property
    def battery_level(self) -> float:
        """Get the battery percentage (if battery powered)."""
        try:
            value = self._data.get("realInfo", {}).get("batteryLevel", 0)
            return cast(float, float(value))
        except (TypeError, ValueError):
            return 0.0

    @property
    def waste_level(self) -> int:
        """Get the waste level percentage."""
        return self._data.get("realInfo", {}).get("wasteLevel", 0)

    @property
    def litter_weight(self) -> float:
        """Get the current litter weight (in grams)."""
        return self._data.get("realInfo", {}).get("litterWeight", 0.0)

    @property
    def odor_eliminator_level(self) -> int:
        """Get the odor eliminator level percentage."""
        return self._data.get("realInfo", {}).get("odorLevel", 0)

    @property
    def times_used_today(self) -> int:
        """Get the number of times used today."""
        return self._data.get("dataRealInfo", {}).get("timesUsedToday", 0)

    @property
    def last_used_time(self) -> str:
        """Get the last time the litter box was used."""
        return self._data.get("dataRealInfo", {}).get("lastUsedTime", "unknown")

    @property
    def auto_cleaning_enabled(self) -> bool:
        """Check if auto-cleaning is enabled."""
        return bool(self._data.get("getAttributeSetting", {}).get("autoCleaningEnabled", False))

    @property
    def cleaning_interval(self) -> int:
        """Get the cleaning interval in minutes."""
        return self._data.get("getAttributeSetting", {}).get("cleaningInterval", 0)

    @property
    def filter_remaining_days(self) -> float | None:
        """Get the remaining filter days."""
        value = self._data.get("realInfo", {}).get("remainingFilterDays", 0)
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @property
    def litter_remaining_days(self) -> float | None:
        """Get the remaining litter days."""
        value = self._data.get("realInfo", {}).get("remainingLitterDays", 0)
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @property
    def firmware_version(self) -> str:
        """Get the firmware version."""
        return self._data.get("getUpgrade", {}).get("currentVersion", "unknown")

    @property
    def has_firmware_update(self) -> bool:
        """Check if a firmware update is available."""
        return bool(self._data.get("getUpgrade", {}).get("hasUpgrade", False))

    @property
    def latest_firmware_version(self) -> str:
        """Get the latest firmware version available."""
        return self._data.get("getUpgrade", {}).get("latestVersion", "unknown")
