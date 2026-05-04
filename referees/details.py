from datetime import datetime
from itertools import chain
from django.db.models import Q, Value, CharField
from .jalali import Persian
from .creg import donor_creg_filter, recipient_creg_filter

def parse_number_list_from_string(input_string):
    numbers = []
    if not input_string:
        return numbers

    try:
        cleaned_string = input_string.strip()
        if cleaned_string.startswith('[') and cleaned_string.endswith(']'):
            cleaned_string = cleaned_string[1:-1]

        number_strings = [s.strip() for s in cleaned_string.split(',') if s.strip()]

        for num_str in number_strings:
            numbers.append(int(num_str))
    except ValueError:
        return []
    except Exception:
        return []
    return numbers

def donor_detail(request, donor, main_recipient_list, status):
    blood_group_rejected_list = []
    age_range_rejected_list = []
    hla_uam_rejected_list = []

    recipients_list = main_recipient_list.filter(
        blood_group__in=donor.recipient_blood_group
    )

    if status == 1:
        blood_group_rejected_list = blood_group_rejected(main_recipient_list, recipients_list)

    recipients_list = recipients_list.filter(
        Q(age__gte=donor.min_recipient_age) &
        Q(age__lte=donor.max_recipient_age)
    )

    if status == 1:
        age_range_rejected_list = age_range_rejected(main_recipient_list, recipients_list, blood_group_rejected_list)

    hla_drb_values = [x for x in [donor.hla_drb_1, donor.hla_drb_2] if x]

    conflict_filter = (
        Q(hla_a_uam__in=[donor.hla_a_1, donor.hla_a_2]) |
        Q(hla_b_uam__in=[donor.hla_b_1, donor.hla_b_2]) |
        Q(hla_drb1_uam__in=[donor.hla_drb1_1, donor.hla_drb1_2]) |
        Q(hla_dqb1_uam__in=[donor.hla_dqb1_1, donor.hla_dqb1_2])
    )

    if hla_drb_values:
        conflict_filter |= Q(hla_drb_uam__in=hla_drb_values)

    conflict_recipients = main_recipient_list.filter(conflict_filter).distinct()

    recipients_list = recipients_list.exclude(
        id__in=conflict_recipients.values_list('id', flat=True)
    )

    if status == 1:
        hla_uam_rejected_list = hla_uam_rejected(main_recipient_list, recipients_list, blood_group_rejected_list, age_range_rejected_list)

    recipients_list = recipients_list.order_by('-point')

    donor_hla_a_b_list = [donor.hla_a_1.value, donor.hla_a_2.value, donor.hla_b_1.value, donor.hla_b_2.value]
    donor_creg_filter(donor_hla_a_b_list, recipients_list)

    creg_filter_param = request.GET.get('creg_filter')

    filtered_recipients_list = recipients_list
    now_creg_filter = ''

    if creg_filter_param == "1":
        now_creg_filter = '1'
        filtered_recipients_list = [recipient for recipient in recipients_list if recipient.creg_status == "No CREG"]
    elif creg_filter_param == "2":
        now_creg_filter = '2'
        filtered_recipients_list = [recipient for recipient in recipients_list if recipient.creg_status != "Near CREG"]

    context = {
        'donor': donor,
        'recipients': filtered_recipients_list,
        'now_creg_filter': now_creg_filter,
        'rejected_list': list(chain(blood_group_rejected_list, age_range_rejected_list, hla_uam_rejected_list))
    }

    if status == 0:
        context['rejected_list'] = []

    return context

