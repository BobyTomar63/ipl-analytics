from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from app.database import Base

class Team(Base):
    __tablename__ = "teams"
    team_id     = Column(Integer, primary_key=True, index=True)
    team_name   = Column(String(100), unique=True, nullable=False)
    short_name  = Column(String(10))
    home_ground = Column(String(100))

class Player(Base):
    __tablename__ = "players"
    player_id   = Column(Integer, primary_key=True, index=True)
    player_name = Column(String(100), nullable=False)
    team_id     = Column(Integer, ForeignKey("teams.team_id"))
    role        = Column(String(50))
    nationality = Column(String(50))

class Match(Base):
    __tablename__ = "matches"
    match_id        = Column(Integer, primary_key=True, index=True)
    season          = Column(Integer, nullable=False)
    match_date      = Column(Date)
    venue           = Column(String(100))
    team1_id        = Column(Integer, ForeignKey("teams.team_id"))
    team2_id        = Column(Integer, ForeignKey("teams.team_id"))
    winner_id       = Column(Integer, ForeignKey("teams.team_id"))
    result          = Column(String(100))
    player_of_match = Column(String(100))

class Delivery(Base):
    __tablename__ = "deliveries"
    delivery_id = Column(Integer, primary_key=True, index=True)
    match_id    = Column(Integer, ForeignKey("matches.match_id"))
    inning      = Column(Integer)
    over_num    = Column(Integer)
    ball_num    = Column(Integer)
    batsman     = Column(String(100))
    bowler      = Column(String(100))
    runs_scored = Column(Integer, default=0)
    extras      = Column(Integer, default=0)
    is_wicket   = Column(Boolean, default=False)
    wicket_type = Column(String(50))