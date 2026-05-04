from collections import Counter

def analysis_recipients(recipients):
    def clean_dict(d):
        return {k: v for k, v in d.items() if v not in [0, None, '', '0']}

    gender_status = Counter(rec.get_gender_display() for rec in recipients)
    age_status = {
        'under_20': recipients.filter(age__lt=20).count(),
        '20_40': recipients.filter(age__gte=20, age__lt=40).count(),
        '40_60': recipients.filter(age__gte=40, age__lt=60).count(),
        '60_80': recipients.filter(age__gte=60, age__lt=80).count(),
        'above_80': recipients.filter(age__gte=80).count(),
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
        "gender_status": clean_dict(dict(gender_status)),
        "age_status": clean_dict(age_status),
        "blood_group_status": clean_dict(dict(blood_group_status)),
        "previous_donation": clean_dict(dict(previous_donation)),
        "medical_urgency": clean_dict(dict(medical_urgency)),
        "candidate_for_2_kidney_TX": clean_dict(dict(candidate_for_2_kidney_TX)),
        "candidate_for_kidney_after_other_organ_TX": clean_dict(dict(candidate_for_kidney_after_other_organ_TX)),
        "cpra": clean_dict(dict(cpra)),
        "desensitized": clean_dict(dict(desensitized)),
        "hla_a": clean_dict(dict(hla_a)),
        "hla_b": clean_dict(dict(hla_b)),
        "hla_drb1": clean_dict(dict(hla_drb1)),
        "hla_drb": clean_dict(dict(hla_drb)),
        "hla_dqb1": clean_dict(dict(hla_dqb1)),
        "hla_a_uam": clean_dict(dict(hla_a_uam)),
        "hla_b_uam": clean_dict(dict(hla_b_uam)),
        "hla_drb1_uam": clean_dict(dict(hla_drb1_uam)),
        "hla_drb_uam": clean_dict(dict(hla_drb_uam)),
        "hla_dqb1_uam": clean_dict(dict(hla_dqb1_uam)),
    }
