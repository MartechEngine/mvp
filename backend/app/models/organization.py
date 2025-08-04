from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseMixin


class Organization(Base, BaseMixin):
    __tablename__ = 'organizations'

    name = Column(String, nullable=False)
    owner_id = Column(BaseMixin.id.type, ForeignKey('users.id'), nullable=False)

    owner = relationship('User')
    members = relationship('Membership', back_populates='organization', cascade='all, delete-orphan')
