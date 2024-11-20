import ipaddress

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from .. import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    port = db.Column(db.Integer, nullable=False)

    networks = db.relationship("NetworkDevice", back_populates="device")

    __table_args__ = (UniqueConstraint("ip", "port", name="_ip_port_uc"),)

    @validates("ip")
    def validate_ip(self, key, ip):
        try:
            _ = ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError("Ip address is invalid") from None
        else:
            return ip

    @validates("port")
    def validate_port(self, key, port):
        if not (0 <= port <= 65535):
            raise ValueError("Port must be in range from 0 to 65535")
        return port

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # Maybe not safe. Consider delete later
            "ip": self.ip,
            "port": self.port
        }
