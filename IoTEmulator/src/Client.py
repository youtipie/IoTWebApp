import asyncio
import json

from aiocoap import Context, Message, GET, PUT


class CoAPClient:
    def __init__(self, uri):
        self.uri = uri

    async def get(self, endpoint=""):
        protocol = await Context.create_client_context()
        request = Message(code=GET, uri=self.uri + endpoint)

        try:
            response = await protocol.request(request).response
            return json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            return f"GET request failed: {e}"

    async def observe(self, endpoint=""):
        protocol = await Context.create_client_context()

        request = Message(code=GET, uri=self.uri + endpoint, observe=0)

        pr = protocol.request(request)

        try:
            async for response in pr.observation:
                yield json.loads(response.payload.decode("utf-8"))
        except Exception as e:
            print(f"OBSERVE request failed: {e}")

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
            return f"PUT request failed: {e}"


if __name__ == "__main__":
    async def main():
        client = CoAPClient("coap://127.0.0.1:9999")
        print(await client.get("/state"))
        print(await client.put("/state", "temperature", 11))
        print(await client.get("/state"))
        async for res in client.observe("/state"):
            print(res)


    asyncio.run(main())
