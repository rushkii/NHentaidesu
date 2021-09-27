from NHentaidesu.scaffold import Scaffold
from NHentaidesu import types
import NHentaidesu

from typing import List

class DoujinImage(types.Object, Scaffold):
    def __init__(
        self,
        nhentai: "NHentaidesu.DoujinClient",
        pages: List[str] = None,
        cover: str = None,
        thumbnail: str = None,
    ):
        super().__init__(nhentai=nhentai)

        self.pages     = pages
        self.cover     = cover
        self.thumbnail = thumbnail

    @staticmethod
    def _parse(nhentai: "NHentaidesu.DoujinClient", **kwargs) -> "DoujinImage":
        if nhentai.use_proxy:
            pages = []
            for page in kwargs['pages']:
                pages.append(nhentai.DDG_URL+page)
            kwargs['pages'] = pages
            kwargs['cover'] = nhentai.DDG_URL+kwargs['cover']
            kwargs['thumbnail'] = nhentai.DDG_URL+kwargs['thumbnail']
        return DoujinImage(nhentai, **kwargs)