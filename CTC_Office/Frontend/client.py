import requests as rq
import asyncio
from dotenv import load_dotenv
import os

CTC_uri = 'http://localhost:8000/api'
WAYSIDE_URI = 'http://localhost:8001/api'

async def addTrain(stations : list = []) -> dict:
    try:
        response = await rq.post(CTC_uri + '/addTrain', json={"Station" : "Station C"})
        return response
    except:
        return 500, "Internal Server Error" 
    
async def getOccupancy()->list:
    try:
        res = await rq.get(WAYSIDE_URI + '')
        return res
    except:
        return 501, "External Server Error"

