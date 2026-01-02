"""Load Silver data to Gold layer."""
import argparse
import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.shared import get_db, logger
from app.models.gold import GoldBase


def create_gold_schema(session):
    """Create gold schema if it doesn't exist."""
    session.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))
    session.commit()
    logger.info("Gold schema created/verified")


def create_gold_tables(engine):
    """Create gold layer tables."""
    GoldBase.metadata.create_all(engine)
    logger.info("Gold tables created")


def generate_dim_time(session, start_year=2100, end_year=2205):
    """Generate time dimension for MIMIC shifted dates."""
    from sqlalchemy.dialects.postgresql import insert
    from app.models.gold import DimTime
    
    logger.info(f"Generating dim_time for {start_year}-{end_year}")
    
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    current = start_date
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    batch = []
    batch_count = 0
    while current <= end_date:
        batch.append({
            'time_key': current,
            'year': current.year,
            'quarter': (current.month - 1) // 3 + 1,
            'month': current.month,
            'month_name': month_names[current.month - 1],
            'week_of_year': current.isocalendar()[1],
            'day_of_month': current.day,
            'day_of_week': current.weekday(),
            'day_name': day_names[current.weekday()],
            'is_weekend': current.weekday() >= 5,
        })
        
        if len(batch) >= 1000:
            # PostgreSQL upsert
            stmt = insert(DimTime).values(batch)
            stmt = stmt.on_conflict_do_nothing(index_elements=['time_key'])
            session.execute(stmt)
            session.commit()
            batch_count += 1
            batch = []
        
        current += timedelta(days=1)
    
    if batch:
        stmt = insert(DimTime).values(batch)
        stmt = stmt.on_conflict_do_nothing(index_elements=['time_key'])
        session.execute(stmt)
        session.commit()
    
    logger.info(f"Generated {(end_date - start_date).days + 1} days")


