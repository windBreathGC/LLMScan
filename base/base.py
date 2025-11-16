from http import HTTPStatus
from typing import Tuple

import httpx
from httpx import TimeoutException, RequestError
from sanic.log import logger
from sqlalchemy.ext.asyncio import AsyncSession

from constants.constant import HTTP_TIMEOUT


class ServiceBase(object):
    __services = {}

    @classmethod
    def set_session(cls, session: AsyncSession) -> None:
        cls.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    def add_service(self, name: str, service):
        self.__services[name] = service

    @classmethod
    def get_service(cls, name: str):
        return cls.__services.get(name)

    @staticmethod
    async def http_request(method: str, url: str, **kwargs) -> Tuple:
        """发起http请求"""
        timeout, data = kwargs.get("timeout", HTTP_TIMEOUT), kwargs.get("data", {})
        body, header, param = kwargs.get("body", {}), kwargs.get("header", {}), kwargs.get("param", {})
        async with httpx.AsyncClient(trust_env=False, verify=False, follow_redirects=True) as client:
            try:
                response = await client.request(method, url, data=data, json=body, headers=header, params=param)
            except TimeoutException:
                info = f"Request {url} failed for timeout"
                logger.error(info)
                return False, info
            except RequestError:
                info = f"Failed to access {url} for request exception"
                logger.error(info)
                return False, info
            if response.status_code != HTTPStatus.OK:
                info = f"Failed to access {url} for status code is {response.status_code}"
                logger.error(info)
                return False, info
            return True, ""
