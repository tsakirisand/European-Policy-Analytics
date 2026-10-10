"""
Unit tests for Database Storage and Ingestion Pipeline.
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base, CountryModel, IndicatorModel, ObservationModel
from src.pipeline.ingestion import seed_metadata, save_observations
from src.metadata.countries import COUNTRIES
from src.metadata.indicators import INDICATORS

TEST_DB_URI = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_seed_metadata(db_session):
    seed_metadata(db_session)
    c_count = db_session.query(CountryModel).count()
    i_count = db_session.query(IndicatorModel).count()
    assert c_count == len(COUNTRIES)
    assert i_count == len(INDICATORS)

def test_save_observations(db_session):
    seed_metadata(db_session)
    records = [
        {
            "country_code": "GRC",
            "indicator_id": "GDP_REAL_GROWTH",
            "period": 2023,
            "value": 2.1,
            "unit": "Percentage change",
            "dataset_code": "nama_10_gdp",
            "is_valid": True,
            "validation_note": "Valid observation"
        }
    ]
    saved = save_observations(db_session, records)
    assert saved == 1

    obs = db_session.query(ObservationModel).first()
    assert obs.country_code == "GRC"
    assert obs.value == 2.1
