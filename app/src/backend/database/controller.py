import asyncio
import time
import uuid

from aiohttp import ContentTypeError, ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from app.logger import logger
from app.src.localization import translate

empty = object()


class Database:
    def __init__(self):
        self.url = 'http://localhost:8000/api_v1/'
        self.token = None

    @staticmethod
    def get_default_headers(token, req_uuid):
        headers = {"RequestUUID": req_uuid or ""}
        if token:
            headers.update({'Authorization': f'Token {token}'})
        return headers

    @staticmethod
    async def _get_api_error_data(response, request_uuid):
        try:
            error = await response.json()
        except ContentTypeError:
            error = await response.text()
            try:
                soup = BeautifulSoup(error, 'html.parser')
                summary_div = soup.find(id='summary')
                h1_text = summary_div.find('h1').get_text(strip=True).replace('\n', '')
                exception_value_text = summary_div.find(class_='exception_value').get_text(strip=True)
            except TypeError:
                pass
            else:
                error = f"HTML {response.status}: {exception_value_text} {h1_text}"

        escaped_error = str(error).replace('<', r'\<')
        logger.error(f"API body of {request_uuid}: {escaped_error}")
        return error

    async def request(self, method, endpoint, token=None, url=None, need_log_params=True, **kwargs):
        if not url:
            url = self.url
        request_uuid = uuid.uuid4()
        logger.info(f"Start API {method.__name__} {endpoint!r} request {request_uuid} "
                    f"{kwargs if need_log_params else ''}")
        start = time.time()
        try:
            async with method(
                    url + endpoint,
                    headers=self.get_default_headers(token or self.token, str(request_uuid)),
                    **kwargs,
            ) as resp:
                logger.debug(f"Received API response {request_uuid}: "
                             f"status {resp.status}, request time {time.time() - start:.2f}s")
                if not resp.ok:
                    if resp.status != 504:
                        error = await self._get_api_error_data(resp, request_uuid)
                    else:
                        raise Exception(translate('api', 'request_timeout_error'))

                    return False, error
                data = await resp.json()
        except asyncio.CancelledError as e:
            logger.error(f"API coroutine was cancelled {request_uuid}: {time.time() - start}, {e!r}")
            raise
        except (asyncio.TimeoutError, TimeoutError) as e:
            logger.error(f"API timeout {request_uuid}: {time.time() - start}, {e!r}")
            raise
        return True, data

    async def login(self, data):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.post, 'auth_api/', need_log_params=False, json=data)
            if not ok:
                return {}
            self.token = result.get('token')
            return result

    async def get_user_songs(self):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'songs/', need_log_params=False)
            if not ok:
                return {}
            return result

    async def get_data_by_name(self, name):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'anything/', name=name)
            if not ok:
                return {}
            return result

    async def get_album(self, title):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'album/', title=title)
            if not ok:
                return {}
            return result

    async def get_author(self, name):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'author/', name=name)
            if not ok:
                return {}
            return result

    async def get_songs_by_genre(self, genre):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'songs/', genre=genre)
            if not ok:
                return {}
            return result

    async def get_songs_by_genre(self, genre):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'songs/', genre=genre)
            if not ok:
                return {}
            return result

    async def activate_subscription(self):
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'auth_api/subscribe/')
            if not ok:
                return {}
            return result
