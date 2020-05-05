from lyra_orm.config import Base
from lyra_orm.config import session
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship, backref


class ApiUser(Base):
    __tablename__ = "api_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(Text)
    roles = Column(Text)
    is_active = Column(Boolean, default=True, server_default="true")

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return session.query(cls).filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return session.query(cls).get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active
