from django.db import models
from multiselectfield import MultiSelectField

class HlaA(models.Model):
    type_choices = [
        ('1', 'COMMON'),
        ('2', 'INTERMEDIATE'),
        ('3', 'UNCOMMON'),
    ]

    value = models.CharField(verbose_name='HLA A', max_length=20, unique=True)
    type = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.value

class HlaB(models.Model):
    type_choices = [
        ('1', 'COMMON'),
        ('2', 'INTERMEDIATE'),
        ('3', 'UNCOMMON'),
    ]

    value = models.CharField(verbose_name='HLA B', max_length=20, unique=True)
    type = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.value

class HlaDRB1(models.Model):
    type_choices = [
        ('1', 'COMMON'),
        ('2', 'INTERMEDIATE'),
        ('3', 'UNCOMMON'),
    ]

    value = models.CharField(verbose_name='HLA DRB1', max_length=20, unique=True)
    type = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.value

class HlaDRB(models.Model):
    value = models.CharField(verbose_name='HLA DRB', max_length=20, unique=True)

    def __str__(self):
        return self.value

class HlaDQB1(models.Model):
    type_choices = [
        ('1', 'COMMON'),
        ('2', 'INTERMEDIATE'),
        ('3', 'UNCOMMON'),
    ]

    value = models.CharField(verbose_name='HLA DQB1', max_length=20, unique=True)
    type = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return self.value

class Donor(models.Model):
    blood_group_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    status_choices = [
        ('1', 'Cadaver Donor'),
        ('2', 'Living Donor'),
    ]

    first_name = models.CharField(verbose_name='نام', max_length=100)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=100)
    national_code = models.IntegerField(verbose_name='کد ملی')
    phone_number = models.IntegerField(verbose_name='شماره تماس')
    age = models.IntegerField(verbose_name='سن')
    blood_group = models.CharField(verbose_name='گروه خونی', max_length=2, choices=blood_group_choices)
    recipient_blood_group = MultiSelectField(verbose_name='گروه خونی مناسب برای گیرنده', help_text='این مقدار توسط سیستیم تعین می گردد', max_length=2, choices=blood_group_choices)
    min_recipient_age = models.IntegerField(verbose_name='حداقل سن مناسب برای گیرنده', help_text='این مقدار توسط سیستیم تعین می گردد')
    max_recipient_age = models.IntegerField(verbose_name='حداکثر سن مناسب برای گیرنده', help_text='این مقدار توسط سیستیم تعین می گردد')
    status = models.CharField(verbose_name='وضعیت', max_length=1, choices=status_choices, help_text='این مقدار توسط سیستیم تعین می گردد')

    hla_a_1 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 1)', related_name='hla_a_1_%(class)s')
    hla_a_2 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 2)', related_name='hla_a_2_%(class)s')
    hla_b_1 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 1)', related_name='hla_b_1_%(class)s')
    hla_b_2 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 2)', related_name='hla_b_2_%(class)s')
    hla_drb1_1 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 1)', related_name='hla_drb1_1_%(class)s')
    hla_drb1_2 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 2)', related_name='hla_drb1_2_%(class)s')
    hla_drb_1 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 1)', null=True, blank=True, related_name='hla_drb_1_%(class)s')
    hla_drb_2 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 2)', null=True, blank=True, related_name='hla_drb_2_%(class)s')
    hla_dqb1_1 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 1)', related_name='hla_dqb1_1_%(class)s')
    hla_dqb1_2 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 2)', related_name='hla_dqb1_2_%(class)s')

    class Meta:
        verbose_name = 'اهدا کننده'
        verbose_name_plural = 'اهدا کنندگان'
        abstract = True

    def __str__(self):
        return f'اهدا کننده {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        compatibility_map = {
            'A': ['A', 'AB'],
            'B': ['B', 'AB'],
            'AB': ['AB'],
            'O': ['O', 'A', 'B', 'AB'],
        }
        self.recipient_blood_group = list(compatibility_map.get(self.blood_group, []))

        super().save(*args, **kwargs)

class CadaverDonor(Donor):
    kdpi = models.FloatField(verbose_name='KDPI', help_text='عددی بین 0 تا 100')

    class Meta:
        verbose_name = 'اهدا کننده مرگ مغزی'
        verbose_name_plural = 'اهدا کنندگان مرگ مغزی'

    def __str__(self):
        return f'اهدا کننده مرگ مغزی {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.status = '1'

        if self.kdpi <= 20:
            self.min_recipient_age = 0
            self.max_recipient_age = self.age
        elif 21 <= self.kdpi <= 75:
            if self.age < 25:
                self.min_recipient_age = 30
                self.max_recipient_age = 200
            else:
                self.min_recipient_age = self.age + 5
                self.max_recipient_age = 200
        else:
            self.min_recipient_age = self.age + 10
            self.max_recipient_age = 200

        super().save(*args, **kwargs)

class LivingDonor(Donor):
    class Meta:
        verbose_name = 'اهدا کننده زنده'
        verbose_name_plural = 'اهدا کنندگان زنده'

    def __str__(self):
        return f'اهدا کننده زنده {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.status = '2'

        self.min_recipient_age = self.age - 10
        self.max_recipient_age = 200

        super().save(*args, **kwargs)

