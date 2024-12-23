from flask_sqlalchemy.query import Query

from .. import db


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    users = db.relationship("UserNetwork", back_populates="network")
    devices = db.relationship("NetworkDevice", back_populates="network")

    @staticmethod
    def query_networks_with_rights() -> Query:
        return db.session.query(Network, UserNetwork.rights).join(
            UserNetwork, UserNetwork.network_id == Network.id
        )

    # TODO: Refactor or optimize
    def delete_network(self) -> None:
        from ..device.models import Device
        network_id = self.id
        subquery = (
            db.session.query(NetworkDevice.device_id)
            .filter(NetworkDevice.network_id != network_id)
            .distinct()
        )

        devices_to_delete = (
            db.session.query(NetworkDevice.device_id)
            .filter(NetworkDevice.network_id == network_id)
            .filter(~NetworkDevice.device_id.in_(subquery))
        )

        db.session.query(NetworkDevice).filter(NetworkDevice.device_id.in_(devices_to_delete)).delete(
            synchronize_session=False)

        db.session.query(Device).filter(Device.id.in_(devices_to_delete)).delete(synchronize_session=False)

        db.session.query(UserNetwork).filter(UserNetwork.network_id == network_id).delete(synchronize_session=False)
        db.session.query(NetworkDevice).filter(NetworkDevice.network_id == network_id).delete(
            synchronize_session=False)

        db.session.query(Network).filter(Network.id == network_id).delete(synchronize_session=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "devices": [device.device.to_dict() for device in self.devices],
            "users": [{**user.user.to_dict(), "rights": user.rights} for user in self.users]
        }


class UserNetwork(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False)
    network_id = db.Column(db.Integer, db.ForeignKey("network.id"), primary_key=True, nullable=False)

    user = db.relationship("User", back_populates="networks")
    network = db.relationship("Network", back_populates="users")
    rights = db.Column(db.String(1), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "network_id", name="_user_network_uc"),)


class NetworkDevice(db.Model):
    network_id = db.Column(db.Integer, db.ForeignKey("network.id"), primary_key=True, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), primary_key=True, nullable=False)

    network = db.relationship("Network", back_populates="devices")
    device = db.relationship("Device", back_populates="networks")

    __table_args__ = (db.UniqueConstraint("network_id", "device_id", name="_network_device_uc"),)
