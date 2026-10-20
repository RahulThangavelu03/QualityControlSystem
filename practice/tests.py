from django.test import TestCase

# Create your tests here.

from datetime import date
from django.test import TestCase
from practice.models import Gauge


from decimal import Decimal

from practice.models import Inspection, InspectionField, InspectionEntry, InspectionTemplate

from practice.models import (
    Gauge,
    Inspection,
    InspectionField,
    InspectionEntry,
    InspectionTemplate,
)


class GaugeExpiryTests(TestCase):
    def test_gauge_is_valid_on_expiry_date(self):
        gauge = Gauge(
            serial_number="VC-104",
            gauge_type="caliper",
            calibaration_expiry_date=date(2026, 10, 19),
        )

        self.assertFalse(
            gauge.is_expired(today=date(2026, 10, 19))
        )

    def test_gauge_is_expired_after_expiry_date(self):
        gauge = Gauge(
            serial_number="VC-105",
            gauge_type="caliper",
            calibaration_expiry_date=date(2026, 10, 19),
        )

        self.assertTrue(
            gauge.is_expired(today=date(2026, 10, 20))
        )



class ToleranceTests(TestCase):
    def setUp(self):
        template = InspectionTemplate.objects.create(
            part_number="PART-101",
            operation_step="Final Inspection",
            customer_agreement="Standard",
            revision="A",
            is_approved=True,
        )



        self.gauge = Gauge.objects.create(
    serial_number="VC-201",
    gauge_type="caliper",
    calibaration_expiry_date=date(2027, 12, 31),
)

        self.field = InspectionField.objects.create(
            template=template,
            name="Diameter",
            field_type="DIMENSION",
            nominal_value=Decimal("25.000"),
            lower_limit=Decimal("24.980"),
            upper_limit=Decimal("25.050"),
            is_ctq=False,
        )

        self.inspection = Inspection.objects.create(
            job_number="JOB-001",
            status="IN_PROGRESS",
        )

    def test_lower_boundary_passes(self):
        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("24.980"),
        )
        entry.full_clean()
        self.assertTrue(entry.passed)

    def test_upper_boundary_passes(self):
        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("25.050"),
        )
        entry.full_clean()
        self.assertTrue(entry.passed)


    def test_below_lower_limit_fails(self):
        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("24.979"),
    
     )
        entry.full_clean()
        self.assertFalse(entry.passed)


    def test_above_upper_limit_fails(self):
        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("25.051"),
     )
        entry.full_clean()
        self.assertFalse(entry.passed)




    def test_failed_ctq_freezes_inspection(self):
        self.field.is_ctq = True
        self.field.save()

        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("24.979"),
        )
        entry.save()  # Save the entry and trigger CTQ freezing

        self.inspection.refresh_from_db()
        self.assertEqual(self.inspection.status, "FROZEN")



    def test_submit_for_review(self):
        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("25.000"),
    )
        entry.save()

        self.inspection.submit_for_review()
        self.assertEqual(self.inspection.status, "PENDING_REVIEW")


    def test_approve_inspection(self):
       self.inspection.status = "PENDING_REVIEW"
       self.inspection.save()

       self.inspection.approve()
       self.assertEqual(self.inspection.status, "APPROVED")


    def test_reject_inspection(self):
        self.inspection.status = "PENDING_REVIEW"
        self.inspection.save()

        self.inspection.reject()
        self.assertEqual(self.inspection.status, "REJECTED")

    def test_cannot_add_entry_after_submission(self):
        from django.core.exceptions import ValidationError

        self.inspection.status = "PENDING_REVIEW"
        self.inspection.save()

        entry = InspectionEntry(
            inspection=self.inspection,
            inspection_field=self.field,
            gauge=self.gauge,
            measured_value=Decimal("25.000"),
    )

        with self.assertRaises(ValidationError):
            entry.save()
