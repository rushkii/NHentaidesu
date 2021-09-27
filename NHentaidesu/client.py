from .methods import Methods
from .scaffold import Scaffold
from .errors import Forbidden, raise_err

from bs4 import BeautifulSoup as bsoup
import asyncio, json, re, aiohttp

class DoujinClient(Methods, Scaffold):
    def __init__(
        self,
        csrf_token: str =None,
        session_id: str = None,
        use_proxy: bool = False
    ) -> None:
        super().__init__()

        self.csrf_token = csrf_token
        self.session_id = session_id
        self.use_proxy     = use_proxy

        self.cookies    = {'csrftoken': csrf_token, 'sessionid': session_id}
        self.headers    = {}
        
        asyncio.ensure_future(self.__init_login())

    async def __init_login(self) -> None:
        '''
        Initiate login for request API that required login.
        '''

        if not bool(self.csrf_token) or not bool(self.session_id):
            return None

        res = await self.request_page('/')
        soup = bsoup(res['text'], 'lxml')
        
        js = soup.find_all('script')[1]
        x_csrf = re.search(r'csrf_token: "([a-zA-Z0-9]+)"', js.prettify()).group(1)
        
        self.headers.update({'X-CSRFToken': x_csrf})
        
        get_user = soup.find('ul', class_='menu right').find_all_next('li')[1]
        user = get_user.a['href'].split('/')[2:4]
        
        print('Logged in as')
        print(f'ID      : {user[0]}')
        print(f'Username: {user[1]}')

    async def request_page(self, path, **kwargs) -> dict:
        '''
        Front-end request
        '''
        async with aiohttp.ClientSession(cookies=self.cookies) as ses:
            async with ses.get(self.HOME_URL+path, headers=self.headers, **kwargs) as res:
                return {
                    'status': res.status,
                    'text': await res.text(),
                    'headers': dict(res.headers),
                    'cookies': dict(res.cookies)
                }

    async def request_api(self, path, method="GET", **kwargs):
        '''
        API request
        '''
        async with aiohttp.ClientSession(cookies=self.cookies) as ses:
            async with ses.request(method, self.API_URL+path, headers=self.headers, **kwargs) as res:
                text = await res.text()
                
                if 'csrf token invalid' in text.lower():
                    raise Forbidden('Login required! please provide your csrf_token and session_id.')
                
                if res.status == 200:
                    return json.loads(text)
                
                raise_err(res.status, json.loads(text)['error'])