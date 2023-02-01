# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func

from db.database import Base
from constants import common


class State(Base):
    __tablename__ = common.DB_TABLES.state

    id = Column(Integer, primary_key=True, nullable=False, unique=False)
    uid = Column(Integer, nullable=False, unique=False)
    username = Column(String(92), nullable=False, unique=False)

    r_bfr = Column(Integer, nullable=False, unique=False, default=0)
    r_afr = Column(Integer, nullable=False, unique=False, default=0)

    tmst_created = Column(DateTime(timezone=True), server_default=func.now())
    tmst_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<State(id="{self.id}", ' \
               f'uid="{self.username}", ' \
               f'username="{self.username}", ' \
               f'r_bfr="{self.r_bfr}", ' \
               f'r_afr="{self.r_afr}",' \
               f'tmst_created="{self.tmst_created}",' \
               f'tmst_updated="{self.tmst_updated}")>'
