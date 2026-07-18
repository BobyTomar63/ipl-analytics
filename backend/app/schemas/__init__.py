from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import date

# ─── MATCH SCHEMAS ──────────────────────
class MatchBase(BaseModel):
    match_id:        int
    season:          int = Field(..., ge=2007, le=2026)
    city:            str
    match_date:      Optional[date]
    team1:           str
    team2:           str
    winner:          str
    player_of_match: Optional[str]
    venue:           Optional[str]
    result:          Optional[str]

    @validator('season')
    def season_valid(cls, v):
        if v < 2007 or v > 2026:
            raise ValueError('Season 2007 aur 2026 ke beech hona chahiye')
        return v

    @validator('team1', 'team2')
    def teams_not_empty(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Team name empty nahi ho sakta')
        return v

    class Config:
        from_attributes = True

# ─── DELIVERY SCHEMAS ───────────────────
class DeliveryBase(BaseModel):
    match_id:    int
    inning:      int = Field(..., ge=1, le=2)
    over_num:    int = Field(..., ge=1, le=20)
    ball_num:    int = Field(..., ge=1, le=10)
    batsman:     str
    bowler:      str
    runs_scored: int = Field(..., ge=0, le=36)
    extras:      int = Field(..., ge=0)
    is_wicket:   bool

    @validator('inning')
    def inning_valid(cls, v):
        if v not in [1, 2]:
            raise ValueError('Inning 1 ya 2 honi chahiye')
        return v

    @validator('runs_scored')
    def runs_valid(cls, v):
        if v < 0 or v > 36:
            raise ValueError('Runs 0 aur 36 ke beech hone chahiye')
        return v

    class Config:
        from_attributes = True

# ─── RESPONSE SCHEMAS ───────────────────
class MatchResponse(MatchBase):
    pass

class DeliveryResponse(DeliveryBase):
    delivery_id: int