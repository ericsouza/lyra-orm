from lyra_orm.config import Base
from sqlalchemy import Column, Integer, Boolean


class ValidateUras(Base):
    __tablename__ = "validate_uras"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=False, server_default="false")

    def __str__(self):
        return self.label
