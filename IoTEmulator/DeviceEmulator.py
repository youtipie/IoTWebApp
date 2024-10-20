import asyncio
import itertools
import json
import random
import traceback
import uuid

from aiocoap import resource, Message, Context, Code

from IoTEmulator.config_type import ConfigType


class DeviceEmulator:
    def __init__(self, ip: str, port: int, config: ConfigType):
        if ip.endswith("/"):
            raise ValueError("Invalid IP Address")
        self.__ip_address = ip
        self.__port = port
        self.config = config
        self.observed_publishers = []
        self.config["id"] = str(uuid.uuid4())  # Assign later on the backend
        self.state = self.generate_state()

    async def observe_device(self, target_ip: str, target_port: int, endpoint=""):
        context = await Context.create_client_context()
        request = Message(code=Code.GET, uri=f"coap://{target_ip}:{target_port}/state{endpoint}", observe=0)
        pr = context.request(request)

        observed_device = {"ip": target_ip, "port": target_port, "endpoint": endpoint}
        if observed_device not in self.observed_publishers:
            self.observed_publishers.append(observed_device)

        try:
            async for response in pr.observation:
                state = json.loads(response.payload.decode("utf-8"))
                print(f"Received state from {target_ip}:{target_port}: {state}")
                # TODO: Act according to instructions received
        except Exception as e:
            print(f"OBSERVE request failed: {e}")

    async def resume_observations(self):
        for publisher in self.observed_publishers:
            await self.observe_device(publisher["ip"], publisher["port"], publisher["endpoint"])

    def generate_state(self) -> dict:
        new_state = {}
        values = itertools.chain(self.config["readings"].items(), self.config["parameters"].items())
        for (name, field) in values:
            value = self.state.get(name) if (hasattr(self, "state")
                                             and name in self.config["parameters"]) else field.get("default")
            if value is None:
                match field.get("type"):
                    case "bool":
                        value = random.choice([True, False])
                    case "range":
                        if not (field.get("min") and field.get("max")):
                            raise ValueError("Range must have both min and max value.")
                        value = random.uniform(field["min"], field["max"])
                    case _:
                        raise TypeError(f"Invalid type for field: '{name}'")
            new_state[name] = value
        return new_state

    class WhoAmI(resource.Resource):
        def __init__(self, current_device):
            self.current_device = current_device
            super().__init__()

        async def render_get(self, request):
            payload = json.dumps(self.current_device).encode("utf-8")
            return Message(payload=payload)

    class State(resource.ObservableResource):
        def __init__(self, current_device):
            self.__current_device = current_device
            super().__init__()
            asyncio.get_event_loop().create_task(self.notify_changes())

        async def notify_changes(self):
            while True:
                self.__current_device.state = self.__current_device.generate_state()
                self.updated_state()
                await asyncio.sleep(5)

        async def render_get(self, request):
            payload = {"success": True, "state": self.__current_device.state}
            return Message(payload=json.dumps(payload).encode("utf-8"))

        async def render_put(self, request):
            payload = json.loads(request.payload.decode("utf-8"))
            name = payload["name"]
            value = payload["value"]

            try:
                message = self.__validate_payload(name, value)
            except Exception as e:
                print(traceback.print_exception(e))
                return Message(payload=json.dumps(
                    {"success": False, "message": "Something went wrong. Probably bad device configuration."}
                ).encode("utf-8"))
            if message:
                return Message(payload=json.dumps({"success": False, "message": message}).encode("utf-8"))

            self.__current_device.state[name] = value
            return Message(payload=json.dumps({"success": True}).encode("utf-8"))

        def __validate_payload(self, name, value):
            if name not in self.__current_device.config["parameters"].keys():
                return "Parameter cannot be modified or doesn't exist."

            field = self.__current_device.config["parameters"][name]
            match field["type"]:
                case "bool":
                    if not isinstance(value, bool):
                        return f"Invalid type: expected 'bool', got '{type(value).__name__}'"
                case "range":
                    if not isinstance(value, (int, float)):
                        return f"Invalid type: expected 'range', got '{type(value).__name__}'"
                    if not field["min"] <= value <= field["max"]:
                        return f"Parameter have to be in range [{field['min']}; {field['max']}]"
            return None

    class Subscribe(resource.Resource):
        def __init__(self, current_device):
            self.__current_device = current_device
            super().__init__()

        async def render_post(self, request):
            payload = json.loads(request.payload.decode("utf-8"))
            ip = payload.get("ip")
            port = payload.get("port")
            if not ip or not port:
                return Message(
                    payload=json.dumps({"success": False, "message": "Invalid subscription data"}).encode("utf-8"))

            asyncio.create_task(self.__current_device.observe_device(ip, port, ""))
            return Message(payload=json.dumps({"success": True, "message": "Subscription successful"}).encode("utf-8"))

    async def run(self):
        root = resource.Site()
        root.add_resource(["whoami"], self.WhoAmI(self))
        root.add_resource(["state"], self.State(self))
        root.add_resource(["subscribe"], self.Subscribe(self))

        await Context.create_server_context(root, bind=(self.__ip_address, self.__port))
        await self.resume_observations()
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    async def main():
        config: ConfigType = {
            "name": "Temp",
            "readings": {
                "is_enabled": {
                    "type": "bool"
                }
            },
            "parameters": {
                "temperature": {
                    "type": "range",
                    "default": 0,
                    "min": -50,
                    "max": 50
                }
            }
        }
        device = DeviceEmulator("127.0.0.1", 9999, config)
        await device.run()


    asyncio.run(main())
