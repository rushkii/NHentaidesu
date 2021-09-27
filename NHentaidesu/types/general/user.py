from NHentaidesu.scaffold import Scaffold
from NHentaidesu import types
import NHentaidesu

from datetime import datetime
import aiohttp
import aiofiles

class GetUser(types.Object, Scaffold):
    def __init__(
        self,
        nhentai: "NHentaidesu.DoujinClient" = None,
        id: int = None,
        username: str = None,
        slug: str = None,
        avatar: str = None,
        favorite_tags: str = None,
        about: str = None,
        is_superuser: bool = None,
        is_staff: bool = None,
        created_at: "datetime" = None
    ):
        super().__init__(nhentai=nhentai)

        self.id            = id
        self.username      = username
        self.slug          = slug
        self.avatar        = avatar
        self.favorite_tags = favorite_tags
        self.about         = about
        self.is_superuser  = is_superuser
        self.is_staff      = is_staff
        self.created_at    = created_at

    @staticmethod
    def _parse(nhentai, **kwargs) -> "GetUser":
        return GetUser(nhentai, **kwargs)

    async def download_avatar(self, path: str = None) -> str:
        if path is None:
            path = f'downloads/avatar_{self.username}_{self.id}.jpg'
        
        # for stabilize between avatar path and avatar url
        avatar = self.avatar.replace(self.IMG_URL, '')

        async with aiohttp.ClientSession() as ses:
            async with ses.get(f"{self.IMG_URL}/{avatar}") as res:
                imbytes = await res.read()

        async with aiofiles.open(path, 'wb') as f:
            await f.write(imbytes)

        return path