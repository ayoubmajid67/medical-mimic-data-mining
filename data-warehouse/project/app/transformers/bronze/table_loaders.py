"""Table-specific loaders for Bronze layer."""
from pathlib import Path
from typing import Dict

from sqlalchemy.orm import Session

from app.models.bronze import (
    BronzeAdmissions,
    BronzeCaregivers,
    BronzeDItems,
    BronzeDLabItems,
    BronzeICUStays,
    BronzeInputEventsCareVue,
    BronzeInputEventsMetaVision,
    BronzeLabEvents,
    BronzeMicrobiologyEvents,
    BronzeNoteEvents,
    BronzeOutputEvents,
    BronzePatients,
    BronzePrescriptions,
    BronzeProcedureEventsMetaVision,
    BronzeServices,
    BronzeTransfers,
)
from app.shared import logger

from .base_loader import BaseCSVLoader


# Field mappings for each table (field_name -> field_type)
FIELD_MAPPINGS = {
    "PATIENTS": {
        "row_id": "int",
        "subject_id": "int",
        "gender": "str",
        "dob": "datetime",
        "dod": "datetime",
        "dod_hosp": "datetime",
        "dod_ssn": "datetime",
        "expire_flag": "bool",
    },
    "ADMISSIONS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "admittime": "datetime",
        "dischtime": "datetime",
        "deathtime": "datetime",
        "admission_type": "str",
        "admission_location": "str",
        "discharge_location": "str",
        "insurance": "str",
        "language": "str",
        "religion": "str",
        "marital_status": "str",
        "ethnicity": "str",
        "edregtime": "datetime",
        "edouttime": "datetime",
        "diagnosis": "str",
        "hospital_expire_flag": "bool",
        "has_chartevents_data": "bool",
    },
    "ICUSTAYS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "dbsource": "str",
        "first_careunit": "str",
        "last_careunit": "str",
        "first_wardid": "int",
        "last_wardid": "int",
        "intime": "datetime",
        "outtime": "datetime",
        "los": "float",
    },
    "CAREGIVERS": {
        "row_id": "int",
        "cgid": "int",
        "label": "str",
        "description": "str",
    },
    "SERVICES": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "transfertime": "datetime",
        "prev_service": "str",
        "curr_service": "str",
    },
    "TRANSFERS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "dbsource": "str",
        "eventtype": "str",
        "prev_careunit": "str",
        "curr_careunit": "str",
        "prev_wardid": "int",
        "curr_wardid": "int",
        "intime": "datetime",
        "outtime": "datetime",
        "los": "float",
    },
    "D_ITEMS": {
        "row_id": "int",
        "itemid": "int",
        "label": "str",
        "abbreviation": "str",
        "dbsource": "str",
        "linksto": "str",
        "category": "str",
        "unitname": "str",
        "param_type": "str",
        "conceptid": "int",
    },
    "D_LABITEMS": {
        "row_id": "int",
        "itemid": "int",
        "label": "str",
        "fluid": "str",
        "category": "str",
        "loinc_code": "str",
    },
    "LABEVENTS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "itemid": "int",
        "charttime": "datetime",
        "value": "str",
        "valuenum": "float",
        "valueuom": "str",
        "flag": "str",
    },
    "INPUTEVENTS_CV": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "charttime": "datetime",
        "itemid": "int",
        "amount": "float",
        "amountuom": "str",
        "rate": "float",
        "rateuom": "str",
        "storetime": "datetime",
        "cgid": "int",
        "orderid": "int",
        "linkorderid": "int",
        "stopped": "str",
        "newbottle": "bool",
        "originalamount": "float",
        "originalamountuom": "str",
        "originalroute": "str",
        "originalrate": "float",
        "originalrateuom": "str",
        "originalsite": "str",
    },
    "INPUTEVENTS_MV": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "starttime": "datetime",
        "endtime": "datetime",
        "itemid": "int",
        "amount": "float",
        "amountuom": "str",
        "rate": "float",
        "rateuom": "str",
        "storetime": "datetime",
        "cgid": "int",
        "orderid": "int",
        "linkorderid": "int",
        "ordercategoryname": "str",
        "secondaryordercategoryname": "str",
        "ordercomponenttypedescription": "str",
        "ordercategorydescription": "str",
        "patientweight": "float",
        "totalamount": "float",
        "totalamountuom": "str",
        "isopenbag": "bool",
        "continueinnextdept": "bool",
        "cancelreason": "str",
        "statusdescription": "str",
        "comments_editedby": "str",
        "comments_canceledby": "str",
        "comments_date": "datetime",
        "originalamount": "float",
        "originalrate": "float",
    },
    "OUTPUTEVENTS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "charttime": "datetime",
        "itemid": "int",
        "value": "float",
        "valueuom": "str",
        "storetime": "datetime",
        "cgid": "int",
        "stopped": "str",
        "newbottle": "bool",
        "iserror": "bool",
    },
    "PRESCRIPTIONS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "startdate": "datetime",
        "enddate": "datetime",
        "drug_type": "str",
        "drug": "str",
        "drug_name_poe": "str",
        "drug_name_generic": "str",
        "formulary_drug_cd": "str",
        "gsn": "str",
        "ndc": "str",
        "prod_strength": "str",
        "dose_val_rx": "str",
        "dose_unit_rx": "str",
        "form_val_disp": "str",
        "form_unit_disp": "str",
        "route": "str",
    },
    "PROCEDUREEVENTS_MV": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "icustay_id": "int",
        "starttime": "datetime",
        "endtime": "datetime",
        "itemid": "int",
        "value": "float",
        "valueuom": "str",
        "location": "str",
        "locationcategory": "str",
        "storetime": "datetime",
        "cgid": "int",
        "orderid": "int",
        "linkorderid": "int",
        "ordercategoryname": "str",
        "secondaryordercategoryname": "str",
        "ordercategorydescription": "str",
        "isopenbag": "bool",
        "continueinnextdept": "bool",
        "cancelreason": "str",
        "statusdescription": "str",
        "comments_editedby": "str",
        "comments_canceledby": "str",
        "comments_date": "datetime",
    },
    "MICROBIOLOGYEVENTS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "chartdate": "date",
        "charttime": "datetime",
        "spec_itemid": "int",
        "spec_type_desc": "str",
        "org_itemid": "int",
        "org_name": "str",
        "isolate_num": "int",
        "ab_itemid": "int",
        "ab_name": "str",
        "dilution_text": "str",
        "dilution_comparison": "str",
        "dilution_value": "float",
        "interpretation": "str",
    },
    "NOTEEVENTS": {
        "row_id": "int",
        "subject_id": "int",
        "hadm_id": "int",
        "chartdate": "datetime",
        "charttime": "datetime",
        "storetime": "datetime",
        "category": "str",
        "description": "str",
        "cgid": "int",
        "iserror": "str",
        "text": "str",
    },
}

