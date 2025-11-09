import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from sanic import Sanic
from sqlalchemy import select, func, update, exists

from base.base import ServiceBase
from constants.constant import BATCH_SIZE
from model.model import PromptModel


class PromptManager(ServiceBase):
    def __init__(self, app: Sanic):
        self.add_service("prompt", self)
        self.__app = app
        self.__executor = ThreadPoolExecutor()

    async def init_prompts(self):
        # 判断表prompt是否已经有数据，如果有数据则跳过初始化
        async with self.session:
            # 查询表是否为空
            stmt = select(exists().select_from(PromptModel))
            result = (await self.session.execute(stmt)).scalar()
        if not result:
            await self.__init_prompts()

    """PRIVATE"""

    async def __init_prompts(self):
        # 解析文件instruction_attack_scenarios内容并初始化到prompt表中
        instruction_prompt_file = Path(self.get_service("file").data_path, "instruction_attack_scenarios.json")
        with instruction_prompt_file.open(encoding="utf-8") as file:
            data = json.load(file)

        prompts, count = [], 0
        for key, values in data.items():
            for item in values:
                prompt = item.get("prompt")
                if not prompt:
                    continue
                item = PromptModel(prompt_id=str(uuid.uuid4()), type=key, prompt=prompt,
                                   response=item.get("response", ""))
                prompts.append(item)
                # 分批写入数据，每次最多只写入BATCH_SIZE条数据，防止慢SQL
                if len(prompts) == BATCH_SIZE:
                    async with self.session:
                        self.session.add_all(prompts)
                        await self.session.commit()
                        count += BATCH_SIZE
                    prompts = []
                else:
                    continue
            if len(prompts) == BATCH_SIZE:
                async with self.session:
                    self.session.add_all(prompts)
                    await self.session.commit()
                    count += BATCH_SIZE
                prompts = []
            else:
                continue
        if prompts:
            async with self.session:
                self.session.add_all(prompts)
                await self.session.commit()
                count += BATCH_SIZE
