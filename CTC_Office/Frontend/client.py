import requests as rq
import asyncio
from dotenv import load_dotenv
import os

uri = 'http://localhost:8000/api/addtrain'

async def addTrain(stations : list = []) -> dict:
    try:
        response = await rq.post("uri", json={"Station" : "Station C"})
        return response
    except:
        return 500, "Internal Server Error" 
