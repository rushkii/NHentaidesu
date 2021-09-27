from NHentaidesu import DoujinClient
import asyncio

nh = DoujinClient()

async def main():
    res = await nh.info(332957)
    print(res)

asyncio.get_event_loop().run_until_complete(main())