from django.db import models
from multiselectfield import MultiSelectField

class Donor(models.Model):
    blood_group_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    first_name = models.CharField(verbose_name='نام', max_length=100)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=100)
    national_code = models.IntegerField(verbose_name='کد ملی')
    phone_number = models.IntegerField(verbose_name='شماره تماس')
    age = models.IntegerField(verbose_name='سن')
    blood_group = models.CharField(verbose_name='گروه خونی', max_length=2, choices=blood_group_choices)
    kdpi = models.FloatField(verbose_name='KDPI', help_text='عددی بین 0 تا 100')
    recipient_blood_group = MultiSelectField(verbose_name='گروه خونی مناسب برای گیرنده', help_text='این مقدار توسط سیستیم تعین می گردد', max_length=2, choices=blood_group_choices)
    min_recipient_age = models.IntegerField(verbose_name='حداقل سن مناسب برای گیرنده', help_text='این مقدار توسط سیستیم تعین می گردد')
    max_recipient_age = models.IntegerField(verbose_name='حداکثر سن مناسب برای گیرنده', help_text='این مقدار توسط سیستیم تعین می گردد')

    class Meta:
        verbose_name = 'اهدا کننده'
        verbose_name_plural = 'اهدا کنندگان'

    def __str__(self):
        return f'اهدا کننده {self.first_name} {self.last_name}'

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
    ]

    cpra_choices = [
        ('1', '≥ 98%'),
        ('2', '95-97%'),
        ('3', 'desensitized'),
    ]

    first_name = models.CharField(verbose_name='نام', max_length=100)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=100)
    national_code = models.IntegerField(verbose_name='کد ملی')
    phone_number = models.IntegerField(verbose_name='شماره تماس')
    age = models.IntegerField(verbose_name='سن')
    blood_group = models.CharField(verbose_name='گروه خونی', max_length=2, choices=blood_group_choices)
    waiting_list = models.IntegerField(help_text='by year')
    dialysis_duration = models.IntegerField(help_text='by year')
    previous_donation = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    medical_urgency = models.CharField(max_length=1, choices=medical_urgency_choices)
    candidate_for_2_kidney_TX = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    candidate_for_kidney_after_other_organ_TX = models.CharField(max_length=3, choices=previous_donation_candidate_choices)
    cpra = models.CharField(max_length=1, choices=cpra_choices)
    point = models.FloatField(verbose_name='امتیاز')

    class Meta:
        verbose_name = 'گیرنده'
        verbose_name_plural = 'گیرندگان'
    
    def __str__(self):
        return f'گیرنده {self.first_name} {self.last_name}'
