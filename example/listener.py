import asyncio

from IoTEmulator import DeviceEmulator
from IoTEmulator import ConfigType


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
    device = DeviceEmulator("127.0.0.1", 9999, "device1.json", config)
    await device.run()


asyncio.run(main())
