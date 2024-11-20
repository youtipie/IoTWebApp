import re

from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from sqlalchemy.orm import validates

from validate_email_address import validate_email


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    networks = db.relationship("UserNetwork", back_populates="user")

    # TODO: Add email verification when user register

    @validates("email")
    def validate_email(self, key, email):
        if not validate_email(email):
            raise ValueError("Invalid email")
        return email

    @validates("password")
    def validate_password(self, key, password):
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None

        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error)
        if not password_ok:
            raise ValueError("Password have to be minimal 8 characters lengths, "
                             "contain at least one lowercase and uppercase symbol")
        return generate_password_hash(password)

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Maybe optimize? Maybe not. Anyway this method shouldn't be used often
    def delete_user(self):
        from ..networks.models import UserNetwork, Network
        user_id = self.id

        user_networks = Network.query_networks_with_rights().filter(UserNetwork.user_id == user_id).all()

        for network, _ in user_networks:
            network.delete_network()

        db.session.query(User).filter(User.id == user_id).delete(synchronize_session=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
