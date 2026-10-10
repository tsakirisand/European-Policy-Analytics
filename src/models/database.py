"""
SQLAlchemy database models and connection engine.
"""

from datetime import datetime
from typing import Generator
from sqlalchemy import (
    create_engine, Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
import config

Base = declarative_base()

class CountryModel(Base):
    __tablename__ = "countries"

    code_iso3 = Column(String(3), primary_key=True)
    code_iso2 = Column(String(2), nullable=False)
    code_eurostat = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    flag = Column(String(10), nullable=False)
    region = Column(String(50), nullable=False)
    is_eu = Column(Boolean, default=True)
    is_aggregate = Column(Boolean, default=False)
    currency = Column(String(10), nullable=False)

    observations = relationship("ObservationModel", back_populates="country", cascade="all, delete-orphan")

class IndicatorModel(Base):
    __tablename__ = "indicators"

    id = Column(String(50), primary_key=True)
    domain_id = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    short_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    unit = Column(String(100), nullable=False)
    unit_symbol = Column(String(30), nullable=False)
    frequency = Column(String(20), nullable=False)
    source_provider = Column(String(100), nullable=False)
    source_dataset_code = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=False)
    change_type = Column(String(20), default="pct")
    better_direction = Column(String(20), default="high")

    observations = relationship("ObservationModel", back_populates="indicator", cascade="all, delete-orphan")

from datetime import datetime, timezone

class ObservationModel(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String(3), ForeignKey("countries.code_iso3"), nullable=False)
    indicator_id = Column(String(50), ForeignKey("indicators.id"), nullable=False)
    period = Column(Integer, nullable=False)  # Year, e.g. 2023
    value = Column(Float, nullable=False)
    unit = Column(String(100), nullable=False)
    frequency = Column(String(20), default="Annual")
    dataset_code = Column(String(100), nullable=False)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_valid = Column(Boolean, default=True)
    validation_note = Column(Text, nullable=True)

    country = relationship("CountryModel", back_populates="observations")
    indicator = relationship("IndicatorModel", back_populates="observations")

    __table_args__ = (
        UniqueConstraint("country_code", "indicator_id", "period", name="uix_country_indicator_period"),
        Index("idx_obs_lookup", "country_code", "indicator_id", "period"),
        Index("idx_obs_ind_period", "indicator_id", "period"),
    )

class IngestionLogModel(Base):
    __tablename__ = "ingestion_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String(50), nullable=False)
    dataset_code = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), nullable=False)  # SUCCESS, WARNING, FAILED
    records_ingested = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

class ValidationLogModel(Base):
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    indicator_id = Column(String(50), nullable=False)
    country_code = Column(String(3), nullable=False)
    period = Column(Integer, nullable=False)
    rule_failed = Column(String(100), nullable=False)
    details = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Engine & Session setup
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} if "sqlite" in config.SQLALCHEMY_DATABASE_URI else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db_session() -> Generator[Session, None, None]:
    """Dependency helper for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
