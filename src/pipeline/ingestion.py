"""
Data Ingestion Pipeline Orchestrator.
Coordinates dataset retrieval from official API connectors with verified dataset dimension parameters.
"""

import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from src.models.database import (
    init_db, SessionLocal, CountryModel, IndicatorModel, ObservationModel, IngestionLogModel, ValidationLogModel
)
from src.metadata.countries import COUNTRIES
from src.metadata.indicators import INDICATORS
from src.connectors.eurostat import EurostatConnector
from src.connectors.worldbank import WorldBankConnector
from src.connectors.ecb import ECBConnector
from src.connectors.oecd import OECDConnector
from src.pipeline.normalizer import DataNormalizer
from src.pipeline.validator import DataValidator

logger = logging.getLogger(__name__)

def seed_metadata(db: Session):
    """Seed countries and indicators tables from metadata definitions."""
    for code_iso3, meta in COUNTRIES.items():
        existing = db.query(CountryModel).filter(CountryModel.code_iso3 == code_iso3).first()
        if not existing:
            c = CountryModel(
                code_iso3=code_iso3,
                code_iso2=meta["code_iso2"],
                code_eurostat=meta["code_eurostat"],
                name=meta["name"],
                flag=meta["flag"],
                region=meta["region"],
                is_eu=meta["is_eu"],
                is_aggregate=meta["is_aggregate"],
                currency=meta["currency"]
            )
            db.add(c)
    db.commit()

    # Purge any deprecated indicators
    db.query(IndicatorModel).filter(IndicatorModel.id == "AVG_ANNUAL_WAGE").delete(synchronize_session=False)
    db.commit()

    for ind_id, meta in INDICATORS.items():
        existing = db.query(IndicatorModel).filter(IndicatorModel.id == ind_id).first()
        if not existing:
            i = IndicatorModel(
                id=ind_id,
                domain_id=meta["domain_id"],
                name=meta["name"],
                short_name=meta["short_name"],
                description=meta["description"],
                unit=meta["unit"],
                unit_symbol=meta["unit_symbol"],
                frequency=meta["frequency"],
                source_provider=meta["source_provider"],
                source_dataset_code=meta["source_dataset_code"],
                source_url=meta["source_url"],
                change_type=meta["change_type"],
                better_direction=meta["better_direction"]
            )
            db.add(i)
        else:
            existing.domain_id = meta["domain_id"]
            existing.name = meta["name"]
            existing.short_name = meta["short_name"]
            existing.description = meta["description"]
            existing.unit = meta["unit"]
            existing.unit_symbol = meta["unit_symbol"]
            existing.frequency = meta["frequency"]
            existing.source_provider = meta["source_provider"]
            existing.source_dataset_code = meta["source_dataset_code"]
            existing.source_url = meta["source_url"]
            existing.change_type = meta["change_type"]
            existing.better_direction = meta["better_direction"]
    db.commit()

def save_observations(db: Session, records: List[Dict[str, Any]]) -> int:
    """Saves or updates validated observation records in database."""
    if not records:
        return 0

    count = 0
    for r in records:
        if not r.get("is_valid", True):
            v_log = ValidationLogModel(
                indicator_id=r["indicator_id"],
                country_code=r["country_code"],
                period=r["period"],
                rule_failed="SanityCheck",
                details=r.get("validation_note", "Invalid record")
            )
            db.add(v_log)
            continue

        existing = db.query(ObservationModel).filter(
            ObservationModel.country_code == r["country_code"],
            ObservationModel.indicator_id == r["indicator_id"],
            ObservationModel.period == r["period"]
        ).first()

        if existing:
            existing.value = r["value"]
            existing.unit = r["unit"]
            existing.dataset_code = r["dataset_code"]
            existing.fetched_at = datetime.now(timezone.utc)
            existing.is_valid = True
            existing.validation_note = r.get("validation_note", "Valid")
        else:
            obs = ObservationModel(
                country_code=r["country_code"],
                indicator_id=r["indicator_id"],
                period=r["period"],
                value=r["value"],
                unit=r["unit"],
                frequency=r.get("frequency", "Annual"),
                dataset_code=r["dataset_code"],
                fetched_at=datetime.now(timezone.utc),
                is_valid=True,
                validation_note=r.get("validation_note", "Valid")
            )
            db.add(obs)
        count += 1

    db.commit()
    return count