class Recipient(models.Model):
    blood_group_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    previous_donation_candidate_choices = [
        ('yes', 'YES'),
        ('no', 'NO'),
    ]

    medical_urgency_choices = [
        ('1', 'no access'),
        ('2', 'cardiomyopathy'),
        ('3', 'none'),
    ]

    cpra_choices = [
        ('1', '≥ 98%'),
        ('2', '95-97%'),
        ('3', 'none'),
    ]

    first_name = models.CharField(verbose_name='نام', max_length=100)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=100)
    national_code = models.IntegerField(verbose_name='کد ملی')
    phone_number = models.IntegerField(verbose_name='شماره تماس')
    age = models.IntegerField(verbose_name='سن')
    blood_group = models.CharField(verbose_name='گروه خونی', max_length=2, choices=blood_group_choices)
    waiting_list = models.CharField(max_length=10)
    dialysis_duration = models.CharField(max_length=10)
    previous_donation = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    medical_urgency = models.CharField(max_length=1, choices=medical_urgency_choices)
    candidate_for_2_kidney_TX = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    candidate_for_kidney_after_other_organ_TX = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    cpra = models.CharField(max_length=1, choices=cpra_choices)
    desensitized = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    hla_a_1 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 1)', related_name='hla_a_1_recipient')
    hla_a_2 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 2)', related_name='hla_a_2_recipient')
    hla_b_1 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 1)', related_name='hla_b_1_recipient')
    hla_b_2 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 2)', related_name='hla_b_2_recipient')
    hla_drb1_1 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 1)', related_name='hla_drb1_1_recipient')
    hla_drb1_2 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 2)', related_name='hla_drb1_2_recipient')
    hla_drb_1 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 1)', null=True, blank=True, related_name='hla_drb_1_recipient')
    hla_drb_2 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 2)', null=True, blank=True, related_name='hla_drb_2_recipient')
    hla_dqb1_1 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 1)', related_name='hla_dqb1_1_recipient')
    hla_dqb1_2 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 2)', related_name='hla_dqb1_2_recipient')
    point = models.FloatField(verbose_name='امتیاز')

    donor_blood_group = MultiSelectField(verbose_name='گروه خونی مناسب برای دهنده', help_text='این مقدار توسط سیستیم تعین می گردد', max_length=2, choices=blood_group_choices)
    min_donor_age = models.IntegerField(verbose_name='حداقل سن مناسب برای دهنده', help_text='این مقدار توسط سیستیم تعین می گردد', default=0)
    max_donor_age = models.IntegerField(verbose_name='حداکثر سن مناسب برای دهنده', help_text='این مقدار توسط سیستیم تعین می گردد')

    class Meta:
        verbose_name = 'گیرنده'
        verbose_name_plural = 'گیرندگان'
    
    def __str__(self):
        return f'گیرنده {self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        compatibility_map = {
            'A': ['O', 'A'],
            'B': ['O', 'B'],
            'AB': ['O', 'A', 'B', 'AB'],
            'O': ['O'],
        }
        self.donor_blood_group = list(compatibility_map.get(self.blood_group, []))

        self.max_donor_age = self.age + 10

        super().save(*args, **kwargs)

class DonorTest(models.Model):
    first_name = models.CharField(verbose_name='نام', max_length=100)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=100)
    hla_a_1 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 1)', related_name='hla_a_1_donor_test')
    hla_a_2 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 2)', related_name='hla_a_2_donor_test')
    hla_b_1 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 1)', related_name='hla_b_1_donor_test')
    hla_b_2 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 2)', related_name='hla_b_2_donor_test')
    hla_drb1_1 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 1)', related_name='hla_drb1_1_donor_test')
    hla_drb1_2 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 2)', related_name='hla_drb1_2_donor_test')
    hla_drb_1 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 1)', null=True, blank=True, related_name='hla_drb_1_donor_test')
    hla_drb_2 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 2)', null=True, blank=True, related_name='hla_drb_2_donor_test')
    hla_dqb1_1 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 1)', related_name='hla_dqb1_1_donor_test')
    hla_dqb1_2 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 2)', related_name='hla_dqb1_2_donor_test')

    class Meta:
        verbose_name = 'اهدا کننده تستی'
        verbose_name_plural = 'اهدا کنندگان تستی'

class RecipientTest(models.Model):
    first_name = models.CharField(verbose_name='نام', max_length=100)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=100)
    hla_a_1 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 1)', related_name='hla_a_1_recipient_test')
    hla_a_2 = models.ForeignKey(HlaA, on_delete=models.DO_NOTHING, verbose_name='HLA A (allele 2)', related_name='hla_a_2_recipient_test')
    hla_b_1 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 1)', related_name='hla_b_1_recipient_test')
    hla_b_2 = models.ForeignKey(HlaB, on_delete=models.DO_NOTHING, verbose_name='HLA B (allele 2)', related_name='hla_b_2_recipient_test')
    hla_drb1_1 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 1)', related_name='hla_drb1_1_recipient_test')
    hla_drb1_2 = models.ForeignKey(HlaDRB1, on_delete=models.DO_NOTHING, verbose_name='HLA DRB1 (allele 2)', related_name='hla_drb1_2_recipient_test')
    hla_drb_1 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 1)', null=True, blank=True, related_name='hla_drb_1_recipient_test')
    hla_drb_2 = models.ForeignKey(HlaDRB, on_delete=models.DO_NOTHING, verbose_name='HLA DRB (allele 2)', null=True, blank=True, related_name='hla_drb_2_recipient_test')
    hla_dqb1_1 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 1)', related_name='hla_dqb1_1_recipient_test')
    hla_dqb1_2 = models.ForeignKey(HlaDQB1, on_delete=models.DO_NOTHING, verbose_name='HLA DQB1 (allele 2)', related_name='hla_dqb1_2_recipient_test')

    class Meta:
        verbose_name = 'گیرنده تستی'
        verbose_name_plural = 'گیرندگان تستی'
