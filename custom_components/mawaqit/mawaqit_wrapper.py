import logging
import os
from mawaqit import AsyncMawaqitClient
from mawaqit.consts import BadCredentialsException

_LOGGER = logging.getLogger(__name__)


async def _test_credentials(username, password):
    """Return True if the MAWAQIT credentials is valid."""
    try:
        client = AsyncMawaqitClient(username=username, password=password)
        await client.login()
        return True
    except BadCredentialsException:
        _LOGGER.error("Error : Bad Credentials")
        return False
    except Exception as e:
        _LOGGER.error("Error %s", e)
    finally:
        await client.close()


async def get_mawaqit_api_token(username, password):
    """Return the MAWAQIT API token."""
    try:
        client = AsyncMawaqitClient(username=username, password=password)
        token = await client.get_api_token()
    except BadCredentialsException as e:
        _LOGGER.error("Error on retrieving API Token: %s", e)
    except Exception as e:
        _LOGGER.error("Error %s", e)
    finally:
        await client.close()
    return token


async def all_mosques_neighborhood(
    latitude, longitude, mosque=None, username=None, password=None, token=None
):
    """Return mosques in the neighborhood if any. Returns a list of dicts."""
    try:
        client = AsyncMawaqitClient(
            latitude, longitude, mosque, username, password, token, session=None
        )
        await client.get_api_token()
        nearest_mosques = await client.all_mosques_neighborhood()
    except BadCredentialsException as e:
        _LOGGER.error("Error on retrieving mosques: %s", e)
    except Exception as e:
        _LOGGER.error("Error %s", e)
    finally:
        await client.close()

    return nearest_mosques


async def fetch_prayer_times(
    latitude=None, longitude=None, mosque=None, username=None, password=None, token=None
):
    """Get prayer times from the MAWAQIT API. Returns a dict."""

    try:
        client = AsyncMawaqitClient(
            latitude, longitude, mosque, username, password, token, session=None
        )
        await client.get_api_token()
        dict_calendar = await client.fetch_prayer_times()

    except BadCredentialsException as e:
        _LOGGER.error("Error on retrieving prayer times: %s", e)
    except Exception as e:
        _LOGGER.error("Error %s", e)
    finally:
        await client.close()

    return dict_calendar


def get_mawaqit_token_from_env():
    return os.environ.get("MAWAQIT_API_KEY", "NA")


def set_mawaqit_token_from_env(mawaqit_token):
    os.environ["MAWAQIT_API_KEY"] = mawaqit_token
