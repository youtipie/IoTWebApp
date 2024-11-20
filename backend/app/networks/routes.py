from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from . import bp
from .models import UserNetwork, Network, NetworkDevice
from .. import db
from ..constants import RIGHTS
from ..device.models import Device
from ..utils import with_auth, with_validation
from ..auth.models import User


@bp.route("", methods=["GET"])
@with_auth
def my_networks(user: User):
    user_networks = (
        Network.query_networks_with_rights()
        .filter(UserNetwork.user_id == user.id)
        .options(
            joinedload(Network.devices).joinedload(NetworkDevice.device),
            joinedload(Network.users).joinedload(UserNetwork.user)
        )
        .all()
    )

    return [{**network.to_dict(), "rights": rights} for network, rights in user_networks], 200


@bp.route("", methods=["POST"])
@with_auth
@with_validation({"name": str})
def create_network(user: User):
    network_name = request.json["name"]
    new_network = Network(name=network_name)
    user_network_association = UserNetwork(
        user=user,
        network=new_network,
        rights=RIGHTS["a"]["code"]
    )
    db.session.add(user_network_association)
    db.session.add(new_network)
    db.session.commit()
    return new_network.to_dict(), 201


@bp.route("<int:network_id>", methods=["PUT"])
@with_auth
@with_validation({"name": str})
def change_network(user: User, network_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) & (UserNetwork.network_id == network_id)
    ).first()

    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or It belongs to other user"}, 404
    if network_with_rights[1] != RIGHTS["a"]["code"]:
        return {"message": "You cannot rename this network"}, 403
    network_with_rights[0].name = request.json["name"]
    db.session.commit()
    return network_with_rights[0].to_dict(), 200


@bp.route("<int:network_id>", methods=["DELETE"])
@with_auth
def delete_network(user: User, network_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) & (UserNetwork.network_id == network_id)
    ).first()

    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or It belongs to other user"}, 404
    if network_with_rights[1] != RIGHTS["a"]["code"]:
        return {"message": "You cannot delete this network"}, 403
    try:
        network_with_rights[0].delete_network()
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message": "Something went wrong. Try again later"}, 500
    return {"message": "Successfully deleted network"}, 200


@bp.route("<int:network_id>/users", methods=["GET"])
@with_auth
def get_users_in_network(user: User, network_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) & (UserNetwork.network_id == network_id)
    ).first()
    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or It belongs to other user"}, 404
    users_in_network = (db.session.query(User, UserNetwork.rights)
                        .join(UserNetwork, UserNetwork.user_id == User.id)
                        .filter(UserNetwork.network_id == network_id).all())
    return [{**user_.to_dict(), "rights": rights} for user_, rights in users_in_network], 200


@bp.route("<int:network_id>/users", methods=["POST"])
@with_auth
@with_validation({"rights": str, "email": str})
def add_user_to_network(user: User, network_id: int):
    # TODO: Send email with JWT access token to accept invitation
    rights = request.json["rights"]
    if rights == RIGHTS["a"]["code"]:
        return {"message": f"You cannot add users to your network with {RIGHTS["a"]["name"]} rights"}
    email = request.json["email"]
    user_to_add = User.query.filter_by(email=email).first()
    if not user_to_add:
        return {"message": "User with such email does not exist"}
    network = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) &
        (UserNetwork.network_id == network_id) &
        (UserNetwork.rights == RIGHTS["a"]["code"])
    ).first()
    if not network:
        return {"message": "Network with such ID doesn't exist or It belongs to other user"}, 404
    try:
        user_network_association = UserNetwork(
            user=user_to_add,
            network=network[0],
            rights=rights
        )
        db.session.add(user_network_association)
        db.session.commit()
        return {"message": "Successfully added user to your network"}, 200
    except SQLAlchemyError as e:
        # print(e)
        db.session.rollback()
        return {"message": "User already belong to this network"}, 400


@bp.route("<int:network_id>/users/<int:target_user_id>", methods=["PUT"])
@with_auth
@with_validation({"rights": str})
def change_user_rights(user: User, network_id: int, target_user_id: int):
    rights = request.json["rights"]
    if user.id == target_user_id:
        return {"message": "You cannot change your own rights"}, 400
    if rights == RIGHTS["a"]["code"]:
        return {"message": f"You cannot change user rights {RIGHTS["a"]["name"]} rights"}, 400

    network_with_rights = UserNetwork.query.filter(
        (UserNetwork.user_id.in_((user.id, target_user_id))) & (UserNetwork.network_id == network_id)
    ).order_by(UserNetwork.rights.asc()).all()
    if len(network_with_rights) != 2:
        return ({"message": "Network with such ID doesn't exist or user with such id does not belong to your network"},
                404)
    if network_with_rights[0].user_id != user.id:
        return {"message": "You are not admin of this network"}, 403
    try:
        network_with_rights[1].rights = rights
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message": "Something went wrong. Try again later"}, 500
    return {"message": "Successfully changed user rights"}, 200


