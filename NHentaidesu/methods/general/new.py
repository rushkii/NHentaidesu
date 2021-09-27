from NHentaidesu import types
from NHentaidesu.scaffold import Scaffold
from NHentaidesu.errors import NotFound

from typing import List
from datetime import datetime

class NewDoujin(Scaffold):
    async def new(
        self,
        page: int = 1,
        offset: int = 0,
        limit: int = 10
    ) -> List["types.DoujinInfo"]:
        if offset > limit:
            offset = 0
            
        res = await self.request_api(f"/galleries/all?page={page}")

        if res['result'] == []:
            raise NotFound("Query not found.")
        
        pages = types.List()
        doujins = types.List()
        split_tag = {}
        merge_tag = types.List()
        
        for res in res['result'][offset:limit]:

            for img, num in zip(res['images']['pages'], range(len(res['images']['pages']))):
                if img['t'] == 'j':
                    ext = 'jpg'
                else:
                    ext = 'png'
                pages.append(f"{self.IMG_URL}/galleries/{res['media_id']}/{num+1}.{ext}")

            for tag in res['tags']:
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

            if res['images']['cover'] == 'j':
                ext = '.jpg'
            else:
                ext = '.png'
            images = types.DoujinImage._parse(
                self,
                pages=pages,
                cover=f"{self.THUMB_URL}/galleries/{res['media_id']}/cover{ext}",
                thumbnail=f"{self.THUMB_URL}/galleries/{res['media_id']}/1{ext}"
            )

            doujins.append(
                types.DoujinInfo._parse(
                    self,
                    id=res['id'],
                    media_id=res['media_id'],
                    title=res['title'],
                    images=images,
                    scanlator=None if res['scanlator'] == "" else res['scanlator'],
                    released=datetime.fromtimestamp(res['upload_date']),
                    tags=types.DoujinTags._parse(
                        self,
                        split=split_tag,
                        merge=merge_tag
                    ),
                    pages=res['num_pages'],
                    favorites=res['num_favorites']
                )
            )
        return doujins