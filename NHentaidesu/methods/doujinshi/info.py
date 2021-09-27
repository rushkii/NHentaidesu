from NHentaidesu.scaffold import Scaffold
from NHentaidesu import types

from bs4 import BeautifulSoup as bsoup
from datetime import datetime
import re

class DoujinInfo(Scaffold):
    async def info(self, id: int = None) -> "types.DoujinInfo":
        if id is None:
            html = await self.request_page('/random')
            soup = bsoup(html['text'], 'lxml')
            gallery_id = soup.find('h3', id='gallery_id').text
            parsed = int(re.search(r"([0-9]+)", gallery_id).group(1))
            data = await self.request_api(f"/gallery/{parsed}")
        else:
            data =  await self.request_api(f"/gallery/{id}")

        pages = types.List()
        split_tag = {}
        merge_tag = types.List()

        for img, num in zip(data['images']['pages'], range(len(data['images']['pages']))):
            if img['t'] == 'j':
                ext = 'jpg'
            else:
                ext = 'png'
            pages.append(f"{self.IMG_URL}/galleries/{data['media_id']}/{num+1}.{ext}")
        
        for tag in data['tags']:
            tp = tag['type']
            if tp not in split_tag:
                split_tag[tp] = []
            tag['url'] = f"{self.HOME_URL}{tag['url']}"
            split_tag[tp].append(tag)

            merge_tag.append(
                types.MergedTags._parse(
                    self,
                    id=tag['id'],
                    type=tag['type'],
                    name=tag['name'],
                    url=tag['url'],
                    count=tag['count'],
                )
            )

        if data['images']['cover'] == 'j':
            ext = '.jpg'
        else:
            ext = '.png'
        
        images = types.DoujinImage._parse(
            self,
            pages=pages,
            cover=f"{self.THUMB_URL}/galleries/{data['media_id']}/cover{ext}",
            thumbnail=f"{self.THUMB_URL}/galleries/{data['media_id']}/1{ext}"
        )

        parsed = types.DoujinInfo._parse(
            self,
            id=id,
            media_id=data['media_id'],
            title=data['title'],
            images=images,
            scanlator=None if data['scanlator'] == "" else data['scanlator'],
            released=datetime.fromtimestamp(data['upload_date']),
            tags=types.DoujinTags._parse(
                self,
                split=split_tag,
                merge=merge_tag
            ),
            pages=data['num_pages'],
            favorites=data['num_favorites']
        )
        return parsed