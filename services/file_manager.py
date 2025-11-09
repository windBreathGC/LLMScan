from pathlib import Path

from base.base import ServiceBase


class FileManager(ServiceBase):
    def __init__(self):
        self.add_service("file", self)
        self.__data_path = Path(Path(__file__).parent.parent, "data")
        # 单次读取文件的最大数为65535，防止过多
        self.chunk = 65535

    @property
    def data_path(self):
        return self.__data_path
