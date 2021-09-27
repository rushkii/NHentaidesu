from NHentaidesu.scaffold import Scaffold
from NHentaidesu import types
import NHentaidesu

from typing import Dict, List

class MergedTags(types.Object, Scaffold):
    def __init__(
        self,
        nhentai: "NHentaidesu.DoujinClient" = None,
        id: int = None,
        type: str = None,
        name: str = None,
        url: str = None,
        count: int = None
    ):
        super().__init__(nhentai=nhentai)

        self.id    = id
        self.type  = type
        self.name  = name
        self.url   = url
        self.count = count

    @staticmethod
    def _parse(nhentai, **kwargs) -> "MergedTags":
        return MergedTags(nhentai, **kwargs)

    async def get_tag(self):
        return await self._nhentai.get_tag(self.id)

class DoujinTags(types.Object, Scaffold):
    def __init__(
        self,
        nhentai: "NHentaidesu.DoujinClient",
        split: Dict[str, str] = None,
        merge: List["MergedTags"] = None,
    ):
        super().__init__(nhentai=nhentai)
        
        self.split = split
        self.merge = merge

    @staticmethod
    def _parse(nhentai, **kwargs) -> "DoujinTags":
        return DoujinTags(nhentai, **kwargs)