from django.db import models
from datetime import date
from datetime import date
from django.db import models





class Product(models.Model):

    title = models.CharField(max_length = 100)

    quantity = models.IntegerField()


class Gauge(models.Model):

    serial_number= models.CharField( max_length=50,unique= True)

    gauge_type= models.CharField(max_length=30)

    calibaration_expiry_date=models.DateField()


    def is_expired(self,today=None):
     
        if today is None:
          today = date.today()

        if today > self.calibaration_expiry_date:
            return True

        return False




class Inspection(models.Model):

    job_number = models.CharField(max_length= 50)



    status = models.CharField(max_length=20, choices = [('PENDING_REVIEW','Pending Review'),('IN_PROGRESS','In Progress'),('FROZEN', 'Frozen'),('APPROVED','Approved'),('REJECTED', 'Rejected')])


    created_at = models.DateTimeField(auto_now_add=True)

    inspector = models.ForeignKey(
    "auth.User",
    on_delete=models.PROTECT,
    null=True,
    blank=True,

)

    reviewed_by = models.ForeignKey(
    "auth.User",
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name="reviewed_inspections",
)

    reviewed_at = models.DateTimeField(null=True, blank=True)


    def submit_for_review(self):
        from django.core.exceptions import ValidationError

        if self.status != "IN_PROGRESS":
            raise ValidationError("Only in-progress inspections can be submitted.")

        if self.entries.count() == 0:
            raise ValidationError("Cannot submit an inspection without entries.")

        if self.entries.filter(passed__isnull=True).exists():
            raise ValidationError("All inspection entries must be completed.")

        if self.entries.filter(passed=False, inspection_field__is_ctq=True).exists():
            raise ValidationError("Failed CTQ inspection cannot be submitted.")

        self.status = "PENDING_REVIEW"
        self.save(update_fields=["status"])


    def approve(self,reviewer=None):
        from django.core.exceptions import ValidationError
        from django.utils import timezone


         
        if self.status != "PENDING_REVIEW":
            raise ValidationError("Only pending inspections can be approved.")

        self.status = "APPROVED"
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()
        self.save(update_fields=["status", "reviewed_by", "reviewed_at"])



    
    def reject(self, reviewer=None):
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.status != "PENDING_REVIEW":
            raise ValidationError("Only pending inspections can be rejected.")

        self.status = "REJECTED"
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()
        self.save(update_fields=["status", "reviewed_by", "reviewed_at"])



class InspectionTemplate(models.Model):

    part_number=models.CharField(max_length =50)
    operation_step=models.CharField(max_length =100)
    customer_agreement=models.CharField(max_length =100)
    revision=models.CharField(max_length =10)
    is_approved =models.BooleanField(default =False)



class InspectionField(models.Model):

  
 name = models.CharField(max_length = 100)
 field_type	= models.CharField(max_length =30 ,choices=[('DIMENSION','DIMENSION'),('THRESHOLD','THRESHOLD'),('VISUAL','VISUAL'),('TOOL_LOG','TOOL LOG')])
 

 nominal_value = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
 lower_limit = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
 upper_limit = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
 is_ctq	= models.BooleanField(default=False)
 template = models.ForeignKey(
    InspectionTemplate,
    on_delete=models.CASCADE,
    related_name="fields"
)
    




class InspectionEntry(models.Model):
    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="entries"
    )
    inspection_field = models.ForeignKey(
        InspectionField,
        on_delete=models.CASCADE
    )
    gauge = models.ForeignKey(
        Gauge,
        on_delete=models.PROTECT
    )
    measured_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
    )
    passed = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def clean(self):
        from django.core.exceptions import ValidationError

       

        if self.inspection.status != "IN_PROGRESS":
          raise ValidationError(
        "Inspection entries cannot be changed after submission."
    )

        if self.gauge.is_expired():
               raise ValidationError("Expired Tool Calibration")

        field = self.inspection_field

        if field.field_type == "DIMENSION":
            if self.measured_value is None:
              raise ValidationError("A measured value is required.")

            if not (field.lower_limit <= self.measured_value <= field.upper_limit):
              self.passed = False
            else:
              self.passed = True
    
        


    def save(self, *args, **kwargs):
        self.full_clean()

        field = self.inspection_field

        if field.field_type == "DIMENSION":
            self.passed = (
            field.lower_limit
            <= self.measured_value
            <= field.upper_limit
        )

        failed_ctq = field.is_ctq and self.passed is False

        super().save(*args, **kwargs)

        if failed_ctq:
            self.inspection.status = "FROZEN"
            self.inspection.save(update_fields=["status"])