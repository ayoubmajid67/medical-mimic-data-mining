# Bronze vs Silver Layer - Detailed Comparison

This document provides a comprehensive comparison between the Bronze and Silver layers in the MIMIC-III data warehouse, including transformation details and visual diagrams.

---

## Executive Summary

| Aspect | Bronze Layer | Silver Layer |
|--------|--------------|--------------|
| **Purpose** | Raw data storage (as-is from CSV) | Cleaned, validated, enriched data |
| **Tables** | 16 tables | 11 tables |
| **Schema** | `bronze.*` | `silver.*` |
| **Data Quality** | None (raw) | Validated, standardized |
| **Calculations** | None | LOS, durations, flags |
| **Audit Trail** | None | `created_at`, `updated_at` |

---

## Transformation Statistics

```
Bronze Layer: 16 tables
Silver Layer: 11 tables
─────────────────────────
• 1 MERGE:        inputevents_cv + inputevents_mv → inputevents
• 9 TRANSFORMS:   1:1 mapping with calculated fields
• 5 SKIPPED:      Reference/dictionary tables (→ Gold dimensions)
• 1 MISSING:      noteevents (CSV file not found)
```

### Merged Tables (2 → 1)

| Bronze Tables | Silver Table | Reason |
|---------------|--------------|--------|
| `inputevents_cv` (CareVue) | `inputevents` | Different ICU systems, same data type |
| `inputevents_mv` (MetaVision) | | Unified with `source_system` field |

### Transformed Tables (1:1 with enrichment)

| Bronze Table | Silver Table | Key Additions |
|--------------|--------------|---------------|
| `patients` | `patients` | `is_deceased`, validated gender |
| `admissions` | `admissions` | `los_days`, `los_hours` |
| `icustays` | `icustays` | `los_icu_days`, `los_icu_hours` |
| `labevents` | `labevents` | Parsed `valuenum`, `is_abnormal` |
| `prescriptions` | `prescriptions` | Parsed doses, `duration_days` |
| `transfers` | `transfers` | `duration_hours`, `is_icu_transfer` |
| `outputevents` | `outputevents` | Standardized measurements |
| `procedureevents_mv` | `procedureevents` | `is_completed`, `is_canceled` |
| `microbiologyevents` | `microbiologyevents` | `is_positive`, `is_resistant` |

### Skipped Tables (→ Gold Layer)

| Bronze Table | Reason | Gold Destination |
|--------------|--------|------------------|
| `caregivers` | Reference data | `dim_caregiver` |
| `services` | Reference data | `dim_service` |
| `d_items` | Dictionary | `dim_item` |
| `d_labitems` | Dictionary | `dim_labitem` |
| `procedures_icd` | Code mappings | `dim_procedure` |

---

## Table Mapping Diagram

```mermaid
flowchart LR
    subgraph Bronze["Bronze Layer (16 tables)"]
        B_PAT[patients]
        B_ADM[admissions]
        B_ICU[icustays]
        B_LAB[labevents]
        B_PRE[prescriptions]
        B_TRA[transfers]
        B_CV[inputevents_cv]
        B_MV[inputevents_mv]
        B_OUT[outputevents]
        B_PRO[procedureevents_mv]
        B_MIC[microbiologyevents]
        B_CAR[caregivers]
        B_SER[services]
        B_DI[d_items]
        B_DL[d_labitems]
        B_ICD[procedures_icd]
    end

    subgraph Silver["Silver Layer (11 tables)"]
        S_PAT[patients]
        S_ADM[admissions]
        S_ICU[icustays]
        S_LAB[labevents]
        S_PRE[prescriptions]
        S_TRA[transfers]
        S_INP[inputevents]
        S_OUT[outputevents]
        S_PRO[procedureevents]
        S_MIC[microbiologyevents]
    end

    subgraph Gold["Gold Layer (dimensions)"]
        G_DIM["dim_*"]
    end

    %% Direct mappings
    B_PAT --> S_PAT
    B_ADM --> S_ADM
    B_ICU --> S_ICU
    B_LAB --> S_LAB
    B_PRE --> S_PRE
    B_TRA --> S_TRA
    B_OUT --> S_OUT
    B_PRO --> S_PRO
    B_MIC --> S_MIC

    %% MERGED tables (highlighted)
    B_CV -->|MERGED| S_INP
    B_MV -->|MERGED| S_INP

    %% Dimension tables (skipped to gold)
    B_CAR -.->|to Gold| G_DIM
    B_SER -.->|to Gold| G_DIM
    B_DI -.->|to Gold| G_DIM
    B_DL -.->|to Gold| G_DIM
    B_ICD -.->|to Gold| G_DIM

    style S_INP fill:#90EE90,stroke:#228B22,stroke-width:3px
    style B_CV fill:#FFB6C1,stroke:#DC143C,stroke-width:2px
    style B_MV fill:#FFB6C1,stroke:#DC143C,stroke-width:2px
```

