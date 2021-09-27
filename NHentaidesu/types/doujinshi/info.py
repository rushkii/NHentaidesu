from NHentaidesu.scaffold import Scaffold
from NHentaidesu import types
import NHentaidesu

from datetime import datetime
from typing import Dict, List, Union
import img2pdf
import os
import aiohttp
import asyncio
import aiofiles
import sys
import zipfile
import magic
import re

M = magic.Magic(mime=True)

class DoujinInfo(types.Object, Scaffold):
    def __init__(
        self,
        nhentai: "NHentaidesu.DoujinClient",
        id: int = None,
        media_id: Union[str, int] = None,
        title: Dict[str, str] = None,
        images: "types.DoujinImage" = None,
        scanlator: str = None,
        released: "datetime" = None,
        tags: "types.DoujinTags" = None,
        pages: int = None,
        favorites: int = None,
    ):
        super().__init__(nhentai=nhentai)
        
        self.id        = id
        self.media_id  = media_id
        self.title     = title
        self.images    = images
        self.scanlator = scanlator
        self.released  = released
        self.tags      = tags
        self.pages     = pages
        self.favorites = favorites

    @staticmethod
    def _parse(nhentai, **kwargs) -> "DoujinInfo":
        return DoujinInfo(nhentai, **kwargs)

    async def related(self) -> List["types.DoujinInfo"]:
        return await self._nhentai.get_related(self.id)

    async def comments(self) -> List["types.DoujinComments"]:
        return await self._nhentai.get_comments(self.id)

    async def download_pdf(self, path: str = None) -> str:
        if path is None:
            filename = f"{re.sub('[^0-9a-zA-Z]+', '_', self.title['pretty'])}_{self.id}"
            path = f"downloads/{filename}.pdf"
            
        imbytes = await self.__handle_download()

        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        
        a4inpt = (img2pdf.mm_to_pt(200),img2pdf.mm_to_pt(300))
        layout_fun = img2pdf.get_layout_fun(a4inpt)
        
        async with aiofiles.open(path,"wb") as f:
            await f.write(img2pdf.convert(imbytes, layout_fun=layout_fun))

        return path

    async def download_zip(self, path: str = None) -> str:
        if path is None:
            filename = f"{re.sub('[^0-9a-zA-Z]+', '_', self.title['pretty'])}_{self.id}"
            path = f"downloads/{filename}.zip"

        imbytes = await self.__handle_download()

        if not os.path.exists('downloads'):
            os.mkdir('downloads')

        z = zipfile.ZipFile(path, 'w')
        
        for byte, i in zip(imbytes, range(1,len(imbytes)+1)):
            ext = NHentaidesu.utils.get_ext(byte)
            z.writestr(f"{filename}/{self.id}_{i}{ext}", byte, compress_type=zipfile.ZIP_DEFLATED)
        
        z.close()

        return path

    async def __handle_download(self) -> List[bytes]:
        self.__downloaded = 0
        
        async def __handler(ses, page):
            async with ses.get(page) as resp:
                self.__downloaded += 1
                sys.stdout.write(f"Downloading... {self.__downloaded}")
                sys.stdout.write("\r")
                return await resp.read()
        
        imbytes = []
        async with aiohttp.ClientSession() as ses:
            for page in self.images.pages:
                imbytes.append(asyncio.ensure_future(__handler(ses, page)))
            imbytes = await asyncio.gather(*imbytes)

        self.__downloaded = 0
        return imbytes