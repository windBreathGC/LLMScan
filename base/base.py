from sqlalchemy.ext.asyncio import AsyncSession


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