---

## Merged Tables Detail: InputEvents

The most significant transformation is merging two separate Bronze tables into one Silver table.

### Before (Bronze): 2 Separate Tables

```mermaid
flowchart TB
    subgraph CareVue["bronze.inputevents_cv"]
        CV1["row_id"]
        CV2["subject_id"]
        CV3["hadm_id"]
        CV4["icustay_id"]
        CV5["charttime ✓"]
        CV6["itemid"]
        CV7["amount"]
        CV8["amountuom"]
        CV9["rate"]
        CV10["rateuom"]
        CV11["stopped"]
        CV12["newbottle"]
        CV13["originalamount"]
        CV14["originalamountuom"]
        CV15["originalroute"]
        CV16["originalrate"]
        CV17["originalrateuom"]
        CV18["originalsite"]
    end

    subgraph MetaVision["bronze.inputevents_mv"]
        MV1["row_id"]
        MV2["subject_id"]
        MV3["hadm_id"]
        MV4["icustay_id"]
        MV5["starttime ✓"]
        MV6["endtime ✓"]
        MV7["itemid"]
        MV8["amount"]
        MV9["amountuom"]
        MV10["rate"]
        MV11["rateuom"]
        MV12["storetime"]
        MV13["cgid"]
        MV14["orderid"]
        MV15["linkorderid"]
        MV16["ordercategoryname"]
        MV17["secondaryordercategoryname"]
        MV18["ordercomponenttypedescription"]
        MV19["ordercategorydescription"]
        MV20["patientweight"]
        MV21["totalamount"]
        MV22["totalamountuom"]
        MV23["isopenbag"]
        MV24["continueinnextdept"]
        MV25["cancelreason"]
        MV26["statusdescription"]
        MV27["originalamount"]
        MV28["originalrate"]
    end

    style CareVue fill:#FFDAB9
    style MetaVision fill:#ADD8E6
```

### After (Silver): 1 Unified Table

```mermaid
flowchart TB
    subgraph Unified["silver.inputevents (MERGED)"]
        U1["row_id"]
        U2["subject_id"]
        U3["hadm_id"]
        U4["icustay_id"]
        U5["source_system ⭐ NEW"]
        U6["itemid"]
        U7["charttime (from CV or MV starttime)"]
        U8["starttime (MV only)"]
        U9["endtime (MV only)"]
        U10["amount"]
        U11["amountuom"]
        U12["rate"]
        U13["rateuom"]
        U14["duration_hours ⭐ NEW (calculated)"]
        U15["is_bolus ⭐ NEW (flag)"]
        U16["created_at ⭐ AUDIT"]
        U17["updated_at ⭐ AUDIT"]
    end

    style Unified fill:#90EE90,stroke:#228B22,stroke-width:3px
```

### Merge Logic

