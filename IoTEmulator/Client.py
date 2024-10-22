import asyncio
import json
import traceback

from aiocoap import Context, Message, GET, PUT, POST, DELETE

from IoTEmulator.config_type import ControlConfig


class CoAPClient:
    def __init__(self, ip, port):
        self.uri = f"coap://{ip}:{port}"

    async def __aenter__(self):
        self.protocol = await Context.create_client_context()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.protocol:
            await self.protocol.shutdown()

    async def get(self, endpoint=""):
        protocol = await Context.create_client_context()
        request = Message(code=GET, uri=self.uri + endpoint)

        try:
            response = await protocol.request(request).response
            return json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            print(traceback.print_exception(e))
            return {"success": False, "message": "Something went wrong."}

    async def observe(self, endpoint=""):
        protocol = await Context.create_client_context()

        request = Message(code=GET, uri=self.uri + endpoint, observe=0)

        pr = protocol.request(request)

        try:
            async for response in pr.observation:
                yield json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            print(traceback.print_exception(e))
            yield {"success": False, "message": "Something went wrong."}

    async def put(self, endpoint, name, value):
        protocol = await Context.create_client_context()
        request = Message(
            code=PUT,
            uri=self.uri + endpoint,
            payload=json.dumps({"name": name, "value": value}).encode("utf-8")
        )

        try:
            response = await protocol.request(request).response
            return json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            print(traceback.print_exception(e))
            return {"success": False, "message": "Something went wrong."}

    async def post(self, endpoint, instructions: ControlConfig):
        protocol = await Context.create_client_context()
        request = Message(
            code=POST,
            uri=self.uri + endpoint,
            payload=json.dumps(instructions).encode("utf-8")
        )

        try:
            response = await protocol.request(request).response
            return json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            print(traceback.print_exception(e))
            return {"success": False, "message": "Something went wrong."}

    async def delete(self, endpoint, subscription_id):
        protocol = await Context.create_client_context()
        request = Message(
            code=DELETE,
            uri=self.uri + endpoint,
            payload=json.dumps(subscription_id).encode("utf-8")
        )

        try:
            response = await protocol.request(request).response
            return json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            print(traceback.print_exception(e))
            return {"success": False, "message": "Something went wrong."}


if __name__ == "__main__":
    async def main():
        async with CoAPClient("127.0.0.1", 9999) as client:
            # print(await client.delete("/subscribe", "7c89f78f-68d4-4175-9996-ba4f324a33a3"))
            # print(await client.delete("/subscribe", "087e1cb8-50cb-410b-a464-3f8aa1d7e9ce"))
            s1 = await client.post("/subscribe", {
                "match": "any",  # all or any
                "instructions": [
                    {
                        "device": ("127.0.0.1", 10000),
                        "name": "brightness",
                        "operator": "==",  # or = or != or < or <= or > or >=
                        "value": 10
                    },
                    {
                        "device": ("127.0.0.1", 10001),
                        "name": "humidity",
                        "operator": ">",  # or = or != or < or <= or > or >=
                        "value": 0
                    }
                ],
                "actions": [
                    {
                        "name": "temperature",
                        "value": 5  # bool or float
                    }
                ]
            })
            s2 = await client.post("/subscribe", {
                "match": "any",  # all or any
                "instructions": [
                    {
                        "device": ("127.0.0.1", 10000),
                        "name": "brightness",
                        "operator": "==",  # or = or != or < or <= or > or >=
                        "value": 10
                    },
                    {
                        "device": ("127.0.0.1", 10001),
                        "name": "humidity",
                        "operator": "<",  # or = or != or < or <= or > or >=
                        "value": 0
                    }
                ],
                "actions": [
                    {
                        "name": "temperature",
                        "value": 20  # bool or float
                    }
                ]
            })
            await asyncio.sleep(5)
            print(await client.delete("/subscribe", s1["subscription_id"]))
            await asyncio.sleep(6)
            print(await client.delete("/subscribe", s2["subscription_id"]))
        # async with CoAPClient("127.0.0.1", 10001) as client:
        #     print(await client.put("/state", "humidity", -5))
        # client = CoAPClient("coap://127.0.0.1:9999")
        # print(await client.post("/subscribe", "127.0.0.1", 10000))
        # print(await client.post("/subscribe", "127.0.0.1", 10001))
        #
        # print(await client.get("/state"))
        # print(await client.put("/state", "temperature", 11))
        # print(await client.get("/state"))
        # async for res in client.observe("/state"):
        #     print(res)


    asyncio.run(main())
