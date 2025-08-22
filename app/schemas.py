from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import PageStatus, StageType, MatchStatus, PartnerKind, TopicType

class ORMB(BaseModel):
    model_config = dict(from_attributes=True)

# ---- Core
class CityBase(ORMB):
    name: str
    countryCode: str
    slug: str
    tz: Optional[str] = None
    airportCodes: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class CityCreate(CityBase): pass
class CityUpdate(ORMB):
    name: Optional[str] = None
    countryCode: Optional[str] = None
    slug: Optional[str] = None
    tz: Optional[str] = None
    airportCodes: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
class City(CityBase):
    id: int

class VenueBase(ORMB):
    name: str
    slug: str
    capacity: Optional[int] = None
    tz: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    city_id: int

class VenueCreate(VenueBase): pass
class VenueUpdate(ORMB):
    name: Optional[str] = None
    slug: Optional[str] = None
    capacity: Optional[int] = None
    tz: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    city_id: Optional[int] = None
class Venue(VenueBase):
    id: int

# ---- Competitions & Matches
class CompetitionBase(ORMB):
    name: str
    code: str
    kind: str
    region: Optional[str] = None
    slug: str
class CompetitionCreate(CompetitionBase): pass
class CompetitionUpdate(ORMB):
    name: Optional[str] = None
    code: Optional[str] = None
    kind: Optional[str] = None
    region: Optional[str] = None
    slug: Optional[str] = None
class Competition(CompetitionBase):
    id: int

class SeasonBase(ORMB):
    yearStart: int
    yearEnd: int
    slug: str
    competition_id: int
class SeasonCreate(SeasonBase): pass
class SeasonUpdate(ORMB):
    yearStart: Optional[int] = None
    yearEnd: Optional[int] = None
    slug: Optional[str] = None
    competition_id: Optional[int] = None
class Season(SeasonBase):
    id: int

class StageBase(ORMB):
    name: str
    type: StageType
    sortOrder: Optional[int] = None
    season_id: int
class StageCreate(StageBase): pass
class StageUpdate(ORMB):
    name: Optional[str] = None
    type: Optional[StageType] = None
    sortOrder: Optional[int] = None
    season_id: Optional[int] = None
class Stage(StageBase):
    id: int

class TeamBase(ORMB):
    name: str
    countryCode: Optional[str] = None
    fifaCode: Optional[str] = None
    slug: str
class TeamCreate(TeamBase): pass
class TeamUpdate(ORMB):
    name: Optional[str] = None
    countryCode: Optional[str] = None
    fifaCode: Optional[str] = None
    slug: Optional[str] = None
class Team(TeamBase):
    id: int

class MatchBase(ORMB):
    round: Optional[str] = None
    kickoff: datetime
    status: MatchStatus
    scoreHome: Optional[int] = None
    scoreAway: Optional[int] = None
    pensHome: Optional[int] = None
    pensAway: Optional[int] = None
    season_id: int
    stage_id: Optional[int] = None
    venue_id: Optional[int] = None
    home_team_id: int
    away_team_id: int
class MatchCreate(MatchBase): pass
class MatchUpdate(ORMB):
    round: Optional[str] = None
    kickoff: Optional[datetime] = None
    status: Optional[MatchStatus] = None
    scoreHome: Optional[int] = None
    scoreAway: Optional[int] = None
    pensHome: Optional[int] = None
    pensAway: Optional[int] = None
    season_id: Optional[int] = None
    stage_id: Optional[int] = None
    venue_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
class Match(MatchBase):
    id: int

# ---- CMS
class PageBase(ORMB):
    slug: str
    title: str
    status: PageStatus
    meta: Optional[str] = None
    publishedAt: Optional[datetime] = None
class PageCreate(PageBase): pass
class PageUpdate(ORMB):
    slug: Optional[str] = None
    title: Optional[str] = None
    status: Optional[PageStatus] = None
    meta: Optional[str] = None
    publishedAt: Optional[datetime] = None
class Page(PageBase):
    id: int

class PageBlockBase(ORMB):
    type: str
    data: Optional[str] = None
    sortOrder: Optional[int] = None
    page_id: int
class PageBlockCreate(PageBlockBase): pass
class PageBlockUpdate(ORMB):
    type: Optional[str] = None
    data: Optional[str] = None
    sortOrder: Optional[int] = None
    page_id: Optional[int] = None
class PageBlock(PageBlockBase):
    id: int

# ---- Affiliates
class AffiliatePartnerBase(ORMB):
    name: str
    kind: PartnerKind
    program: Optional[str] = None
    baseUrl: Optional[str] = None
    geoRules: Optional[str] = None
    active: bool
class AffiliatePartnerCreate(AffiliatePartnerBase): pass
class AffiliatePartnerUpdate(ORMB):
    name: Optional[str] = None
    kind: Optional[PartnerKind] = None
    program: Optional[str] = None
    baseUrl: Optional[str] = None
    geoRules: Optional[str] = None
    active: Optional[bool] = None
class AffiliatePartner(AffiliatePartnerBase):
    id: int

class AffiliateOfferBase(ORMB):
    name: str
    deeplinkPattern: str
    params: Optional[str] = None
    active: bool
    partner_id: int
class AffiliateOfferCreate(AffiliateOfferBase): pass
class AffiliateOfferUpdate(ORMB):
    name: Optional[str] = None
    deeplinkPattern: Optional[str] = None
    params: Optional[str] = None
    active: Optional[bool] = None
    partner_id: Optional[int] = None
class AffiliateOffer(AffiliateOfferBase):
    id: int

class OutboundClickBase(ORMB):
    targetUrl: str
    utm: Optional[str] = None
    ip: Optional[str] = None
    country: Optional[str] = None
    userAgent: Optional[str] = None
    createdAt: datetime
    offer_id: int
class OutboundClickCreate(OutboundClickBase): pass
class OutboundClickUpdate(ORMB):
    targetUrl: Optional[str] = None
    utm: Optional[str] = None
    ip: Optional[str] = None
    country: Optional[str] = None
    userAgent: Optional[str] = None
    createdAt: Optional[datetime] = None
    offer_id: Optional[int] = None
class OutboundClick(OutboundClickBase):
    id: int

# ---- Email + Alerts
class EmailSubscriberBase(ORMB):
    email: EmailStr
    locale: Optional[str] = None
    doubleOptIn: Optional[bool] = None
    status: Optional[str] = None
    createdAt: datetime
    unsubscribedAt: Optional[datetime] = None
class EmailSubscriberCreate(EmailSubscriberBase): pass
class EmailSubscriberUpdate(ORMB):
    email: Optional[EmailStr] = None
    locale: Optional[str] = None
    doubleOptIn: Optional[bool] = None
    status: Optional[str] = None
    createdAt: Optional[datetime] = None
    unsubscribedAt: Optional[datetime] = None
class EmailSubscriber(EmailSubscriberBase):
    id: int

class AlertSubscriptionBase(ORMB):
    topicType: TopicType
    topicRef: str
    channel: str
    createdAt: datetime
    subscriber_id: int
class AlertSubscriptionCreate(AlertSubscriptionBase): pass
class AlertSubscriptionUpdate(ORMB):
    topicType: Optional[TopicType] = None
    topicRef: Optional[str] = None
    channel: Optional[str] = None
    createdAt: Optional[datetime] = None
    subscriber_id: Optional[int] = None
class AlertSubscription(AlertSubscriptionBase):
    id: int