```python
# CareVue records
{
    "source_system": "CareVue",
    "charttime": bronze.charttime,      # CV uses charttime
    "starttime": None,                  # CV doesn't have start/end
    "endtime": None,
    "is_bolus": bronze.rate is None,    # No rate = bolus
}

# MetaVision records  
{
    "source_system": "MetaVision",
    "charttime": bronze.starttime,      # MV uses starttime as charttime
    "starttime": bronze.starttime,
    "endtime": bronze.endtime,
    "duration_hours": (endtime - starttime) / 3600,
    "is_bolus": bronze.orderid is None,
}
```

---

## Detailed Table Comparisons

### 1. PATIENTS

```mermaid
flowchart LR
    subgraph Bronze["bronze.patients"]
        B1["row_id"]
        B2["subject_id"]
        B3["gender"]
        B4["dob"]
        B5["dod"]
        B6["dod_hosp"]
        B7["dod_ssn"]
        B8["expire_flag"]
    end

    subgraph Silver["silver.patients"]
        S1["subject_id"]
        S2["gender ✓ validated M/F"]
        S3["date_of_birth"]
        S4["date_of_death"]
        S5["is_deceased ⭐ NEW"]
        S6["dob_shift_years ⭐ NEW"]
        S7["created_at ⭐ AUDIT"]
        S8["updated_at ⭐ AUDIT"]
    end

    B2 --> S1
    B3 -->|"validated"| S2
    B4 -->|"date only"| S3
    B5 -->|"date only"| S4
    B5 -->|"calculated"| S5
    B6 -->|"merged"| S5

    style S5 fill:#90EE90
    style S6 fill:#90EE90
    style S7 fill:#87CEEB
    style S8 fill:#87CEEB
```

| Bronze Column | Silver Column | Transformation |
|---------------|---------------|----------------|
| `row_id` | ❌ Removed | Not needed as PK |
| `subject_id` | `subject_id` | Primary key |
| `gender` | `gender` | **Validated**: Only M/F allowed |
| `dob` | `date_of_birth` | DateTime → Date |
| `dod` | `date_of_death` | DateTime → Date |
| `dod_hosp` | ❌ Removed | Merged into `is_deceased` |
| `dod_ssn` | ❌ Removed | Merged into `is_deceased` |
| `expire_flag` | ❌ Removed | Replaced by `is_deceased` |
| ❌ | `is_deceased` | **NEW**: Boolean flag |
| ❌ | `dob_shift_years` | **NEW**: Age anonymization info |
| ❌ | `created_at` | **NEW**: Audit timestamp |
| ❌ | `updated_at` | **NEW**: Audit timestamp |

---

### 2. ADMISSIONS

```mermaid
flowchart LR
    subgraph Bronze["bronze.admissions"]
        B1["row_id"]
        B2["subject_id"]
        B3["hadm_id"]
        B4["admittime"]
        B5["dischtime"]
        B6["deathtime"]
        B7["admission_type"]
        B8["admission_location"]
        B9["discharge_location"]
        B10["insurance"]
        B11["language"]
        B12["religion"]
        B13["marital_status"]
        B14["ethnicity"]
        B15["edregtime"]
        B16["edouttime"]
        B17["diagnosis"]
        B18["hospital_expire_flag (0/1)"]
        B19["has_chartevents_data"]
    end

    subgraph Silver["silver.admissions"]
        S1["hadm_id"]
        S2["subject_id"]
        S3["admittime"]
        S4["dischtime"]
        S5["los_days ⭐ NEW"]
        S6["los_hours ⭐ NEW"]
        S7["admission_type"]
        S8["admission_location"]
        S9["discharge_location"]
        S10["edregtime"]
        S11["edouttime"]
        S12["diagnosis"]
        S13["hospital_expire_flag (boolean)"]
        S14["insurance"]
        S15["language"]
        S16["religion"]
        S17["marital_status"]
        S18["ethnicity"]
        S19["created_at ⭐ AUDIT"]
        S20["updated_at ⭐ AUDIT"]
    end

    B4 --> S3
    B5 --> S4
    B4 -->|"calculated"| S5
    B5 -->|"calculated"| S5
    B18 -->|"int→bool"| S13

    style S5 fill:#90EE90
    style S6 fill:#90EE90
    style S19 fill:#87CEEB
    style S20 fill:#87CEEB
```

