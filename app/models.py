from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, Boolean, Enum, UniqueConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base
import enum

# ===== Enums =====
class PageStatus(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"

class StageType(enum.Enum):
    GROUP = "GROUP"
    KO = "KO"

class MatchStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"
    LIVE = "LIVE"
    FT = "FT"
    POSTPONED = "POSTPONED"
    CANCELED = "CANCELED"

class PartnerKind(enum.Enum):
    HOTEL = "HOTEL"
    FLIGHT = "FLIGHT"
    TOUR = "TOUR"
    TICKET = "TICKET"
    STREAMING = "STREAMING"

class TopicType(enum.Enum):
    TEAM = "TEAM"
    CITY = "CITY"
    COMPETITION = "COMPETITION"

# ===== Core locations =====
class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    countryCode: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    tz: Mapped[str | None] = mapped_column(String)
    airportCodes: Mapped[str | None] = mapped_column(String)
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)

    venues: Mapped[list["Venue"]] = relationship(back_populates="city", cascade="all,delete-orphan")

class Venue(Base):
    __tablename__ = "venues"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    capacity: Mapped[int | None] = mapped_column(Integer)
    tz: Mapped[str | None] = mapped_column(String)
    lat: Mapped[float | None] = mapped_column(Float)
    lng: Mapped[float | None] = mapped_column(Float)

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="RESTRICT"), nullable=False, index=True)
    city: Mapped[City] = relationship(back_populates="venues")

    matches: Mapped[list["Match"]] = relationship(back_populates="venue")

# ===== Competitions & matches =====
class Competition(Base):
    __tablename__ = "competitions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    kind: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str | None] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    seasons: Mapped[list["Season"]] = relationship(back_populates="competition", cascade="all,delete-orphan")

class Season(Base):
    __tablename__ = "seasons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    yearStart: Mapped[int] = mapped_column(Integer, nullable=False)
    yearEnd: Mapped[int] = mapped_column(Integer, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id", ondelete="RESTRICT"), nullable=False, index=True)
    competition: Mapped[Competition] = relationship(back_populates="seasons")

    stages: Mapped[list["Stage"]] = relationship(back_populates="season", cascade="all,delete-orphan")
    matches: Mapped[list["Match"]] = relationship(back_populates="season")

class Stage(Base):
    __tablename__ = "stages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[StageType] = mapped_column(Enum(StageType), nullable=False)
    sortOrder: Mapped[int | None] = mapped_column(Integer)

    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="RESTRICT"), nullable=False, index=True)
    season: Mapped[Season] = relationship(back_populates="stages")

    matches: Mapped[list["Match"]] = relationship(back_populates="stage")

class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    countryCode: Mapped[str | None] = mapped_column(String)
    fifaCode: Mapped[str | None] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    home_matches: Mapped[list["Match"]] = relationship(back_populates="homeTeam", foreign_keys="Match.home_team_id")
    away_matches: Mapped[list["Match"]] = relationship(back_populates="awayTeam", foreign_keys="Match.away_team_id")

class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    round: Mapped[str | None] = mapped_column(String)
    kickoff: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus), nullable=False)
    scoreHome: Mapped[int | None] = mapped_column(Integer)
    scoreAway: Mapped[int | None] = mapped_column(Integer)
    pensHome: Mapped[int | None] = mapped_column(Integer)
    pensAway: Mapped[int | None] = mapped_column(Integer)

    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="RESTRICT"), nullable=False, index=True)
    stage_id: Mapped[int | None] = mapped_column(ForeignKey("stages.id", ondelete="SET NULL"), index=True)
    venue_id: Mapped[int | None] = mapped_column(ForeignKey("venues.id", ondelete="SET NULL"), index=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False, index=True)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False, index=True)

    season: Mapped[Season] = relationship(back_populates="matches")
    stage: Mapped[Stage] = relationship(back_populates="matches")
    venue: Mapped[Venue] = relationship(back_populates="matches")
    homeTeam: Mapped[Team] = relationship(back_populates="home_matches", foreign_keys=[home_team_id])
    awayTeam: Mapped[Team] = relationship(back_populates="away_matches", foreign_keys=[away_team_id])

# ===== CMS-like dynamic pages =====
class Page(Base):
    __tablename__ = "pages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[PageStatus] = mapped_column(Enum(PageStatus), nullable=False)
    meta: Mapped[str | None] = mapped_column(Text)
    publishedAt: Mapped[datetime | None] = mapped_column()

    blocks: Mapped[list["PageBlock"]] = relationship(back_populates="page", cascade="all,delete-orphan")

class PageBlock(Base):
    __tablename__ = "page_blocks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[str | None] = mapped_column(Text)
    sortOrder: Mapped[int | None] = mapped_column(Integer)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, index=True)
    page: Mapped[Page] = relationship(back_populates="blocks")

# ===== Affiliates & tracking =====
class AffiliatePartner(Base):
    __tablename__ = "affiliate_partners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    kind: Mapped[PartnerKind] = mapped_column(Enum(PartnerKind), nullable=False)
    program: Mapped[str | None] = mapped_column(String)
    baseUrl: Mapped[str | None] = mapped_column(String)
    geoRules: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    offers: Mapped[list["AffiliateOffer"]] = relationship(back_populates="partner", cascade="all,delete-orphan")

class AffiliateOffer(Base):
    __tablename__ = "affiliate_offers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    deeplinkPattern: Mapped[str] = mapped_column(String, nullable=False)
    params: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    partner_id: Mapped[int] = mapped_column(ForeignKey("affiliate_partners.id", ondelete="RESTRICT"), nullable=False, index=True)
    partner: Mapped[AffiliatePartner] = relationship(back_populates="offers")

    clicks: Mapped[list["OutboundClick"]] = relationship(back_populates="offer", cascade="all,delete-orphan")

class OutboundClick(Base):
    __tablename__ = "outbound_clicks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    targetUrl: Mapped[str] = mapped_column(String, nullable=False)
    utm: Mapped[str | None] = mapped_column(Text)
    ip: Mapped[str | None] = mapped_column(String)
    country: Mapped[str | None] = mapped_column(String)
    userAgent: Mapped[str | None] = mapped_column(String)
    createdAt: Mapped[datetime] = mapped_column(nullable=False)

    offer_id: Mapped[int] = mapped_column(ForeignKey("affiliate_offers.id", ondelete="CASCADE"), nullable=False, index=True)
    offer: Mapped[AffiliateOffer] = relationship(back_populates="clicks")

# ===== Email subscribers & alerts =====
class EmailSubscriber(Base):
    __tablename__ = "email_subscribers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    locale: Mapped[str | None] = mapped_column(String)
    doubleOptIn: Mapped[bool | None] = mapped_column(Boolean)
    status: Mapped[str | None] = mapped_column(String)
    createdAt: Mapped[datetime] = mapped_column(nullable=False)
    unsubscribedAt: Mapped[datetime | None] = mapped_column()

    subscriptions: Mapped[list["AlertSubscription"]] = relationship(back_populates="subscriber", cascade="all,delete-orphan")

class AlertSubscription(Base):
    __tablename__ = "alert_subscriptions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topicType: Mapped[TopicType] = mapped_column(Enum(TopicType), nullable=False)
    topicRef: Mapped[str] = mapped_column(String, nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(nullable=False)

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("email_subscribers.id", ondelete="CASCADE"), nullable=False, index=True)
    subscriber: Mapped[EmailSubscriber] = relationship(back_populates="subscriptions")
