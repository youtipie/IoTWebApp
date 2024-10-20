import asyncio
import itertools
import json
import random
import traceback
import uuid

from aiocoap import resource, Message, Context

from IoTEmulator.config_type import ConfigType


class DeviceEmulator:
    def __init__(self, ip: str, port: int, config: ConfigType):
        if ip.endswith("/"):
            raise ValueError("Invalid IP Address")
        self.__ip_address = ip
        self.__port = port
        self.__config = config
        self.__config["id"] = str(uuid.uuid4())  # Assign later on the backend
        self.__state = self.__generate_state()

    def __generate_state(self) -> dict:
        new_state = {}
        values = itertools.chain(self.__config["readings"].items(), self.__config["parameters"].items())
        for (name, field) in values:
            value = self.__state.get(name) if (hasattr(self, "__state")
                                               and name in self.__config["parameters"]) else field.get("default")
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
        def __init__(self, config: ConfigType):
            self.__config = config
            super().__init__()

        async def render_get(self, request):
            payload = json.dumps(self.__config).encode("utf-8")
            return Message(payload=payload)

    class State(resource.Resource):
        def __init__(self, config: ConfigType, state):
            self.__config = config
            self.__state = state
            super().__init__()

        async def render_get(self, request):
            payload = {"success": True, "state": self.__state}
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

            self.__state[name] = value
            return Message(payload=json.dumps({"success": True}).encode("utf-8"))

        def __validate_payload(self, name, value):
            if name not in self.__config["parameters"].keys():
                return "Parameter cannot be modified or doesn't exist."

            field = self.__config["parameters"][name]
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

    async def run(self):
        root = resource.Site()
        root.add_resource(["whoami"], self.WhoAmI(self.__config))
        root.add_resource(["state"], self.State(self.__config, self.__state))

        await Context.create_server_context(root, bind=(self.__ip_address, self.__port))
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