**Key Transformation - LOS Calculation:**
```python
los_days = (dischtime - admittime).total_seconds() / 86400
los_hours = (dischtime - admittime).total_seconds() / 3600
```

---

### 3. ICUSTAYS

| Bronze Column | Silver Column | Transformation |
|---------------|---------------|----------------|
| `icustay_id` | `icustay_id` | Primary key |
| `subject_id` | `subject_id` | Foreign key |
| `hadm_id` | `hadm_id` | Foreign key |
| `first_careunit` | `first_careunit` | No change |
| `last_careunit` | `last_careunit` | No change |
| `first_wardid` | `first_wardid` | No change |
| `last_wardid` | `last_wardid` | No change |
| `intime` | `intime` | No change |
| `outtime` | `outtime` | No change |
| `los` | ❌ Removed | Replaced by calculated fields |
| ❌ | `los_icu_days` | **NEW**: Calculated from timestamps |
| ❌ | `los_icu_hours` | **NEW**: Calculated from timestamps |

**Why recalculate LOS?**
- Bronze `los` may have inconsistencies
- Silver calculates from actual timestamps for accuracy

---

### 4. LABEVENTS

```mermaid
flowchart LR
    subgraph Bronze["bronze.labevents"]
        B1["row_id"]
        B2["subject_id"]
        B3["hadm_id"]
        B4["itemid"]
        B5["charttime"]
        B6["value (string)"]
        B7["valuenum (float, nullable)"]
        B8["valueuom"]
        B9["flag (string)"]
    end

    subgraph Silver["silver.labevents"]
        S1["row_id"]
        S2["subject_id"]
        S3["hadm_id"]
        S4["itemid"]
        S5["charttime"]
        S6["value"]
        S7["valuenum ✓ parsed"]
        S8["valueuom"]
        S9["flag"]
        S10["is_abnormal ⭐ NEW"]
        S11["created_at ⭐ AUDIT"]
        S12["updated_at ⭐ AUDIT"]
    end

    B6 -->|"parse if needed"| S7
    B7 --> S7
    B9 -->|"derive flag"| S10

    style S10 fill:#90EE90
    style S11 fill:#87CEEB
    style S12 fill:#87CEEB
```

**Value Parsing Logic:**
```python
# Bronze value might be: ">10", "<0.5", "NEGATIVE", "5.5"
def parse_numeric(value):
    if not value:
        return None
    value = value.strip()
    for prefix in ['>', '<', '>=', '<=', '~']:
        if value.startswith(prefix):
            value = value[len(prefix):]
    try:
        return float(value)
    except:
        return None

# Use bronze valuenum if available, else parse
silver_valuenum = bronze.valuenum or parse_numeric(bronze.value)
```

**Abnormal Flag Logic:**
```python
is_abnormal = bronze.flag.upper() in ['ABNORMAL', 'H', 'L', 'A', 'HIGH', 'LOW']
```

---

### 5. PRESCRIPTIONS

| Bronze Column | Silver Column | Transformation |
|---------------|---------------|----------------|
| `dose_val_rx` | `dose_val_rx` | **Parsed to float** |
| `form_val_disp` | `form_val_disp` | **Parsed to float** |
| `startdate` | `startdate` | No change |
| `enddate` | `enddate` | No change |
| ❌ | `duration_days` | **NEW**: `enddate - startdate` |

---

### 6. TRANSFERS

| Bronze Column | Silver Column | Transformation |
|---------------|---------------|----------------|
| `intime` | `intime` | No change |
| `outtime` | `outtime` | No change |
| `curr_careunit` | `curr_careunit` | No change |
| ❌ | `duration_hours` | **NEW**: `outtime - intime` |
| ❌ | `is_icu_transfer` | **NEW**: Boolean flag if ICU |