def recipient_detail(request, recipient, main_cadaver_donor_list, main_living_donor_list, status):
    cadaver_blood_group_rejected_list = []
    living_blood_group_rejected_list = []
    cadaver_age_range_rejected_list = []
    living_age_range_rejected_list = []
    cadaver_hla_uam_rejected_list = []
    living_hla_uam_rejected_list = []

    if recipient.search_donor == '2':
        main_living_donor_list = main_living_donor_list.none()
    elif recipient.search_donor == '3':
        main_cadaver_donor_list = main_cadaver_donor_list.none()

    cadaver_donor_list = main_cadaver_donor_list.filter(
        blood_group__in=recipient.donor_blood_group
    )

    if status == 1:
        cadaver_blood_group_rejected_list = blood_group_rejected(
            main_cadaver_donor_list,
            cadaver_donor_list
        )

    living_donor_list = main_living_donor_list.filter(
        blood_group__in=recipient.donor_blood_group
    )

    if status == 1:
        living_blood_group_rejected_list = blood_group_rejected(
            main_living_donor_list,
            living_donor_list
        )

    cadaver_donor_list = cadaver_donor_list.filter(
        Q(age__gte=recipient.min_donor_age) &
        Q(age__lte=recipient.max_donor_age)
    )

    if status == 1:
        cadaver_age_range_rejected_list = age_range_rejected(
            main_cadaver_donor_list,
            cadaver_donor_list,
            cadaver_blood_group_rejected_list
        )

    living_donor_list = living_donor_list.filter(
        Q(age__gte=recipient.min_donor_age) &
        Q(age__lte=recipient.max_donor_age)
    )

    if status == 1:
        living_age_range_rejected_list = age_range_rejected(
            main_living_donor_list,
            living_donor_list,
            living_blood_group_rejected_list
        )

    cadaver_donor_list = cadaver_donor_list.exclude(
        Q(hla_a_1__in=recipient.hla_a_uam.all()) |
        Q(hla_a_2__in=recipient.hla_a_uam.all()) |
        Q(hla_b_1__in=recipient.hla_b_uam.all()) |
        Q(hla_b_2__in=recipient.hla_b_uam.all()) |
        Q(hla_drb1_1__in=recipient.hla_drb1_uam.all()) |
        Q(hla_drb1_2__in=recipient.hla_drb1_uam.all()) |
        Q(hla_drb_1__in=recipient.hla_drb_uam.all()) |
        Q(hla_drb_2__in=recipient.hla_drb_uam.all()) |
        Q(hla_dqb1_1__in=recipient.hla_dqb1_uam.all()) |
        Q(hla_dqb1_2__in=recipient.hla_dqb1_uam.all())
    )

    if status == 1:
        cadaver_hla_uam_rejected_list = hla_uam_rejected(
            main_cadaver_donor_list,
            cadaver_donor_list,
            cadaver_blood_group_rejected_list,
            cadaver_age_range_rejected_list
        )

    living_donor_list = living_donor_list.exclude(
        Q(hla_a_1__in=recipient.hla_a_uam.all()) |
        Q(hla_a_2__in=recipient.hla_a_uam.all()) |
        Q(hla_b_1__in=recipient.hla_b_uam.all()) |
        Q(hla_b_2__in=recipient.hla_b_uam.all()) |
        Q(hla_drb1_1__in=recipient.hla_drb1_uam.all()) |
        Q(hla_drb1_2__in=recipient.hla_drb1_uam.all()) |
        Q(hla_drb_1__in=recipient.hla_drb_uam.all()) |
        Q(hla_drb_2__in=recipient.hla_drb_uam.all()) |
        Q(hla_dqb1_1__in=recipient.hla_dqb1_uam.all()) |
        Q(hla_dqb1_2__in=recipient.hla_dqb1_uam.all())
    )

    if status == 1:
        living_hla_uam_rejected_list = hla_uam_rejected(
            main_living_donor_list,
            living_donor_list,
            living_blood_group_rejected_list,
            living_age_range_rejected_list
        )

    donors_list = list(chain(cadaver_donor_list, living_donor_list))

    recipient_hla_a_b_uams = [hla.value for hla in recipient.hla_a_uam.all()] + \
        [hla.value for hla in recipient.hla_b_uam.all()]
    
    recipient_creg_filter(recipient_hla_a_b_uams, donors_list)

    creg_filter_param = request.GET.get('creg_filter')

    filtered_donors_list = donors_list
    now_creg_filter = ''

    if creg_filter_param == "1":
        now_creg_filter = '1'
        filtered_donors_list = [donor for donor in donors_list if donor.creg_status == "No CREG"]
    elif creg_filter_param == "2":
        now_creg_filter = '2'
        filtered_donors_list = [donor for donor in donors_list if donor.creg_status != "Near CREG"]

    recipient_hla_uams = list(chain(
        recipient.hla_a_uam.all(),
        recipient.hla_b_uam.all(),
        recipient.hla_drb1_uam.all(),
        recipient.hla_drb_uam.all(),
        recipient.hla_dqb1_uam.all(),
    ))

    if recipient_hla_uams:
        is_recipient_hla_uams = True
    else:
        is_recipient_hla_uams = False

    if all(value is not None for value in [
        recipient.waiting_list,
        recipient.dialysis_duration,
        recipient.age,
        recipient.previous_donation,
        recipient.medical_urgency,
        recipient.candidate_for_2_kidney_TX,
        recipient.candidate_for_kidney_after_other_organ_TX,
        recipient.cpra,
        recipient.desensitized
    ]):
        if isinstance(recipient.waiting_list, str):
            try:
                waiting_list_date = Persian(recipient.waiting_list).gregorian_datetime()
                now_date = datetime.now().date()
                delta_days = (now_date - waiting_list_date).days
                waiting_list_p = round((delta_days / 365), 2)
            except:
                pass
            
        if isinstance(recipient.dialysis_duration, str):
            try:
                dialysis_duration_date = Persian(recipient.dialysis_duration).gregorian_datetime()
                now_date = datetime.now().date()
                delta_days = (now_date - dialysis_duration_date).days
                dialysis_duration_p = (delta_days / 365)
            except:
                pass

        dialysis_duration_p = round((dialysis_duration_p * 0.5), 2)
        age = recipient.age
        previous_donation = recipient.previous_donation
        medical_urgency = recipient.medical_urgency
        candidate_for_2_kidney_TX = recipient.candidate_for_2_kidney_TX
        candidate_for_kidney_after_other_organ_TX = recipient.candidate_for_kidney_after_other_organ_TX
        cpra = recipient.cpra
        desensitized = recipient.desensitized

        if 0 <= age <= 10:
            age_p = 4
        elif 11 <= age <= 17:
            age_p = 3
        else:
            age_p = 0
            
        if previous_donation == 'yes':
            previous_donation_p = 3
        else:
            previous_donation_p = 0
        
        if medical_urgency == '3':
            medical_urgency_p = 0
        else:
            medical_urgency_p = 3
            
        if candidate_for_2_kidney_TX == 'yes':
            candidate_for_2_kidney_TX_p = 2
        else:
            candidate_for_2_kidney_TX_p = 0

        if candidate_for_kidney_after_other_organ_TX == 'yes':
            candidate_for_kidney_after_other_organ_TX_p = 2
        else:
            candidate_for_kidney_after_other_organ_TX_p = 0

        if cpra == '1':
            cpra_p = 10
        elif cpra == '2':
            cpra_p = 4
        else:
            cpra_p = 0

        if desensitized == 'yes':
            desensitized_p = 10
        else:
            desensitized_p = 0
    else:
        waiting_list_p = 0
        dialysis_duration_p = 0
        age_p = 0
        previous_donation_p = 0
        medical_urgency_p = 0
        candidate_for_2_kidney_TX_p = 0
        candidate_for_kidney_after_other_organ_TX_p = 0
        cpra_p = 0
        desensitized_p = 0

    context = {
        'recipient': recipient,
        'recipient_hla_uams': recipient_hla_uams,
        'is_recipient_hla_uams': is_recipient_hla_uams,
        'now_creg_filter': now_creg_filter,
        'donors': filtered_donors_list,
        'rejected_list': list(chain(
            cadaver_blood_group_rejected_list, living_blood_group_rejected_list,
            cadaver_age_range_rejected_list, living_age_range_rejected_list,
            cadaver_hla_uam_rejected_list, living_hla_uam_rejected_list
        )),
        'waiting_list_p': waiting_list_p,
        'dialysis_duration_p': dialysis_duration_p,
        'age_p': age_p,
        'previous_donation_p': previous_donation_p,
        'medical_urgency_p': medical_urgency_p,
        'candidate_for_2_kidney_TX_p': candidate_for_2_kidney_TX_p,
        'candidate_for_kidney_after_other_organ_TX_p': candidate_for_kidney_after_other_organ_TX_p,
        'cpra_p': cpra_p,
        'desensitized_p': desensitized_p,
    }

    if status == 0:
        context['rejected_list'] = []

    return context