@bp.route("<int:network_id>/users/<int:target_user_id>", methods=["DELETE"])
@with_auth
def delete_user_from_network(user: User, network_id: int, target_user_id: int):
    if user.id == target_user_id:
        return {"message": "You cannot delete yourself from your network"}, 400

    network_with_rights = UserNetwork.query.filter(
        (UserNetwork.user_id.in_((user.id, target_user_id))) & (UserNetwork.network_id == network_id)
    ).order_by(UserNetwork.rights.asc()).all()
    if len(network_with_rights) != 2:
        return ({"message": "Network with such ID doesn't exist or user with such id does not belong to your network"},
                404)
    if network_with_rights[0].user_id != user.id:
        return {"message": "You are not admin of this network"}, 403
    try:
        db.session.query(UserNetwork).filter(UserNetwork.network_id == network_id).filter(
            UserNetwork.user_id == target_user_id).delete()
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message": "Something went wrong. Try again later"}, 500
    return {"message": "Successfully deleted user from your network"}, 200


@bp.route("<int:network_id>/quit", methods=["POST"])
@with_auth
def quit_network(user: User, network_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) & (UserNetwork.network_id == network_id)
    ).first()
    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or you already quit it"}, 404
    if network_with_rights[1] == RIGHTS["a"]["code"]:
        try:
            network_with_rights[0].delete_network()
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {"message": "Something went wrong. Try again later"}, 500
    else:
        db.session.query(UserNetwork).filter(UserNetwork.network_id == network_id).filter(
            UserNetwork.user_id == user.id).delete()
        db.session.commit()
    return {"message": "Successfully quit network"}, 200


@bp.route("<int:network_id>/devices", methods=["GET"])
@with_auth
def get_devices_in_network(user: User, network_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) & (UserNetwork.network_id == network_id)
    ).first()
    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or It belongs to other user"}, 404
    device_in_network = (
        db.session.query(Device).join(NetworkDevice, NetworkDevice.device_id == Device.id)
        .join(Network, NetworkDevice.network_id == Network.id)
        .filter(NetworkDevice.network_id == network_id)
        .all()
    )
    return [device.to_dict() for device in device_in_network], 200


@bp.route("<int:network_id>/devices", methods=["POST"])
@with_auth
@with_validation({"ip": str, "port": int, "name": str})
def add_device_to_network(user: User, network_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) &
        (UserNetwork.network_id == network_id) &
        (UserNetwork.rights.in_((RIGHTS["a"]["code"], RIGHTS["w"]["code"])))
    ).first()
    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or don't have appropriate rights"}, 404
    try:
        ip = request.json["ip"]
        port = request.json["port"]
        name = request.json["name"]
        device = Device.query.filter_by(ip=ip, port=port).first()

        if not device:
            device = Device(ip=ip, port=port, name=name)

        network_device_association = NetworkDevice(
            device=device,
            network=network_with_rights[0]
        )

        db.session.add(network_device_association)
        db.session.commit()
    except ValueError as e:
        return {"message": str(e)}, 400
    except SQLAlchemyError as e:
        print(e)
        return {"message": "Something went wrong. Try again later"}, 500
    return device.to_dict(), 200


@bp.route("<int:network_id>/devices/<int:device_id>", methods=["DELETE"])
@with_auth
def delete_device_from_network(user: User, network_id: int, device_id: int):
    network_with_rights = Network.query_networks_with_rights().filter(
        (UserNetwork.user_id == user.id) &
        (UserNetwork.network_id == network_id) &
        (UserNetwork.rights.in_((RIGHTS["a"]["code"], RIGHTS["w"]["code"])))
    ).first()
    if not network_with_rights:
        return {"message": "Network with such ID doesn't exist or don't have appropriate rights"}, 404
    device_association = NetworkDevice.query.filter_by(device_id=device_id, network_id=network_id).first()
    if not device_association:
        return {"message": "No device with such id in this network"}
    try:
        # TODO: Delete all observation from device. Or forbid on frontend
        db.session.delete(device_association)
        db.session.commit()
        # Check if device is present in other networks. If no - delete device
        remaining_associations = db.session.query(NetworkDevice).filter_by(
            device_id=device_id
        ).count()
        if remaining_associations == 0:
            device = db.session.query(Device).filter_by(id=device_id).first()
            db.session.delete(device)
            db.session.commit()
    except ValueError as e:
        return {"message": str(e)}, 400
    except SQLAlchemyError as e:
        # print(e)
        return {"message": "Unexpected error occurred. Try again later"}, 500
    return {"message": "Successfully deleted"}, 200