# Model class mapping
MODEL_CLASSES = {
    "PATIENTS": BronzePatients,
    "ADMISSIONS": BronzeAdmissions,
    "ICUSTAYS": BronzeICUStays,
    "CAREGIVERS": BronzeCaregivers,
    "SERVICES": BronzeServices,
    "TRANSFERS": BronzeTransfers,
    "D_ITEMS": BronzeDItems,
    "D_LABITEMS": BronzeDLabItems,
    "LABEVENTS": BronzeLabEvents,
    "INPUTEVENTS_CV": BronzeInputEventsCareVue,
    "INPUTEVENTS_MV": BronzeInputEventsMetaVision,
    "OUTPUTEVENTS": BronzeOutputEvents,
    "PRESCRIPTIONS": BronzePrescriptions,
    "PROCEDUREEVENTS_MV": BronzeProcedureEventsMetaVision,
    "MICROBIOLOGYEVENTS": BronzeMicrobiologyEvents,
    "NOTEEVENTS": BronzeNoteEvents,
}


def load_table(
    session: Session,
    table_name: str,
    csv_dir: Path,
    batch_size: int = 1000,
) -> Dict[str, int]:
    """
    Load a specific table from CSV.

    Args:
        session: SQLAlchemy session
        table_name: Name of table to load (e.g., 'PATIENTS')
        csv_dir: Directory containing CSV files
        batch_size: Batch size for loading

    Returns:
        Loading statistics

    Raises:
        ValueError: If table name is invalid
        FileNotFoundError: If CSV file doesn't exist
    """
    if table_name not in MODEL_CLASSES:
        raise ValueError(f"Invalid table name: {table_name}. Available: {list(MODEL_CLASSES.keys())}")

    csv_path = csv_dir / f"{table_name}.csv"
    model_class = MODEL_CLASSES[table_name]
    field_mapping = FIELD_MAPPINGS[table_name]

    logger.info(f"Loading table: {table_name} from {csv_path}")

    loader = BaseCSVLoader(
        model_class=model_class,
        csv_path=csv_path,
        batch_size=batch_size,
        skip_errors=True,
    )

    loader.load(session, field_mapping)
    return loader.get_stats()


def load_all_tables(session: Session, csv_dir: Path, batch_size: int = 1000) -> Dict[str, Dict[str, int]]:
    """
    Load all tables from CSVs.

    Args:
        session: SQLAlchemy session
        csv_dir: Directory containing CSV files
        batch_size: Batch size for loading

    Returns:
        Statistics for each table
    """
    all_stats = {}

    for table_name in MODEL_CLASSES.keys():
        try:
            stats = load_table(session, table_name, csv_dir, batch_size)
            all_stats[table_name] = stats
        except FileNotFoundError:
            logger.warning(f"CSV not found for {table_name}, skipping")
        except Exception as e:
            logger.error(f"Failed to load {table_name}: {e}")
            all_stats[table_name] = {"error": str(e)}

    return all_stats
