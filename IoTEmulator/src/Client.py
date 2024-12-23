import json
import traceback

from aiocoap import Context, Message, GET, PUT, POST, DELETE, error

from .config_type import ControlConfig


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
        except error.NetworkError as e:
            print(e)
            return {"success": False, "message": "Device is not reachable."}
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
        except error.NetworkError as e:
            print(e)
            yield {"success": False, "message": "Device is not reachable."}
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
        except error.NetworkError as e:
            print(e)
            return {"success": False, "message": "Device is not reachable."}
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
        except error.NetworkError as e:
            print(e)
            return {"success": False, "message": "Device is not reachable."}
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
        except error.NetworkError as e:
            print(e)
            return {"success": False, "message": "Device is not reachable."}
        except Exception as e:
            print(traceback.print_exception(e))
            return {"success": False, "message": "Something went wrong."}