def notification_maker(condition):
    condition_dict = {
        'blood_group': 'Rejected due to blood group incompatibility',
        'age_range': 'Rejected due to being outside the eligible age range for transplantation',
        'hla_uam': 'Rejected due to incompatible HLA UAM antigens'
    }

    return condition_dict[condition]

def blood_group_rejected(main_list, accepted_list_1):
    return main_list.exclude(
        id__in=accepted_list_1.values_list('id', flat=True)
    ).annotate(
        reason_for_rejection=Value(
            notification_maker('blood_group'),
            output_field=CharField()
        )
    )

def age_range_rejected(main_list, accepted_list_1, accepted_list_2):
    return main_list.exclude(
        id__in=accepted_list_1.values_list('id', flat=True)
    ).exclude(
        id__in=accepted_list_2.values_list('id', flat=True)
    ).annotate(
        reason_for_rejection=Value(
            notification_maker('age_range'),
            output_field=CharField()
        )
    )

def hla_uam_rejected(main_list, accepted_list_1, accepted_list_2, accepted_list_3):
    return main_list.exclude(
        id__in=accepted_list_1.values_list('id', flat=True)
    ).exclude(
        id__in=accepted_list_2.values_list('id', flat=True)
    ).exclude(
        id__in=accepted_list_3.values_list('id', flat=True)
    ).annotate(
        reason_for_rejection=Value(
            notification_maker('hla_uam'),
            output_field=CharField()
        )
    )