**ICU Detection:**
```python
ICU_UNITS = ['MICU', 'SICU', 'CCU', 'CSRU', 'TSICU', 'NICU', 'NWARD']
is_icu_transfer = curr_careunit in ICU_UNITS or prev_careunit in ICU_UNITS
```

---

### 7. PROCEDUREEVENTS

| Bronze Column | Silver Column | Transformation |
|---------------|---------------|----------------|
| `statusdescription` | `status_description` | Renamed |
| `cancelreason` | ❌ | Replaced by `is_canceled` |
| ❌ | `is_completed` | **NEW**: Boolean flag |
| ❌ | `is_canceled` | **NEW**: Boolean flag |
| ❌ | `duration_hours` | **NEW**: `endtime - starttime` |

---

### 8. MICROBIOLOGYEVENTS

| Bronze Column | Silver Column | Transformation |
|---------------|---------------|----------------|
| `org_name` | `org_name` | No change |
| `interpretation` | `interpretation` | No change |
| ❌ | `is_positive` | **NEW**: `org_name is not null` |
| ❌ | `is_resistant` | **NEW**: `interpretation == 'R'` |

---

## Summary: New Silver Fields

### Calculated Metrics (from timestamps)
| Field | Table | Calculation |
|-------|-------|-------------|
| `los_days` | admissions | `(dischtime - admittime) / 86400` |
| `los_hours` | admissions | `(dischtime - admittime) / 3600` |
| `los_icu_days` | icustays | `(outtime - intime) / 86400` |
| `los_icu_hours` | icustays | `(outtime - intime) / 3600` |
| `duration_hours` | transfers, procedures, inputs | `(end - start) / 3600` |
| `duration_days` | prescriptions | `enddate - startdate` |

### Boolean Flags (derived from data)
| Field | Table | Logic |
|-------|-------|-------|
| `is_deceased` | patients | `dod IS NOT NULL` |
| `is_abnormal` | labevents | `flag IN ('H', 'L', 'A')` |
| `is_icu_transfer` | transfers | `careunit IN ICU_UNITS` |
| `is_completed` | procedures | `status != 'CANCELED'` |
| `is_canceled` | procedures | `status == 'CANCELED'` |
| `is_positive` | microbiology | `org_name IS NOT NULL` |
| `is_resistant` | microbiology | `interpretation == 'R'` |
| `is_bolus` | inputevents | `rate IS NULL OR orderid IS NULL` |

### Data Quality Fields
| Field | Table | Purpose |
|-------|-------|---------|
| `source_system` | inputevents | Tracks origin (CareVue/MetaVision) |
| `created_at` | ALL | When record was created in silver |
| `updated_at` | ALL | When record was last modified |

---

## Tables Not Transformed to Silver

These tables skip Silver and go directly to Gold as dimension tables:

| Bronze Table | Reason | Gold Destination |
|--------------|--------|------------------|
| `caregivers` | Reference data | `dim_caregiver` |
| `services` | Reference data | `dim_service` |
| `d_items` | Dictionary | `dim_item` |
| `d_labitems` | Dictionary | `dim_labitem` |
| `procedures_icd` | Code mappings | `dim_procedure` |
| `noteevents` | ❌ CSV not found | Skip |

---

## Data Quality Improvements

| Issue in Bronze | Fix in Silver |
|-----------------|---------------|
| Null `valuenum` with parseable `value` | Parse numeric from string |
| Multiple death columns (`dod`, `dod_hosp`) | Single `is_deceased` flag |
| Integer flags (0/1) | Boolean types |
| Separate CV/MV tables | Unified with `source_system` |
| Missing LOS | Calculated from timestamps |
| String dates | Proper date types |
| Inconsistent gender values | Validated M/F only |
