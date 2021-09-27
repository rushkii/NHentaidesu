class Scaffold:
    HOME_URL = 'https://nhentai.net'
    API_URL = 'https://nhentai.net/api'
    IMG_URL = 'https://i.nhentai.net'
    THUMB_URL = 'https://t.nhentai.net'
    DDG_URL = 'https://external-content.duckduckgo.com/iu/?u='

    def __init__(self) -> None:
        self.csrf_token = None
        self.session_id = None
        self.use_proxy  = False

        self.cookies    = None
        self.headers    = None

    async def request_page(self, path, **kwargs):
        pass

    async def request_api(self, path, method="GET", **kwargs):
        pass