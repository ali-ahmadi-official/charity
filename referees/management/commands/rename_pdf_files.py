import uuid
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from referees.models import CadaverDonor, LivingDonor, Recipient, HistoryCall

class Command(BaseCommand):
    help = "Rename existing PDF files to ASCII UUID filenames"

    def rename_file(self, file_field, folder):
        if not file_field:
            return None

        old_name = file_field.name

        if not old_name:
            return None

        old_path = Path(file_field.path)

        if not old_path.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"File not found: {old_path}"
                )
            )
            return None

        extension = old_path.suffix.lower()

        new_filename = f"{uuid.uuid4().hex}{extension}"
        new_name = f"{folder}/{new_filename}"

        new_path = old_path.parent / new_filename

        old_path.rename(new_path)

        return new_name

    @transaction.atomic
    def handle(self, *args, **options):

        # -------------------------
        # Recipient
        # -------------------------

        for obj in Recipient.objects.all():

            changed = False

            for field_name in [
                "pcr_based_pdf",
                "class_i_pdf",
                "class_ii_pdf",
            ]:

                field = getattr(obj, field_name)

                if field:
                    new_name = self.rename_file(
                        field,
                        "recipient_pdf"
                    )

                    if new_name:
                        setattr(obj, field_name, new_name)
                        changed = True

            if changed:
                obj.save(
                    update_fields=[
                        "pcr_based_pdf",
                        "class_i_pdf",
                        "class_ii_pdf",
                    ]
                )

        # -------------------------
        # HistoryCall
        # -------------------------

        for obj in HistoryCall.objects.all():

            changed = False

            for field_name in [
                "class_i_pdf",
                "class_ii_pdf",
            ]:

                field = getattr(obj, field_name)

                if field:
                    new_name = self.rename_file(
                        field,
                        "recipient_pdf"
                    )

                    if new_name:
                        setattr(obj, field_name, new_name)
                        changed = True

            if changed:
                obj.save(
                    update_fields=[
                        "class_i_pdf",
                        "class_ii_pdf",
                    ]
                )

        # -------------------------
        # Donors
        # -------------------------
        
        for DonorModel in [CadaverDonor, LivingDonor]:
        
            for obj in DonorModel.objects.all():
        
                if obj.pcr_based_pdf:
        
                    new_name = self.rename_file(
                        obj.pcr_based_pdf,
                        "donor_pdf"
                    )
        
                    if new_name:
                        obj.pcr_based_pdf = new_name
                        obj.save(
                            update_fields=["pcr_based_pdf"]
                        )

        self.stdout.write(
            self.style.SUCCESS(
                "All PDF files renamed successfully."
            )
        )