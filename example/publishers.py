import asyncio

from IoTEmulator import DeviceEmulator
from IoTEmulator import ConfigType

config: ConfigType = {
    "name": "Temp1",
    "readings": {
        "is_enabled": {
            "type": "bool",
            "default": False
        }
    },
    "parameters": {
        "brightness": {
            "type": "range",
            "min": -50,
            "max": 50,
        }
    }
}

config1: ConfigType = {
    "name": "Temp2",
    "readings": {
        "is_enabled": {
            "type": "bool"
        }
    },
    "parameters": {
        "humidity": {
            "type": "range",
            "min": -50,
            "max": 50
        }
    }
}


async def main():
    device = DeviceEmulator("127.0.0.1", 10000, "device2.json", config)
    device1 = DeviceEmulator("127.0.0.1", 10001, "device3.json", config1)

    await asyncio.gather(*[device.run(), device1.run()])


asyncio.run(main())
