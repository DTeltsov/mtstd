import asyncio
import time
import uuid

from aiohttp import ContentTypeError, ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from app.logger import logger
from app.src.localization import translate


class Database:
    """
    The `Database` class represents an interface for interacting with a remote API.

    Attributes:
    - url (str): The base URL of the API.
    - token (str): The authentication token.

    Methods:
    - get_default_headers(token, req_uuid): Returns default headers for API requests.
    - _get_api_error_data(response, request_uuid): Extracts error data from the API response.
    - request(method, endpoint, token=None, url=None, need_log_params=True, **kwargs): Sends an API request.
    - login(data): Authenticates a user based on the provided data.
    - get_album(title): Retrieves album information based on the title.
    - get_author(name): Retrieves author information based on the name.
    - get_songs_by_genre(genre): Retrieves songs based on the genre.
    - activate_subscription(): Activates a subscription.

    Note: The methods in this class are asynchronous and should be awaited in an asynchronous context.
    """
    def __init__(self):
        """
        Initializes a new `Database` instance.

        Sets the default base URL of the API and initializes the token to `None`.
        """
        self.url = 'http://localhost:8000/api_v1/'
        self.token = None

    @staticmethod
    def get_default_headers(token, req_uuid):
        """
        Returns default headers for API requests.

        Parameters:
        - token (str): The authentication token.
        - req_uuid (str): The unique identifier for the request.

        Returns:
        dict: Default headers for API requests.
        """
        headers = {"RequestUUID": req_uuid or ""}
        if token:
            headers.update({'Authorization': f'Token {token}'})
        return headers

    @staticmethod
    async def _get_api_error_data(response, request_uuid):
        """
        Extracts error data from the API response.

        Parameters:
        - response: The API response object.
        - request_uuid (str): The unique identifier for the request.

        Returns:
        Any: Error data extracted from the API response.
        """
        try:
            error = await response.json()
        except ContentTypeError:
            error = await response.text()
            try:
                soup = BeautifulSoup(error, 'html.parser')
                summary_div = soup.find(id='summary')
                h1_text = summary_div.find('h1').get_text(strip=True).replace('\n', '')
                exception_value_text = summary_div.find(class_='exception_value').get_text(strip=True)
            except (TypeError, AttributeError):
                pass
            else:
                error = f"HTML {response.status}: {exception_value_text} {h1_text}"

        escaped_error = str(error).replace('<', r'\<')
        logger.error(f"API body of {request_uuid}: {escaped_error}")
        return error

    async def request(self, method, endpoint, token=None, url=None, need_log_params=True, file=False, **kwargs):
        """
        Sends an API request.

        Parameters:
        - method: The HTTP method for the request (e.g., `session.get`).
        - endpoint (str): The API endpoint.
        - token (str): The authentication token.
        - url (str): The base URL of the API.
        - need_log_params (bool): Indicates whether to log the request parameters.
        - **kwargs: Additional keyword arguments for the API request.

        Returns:
        Tuple[bool, Any]: A tuple indicating the success status and the data received from the API.
        """
        if not url:
            url = self.url
        request_uuid = uuid.uuid4()
        logger.info(f"Start API {method.__name__} {endpoint!r} request {request_uuid} "
                    f"{kwargs if need_log_params else ''}")
        start = time.time()
        try:
            async with method(
                    url + endpoint if not file else endpoint,
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
                data = await resp.read() if file else await resp.json()
        except asyncio.CancelledError as e:
            logger.error(f"API coroutine was cancelled {request_uuid}: {time.time() - start}, {e!r}")
            raise
        except (asyncio.TimeoutError, TimeoutError) as e:
            logger.error(f"API timeout {request_uuid}: {time.time() - start}, {e!r}")
            raise
        return True, data

    async def login(self, data):
        """
        Authenticates a user based on the provided data.

        Parameters:
        - data: Data for user authentication.

        Returns:
        dict: User authentication result.
        """
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            if token := data.get('token'):
                ok, result = await self.request(
                    session.get, 'auth_api/login_by_token/', need_log_params=False, token=token
                )
            else:
                ok, result = await self.request(session.post, 'auth_api/login/', need_log_params=False, json=data)
            if not ok:
                return {}
            self.token = result.get('token')
            return result

    async def get_album(self, title):
        """
        Retrieves album information based on the title.

        Parameters:
        - title (str): The title of the album.

        Returns:
        dict: Album information.
        """
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'music/album/', params=dict(title=title))
            if not ok:
                return {}
            return result

    async def get_author(self, name):
        """
        Retrieves author information based on the name.

        Parameters:
        - name (str): The name of the author.

        Returns:
        dict: Author information.
        """
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'music/author/', name=name)
            if not ok:
                return {}
            return result

    async def get_songs_by_genre(self, genre):
        """
        Retrieves songs based on the genre.

        Parameters:
        - genre (str): The genre of the songs.

        Returns:
        dict: Information about songs matching the specified genre.
        """
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'music/song/', genre=genre)
            if not ok:
                return {}
            return result

    async def activate_subscription(self):
        """
        Activates a subscription.

        Returns:
        dict: Information about the activated subscription.
        """
        async with ClientSession(timeout=ClientTimeout(5)) as session:
            ok, result = await self.request(session.get, 'auth_api/subscribe/')
            if not ok:
                return {}
            return result

    async def download_audio(self, url):
        async with ClientSession() as session:
            ok, result = await self.request(session.get, url, file=True)
            if not ok:
                return {}
            return result
