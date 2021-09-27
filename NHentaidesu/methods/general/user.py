from NHentaidesu import types
from NHentaidesu.scaffold import Scaffold

from typing import List
from bs4 import BeautifulSoup as bsoup
import dateparser

class GetUser(Scaffold):
    async def get_user(
        self,
        user_id: int,
        username: str
    ) -> List["types.GetUser"]:
        result = await self.request_page(f"/users/{user_id}/{username}")
        soup = bsoup(result['text'], 'lxml')

        user_info = soup.find('div', class_='user-info')
        joined = user_info.find_next('p').text.replace('Joined: ', '')
        
        return types.GetUser._parse(
            self,
            id=user_id,
            username=username,
            slug=user_info.find_next('h1').text,
            avatar=soup.find('div', class_='bigavatar').img['src'],
            created_at=dateparser.parse(joined)
        )