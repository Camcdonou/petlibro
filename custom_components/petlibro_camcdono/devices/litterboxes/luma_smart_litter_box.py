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
        return self.online

    @property
    def online(self) -> bool:
        """Return the online status of the litter box."""
        return bool(self._data.get("online", False))

    @property
    def wifi_rssi(self) -> int:
        """Get the Wi-Fi signal strength."""
        return self._data.get("wifiRssi", -100)

    @property
    def wifi_rssi_level(self) -> int:
        """Get the Wi-Fi signal strength level (1-4)."""
        return self._data.get("wifiRssiLevel", 0)

    @property
    def battery_state(self) -> str:
        """Get the battery state."""
        return self._data.get("batteryState", "unknown")

    @property
    def electric_quantity(self) -> int:
        """Get the electric quantity/battery percentage."""
        return self._data.get("electricQuantity", 0)

    # Waste Management
    @property
    def rubbish_full_state(self) -> bool:
        """Check if the waste bin is full."""
        return bool(self._data.get("rubbishFullState", False))

    @property
    def rubbish_inplace_state(self) -> bool:
        """Check if the waste bin is installed."""
        return bool(self._data.get("rubbishInplaceState", False))

    @property
    def garbage_warehouse_state(self) -> str:
        """Get the garbage warehouse state."""
        return self._data.get("garbageWarehouseState", "NORMAL")

    @property
    def garbage_warehouse_leave_state(self) -> str:
        """Get the garbage warehouse leave state."""
        return self._data.get("garbageWarehouseLeaveState", "NORMAL")

    # Maintenance & Filters
    @property
    def filter_state(self) -> str:
        """Get the filter state."""
        return self._data.get("filterState", "GOOD")

    @property
    def remaining_replacement_days(self) -> int:
        """Get the remaining filter replacement days."""
        return self._data.get("remainingReplacementDays", 0)

    @property
    def clean_state(self) -> str:
        """Get the cleanliness state."""
        return self._data.get("cleanState", "GOOD")

    @property
    def remaining_cleaning_days(self) -> int:
        """Get the remaining cleaning days."""
        return self._data.get("remainingCleaningDays", 0)

    @property
    def mat_state(self) -> str:
        """Get the mat condition state."""
        return self._data.get("matState", "GOOD")

    @property
    def remaining_mat_days(self) -> int:
        """Get the remaining mat replacement days."""
        return self._data.get("remainingMatDays", 0)

    # Door & Cleaning
    @property
    def door_state(self) -> str:
        """Get the door state (OPEN/CLOSE)."""
        return self._data.get("doorState", "CLOSE")

    @property
    def vacuum_state(self) -> bool:
        """Get the vacuum state."""
        return bool(self._data.get("vacuumState", False))

    @property
    def vacuum_mode(self) -> str:
        """Get the vacuum mode."""
        return self._data.get("vacuumMode", "NORMAL")

    @property
    def throw_mode(self) -> str:
        """Get the throw mode."""
        return self._data.get("throwMode", "NORMAL")

    # Deodorization
    @property
    def deodorization_mode(self) -> str:
        """Get the active deodorization mode."""
        return self._data.get("actDeodorizationMode", "SMART")

    @property
    def deodorization_state_on(self) -> bool:
        """Check if deodorization is currently running."""
        return bool(self._data.get("deodorizationStateOn", False))

    @property
    def deodorization_timer_off_switch(self) -> bool:
        """Get the deodorization timer off switch state."""
        return bool(self._data.get("deodorizationTimerOffSwitch", False))

    @property
    def timed_deodorization_start_time(self) -> int:
        """Get the timed deodorization start time."""
        return self._data.get("timedDeodorizationStartTime", 0)

    # Camera
    @property
    def has_camera(self) -> bool:
        """Check if device has a camera."""
        return bool(self._data.get("cameraId"))

    @property
    def camera_id(self) -> str:
        """Get the camera ID."""
        return self._data.get("cameraId", "")

    @property
    def camera_switch(self) -> bool:
        """Get the camera switch state."""
        return bool(self._data.get("cameraSwitch", False))

    @property
    def camera_auth_info(self) -> str:
        """Get the camera authentication info."""
        return self._data.get("cameraAuthInfo", "")

    @property
    def device_ai_cloud_storage_state(self) -> int:
        """Get the AI cloud storage state."""
        return self._data.get("deviceAICloudStorageState", 0)

    # Settings
    @property
    def enable_sound(self) -> bool:
        """Check if sound is enabled."""
        return bool(self._data.get("enableSound", False))

    @property
    def enable_light(self) -> bool:
        """Check if light is enabled."""
        return bool(self._data.get("enableLight", False))

    @property
    def enable_auto_upgrade(self) -> bool:
        """Check if auto upgrade is enabled."""
        return bool(self._data.get("enableAutoUpgrade", False))

    # Device Status
    @property
    def device_stopped_working(self) -> bool:
        """Check if the device has stopped working."""
        return bool(self._data.get("deviceStoppedWorking", False))

    @property
    def exception_message(self) -> str:
        """Get any exception message."""
        return self._data.get("exceptionMessage", "")

    # Firmware
    @property
    def firmware_version(self) -> str:
        """Get the firmware version."""
        return self._data.get("softwareVersion", "unknown")

    @property
    def hardware_version(self) -> str:
        """Get the hardware version."""
        return self._data.get("hardwareVersion", "unknown")

    @property
    def has_firmware_update(self) -> bool:
        """Check if a firmware update is available."""
        return bool(self._data.get("getUpgrade", {}).get("hasUpgrade", False))

    @property
    def latest_firmware_version(self) -> str:
        """Get the latest firmware version available."""
        return self._data.get("getUpgrade", {}).get("latestVersion", "unknown")

    # Button/Control Methods
    async def set_filter_reset(self):
        """Reset the filter replacement counter."""
        await self.api.set_filter_reset(self.serial)
        await self.refresh()

    async def set_cleaning_reset(self):
        """Reset the cleaning reminder counter."""
        await self.api.set_cleaning_reset(self.serial)
        await self.refresh()

    async def set_light_on(self):
        """Turn on the indicator light."""
        await self.api.set_light_enable(self.serial, True)
        await self.refresh()

    async def set_light_off(self):
        """Turn off the indicator light."""
        await self.api.set_light_enable(self.serial, False)
        await self.refresh()

    async def set_sound_on(self):
        """Turn on sound."""
        await self.api.set_sound_enable(self.serial, True)
        await self.refresh()

    async def set_sound_off(self):
        """Turn off sound."""
        await self.api.set_sound_enable(self.serial, False)
        await self.refresh()
