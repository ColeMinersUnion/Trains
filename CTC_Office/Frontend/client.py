import aiohttp
import asyncio

CTC_url = 'http://localhost:8000/api'
WAYSIDE_URL = 'http://10.5.110.45:8000'
TIMING_URL = 'http://localhost:5000/api'

headers = {"Content-Type": "application/json"}


async def post(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()  # Await the JSON response
            return data
    
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()  # Await the JSON response
            #print(data)
            return data

async def blocks():
    url = CTC_url + '/blocks'
    res = await fetch(url)
    return res

async def maintenance():
    maintenance = await blocks()
    url = WAYSIDE_URL + '/block/maintenance'
    res = await post(url, maintenance)
    print(res)

#!Sending files
async def sendFile():
    
    data = aiohttp.FormData()
    data.add_field('file',
               open('report.xls', 'rb'),
               filename='report.xls',
               content_type='application/vnd.ms-excel')

async def getSimSpeedState():
    url = TIMING_URL + '/get'
    return await fetch(url)

async def setSimSpeedState(newState: bool):
    url = TIMING_URL + '/set'
    return await post(url, {"Suggested State":newState})



if(__name__ == '__main__'):
    asyncio.run(maintenance())
    print("Done")
