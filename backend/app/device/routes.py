from typing import Optional

from flask import request

from IoTEmulator import CoAPClient, ControlConfig
from . import bp
from .models import Device
from ..networks.models import UserNetwork, NetworkDevice
from .. import db
from ..constants import RIGHTS
from ..utils import with_auth
from ..auth.models import User


def get_device(user_id: id, device_id: id) -> Optional[Device]:
    results = db.session.query(UserNetwork, NetworkDevice).filter(
        (UserNetwork.user_id == user_id) &
        (UserNetwork.network_id == NetworkDevice.network_id) &
        (NetworkDevice.device_id == device_id) &
        (UserNetwork.rights.in_((RIGHTS["a"]["code"], RIGHTS["w"]["code"])))
    ).first()
    return results[-1].device if results else None


@bp.route("<int:device_id>/state", methods=["GET"])
@with_auth
async def get_device_state(user: User, device_id: int):
    device = get_device(user.id, device_id)
    if not device:
        return {"message": "No device exists with such id"}, 404
    async with CoAPClient(device.ip, device.port) as client:
        response = await client.get("/state")
        return response, 200 if response["success"] else 500


@bp.route("<int:device_id>/config", methods=["GET"])
@with_auth
async def get_device_config(user: User, device_id: int):
    device = get_device(user.id, device_id)
    if not device:
        return {"message": "No device exists with such id"}, 404
    async with CoAPClient(device.ip, device.port) as client:
        response = await client.get("/whoami")
        if response:
            response["id"] = device.id
        return response, 200 if response else 500


@bp.route("<int:device_id>/subscriptions", methods=["GET"])
@with_auth
async def get_device_subscriptions(user: User, device_id: int):
    device = get_device(user.id, device_id)
    if not device:
        return {"message": "No device exists with such id"}, 404
    async with CoAPClient(device.ip, device.port) as client:
        response = await client.get("/subscribe")
        if response.get("success"):
            for subscription in response["subscriptions"]:
                for instruction in subscription["instructions"]:
                    found_device = db.session.query(Device).filter(
                        (Device.ip == instruction["device"][0]) &
                        (Device.port == instruction["device"][1])
                    ).first()
                    if not found_device:
                        return {"message": "Could not find devices from subscription:" + subscription["id"]}, 404
                    instruction["device"] = found_device.id
        return response, 200 if response["success"] else 500


@bp.route("<int:device_id>/subscriptions", methods=["POST"])
@with_auth
async def subscribe_device(user: User, device_id: int):
    subscribe_config: ControlConfig = request.json.get("config")
    if not subscribe_config:
        return {"message": "missing value for a 'config' field"}, 400

    for instruction in subscribe_config["instructions"]:
        device = get_device(user.id, instruction["device"])
        if not device:
            return {"message": "Trying to subscribe to device that does not exist"}, 404
        instruction["device"] = (device.ip, device.port)
    device = get_device(user.id, device_id)
    if not device:
        return {"message": "No device exists with such id"}, 404
    async with CoAPClient(device.ip, device.port) as client:
        response = await client.post("/subscribe", subscribe_config)
        return response, 200 if response["success"] else 500


@bp.route("<int:device_id>/subscriptions/<subscription_id>", methods=["DELETE"])
@with_auth
async def delete_subscription(user: User, device_id: int, subscription_id: int):
    device = get_device(user.id, device_id)
    if not device:
        return {"message": "No device exists with such id"}, 404
    async with CoAPClient(device.ip, device.port) as client:
        response = await client.delete("/subscribe", subscription_id)
        return response, 200 if response["success"] else 500
