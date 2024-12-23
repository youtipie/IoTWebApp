import asyncio

from IoTEmulator import CoAPClient


async def main():
    async with CoAPClient("127.0.0.1", 9999) as client:
        s1 = await client.post("/subscribe", {
            "match": "any",
            "instructions": [
                {
                    "device": ("127.0.0.1", 10000),
                    "name": "brightness",
                    "operator": "==",
                    "value": 10
                },
                {
                    "device": ("127.0.0.1", 10001),
                    "name": "humidity",
                    "operator": ">",
                    "value": 0
                }
            ],
            "actions": [
                {
                    "name": "temperature",
                    "value": 5
                }
            ]
        })
        s2 = await client.post("/subscribe", {
            "match": "any",
            "instructions": [
                {
                    "device": ("127.0.0.1", 10000),
                    "name": "brightness",
                    "operator": "==",
                    "value": 10
                },
                {
                    "device": ("127.0.0.1", 10001),
                    "name": "humidity",
                    "operator": "<",
                    "value": 0
                }
            ],
            "actions": [
                {
                    "name": "temperature",
                    "value": 20
                }
            ]
        })
        print(s1, s2)
        print(await client.get("/subscribe"))
        # await asyncio.sleep(5)
        # print(await client.delete("/subscribe", s1["subscription_id"]))
        # await asyncio.sleep(6)
        # print(await client.delete("/subscribe", s2["subscription_id"]))


asyncio.run(main())