def load_dim_patient(session):
    """Load patient dimension from silver.patients."""
    logger.info("Loading dim_patient...")
    
    session.execute(text("""
        INSERT INTO gold.dim_patient (subject_id, gender, is_deceased, total_admissions, total_icu_stays, first_admission, last_admission)
        SELECT 
            p.subject_id,
            p.gender,
            p.is_deceased,
            COALESCE(a.total_admissions, 0),
            COALESCE(i.total_icu_stays, 0),
            a.first_admission,
            a.last_admission
        FROM silver.patients p
        LEFT JOIN (
            SELECT subject_id, 
                   COUNT(*) as total_admissions,
                   MIN(admittime) as first_admission,
                   MAX(admittime) as last_admission
            FROM silver.admissions
            GROUP BY subject_id
        ) a ON p.subject_id = a.subject_id
        LEFT JOIN (
            SELECT subject_id, COUNT(*) as total_icu_stays
            FROM silver.icustays
            GROUP BY subject_id
        ) i ON p.subject_id = i.subject_id
        ON CONFLICT (subject_id) DO UPDATE SET
            gender = EXCLUDED.gender,
            is_deceased = EXCLUDED.is_deceased,
            total_admissions = EXCLUDED.total_admissions,
            total_icu_stays = EXCLUDED.total_icu_stays,
            first_admission = EXCLUDED.first_admission,
            last_admission = EXCLUDED.last_admission
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_patient")).scalar()
    logger.info(f"Loaded {count} patients to dim_patient")


def load_dim_labitem(session):
    """Load lab item dimension from bronze.d_labitems."""
    logger.info("Loading dim_labitem...")
    
    session.execute(text("""
        INSERT INTO gold.dim_labitem (itemid, label, fluid, category, loinc_code)
        SELECT itemid, label, fluid, category, loinc_code
        FROM bronze.d_labitems
        ON CONFLICT (itemid) DO UPDATE SET
            label = EXCLUDED.label,
            fluid = EXCLUDED.fluid,
            category = EXCLUDED.category,
            loinc_code = EXCLUDED.loinc_code
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_labitem")).scalar()
    logger.info(f"Loaded {count} lab items to dim_labitem")


def load_dim_item(session):
    """Load item dimension from bronze.d_items."""
    logger.info("Loading dim_item...")
    
    session.execute(text("""
        INSERT INTO gold.dim_item (itemid, label, abbreviation, dbsource, linksto, category, unitname, param_type, conceptid)
        SELECT itemid, label, abbreviation, dbsource, linksto, category, unitname, param_type, conceptid
        FROM bronze.d_items
        ON CONFLICT (itemid) DO UPDATE SET
            label = EXCLUDED.label,
            abbreviation = EXCLUDED.abbreviation,
            dbsource = EXCLUDED.dbsource,
            linksto = EXCLUDED.linksto,
            category = EXCLUDED.category,
            unitname = EXCLUDED.unitname
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_item")).scalar()
    logger.info(f"Loaded {count} items to dim_item")


def load_dim_careunit(session):
    """Load careunit dimension from icustays."""
    logger.info("Loading dim_careunit...")
    
    icu_units = ['MICU', 'SICU', 'CCU', 'CSRU', 'TSICU', 'NICU', 'NWARD']
    
    session.execute(text("""
        INSERT INTO gold.dim_careunit (careunit, unit_type, is_icu)
        SELECT DISTINCT 
            first_careunit as careunit,
            CASE 
                WHEN first_careunit IN ('MICU', 'SICU', 'CCU', 'CSRU', 'TSICU', 'NICU') THEN 'ICU'
                WHEN first_careunit = 'NWARD' THEN 'Ward'
                ELSE 'Other'
            END as unit_type,
            first_careunit IN ('MICU', 'SICU', 'CCU', 'CSRU', 'TSICU', 'NICU', 'NWARD') as is_icu
        FROM silver.icustays
        WHERE first_careunit IS NOT NULL
        ON CONFLICT (careunit) DO NOTHING
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_careunit")).scalar()
    logger.info(f"Loaded {count} care units to dim_careunit")


def load_fact_admission(session):
    """Load admission facts from silver."""
    logger.info("Loading fact_admission...")
    
    session.execute(text("""
        INSERT INTO gold.fact_admission (
            hadm_id, subject_id, admission_type, admission_location, discharge_location,
            insurance, admittime, dischtime, los_days, los_hours,
            num_icu_stays, num_lab_tests, num_prescriptions, num_procedures, num_transfers,
            hospital_expire, patient_key, admit_date_key, disch_date_key
        )
        SELECT 
            a.hadm_id,
            a.subject_id,
            a.admission_type,
            a.admission_location,
            a.discharge_location,
            a.insurance,
            a.admittime,
            a.dischtime,
            a.los_days,
            a.los_hours,
            COALESCE(i.num_icu_stays, 0),
            COALESCE(l.num_lab_tests, 0),
            COALESCE(p.num_prescriptions, 0),
            COALESCE(pr.num_procedures, 0),
            COALESCE(t.num_transfers, 0),
            a.hospital_expire_flag,
            dp.patient_key,
            DATE(a.admittime),
            DATE(a.dischtime)
        FROM silver.admissions a
        LEFT JOIN gold.dim_patient dp ON a.subject_id = dp.subject_id
        LEFT JOIN (
            SELECT hadm_id, COUNT(*) as num_icu_stays
            FROM silver.icustays GROUP BY hadm_id
        ) i ON a.hadm_id = i.hadm_id
        LEFT JOIN (
            SELECT hadm_id, COUNT(*) as num_lab_tests
            FROM silver.labevents GROUP BY hadm_id
        ) l ON a.hadm_id = l.hadm_id
        LEFT JOIN (
            SELECT hadm_id, COUNT(*) as num_prescriptions
            FROM silver.prescriptions GROUP BY hadm_id
        ) p ON a.hadm_id = p.hadm_id
        LEFT JOIN (
            SELECT hadm_id, COUNT(*) as num_procedures
            FROM silver.procedureevents GROUP BY hadm_id
        ) pr ON a.hadm_id = pr.hadm_id
        LEFT JOIN (
            SELECT hadm_id, COUNT(*) as num_transfers
            FROM silver.transfers GROUP BY hadm_id
        ) t ON a.hadm_id = t.hadm_id
        ON CONFLICT (hadm_id) DO UPDATE SET
            los_days = EXCLUDED.los_days,
            num_icu_stays = EXCLUDED.num_icu_stays,
            num_lab_tests = EXCLUDED.num_lab_tests,
            num_prescriptions = EXCLUDED.num_prescriptions,
            num_procedures = EXCLUDED.num_procedures,
            num_transfers = EXCLUDED.num_transfers
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_admission")).scalar()
    logger.info(f"Loaded {count} admissions to fact_admission")


def load_agg_patient_summary(session):
    """Load patient summary aggregate."""
    logger.info("Loading agg_patient_summary...")
    
    session.execute(text("""
        INSERT INTO gold.agg_patient_summary (
            subject_id, patient_key, gender, is_deceased,
            total_admissions, total_icu_stays, total_lab_tests, total_prescriptions,
            total_los_days, avg_los_days, first_admission, last_admission
        )
        SELECT 
            p.subject_id,
            dp.patient_key,
            p.gender,
            p.is_deceased,
            COALESCE(a.total_admissions, 0),
            COALESCE(i.total_icu_stays, 0),
            COALESCE(l.total_lab_tests, 0),
            COALESCE(pr.total_prescriptions, 0),
            COALESCE(a.total_los_days, 0),
            a.avg_los_days,
            a.first_admission,
            a.last_admission
        FROM silver.patients p
        LEFT JOIN gold.dim_patient dp ON p.subject_id = dp.subject_id
        LEFT JOIN (
            SELECT subject_id,
                   COUNT(*) as total_admissions,
                   SUM(los_days) as total_los_days,
                   AVG(los_days) as avg_los_days,
                   MIN(admittime) as first_admission,
                   MAX(admittime) as last_admission
            FROM silver.admissions GROUP BY subject_id
        ) a ON p.subject_id = a.subject_id
        LEFT JOIN (
            SELECT subject_id, COUNT(*) as total_icu_stays
            FROM silver.icustays GROUP BY subject_id
        ) i ON p.subject_id = i.subject_id
        LEFT JOIN (
            SELECT subject_id, COUNT(*) as total_lab_tests
            FROM silver.labevents GROUP BY subject_id
        ) l ON p.subject_id = l.subject_id
        LEFT JOIN (
            SELECT subject_id, COUNT(*) as total_prescriptions
            FROM silver.prescriptions GROUP BY subject_id
        ) pr ON p.subject_id = pr.subject_id
        ON CONFLICT (subject_id) DO UPDATE SET
            total_admissions = EXCLUDED.total_admissions,
            total_icu_stays = EXCLUDED.total_icu_stays,
            total_lab_tests = EXCLUDED.total_lab_tests,
            total_prescriptions = EXCLUDED.total_prescriptions,
            total_los_days = EXCLUDED.total_los_days,
            avg_los_days = EXCLUDED.avg_los_days
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.agg_patient_summary")).scalar()
    logger.info(f"Loaded {count} patient summaries")


def load_agg_icu_performance(session):
    """Load ICU performance aggregate."""
    logger.info("Loading agg_icu_performance...")
    
    session.execute(text("""
        INSERT INTO gold.agg_icu_performance (
            careunit, total_stays, total_patients,
            avg_los_days, max_los_days
        )
        SELECT 
            first_careunit as careunit,
            COUNT(*) as total_stays,
            COUNT(DISTINCT subject_id) as total_patients,
            AVG(los_icu_days) as avg_los_days,
            MAX(los_icu_days) as max_los_days
        FROM silver.icustays
        WHERE first_careunit IS NOT NULL
        GROUP BY first_careunit
        ON CONFLICT (careunit) DO UPDATE SET
            total_stays = EXCLUDED.total_stays,
            total_patients = EXCLUDED.total_patients,
            avg_los_days = EXCLUDED.avg_los_days,
            max_los_days = EXCLUDED.max_los_days
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.agg_icu_performance")).scalar()
    logger.info(f"Loaded {count} ICU performance records")


# ============================================================
# ADDITIONAL DIMENSION LOADERS (from Silver layer)
# ============================================================

def load_dim_service(session):
    """Load service dimension by extracting unique services from admissions."""
    logger.info("Loading dim_service...")
    
    # Extract unique services from admissions (marital_status could represent service in some contexts)
    # Since Silver layer doesn't have a dedicated services table, we create a service dimension
    # from unique admission types and locations
    session.execute(text("""
        INSERT INTO gold.dim_service (curr_service, service_description)
        SELECT DISTINCT admission_type,
            CASE admission_type
                WHEN 'EMERGENCY' THEN 'Emergency Services'
                WHEN 'ELECTIVE' THEN 'Elective Services'
                WHEN 'URGENT' THEN 'Urgent Care'
                WHEN 'NEWBORN' THEN 'Newborn Services'
                ELSE admission_type
            END as service_description
        FROM silver.admissions
        WHERE admission_type IS NOT NULL
        ON CONFLICT (curr_service) DO NOTHING
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_service")).scalar()
    logger.info(f"Loaded {count} services to dim_service")


def load_dim_procedure_icd(session):
    """Load procedure ICD dimension from silver.procedureevents."""
    logger.info("Loading dim_procedure_icd...")
    
    # Extract unique item IDs from procedureevents as procedure codes
    session.execute(text("""
        INSERT INTO gold.dim_procedure_icd (icd9_code)
        SELECT DISTINCT CAST(itemid AS VARCHAR)
        FROM silver.procedureevents
        WHERE itemid IS NOT NULL
        ON CONFLICT (icd9_code) DO NOTHING
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_procedure_icd")).scalar()
    logger.info(f"Loaded {count} procedure codes to dim_procedure_icd")


def load_dim_caregiver(session):
    """Load caregiver dimension from silver.caregivers."""
    logger.info("Loading dim_caregiver...")
    
    session.execute(text("""
        INSERT INTO gold.dim_caregiver (cgid, label, description)
        SELECT cgid, label, description
        FROM silver.caregivers
        WHERE cgid IS NOT NULL
        ON CONFLICT (cgid) DO UPDATE SET
            label = EXCLUDED.label,
            description = EXCLUDED.description
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.dim_caregiver")).scalar()
    logger.info(f"Loaded {count} caregivers to dim_caregiver")


# ============================================================
# ADDITIONAL FACT LOADERS
# ============================================================

def load_fact_icu_stay(session):
    """Load ICU stay facts from silver."""
    logger.info("Loading fact_icu_stay...")
    
    session.execute(text("""
        INSERT INTO gold.fact_icu_stay (
            icustay_id, subject_id, hadm_id, first_careunit, last_careunit,
            intime, outtime, los_icu_days, los_icu_hours, patient_key, in_date_key
        )
        SELECT 
            i.icustay_id, i.subject_id, i.hadm_id, i.first_careunit, i.last_careunit,
            i.intime, i.outtime, i.los_icu_days, i.los_icu_hours,
            dp.patient_key, DATE(i.intime)
        FROM silver.icustays i
        LEFT JOIN gold.dim_patient dp ON i.subject_id = dp.subject_id
        ON CONFLICT (icustay_id) DO NOTHING
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_icu_stay")).scalar()
    logger.info(f"Loaded {count} ICU stays to fact_icu_stay")


def load_fact_lab_event(session):
    """Load lab event facts from silver (sample for performance)."""
    logger.info("Loading fact_lab_event...")
    
    session.execute(text("""
        INSERT INTO gold.fact_lab_event (
            row_id, subject_id, hadm_id, itemid, charttime, value, valuenum, valueuom,
            is_abnormal, patient_key, labitem_key, chart_date_key
        )
        SELECT 
            l.row_id, l.subject_id, l.hadm_id, l.itemid, l.charttime, l.value, l.valuenum, l.valueuom,
            COALESCE(l.is_abnormal, false),
            dp.patient_key, dl.labitem_key, DATE(l.charttime)
        FROM silver.labevents l
        LEFT JOIN gold.dim_patient dp ON l.subject_id = dp.subject_id
        LEFT JOIN gold.dim_labitem dl ON l.itemid = dl.itemid
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_lab_event")).scalar()
    logger.info(f"Loaded {count} lab events to fact_lab_event")


def load_fact_prescription(session):
    """Load prescription facts from silver."""
    logger.info("Loading fact_prescription...")
    
    session.execute(text("""
        INSERT INTO gold.fact_prescription (
            row_id, subject_id, hadm_id, drug, drug_name_generic, drug_type,
            startdate, enddate, dose_unit, route,
            patient_key, start_date_key
        )
        SELECT 
            p.row_id, p.subject_id, p.hadm_id, p.drug, p.drug_name_generic, p.drug_type,
            p.startdate, p.enddate, 
            p.dose_unit_rx, p.route,
            dp.patient_key, DATE(p.startdate)
        FROM silver.prescriptions p
        LEFT JOIN gold.dim_patient dp ON p.subject_id = dp.subject_id
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_prescription")).scalar()
    logger.info(f"Loaded {count} prescriptions to fact_prescription")


def load_fact_transfer(session):
    """Load transfer facts from silver."""
    logger.info("Loading fact_transfer...")
    
    session.execute(text("""
        INSERT INTO gold.fact_transfer (
            row_id, subject_id, hadm_id, eventtype, prev_careunit, curr_careunit,
            intime, outtime, is_icu_transfer, patient_key
        )
        SELECT 
            t.row_id, t.subject_id, t.hadm_id, t.eventtype, t.prev_careunit, t.curr_careunit,
            t.intime, t.outtime,
            CASE WHEN t.curr_careunit IN ('MICU', 'SICU', 'CCU', 'CSRU', 'TSICU', 'NICU') THEN true ELSE false END,
            dp.patient_key
        FROM silver.transfers t
        LEFT JOIN gold.dim_patient dp ON t.subject_id = dp.subject_id
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_transfer")).scalar()
    logger.info(f"Loaded {count} transfers to fact_transfer")


def load_fact_input_event(session):
    """Load input event facts from silver."""
    logger.info("Loading fact_input_event...")
    
    session.execute(text("""
        INSERT INTO gold.fact_input_event (
            row_id, subject_id, hadm_id, icustay_id, itemid, cgid, source_system,
            charttime, amount, amountuom, rate, rateuom,
            patient_key, item_key, caregiver_key
        )
        SELECT 
            i.row_id, i.subject_id, i.hadm_id, i.icustay_id, i.itemid, i.cgid, i.source_system,
            i.charttime, i.amount, i.amountuom, i.rate, i.rateuom,
            dp.patient_key, di.item_key, dc.caregiver_key
        FROM silver.inputevents i
        LEFT JOIN gold.dim_patient dp ON i.subject_id = dp.subject_id
        LEFT JOIN gold.dim_item di ON i.itemid = di.itemid
        LEFT JOIN gold.dim_caregiver dc ON i.cgid = dc.cgid
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_input_event")).scalar()
    logger.info(f"Loaded {count} input events to fact_input_event")


def load_fact_output_event(session):
    """Load output event facts from silver."""
    logger.info("Loading fact_output_event...")
    
    session.execute(text("""
        INSERT INTO gold.fact_output_event (
            row_id, subject_id, hadm_id, icustay_id, itemid, charttime, value,
            patient_key, item_key
        )
        SELECT 
            o.row_id, o.subject_id, o.hadm_id, o.icustay_id, o.itemid, o.charttime, o.value,
            dp.patient_key, di.item_key
        FROM silver.outputevents o
        LEFT JOIN gold.dim_patient dp ON o.subject_id = dp.subject_id
        LEFT JOIN gold.dim_item di ON o.itemid = di.itemid
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_output_event")).scalar()
    logger.info(f"Loaded {count} output events to fact_output_event")


def load_fact_procedure(session):
    """Load procedure facts from silver."""
    logger.info("Loading fact_procedure...")
    
    session.execute(text("""
        INSERT INTO gold.fact_procedure (
            row_id, subject_id, hadm_id, icustay_id, itemid, starttime, endtime,
            value, valueuom,
            patient_key, item_key
        )
        SELECT 
            p.row_id, p.subject_id, p.hadm_id, p.icustay_id, p.itemid, p.starttime, p.endtime,
            p.value, p.valueuom,
            dp.patient_key, di.item_key
        FROM silver.procedureevents p
        LEFT JOIN gold.dim_patient dp ON p.subject_id = dp.subject_id
        LEFT JOIN gold.dim_item di ON p.itemid = di.itemid
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_procedure")).scalar()
    logger.info(f"Loaded {count} procedures to fact_procedure")


def load_fact_microbiology(session):
    """Load microbiology facts from silver."""
    logger.info("Loading fact_microbiology...")
    
    session.execute(text("""
        INSERT INTO gold.fact_microbiology (
            row_id, subject_id, hadm_id, chartdate, charttime, spec_type_desc,
            org_name, ab_name, interpretation, is_positive, is_resistant,
            patient_key
        )
        SELECT 
            m.row_id, m.subject_id, m.hadm_id, m.chartdate, m.charttime, m.spec_type_desc,
            m.org_name, m.ab_name, m.interpretation,
            COALESCE(m.org_name IS NOT NULL, false),
            COALESCE(m.interpretation = 'R', false),
            dp.patient_key
        FROM silver.microbiologyevents m
        LEFT JOIN gold.dim_patient dp ON m.subject_id = dp.subject_id
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.fact_microbiology")).scalar()
    logger.info(f"Loaded {count} microbiology events to fact_microbiology")


# ============================================================
# ADDITIONAL AGGREGATE LOADERS (from Silver layer)
# ============================================================

def load_agg_daily_census(session):
    """Load daily census aggregate from Silver layer."""
    logger.info("Loading agg_daily_census...")
    
    session.execute(text("""
        INSERT INTO gold.agg_daily_census (
            date_key, active_patients, new_admissions, discharges
        )
        SELECT 
            DATE(a.admittime) as date_key,
            COUNT(DISTINCT a.subject_id) as active_patients,
            COUNT(*) as new_admissions,
            0 as discharges
        FROM silver.admissions a
        WHERE a.admittime IS NOT NULL
        GROUP BY DATE(a.admittime)
        ON CONFLICT (date_key) DO UPDATE SET
            active_patients = EXCLUDED.active_patients,
            new_admissions = EXCLUDED.new_admissions
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.agg_daily_census")).scalar()
    logger.info(f"Loaded {count} daily census records to agg_daily_census")


def load_agg_lab_summary(session):
    """Load lab summary aggregate from Silver layer."""
    logger.info("Loading agg_lab_summary...")
    
    # agg_lab_summary uses: subject_id, itemid, test_count, abnormal_count, abnormal_rate
    session.execute(text("""
        INSERT INTO gold.agg_lab_summary (
            subject_id, itemid, test_count, abnormal_count, abnormal_rate,
            min_value, max_value, avg_value, first_test, last_test
        )
        SELECT 
            l.subject_id,
            l.itemid,
            COUNT(*) as test_count,
            SUM(CASE WHEN l.is_abnormal THEN 1 ELSE 0 END) as abnormal_count,
            AVG(CASE WHEN l.is_abnormal THEN 1.0 ELSE 0.0 END) as abnormal_rate,
            MIN(l.valuenum) as min_value,
            MAX(l.valuenum) as max_value,
            AVG(l.valuenum) as avg_value,
            MIN(l.charttime) as first_test,
            MAX(l.charttime) as last_test
        FROM silver.labevents l
        WHERE l.subject_id IS NOT NULL AND l.itemid IS NOT NULL
        GROUP BY l.subject_id, l.itemid
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.agg_lab_summary")).scalar()
    logger.info(f"Loaded {count} lab summary records to agg_lab_summary")


def load_agg_medication_usage(session):
    """Load medication usage aggregate from Silver layer."""
    logger.info("Loading agg_medication_usage...")
    
    # agg_medication_usage uses: drug, prescription_count, patient_count
    session.execute(text("""
        INSERT INTO gold.agg_medication_usage (
            drug, prescription_count, patient_count
        )
        SELECT 
            p.drug,
            COUNT(*) as prescription_count,
            COUNT(DISTINCT p.subject_id) as patient_count
        FROM silver.prescriptions p
        WHERE p.drug IS NOT NULL
        GROUP BY p.drug
        ON CONFLICT (drug) DO UPDATE SET
            prescription_count = EXCLUDED.prescription_count,
            patient_count = EXCLUDED.patient_count
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.agg_medication_usage")).scalar()
    logger.info(f"Loaded {count} medication usage records to agg_medication_usage")


def load_agg_infection_stats(session):
    """Load infection statistics aggregate from Silver layer."""
    logger.info("Loading agg_infection_stats...")
    
    # agg_infection_stats uses: organism_name, total_cultures, positive_cultures, resistance_tests, resistant_count
    session.execute(text("""
        INSERT INTO gold.agg_infection_stats (
            organism_name, total_cultures, positive_cultures, resistance_tests, resistant_count
        )
        SELECT 
            m.org_name as organism_name,
            COUNT(*) as total_cultures,
            COUNT(*) as positive_cultures,
            SUM(CASE WHEN m.interpretation IS NOT NULL THEN 1 ELSE 0 END) as resistance_tests,
            SUM(CASE WHEN m.interpretation = 'R' THEN 1 ELSE 0 END) as resistant_count
        FROM silver.microbiologyevents m
        WHERE m.org_name IS NOT NULL
        GROUP BY m.org_name
        ON CONFLICT (organism_name) DO UPDATE SET
            total_cultures = EXCLUDED.total_cultures,
            positive_cultures = EXCLUDED.positive_cultures,
            resistance_tests = EXCLUDED.resistance_tests,
            resistant_count = EXCLUDED.resistant_count
    """))
    session.commit()
    
    count = session.execute(text("SELECT COUNT(*) FROM gold.agg_infection_stats")).scalar()
    logger.info(f"Loaded {count} infection stats records to agg_infection_stats")


def main():
    parser = argparse.ArgumentParser(description="Load Silver data to Gold layer")
    parser.add_argument("--skip-time", action="store_true", help="Skip dim_time generation")
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("SILVER → GOLD TRANSFORMATION")
    logger.info("=" * 60)
    
    try:
        with get_db() as session:
            # Create schema and tables
            create_gold_schema(session)
            create_gold_tables(session.get_bind())
            
            # Phase 1: Dimensions
            logger.info("\n--- Loading Dimensions ---")
            if not args.skip_time:
                generate_dim_time(session)
            load_dim_patient(session)
            load_dim_labitem(session)
            load_dim_item(session)
            load_dim_careunit(session)
            load_dim_service(session)
            load_dim_procedure_icd(session)
            load_dim_caregiver(session)
            
            # Phase 2: Facts
            logger.info("\n--- Loading Facts ---")
            load_fact_admission(session)
            load_fact_icu_stay(session)
            load_fact_lab_event(session)
            load_fact_prescription(session)
            load_fact_transfer(session)
            load_fact_input_event(session)
            load_fact_output_event(session)
            load_fact_procedure(session)
            load_fact_microbiology(session)
            
            # Phase 3: Aggregates
            logger.info("\n--- Loading Aggregates ---")
            load_agg_patient_summary(session)
            load_agg_icu_performance(session)
            load_agg_daily_census(session)
            load_agg_lab_summary(session)
            load_agg_medication_usage(session)
            load_agg_infection_stats(session)
            
            logger.info("\n" + "=" * 60)
            logger.info("Gold layer loading complete!")
            logger.info("=" * 60)
            
        return 0
        
    except Exception as e:
        logger.error(f"Gold layer loading failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())


