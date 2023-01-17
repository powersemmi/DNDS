import asyncio
import time
from asyncio import AbstractEventLoop
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from dnd.database.models.gamesets import GameSet


@dataclass
class GameSetConfig:
    ...


class GameSetStorage:
    _gamesets: dict[int, GameSet] = {}

    def __init__(self, stay_alive: float = 60.0 * 15):
        self.set_alive = True
        self.stay_alive = stay_alive

    @classmethod
    def get_running_set(cls, set_id: int) -> GameSet | None:
        return cls._gamesets.get(set_id)

    @classmethod
    def set_resumed_set(cls, set_id: int, game_set: GameSet) -> GameSet:
        cls._gamesets[set_id] = game_set
        return cls._gamesets[set_id]

    async def cleaner(self, session: AsyncSession, delay: int = 60):
        while self.set_alive:
            current_time = time.time()
            await self.dump(session=session)
            for game_id, gameset in self._gamesets.items():
                if current_time - gameset.timer >= self.stay_alive:
                    self._gamesets.pop(game_id)
            await asyncio.sleep(delay)

    async def dump(self, session: AsyncSession) -> bool:
        res = await asyncio.gather(
            *[i.save(session=session) for i in self._gamesets.values()]
        )
        if all(res):
            return True
        else:
            return False

    def start(self, loop: AbstractEventLoop) -> None:
        asyncio.run_coroutine_threadsafe(self.cleaner(), loop=loop)
