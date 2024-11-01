import aiohttp
import asyncio

CTC_uri = 'http://localhost:8000/api'
WAYSIDE_URI = 'http://10.5.110.45:8000'

headers = {"Content-Type": "application/json"}

async def post(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()  # Await the JSON response
            return data
    
async def fetch(url):
    #blocks = await rq.get(CTC_uri + '/blocks')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()  # Await the JSON response
            #print(data)
            return data

async def blocks():
    url = CTC_uri + '/blocks'
    res = await fetch(url)
    return res

async def maintenance():
    maintenance = await blocks()
    url = WAYSIDE_URI + '/block/maintenance'
    res = await post(url, maintenance)
    print(res)

if(__name__ == '__main__'):
    asyncio.run(maintenance())
    print("Done")
