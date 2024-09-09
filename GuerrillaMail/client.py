import aiohttp
import secrets
import re
import time
from aiohttp import TCPConnector
from .models import Message

class Client:
    def __init__(self,
                 proxy: str = ""):
        self.session = aiohttp.ClientSession(base_url="https://www.guerrillamail.com", raise_for_status=True, connector=TCPConnector(ssl=False))
        self.proxy = proxy
        self.host = 'www.guerrillamail.com'
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0'
    
    @property
    def headers(self):
        return {
            'Host': self.host,
            'User-Agent': self.userAgent,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': f'ApiToken {self._api_token}',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Content-Length': '34',
            'Origin': 'https://www.guerrillamail.com',
            'Referer': 'https://www.guerrillamail.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
        }
    
    async def __aenter__(self):
        await self._init_guerrilla()
        return self
    
    async def __aexit__(self,*args):
        await self.session.close()

    async def _init_guerrilla(self):
        async with self.session.get('/',proxy=self.proxy) as response:
            text = await response.text()
            self._api_token = re.compile(r"api_token : '(\w+)'",flags=re.A).findall(text)[0]
            self.domain_list = re.compile(r'<option value="([\w.]+)">',flags=re.A).findall(text)

    async def create_email(self,
                           alias: str,
                           domain: str|None = None) -> str:
        domain = domain if domain else secrets.choice(self.domain_list)
        params = {
            'f': 'set_email_user',
        }
        data = {
            'email_user': alias,
            'lang': 'en',
            'site': 'guerrillamail.com',
            'in': ' Set cancel',
        }
        await self.session.post('/ajax.php',params=params, data=data, headers=self.headers, proxy=self.proxy)
        return alias + "@" + domain
    
    async def get_messages(self,
                           email: str) -> list[Message]:
        headers = self.headers
        headers.pop('Content-Type')
        params = {
            'f': 'check_email',
            'seq': '1',
            'site': 'guerrillamail.com',
            'in': email.split("@")[0],
            '_': str(int(time.time()*1000)),
        }
        async with self.session.get('/ajax.php', params=params, headers=headers, proxy=self.proxy) as response:
            res = await response.json()
        return [Message(message) for message in res["list"]]
    
    async def delete_email(self,
                           email: str) -> bool:
        params = {
            'f': 'forget_me',
        }
        data = {
            'site': 'guerrillamail.com',
            'in': email.split('@')[0],
        }
        async with self.session.post('/ajax.php',params=params, headers=self.headers, data=data, proxy=self.proxy, raise_for_status=False) as response:
            return response.status == 200
