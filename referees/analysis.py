import re
from collections import Counter
from datetime import datetime
from .jalali import Persian

def field_to_date(field):
    if isinstance(field, str):
        try:
            field_date = Persian(field).gregorian_datetime()
            now_date = datetime.now().date()
            diff_in_months = (now_date.year - field_date.year) * 12 + (now_date.month - field_date.month)

            return diff_in_months
        except:
            return None
        
def average_numbers(items):
    numbers = [x for x in items if x is not None]
    
    if not numbers:
        return None
    
    years = sum(numbers) // 12
    months = sum(numbers) % 12

    return f"{years} years and {months} months"

def format_counts_with_percent(data):
    total = sum(data.values())
    return {
        key: f'{value} ({value / total * 100:.0f}%)'
        for key, value in data.items()
    }

def analysis_recipients(recipients):
    def clean_dict(d):
        return {k: v for k, v in d.items() if v not in [0, None, '', '0']}
    
    waiting_list = [field_to_date(rec.waiting_list) for rec in recipients]
    waiting_list_status = average_numbers(waiting_list)

    dialysis_duration = [field_to_date(rec.dialysis_duration) for rec in recipients]
    dialysis_duration_status = average_numbers(dialysis_duration)

    gender_status = Counter(rec.get_gender_display() for rec in recipients)
    age_status = {
        'کمتر از 20 سال': recipients.filter(age__lt=20).count(),
        '20 تا 40 سال': recipients.filter(age__gte=20, age__lt=40).count(),
        '40 تا 60 سال': recipients.filter(age__gte=40, age__lt=60).count(),
        '60 تا 80 سال': recipients.filter(age__gte=60, age__lt=80).count(),
        'بیش از 80 سال': recipients.filter(age__gte=80).count(),
    }
    blood_group_status = Counter(recipients.values_list('blood_group', flat=True))
    previous_donation = Counter(rec.get_previous_donation_display() for rec in recipients)
    medical_urgency = Counter(rec.get_medical_urgency_display() for rec in recipients)
    candidate_for_2_kidney_TX = Counter(rec.get_candidate_for_2_kidney_TX_display() for rec in recipients)
    candidate_for_kidney_after_other_organ_TX = Counter(rec.get_candidate_for_kidney_after_other_organ_TX_display() for rec in recipients)
    cpra = Counter(rec.get_cpra_display() for rec in recipients)
    desensitized = Counter(rec.get_desensitized_display() for rec in recipients)

    hla_a = Counter([r.hla_a_1.value for r in recipients] + [r.hla_a_2.value for r in recipients])
    hla_b = Counter([r.hla_b_1.value for r in recipients] + [r.hla_b_2.value for r in recipients])
    hla_drb1 = Counter([r.hla_drb1_1.value for r in recipients] + [r.hla_drb1_2.value for r in recipients])
    hla_drb = Counter(
        [r.hla_drb_1.value for r in recipients if r.hla_drb_1] +
        [r.hla_drb_2.value for r in recipients if r.hla_drb_2]
    )
    hla_dqb1 = Counter([r.hla_dqb1_1.value for r in recipients] + [r.hla_dqb1_2.value for r in recipients])

    def count_m2m(recipients, field):
        c = Counter()
        for rec in recipients:
            for allele in getattr(rec, field).all():
                c[allele.value] += 1
        return c

    hla_a_uam = count_m2m(recipients, 'hla_a_uam')
    hla_b_uam = count_m2m(recipients, 'hla_b_uam')
    hla_drb1_uam = count_m2m(recipients, 'hla_drb1_uam')
    hla_drb_uam = count_m2m(recipients, 'hla_drb_uam')
    hla_dqb1_uam = count_m2m(recipients, 'hla_dqb1_uam')

    return {
        "waiting_list_status": waiting_list_status,
        "dialysis_duration_status": dialysis_duration_status,
        "gender_status": format_counts_with_percent(clean_dict(dict(gender_status))),
        "age_status": format_counts_with_percent(clean_dict(age_status)),
        "blood_group_status": format_counts_with_percent(clean_dict(dict(blood_group_status))),
        "previous_donation": format_counts_with_percent(clean_dict(dict(previous_donation))),
        "medical_urgency": format_counts_with_percent(clean_dict(dict(medical_urgency))),
        "candidate_for_2_kidney_TX": format_counts_with_percent(clean_dict(dict(candidate_for_2_kidney_TX))),
        "candidate_for_kidney_after_other_organ_TX": format_counts_with_percent(clean_dict(dict(candidate_for_kidney_after_other_organ_TX))),
        "cpra": format_counts_with_percent(clean_dict(dict(cpra))),
        "desensitized": format_counts_with_percent(clean_dict(dict(desensitized))),
        "hla_a": format_counts_with_percent(clean_dict(dict(hla_a))),
        "hla_b": format_counts_with_percent(clean_dict(dict(hla_b))),
        "hla_drb1": format_counts_with_percent(clean_dict(dict(hla_drb1))),
        "hla_drb": format_counts_with_percent(clean_dict(dict(hla_drb))),
        "hla_dqb1": format_counts_with_percent(clean_dict(dict(hla_dqb1))),
        "hla_a_uam": format_counts_with_percent(clean_dict(dict(hla_a_uam))),
        "hla_b_uam": format_counts_with_percent(clean_dict(dict(hla_b_uam))),
        "hla_drb1_uam": format_counts_with_percent(clean_dict(dict(hla_drb1_uam))),
        "hla_drb_uam": format_counts_with_percent(clean_dict(dict(hla_drb_uam))),
        "hla_dqb1_uam": format_counts_with_percent(clean_dict(dict(hla_dqb1_uam))),
    }

