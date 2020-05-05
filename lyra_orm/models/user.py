from lyra_orm.config import session
from lyra_orm.config import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Boolean,
)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(Text)
    is_admin = Column(Boolean, default=False, server_default="false")
    is_active = Column(Boolean, default=True, server_default="true")

    def is_user_admin(self):
        return True if self.is_admin == True else False
