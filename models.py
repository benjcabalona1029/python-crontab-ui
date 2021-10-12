from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(String, index=True)
    name = Column(String, unique=True)
    schedule = Column(String)
    next_run = Column(String, default=None)
    status = Column(String, default=None)
    is_active = Column(Boolean, default=False)
