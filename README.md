<p align="center">
    <a href="https://github.com/rushkii/NHentaidesu">
        <img src="https://i.ibb.co/jHz73HD/logo-090da3be7b51.png" alt="Pyrogram">
    </a>
    <br>
    <b>NHentai API Wrapper for Python</b>
    <br>
    <img alt="Down/Week" src="https://img.shields.io/hexpm/dw/NHentaidesu">
    <img alt="Release" src="https://img.shields.io/pypi/v/NHentaidesu?color=blue&label=Release">
    <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-blue.svg">
</p>

### Usage for asynchronous
```python
from NHentaidesu import DoujinClient
import asyncio

nh = DoujinClient()

async def main():
    res = await nh.info(332957)
    print(res)

asyncio.get_event_loop().run_until_complete(main())
```
### Usage for synchronous
```python
from NHentaidesu import DoujinClient

nh = DoujinClient()
res = nh.info(332957)
print(res)
```
### Usage for login
```python
from NHentaidesu import DoujinClient

nh = DoujinClient(csrf_token="YOUR_CSRF_TOKEN", session_id="YOUR_SESSION_ID", use_proxy=True)
# if you unable to download/render the image set use_proxy to True
# use_proxy is just using a Duckduckgo image URL.
```

### Features
- **Hybrid**: Supported bot asynchronous and synchronous runtime.
- **Download**: You can download doujinshi and user avatar.
- **Complete**: This library is complete, but if you see any missing you can open issue.
- **Typed-code**: Function and object are typed.

### Question
- **Q**: How do I get my **csrf_token** and **session_id**?
- **A**: You can get it from developer tools in your PC or laptop browser.
- **Q**: Why am I receiving `ImportError: failed to find libmagic.  Check your installation`?
- **A**: You can solve it by installing libmagic. [See stackoverflow](https://stackoverflow.com/questions/18374103/exception-valuefailed-to-find-libmagic-check-your-installation-in-windows-7)

### Requirements
- Python 3.6 or higher

### Support
- You can support this library by giving a star
- If you want to donate me you can contact me in [Telegram](https://t.me/nekoha).

### Copyright
Copyright (c) 2021 [Kiizuha](hhtps://github.com/rushkii)