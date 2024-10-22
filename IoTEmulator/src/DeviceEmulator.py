import asyncio
import itertools
import json
import os
import random
import traceback
import uuid
from typing import List

from aiocoap import resource, Message, Context, Code

from IoTEmulator.src.Client import CoAPClient
from IoTEmulator.src.config_type import ConfigType, ControlConfig, operators_dict


class DeviceEmulator:
    def __init__(self, ip: str, port: int, datafile_location, config: ConfigType = None):
        if ip.endswith("/"):
            raise ValueError("Invalid IP Address")
        self.__ip_address = ip
        self.__port = port
        self.datafile_location = datafile_location
        self.config: ConfigType = {}
        self.observed_publishers = []
        self.publisher_states = {}
        self.instructions: List[ControlConfig] = []
        self.subscriptions_to_cancel = []
        self.observations = {}
        self.config["id"] = str(uuid.uuid4())  # Assign later on the backend
        self.load_data(config)
        self.state = self.generate_state()

    def save_data(self):
        data = {
            "config": self.config,
            "observed_publishers": self.observed_publishers,
            "instructions": self.instructions
        }
        with open(self.datafile_location, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self, config=None):
        if os.path.exists(self.datafile_location):
            with open(self.datafile_location, "r") as f:
                data = json.load(f)
                self.config = data.get("config", self.config)
                self.observed_publishers = data.get("observed_publishers", [])
                self.instructions = data.get("instructions", [])
            print("Data loaded successfully!")
        else:
            print("No saved data found, starting with default config.")
            if config is None:
                raise ValueError("Config cannot be empty!")
            self.config = config
            self.save_data()

    async def observe_device_state(self, target_ip: str, target_port: int):
        context = await Context.create_client_context()
        request = Message(code=Code.GET, uri=f"coap://{target_ip}:{target_port}/state", observe=0)
        pr = context.request(request)

        try:
            async for response in pr.observation:
                response = json.loads(response.payload.decode("utf-8"))
                if response.get("success"):
                    self.publisher_states[(target_ip, target_port)] = response.get("state")

                    for control_config in self.instructions:
                        try:
                            conditions = 0
                            max_conditions = 1 if control_config["match"] == "any" else (
                                len(control_config["instructions"]))
                            for instruction in control_config["instructions"]:
                                device_state = self.publisher_states.get(tuple(instruction["device"]))
                                if device_state is not None:
                                    real_value = device_state[instruction["name"]]
                                    expected_value = instruction["value"]
                                    operator = instruction["operator"]
                                    result = operators_dict[operator](real_value, expected_value)
                                    if result:
                                        conditions += 1
                                        if conditions == max_conditions:
                                            for action in control_config["actions"]:
                                                name = action["name"]
                                                value = action["value"]
                                                self.state[name] = value
                                                print(f"{control_config["id"]}: {self.state}")
                                            break
                        except (KeyError, TypeError, AttributeError) as e:
                            print(traceback.print_exception(e))
                            print("Something went wrong. Config was changed or publisher "
                                  "device changed it's state. Revoking subscription")
                            # CANCEL OR NOT? May cause bugs but I am not sure
                            self.observed_publishers.remove({"ip": target_ip, "port": target_port})
                            await self.cancel_observation((target_ip, target_port))
        except Exception as e:
            print(traceback.print_exception(e))

    async def resume_observations(self):
        for publisher in self.observed_publishers:
            print(f"Resuming observation for publisher {publisher}")
            self.observations[(publisher["ip"], publisher["port"])] = asyncio.create_task(
                self.observe_device_state(publisher["ip"], publisher["port"]))

    async def cancel_observation(self, device):
        observation = self.observations[device]
        if observation:
            observation.cancel()
            try:
                await observation
            except asyncio.CancelledError:
                print("Canceled", observation)

    async def cancel_all_observations(self):
        for observation in self.observations.values():
            if observation:
                observation.cancel()
                try:
                    await observation
                except asyncio.CancelledError:
                    print("Canceled", observation)
        self.observations = {}

    def validate_state_update(self, name, value, config=None):
        if not config:
            config = self.config
        if name not in config["parameters"].keys():
            return f"Parameter '{name}' cannot be modified or doesn't exist."

        field = config["parameters"][name]
        match field["type"]:
            case "bool":
                if not isinstance(value, bool) or isinstance(value, (int, float)):
                    return f"Invalid type: expected 'bool', got '{type(value).__name__}'"
            case "range":
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    return f"Invalid type: expected 'range', got '{type(value).__name__}'"
                if not field["min"] <= value <= field["max"]:
                    return f"'{name}' have to be in range [{field['min']}; {field['max']}]"
        return None

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
                        value = random.uniform(float(field["min"]), float(field["max"]))
                    case _:
                        raise TypeError(f"Invalid type for field: '{name}'")
            new_state[name] = value
        return new_state

    class WhoAmI(resource.Resource):
        def __init__(self, current_device):
            self.current_device = current_device
            super().__init__()

        async def render_get(self, request):
            payload = json.dumps(self.current_device.config).encode("utf-8")
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
                message = self.__current_device.validate_state_update(name, value)
            except Exception as e:
                print(traceback.print_exception(e))
                return Message(payload=json.dumps(
                    {"success": False, "message": "Something went wrong. Probably bad device configuration."}
                ).encode("utf-8"))
            if message:
                return Message(payload=json.dumps({"success": False, "message": message}).encode("utf-8"))

            self.__current_device.state[name] = value
            return Message(payload=json.dumps({"success": True}).encode("utf-8"))

    class Subscribe(resource.Resource):
        def __init__(self, current_device):
            self.__current_device = current_device
            super().__init__()

        async def render_post(self, request):
            # Instead of validating instructions while observing. Validate here and reject subscription if failed.
            control_config: ControlConfig = json.loads(request.payload.decode("utf-8"))

            try:
                if control_config["match"] not in ["all", "any"]:
                    return Message(payload=json.dumps(
                        {"success": False, "message": "Match parameter have to be either 'all' or 'any'."}
                    ).encode("utf-8"))

                # Validate actions
                actions = control_config["actions"]
                if len(actions) == 0:
                    return Message(payload=json.dumps(
                        {"success": False, "message": "No actions received!"}
                    ).encode("utf-8"))

                for action in actions:
                    name = action["name"]
                    value = action["value"]
                    validation_message = self.__current_device.validate_state_update(name, value)
                    if validation_message:
                        return Message(payload=json.dumps(
                            {"success": False, "message": validation_message}
                        ).encode("utf-8"))

                # Validate instructions
                temp_states = {}
                temp_configs = {}

                for instruction in control_config["instructions"]:
                    device = tuple(instruction["device"])  # (ip, port)
                    if not temp_states.get(device):
                        async with CoAPClient(device[0], device[1]) as client:
                            response = await client.get("/state")
                            device_state = response.get("state")
                            if not device_state:
                                return Message(payload=json.dumps({
                                    "success": False, "message": "One of the devices is inaccessible. "
                                                                 "Make sure all devices exist and connected to network."
                                }).encode("utf-8"))
                            temp_states[device] = device_state
                    if not temp_configs.get(device):
                        async with CoAPClient(device[0], device[1]) as client:
                            config = await client.get("/whoami")
                            if not config:
                                return Message(payload=json.dumps({
                                    "success": False, "message": "One of the devices is inaccessible. "
                                                                 "Make sure all devices exist and connected to network."
                                }).encode("utf-8"))
                            temp_configs[device[0], device[1]] = config
                    device_state = temp_states[device]
                    device_config = temp_configs[device]
                    name = instruction["name"]
                    operator = instruction["operator"]
                    value = instruction["value"]

                    if device_state.get(name) is None:
                        return Message(payload=json.dumps(
                            {"success": False, "message": f"Parameter '{name}' does not exist."}
                        ).encode("utf-8"))
                    if operator not in operators_dict:
                        return Message(payload=json.dumps(
                            {"success": False, "message": f"Invalid operator: {operator}"}
                        ).encode("utf-8"))
                    validation_message = self.__current_device.validate_state_update(name, value, device_config)
                    if validation_message:
                        return Message(payload=json.dumps(
                            {"success": False, "message": validation_message}
                        ).encode("utf-8"))

                    # Everything good. We can start observing
                    observed_device = {"ip": device[0], "port": device[1]}
                    if observed_device not in self.__current_device.observed_publishers:
                        self.__current_device.observed_publishers.append(observed_device)
            except (KeyError, TypeError, AttributeError) as e:
                print(traceback.print_exception(e))
                return Message(payload=json.dumps(
                    {"success": False, "message": "Invalid subscription data"}
                ).encode("utf-8"))

            # Assign id on backend?
            instruction_id = str(uuid.uuid4())
            control_config["id"] = instruction_id
            self.__current_device.instructions.append(control_config)
            await self.__current_device.cancel_all_observations()
            await self.__current_device.resume_observations()
            self.__current_device.save_data()
            return Message(payload=json.dumps(
                {"success": True, "message": "Subscription successful.", "subscription_id": instruction_id}
            ).encode("utf-8"))

        async def render_delete(self, request):
            subscription_id = json.loads(request.payload.decode("utf-8"))
            self.__current_device.instructions = [
                sub for sub in self.__current_device.instructions if sub.get("id") != subscription_id
            ]

            if len(self.__current_device.instructions) == 0:
                self.__current_device.observed_publishers = []
                # CANCEL ALL OBSERVATIONS
                await self.__current_device.cancel_all_observations()

            for subscription in self.__current_device.instructions:
                for device in self.__current_device.observed_publishers:
                    ip = device["ip"]
                    port = device["port"]
                    is_used = False

                    for instruction in subscription["instructions"]:
                        if [ip, port] == instruction["device"]:
                            is_used = True
                            break

                    if not is_used:
                        self.__current_device.observed_publishers.remove(device)
                        # CANCEL OBSERVATION TASK
                        await self.__current_device.cancel_observation((ip, port))

            self.__current_device.save_data()
            return Message(payload=json.dumps(
                {"success": True, "message": f"Subscription successfully canceled: {subscription_id}"}
            ).encode("utf-8"))

    async def run(self):
        root = resource.Site()
        root.add_resource(["whoami"], self.WhoAmI(self))
        root.add_resource(["state"], self.State(self))
        root.add_resource(["subscribe"], self.Subscribe(self))

        await Context.create_server_context(root, bind=(self.__ip_address, self.__port))
        await self.resume_observations()
        await asyncio.get_running_loop().create_future()