def analysis_donors(donors):
    def clean_dict(d):
        return {k: v for k, v in d.items() if v not in [0, None, '', '0']}

    gender_status = Counter(rec.get_gender_display() for rec in donors)
    age_status = {
        'کمتر از 20 سال': donors.filter(age__lt=20).count(),
        '20 تا 40 سال': donors.filter(age__gte=20, age__lt=40).count(),
        '40 تا 60 سال': donors.filter(age__gte=40, age__lt=60).count(),
        '60 تا 80 سال': donors.filter(age__gte=60, age__lt=80).count(),
        'بیش از 80 سال': donors.filter(age__gte=80).count(),
    }
    blood_group_status = Counter(donors.values_list('blood_group', flat=True))

    hla_a = Counter([r.hla_a_1.value for r in donors] + [r.hla_a_2.value for r in donors])
    hla_b = Counter([r.hla_b_1.value for r in donors] + [r.hla_b_2.value for r in donors])
    hla_drb1 = Counter([r.hla_drb1_1.value for r in donors] + [r.hla_drb1_2.value for r in donors])
    hla_drb = Counter(
        [r.hla_drb_1.value for r in donors if r.hla_drb_1] +
        [r.hla_drb_2.value for r in donors if r.hla_drb_2]
    )
    hla_dqb1 = Counter([r.hla_dqb1_1.value for r in donors] + [r.hla_dqb1_2.value for r in donors])

    return {
        "gender_status": format_counts_with_percent(clean_dict(dict(gender_status))),
        "age_status": format_counts_with_percent(clean_dict(age_status)),
        "blood_group_status": format_counts_with_percent(clean_dict(dict(blood_group_status))),
        "hla_a": format_counts_with_percent(clean_dict(dict(hla_a))),
        "hla_b": format_counts_with_percent(clean_dict(dict(hla_b))),
        "hla_drb1": format_counts_with_percent(clean_dict(dict(hla_drb1))),
        "hla_drb": format_counts_with_percent(clean_dict(dict(hla_drb))),
        "hla_dqb1": format_counts_with_percent(clean_dict(dict(hla_dqb1))),
    }

def parse_value(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        match = re.match(r'^\s*([+-]?\d+(?:\.\d+)?)', value)
        if match:
            num = match.group(1)
            return float(num) if '.' in num else int(num)
    return 0

def merge_analysis_results(result1, result2):
    merged = {}

    all_keys = set(result1.keys()) | set(result2.keys())

    for key in all_keys:
        dict1 = result1.get(key, {})
        dict2 = result2.get(key, {})

        parsed_dict1 = {k: parse_value(v) for k, v in dict1.items()}
        parsed_dict2 = {k: parse_value(v) for k, v in dict2.items()}

        counter = Counter(parsed_dict1) + Counter(parsed_dict2)

        total = sum(counter.values())

        merged[key] = {
            k: f"{v} ({round((v / total) * 100)}%)" if total else f"{v} (0%)"
            for k, v in counter.items()
            if v not in [0, None, '', '0']
        }

    return merged
