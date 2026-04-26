creg_dict = {
    "A1C": ["A*01", "A*03", "A*11", "A*19", "A*36", "A*80", ["A*29", "A*30", "A*31"]],
    "A2": ["A*02", "A*09", "A*28", "B*17", ["A*23", "A*24"], ["A*68", "A*69"], ["B*57", "B*58"]],
    "A10C": ["A*10", "A*32", "A*33", "A*43", "A*74", ["A*25", "A*26", "A*34", "A*66"]],
    "BW4": ["A*09", "A*25", "A*32", "B*13", "B*27", "B*37", "B*38", "B*44", "B*47", "B*49", "B*51", "B*52", "B*53", "B*57", "B*58", "B*59", "B*63", "B*67", ["A*23", "A*24"]],
    "B5C": ["B*05", "B*18", "B*35", "B*53", ["B*51", "B*52"]],
    "B5C2": ["B*05", "B*15", "B*17", "B*21", "B*35", "B*53", "B*73", "B*78", ["B*51", "B*52"], ["B*62", "B*63", "B*71", "B*72", "B*75", "B*76", "B*77"], ["B*57", "B*58"], ["B*49", "B*50"]],
    "BW6": ["B*07", "B*08", "B*14", "B*18", "B*35", "B*39", "B*40", "B*41", "B*42", "B*45", "B*46", "B*48", "B*50", "B*54", "B*55", "B*56", "B*62", "B*64", "B*65", "B*67", "B*71", "B*72", "B*73", "B*75", "B*76", ["B*60", "B*61"]],
    "B7C": ["B*07", "B*08", "B*13", "B*27", "B*41", "B*42", "B*47", "B*48", "B*54", "B*55", "B*56", "B*60", "B*61", "B*81"],
    "B8C": ["B*08", "B*18", "B*38", "B*39", "B*64", "B*65"],
    "B12C": ["B*12", "B*13", "B*37", "B*41", "B*47", "B*21", "B*40", "B*60", "B*61", ["B*44", "B*45"], ["B*49", "B*50"]]
}

def find_creg_matches(recipient_hla_list, donor_hla_list):
    all_alleles = set()
    for v in creg_dict.values():
        for x in v:
            if isinstance(x, list):
                all_alleles.update(x)
            else:
                all_alleles.add(x)
    r = [x for x in list(dict.fromkeys(recipient_hla_list)) if x in all_alleles]
    d = [x for x in list(dict.fromkeys(donor_hla_list)) if x in all_alleles]
    near_creg_list, creg_list = [], []

    for key, alleles in creg_dict.items():
        suballeles = [x for x in alleles if isinstance(x, list)]

        for ra in r[:]:
            for da in d[:]:
                if ra in alleles and da in alleles:
                    creg_list.append({"recipient": ra, "donor": da, "group": key})
                    continue

                elif ra in alleles and any(da in g for g in suballeles): 
                    creg_list.append({"recipient": ra, "donor": da, "group": key})
                    continue

                elif da in alleles and any(ra in g for g in suballeles): 
                    creg_list.append({"recipient": ra, "donor": da, "group": key})
                    continue

                elif any(ra in g and da in g for g in suballeles):
                    near_creg_list.append({"recipient": ra, "donor": da, "group": key})
                    continue

                elif any(da in g for g in suballeles) and any(ra in g for g in suballeles):
                    creg_list.append({"recipient": ra, "donor": da, "group": key})
                    continue
                
                else:
                    continue

    if near_creg_list:
        creg_status = "Near CREG"
    elif creg_list:
        creg_status = "With CREG"
    else:
        creg_status = "No CREG"

    return creg_status, near_creg_list, creg_list

def donor_creg_filter(donor_hla_a_b_list, recipients):
    for recipient in recipients:
        recipient_hla_a_b_uams = [hla.value for hla in recipient.hla_a_uam.all()] + \
            [hla.value for hla in recipient.hla_b_uam.all()]
        creg_status, near_creg_list, creg_list = find_creg_matches(recipient_hla_a_b_uams, donor_hla_a_b_list) 

        recipient.creg_status = creg_status
        recipient.near_creg_list = near_creg_list
        recipient.creg_list = creg_list

def recipient_creg_filter(recipient_hla_a_b_uams, donors):
    for donor in donors:
        donor_hla_a_b_list = [donor.hla_a_1.value, donor.hla_a_2.value, donor.hla_b_1.value, donor.hla_b_2.value]
        creg_status, near_creg_list, creg_list = find_creg_matches(recipient_hla_a_b_uams, donor_hla_a_b_list) 

        donor.creg_status = creg_status
        donor.near_creg_list = near_creg_list
        donor.creg_list = creg_list
