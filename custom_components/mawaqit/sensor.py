"""Platform to retrieve Mawaqit prayer times information for Home Assistant."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import homeassistant.util.dt as dt_util

from .const import DATA_UPDATED, DOMAIN, PRAYER_TIMES_ICON, SENSOR_TYPES

import json
import os
import logging


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Mawaqit prayer times sensor platform."""

    client = hass.data[DOMAIN]
    if not client:
        _LOGGER.error("Error retrieving client object.")

    entities = []
    for sensor_type in SENSOR_TYPES:
        if sensor_type in [
            "Fajr",
            "Shurouq",
            "Dhuhr",
            "Asr",
            "Maghrib",
            "Isha",
            "Jumua",
            "Jumua 2",  # "Aid", "Aid 2",
            "Fajr Iqama",
            "Shurouq Iqama",
            "Dhuhr Iqama",
            "Asr Iqama",
            "Maghrib Iqama",
            "Isha Iqama",
            "Next Salat Name",
            "Next Salat Time",
            "Next Salat Preparation",
        ]:
            sensor = MawaqitPrayerTimeSensor(sensor_type, client)
            entities.append(sensor)
    async_add_entities(entities, True)

    name = "My Mosque"
    sensor1 = [MyMosqueSensor(name, hass)]
    async_add_entities(sensor1, True)


class MawaqitPrayerTimeSensor(SensorEntity):
    """Representation of an Mawaqit prayer time sensor."""

    def __init__(self, sensor_type, client):
        """Initialize the Mawaqit prayer time sensor."""
        self.sensor_type = sensor_type
        self.client = client

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.sensor_type} {SENSOR_TYPES[self.sensor_type]}"

    @property
    def unique_id(self):
        """Return the unique id of the entity."""
        return self.sensor_type

    @property
    def icon(self):
        """Icon to display in the front end."""
        return PRAYER_TIMES_ICON

    # @property
    # def state(self):
    #     """Return the state of the sensor."""
    #     return (
    #         self.client.prayer_times_info.get(self.sensor_type)
    #         .astimezone(dt_util.UTC)
    #         .isoformat()
    #     )

    @property
    def native_value(self):
        """Return the state of the sensor.  .astimezone(dt_util.UTC)"""
        if self.sensor_type in [
            "Fajr",
            "Shurouq",
            "Dhuhr",
            "Asr",
            "Maghrib",
            "Isha",
            "Jumua",
            "Jumua 2",  # "Aid", "Aid 2",
            "Fajr Iqama",
            "Shurouq Iqama",
            "Dhuhr Iqama",
            "Asr Iqama",
            "Maghrib Iqama",
            "Isha Iqama",
            "Next Salat Time",
            "Next Salat Preparation",
        ]:
            time = self.client.prayer_times_info.get(self.sensor_type)
            if time is not None:
                return time.astimezone(dt_util.UTC)
            else:
                return None

        else:
            return self.client.prayer_times_info.get(self.sensor_type)

    @property
    def should_poll(self):
        """Disable polling."""
        return False

    @property
    def device_class(self):
        """Return the device class."""
        if self.sensor_type in [
            "Fajr",
            "Shurouq",
            "Dhuhr",
            "Asr",
            "Maghrib",
            "Isha",
            "Jumua",
            "Jumua 2",  # "Aid", "Aid 2",
            "Fajr Iqama",
            "Shurouq Iqama",
            "Dhuhr Iqama",
            "Asr Iqama",
            "Maghrib Iqama",
            "Isha Iqama",
            "Next Salat Time",
            "Next Salat Preparation",
        ]:
            return SensorDeviceClass.TIMESTAMP
        else:
            return None

    async def async_added_to_hass(self):
        """Handle entity which will be added."""
        self.async_on_remove(
            async_dispatcher_connect(self.hass, DATA_UPDATED, self.async_write_ha_state)
        )


class MyMosqueSensor(SensorEntity):
    """Representation of a mosque sensor."""

    def __init__(self, name, hass):
        """Initialize the mosque sensor."""
        self.hass = hass
        self._attributes = {}
        self._name = name
        self._state = None
        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude
        self._latitude = latitude
        self._longitude = longitude

    # @Throttle(TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the latest data from the Mawaqit API."""
        current_dir = os.path.dirname(os.path.realpath(__file__))

        def read():
            with open("{}/data/my_mosque_NN.txt".format(current_dir), "r") as f:
                data = json.load(f)
            return data

        data = await self.hass.async_add_executor_job(read)

        for k, v in data.items():
            if str(k) != "uuid" and str(k) != "id" and str(k) != "slug":
                self._attributes[k] = str(v)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attributes["name"]

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:mosque"

    @property
    def extra_state_attributes(self):
        """Return attributes for the sensor."""
        return self._attributes
