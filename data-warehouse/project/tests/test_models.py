"""Unit tests for Bronze layer models."""
import pytest
from datetime import datetime

from app.models.bronze import (
    BronzePatients,
    BronzeAdmissions,
    BronzeICUStays,
    BronzeCaregivers,
)


class TestBronzePatients:
    """Test BronzePatients model."""

    def test_create_patient(self):
        """Test creating a patient instance."""
        patient = BronzePatients(
            row_id=1,
            subject_id=10001,
            gender="M",
            dob=datetime(1980, 1, 1),
            dod=None,
            dod_hosp=None,
            dod_ssn=None,
            expire_flag=False,
        )

        assert patient.subject_id == 10001
        assert patient.gender == "M"
        assert patient.expire_flag is False

    def test_patient_repr(self):
        """Test patient string representation."""
        patient = BronzePatients(
            row_id=1,
            subject_id=10001,
            gender="F",
            dob=datetime(1980, 1, 1),
            expire_flag=True,
        )

        repr_str = repr(patient)
        assert "10001" in repr_str
        assert "F" in repr_str


class TestBronzeAdmissions:
    """Test BronzeAdmissions model."""

    def test_create_admission(self):
        """Test creating an admission instance."""
        admission = BronzeAdmissions(
            row_id=1,
            subject_id=10001,
            hadm_id=100001,
            admittime=datetime(2020, 1, 1, 10, 0),
            dischtime=datetime(2020, 1, 5, 14, 30),
            admission_type="EMERGENCY",
            diagnosis="SEPSIS",
            hospital_expire_flag=False,
            has_chartevents_data=True,
        )

        assert admission.hadm_id == 100001
        assert admission.admission_type == "EMERGENCY"
        assert admission.diagnosis == "SEPSIS"

    def test_admission_repr(self):
        """Test admission string representation."""
        admission = BronzeAdmissions(
            row_id=1,
            subject_id=10001,
            hadm_id=100001,
            admittime=datetime(2020, 1, 1),
            admission_type="EMERGENCY",
            hospital_expire_flag=False,
            has_chartevents_data=True,
        )

        repr_str = repr(admission)
        assert "100001" in repr_str
        assert "EMERGENCY" in repr_str


class TestBronzeICUStays:
    """Test BronzeICUStays model."""

    def test_create_icustay(self):
        """Test creating an ICU stay instance."""
        icustay = BronzeICUStays(
            row_id=1,
            subject_id=10001,
            hadm_id=100001,
            icustay_id=200001,
            first_careunit="MICU",
            last_careunit="MICU",
            intime=datetime(2020, 1, 1, 12, 0),
            outtime=datetime(2020, 1, 3, 10, 0),
            los=1.92,
        )

        assert icustay.icustay_id == 200001
        assert icustay.first_careunit == "MICU"
        assert icustay.los == 1.92


class TestBronzeCaregivers:
    """Test BronzeCaregivers model."""

    def test_create_caregiver(self):
        """Test creating a caregiver instance."""
        caregiver = BronzeCaregivers(
            row_id=1,
            cgid=5001,
            label="RN",
            description="Registered Nurse",
        )

        assert caregiver.cgid == 5001
        assert caregiver.label == "RN"
        assert caregiver.description == "Registered Nurse"
