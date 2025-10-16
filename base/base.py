from sqlalchemy.ext.asyncio import AsyncSession


class ServiceBase(object):
    __services = {}

    @classmethod
    def set_session(cls, session: AsyncSession) -> None:
        cls.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    def add_service(self, name: str):
        self.__services[name] = self

    def get_service(self, name: str):
        return self.__services.get(name)

