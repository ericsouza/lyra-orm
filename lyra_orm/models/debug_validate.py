from lyra_orm.config import Base, session
from sqlalchemy import Column, Integer, Boolean


class ValidateUras(Base):
    __tablename__ = "validate_uras"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=False, server_default="false")

    def __str__(self):
        return self.label

    @classmethod
    def get_is_active(cls):
        return session.query(cls).first().is_active

    def save_to_db(self):
        session.add(self)
        session.commit()
        session.close()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
        session.close()
