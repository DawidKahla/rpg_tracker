from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.db_setup import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    system = Column(String, nullable=False)
    start_date = Column(Date)
    notes = Column(String, nullable=True)

    sessions = relationship("Session", back_populates="campaign")
    heroes = relationship("Hero", back_populates="campaign")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    session_date = Column(Date)
    title = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    campaign = relationship("Campaign", back_populates="sessions")


class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    notes = Column(String, nullable=True)

    campaign = relationship("Campaign", back_populates="heroes")