def run_ingestion_pipeline(indicator_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """Executes live data retrieval pipeline for specified indicators."""
    init_db()
    db = SessionLocal()
    try:
        seed_metadata(db)
        
        target_indicators = indicator_ids if indicator_ids else list(INDICATORS.keys())
        results = {"total_ingested": 0, "indicators_processed": len(target_indicators), "status": "SUCCESS", "details": []}

        wb_connector = WorldBankConnector()
        eurostat_connector = EurostatConnector()
        ecb_connector = ECBConnector()

        for ind_id in target_indicators:
            meta = INDICATORS.get(ind_id)
            if not meta:
                continue

            raw_records = []
            provider = meta["source_provider"]

            try:
                # 1. World Bank API Connectors
                european_iso3_codes = list(COUNTRIES.keys())
                if ind_id == "LIFE_EXPECTANCY":
                    raw_records = wb_connector.fetch_indicator("SP.DYN.LE00.IN", 2000, 2025, country_codes=european_iso3_codes)
                elif ind_id == "TRADE_BALANCE_GDP":
                    raw_records = wb_connector.fetch_indicator("NE.RSB.GNFS.ZS", 2000, 2025, country_codes=european_iso3_codes)
                elif ind_id == "GDP_PER_CAPITA":
                    raw_records = wb_connector.fetch_indicator("NY.GDP.PCAP.CD", 2000, 2025, country_codes=european_iso3_codes)

                # 2. Eurostat API Connectors with explicit dimension filters
                elif ind_id == "AVG_FULL_TIME_ADJUSTED_SALARY":
                    raw_records = eurostat_connector.fetch_dataset("nama_10_fte", {"unit": "EUR"})
                elif ind_id == "MINIMUM_MONTHLY_WAGE":
                    raw_records = eurostat_connector.fetch_dataset("earn_mw_cur", {"currency": "EUR"})
                elif ind_id == "AVG_NET_ANNUAL_SALARY":
                    raw_records = eurostat_connector.fetch_dataset("earn_nt_net", {"currency": "EUR"})
                elif ind_id == "GDP_REAL_GROWTH":
                    raw_records = eurostat_connector.fetch_dataset("nama_10_gdp", {"unit": "CLV_PCH_PRE", "na_item": "B1GQ"})
                elif ind_id == "UNEMP_RATE":
                    raw_records = eurostat_connector.fetch_dataset("une_rt_a", {"unit": "PC_ACT", "age": "Y15-74", "sex": "T"})
                elif ind_id == "HICP_INFLATION":
                    raw_records = eurostat_connector.fetch_dataset("prc_hicp_aind", {"unit": "RCH_A_AVG", "coicop": "CP00"})
                elif ind_id == "POPULATION":
                    raw_records = eurostat_connector.fetch_dataset("demo_gind", {"indic_de": "JAN"})
                elif ind_id == "GDP_PC_PPP":
                    raw_records = eurostat_connector.fetch_dataset("nama_10_pc", {"unit": "CP_PPS_EU27_2020_HAB", "na_item": "B1GQ"})
                elif ind_id == "YOUTH_UNEMP_RATE":
                    raw_records = eurostat_connector.fetch_dataset("une_rt_a", {"unit": "PC_ACT", "age": "Y15-24", "sex": "T"})
                elif ind_id == "GOV_DEBT_GDP":
                    raw_records = eurostat_connector.fetch_dataset("gov_10dd_edpt1", {"unit": "PC_GDP", "sector": "S13", "na_item": "GD"})
                elif ind_id == "GOV_DEFICIT_GDP":
                    raw_records = eurostat_connector.fetch_dataset("gov_10dd_edpt1", {"unit": "PC_GDP", "sector": "S13", "na_item": "B9"})
                elif ind_id == "RENEWABLE_ENERGY_SHARE":
                    raw_records = eurostat_connector.fetch_dataset("nrg_ind_ren", {"unit": "PC", "nrg_bal": "REN"})
                elif ind_id == "GHG_EMISSIONS":
                    raw_records = eurostat_connector.fetch_dataset("env_air_gge", {"unit": "THS_T", "airpol": "GHG", "src_crf": "TOTXMEMO"})
                elif ind_id == "POVERTY_RISK_RATE":
                    raw_records = eurostat_connector.fetch_dataset("ilc_peps01n", {"unit": "PC", "age": "TOTAL", "sex": "T"})

                # 3. ECB API Connectors
                elif ind_id == "ECB_POLICY_RATE":
                    raw_records = ecb_connector.fetch_policy_rate()
                elif ind_id == "HOUSEHOLD_LENDING_RATE":
                    raw_records = ecb_connector.fetch_household_lending_rate("DE")

                # Save non-empty observations
                if raw_records:
                    norm_records = DataNormalizer.normalize_and_deduplicate(raw_records, ind_id)
                    validated_records = DataValidator.filter_and_mark_validations(norm_records)
                    saved_count = save_observations(db, validated_records)
                else:
                    logger.warning(f"API returned 0 records for {ind_id}. Preserving database data.")
                    saved_count = 0

                log = IngestionLogModel(
                    provider=provider,
                    dataset_code=meta["source_dataset_code"],
                    status="SUCCESS" if saved_count > 0 else "WARNING",
                    records_ingested=saved_count,
                    error_message=None if saved_count > 0 else "No API records retrieved"
                )
                db.add(log)
                db.commit()

                results["total_ingested"] += saved_count
                results["details"].append({"indicator": ind_id, "count": saved_count, "status": "SUCCESS"})

            except Exception as e:
                logger.error(f"Error ingesting indicator {ind_id}: {e}")
                log = IngestionLogModel(
                    provider=provider,
                    dataset_code=meta["source_dataset_code"],
                    status="FAILED",
                    records_ingested=0,
                    error_message=str(e)
                )
                db.add(log)
                db.commit()
                results["details"].append({"indicator": ind_id, "count": 0, "status": "FAILED", "error": str(e)})

        return results
    finally:
        db.close()
