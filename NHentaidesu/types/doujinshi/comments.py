from NHentaidesu.scaffold import Scaffold
from NHentaidesu import types
import NHentaidesu

from datetime import datetime

class DoujinComments(types.Object, Scaffold):
    def __init__(
        self,
        nhentai: "NHentaidesu.DoujinClient" = None,
        id: int = None,
        gallery_id: int = None,
        user: "types.GetUser" = None,
        post_date: datetime = None,
        text: str = None
    ):
        super().__init__(nhentai=nhentai)

        self.id         = id
        self.gallery_id = gallery_id
        self.user       = user
        self.post_date  = post_date
        self.text       = text

    @staticmethod
    def _parse(nhentai, **kwargs) -> "DoujinComments":
        return DoujinComments(nhentai, **kwargs)

    async def delete(self) -> bool:
        return await self._nhentai.delete_comment(self.id)

    async def flag(self, reason: str) -> bool:
        return await self._nhentai.flag_comment(self.id, reason)
