function mismatchPoint(type1, type2) {
    if (type1 === type2) return 4;
    if ((type1 === "COMMON" && type2 === "INTERMEDIATE") || (type1 === "INTERMEDIATE" && type2 === "COMMON")) return 2;
    if ((type1 === "INTERMEDIATE" && type2 === "UNCOMMON") || (type1 === "UNCOMMON" && type2 === "INTERMEDIATE")) return 2;
    if ((type1 === "COMMON" && type2 === "UNCOMMON") || (type1 === "UNCOMMON" && type2 === "COMMON")) return 0;
    return 0;
}

function calculateLocusScore(r1, r1_type, r2, r2_type, donorList) {
    function scoreOneAllele(don, donType) {
        const match = [r1, r2].find(r => r === don);
        if (match) return 5;

        const scores = [r1_type, r2_type].map(rt => mismatchPoint(donType, rt));
        return Math.max(...scores);
    }

    return donorList.reduce((sum, d) => sum + scoreOneAllele(d.value, d.type), 0);
}

function scoreHlaDrb(rec1, rec2, donor1, donor2) {

    const isNone = val => !val || val.trim().toLowerCase() === "none";

    const donorEmpty1 = isNone(donor1);
    const donorEmpty2 = isNone(donor2);

    // قانون 4: دهنده فقط یک DRB دارد
    if (donorEmpty1 || donorEmpty2) {
        const donorValue = donorEmpty1 ? donor2 : donor1;
        return (rec1 === donorValue || rec2 === donorValue) ? 10 : 5;
    }

    // قانون 3: دهنده هر دو DRB یکسان دارد
    if (donor1 === donor2) {
        return (rec1 === donor1 || rec2 === donor1) ? 10 : 0;
    }

    // قانون 1: هر دو آلل یکسان هستند (ترتیب مهم نیست)
    if (
        (rec1 === donor1 && rec2 === donor2) ||
        (rec1 === donor2 && rec2 === donor1)
    ) {
        return 10;
    }

    // قانون 2: فقط یکی از DRBها مشترک است
    const matches = [rec1, rec2].filter(
        r => r === donor1 || r === donor2
    ).length;

    return matches === 1 ? 5 : 0;
}

const donor = {
    hla_a_first: document.getElementById('hla_a_first_donor').innerText.trim(),
    hla_a_first_type: document.getElementById('hla_a_first_donor_type').innerText.trim(),
    hla_a_second: document.getElementById('hla_a_second_donor').innerText.trim(),
    hla_a_second_type: document.getElementById('hla_a_second_donor_type').innerText.trim(),

    hla_b_first: document.getElementById('hla_b_first_donor').innerText.trim(),
    hla_b_first_type: document.getElementById('hla_b_first_donor_type').innerText.trim(),
    hla_b_second: document.getElementById('hla_b_second_donor').innerText.trim(),
    hla_b_second_type: document.getElementById('hla_b_second_donor_type').innerText.trim(),

    hla_drb1_first: document.getElementById('hla_drb1_first_donor').innerText.trim(),
    hla_drb1_first_type: document.getElementById('hla_drb1_first_donor_type').innerText.trim(),
    hla_drb1_second: document.getElementById('hla_drb1_second_donor').innerText.trim(),
    hla_drb1_second_type: document.getElementById('hla_drb1_second_donor_type').innerText.trim(),

    hla_drb_first: document.getElementById('hla_drb_first_donor').innerText.trim(),
    hla_drb_first_type: document.getElementById('hla_drb_first_donor_type').innerText.trim(),
    hla_drb_second: document.getElementById('hla_drb_second_donor').innerText.trim(),
    hla_drb_second_type: document.getElementById('hla_drb_second_donor_type').innerText.trim(),

    hla_dqb1_first: document.getElementById('hla_dqb1_first_donor').innerText.trim(),
    hla_dqb1_first_type: document.getElementById('hla_dqb1_first_donor_type').innerText.trim(),
    hla_dqb1_second: document.getElementById('hla_dqb1_second_donor').innerText.trim(),
    hla_dqb1_second_type: document.getElementById('hla_dqb1_second_donor_type').innerText.trim(),
};

const hal_a_list = [
    { value: donor.hla_a_first, type: donor.hla_a_first_type },
    { value: donor.hla_a_second, type: donor.hla_a_second_type }
];
const hal_b_list = [
    { value: donor.hla_b_first, type: donor.hla_b_first_type },
    { value: donor.hla_b_second, type: donor.hla_b_second_type }
];
const hal_drb1_list = [
    { value: donor.hla_drb1_first, type: donor.hla_drb1_first_type },
    { value: donor.hla_drb1_second, type: donor.hla_drb1_second_type }
];
const hal_drb_list = [
    { value: donor.hla_drb_first, type: donor.hla_drb_first_type },
    { value: donor.hla_drb_second, type: donor.hla_drb_second_type }
];
const hal_dqb1_list = [
    { value: donor.hla_dqb1_first, type: donor.hla_dqb1_first_type },
    { value: donor.hla_dqb1_second, type: donor.hla_dqb1_second_type }
];

const trs = document.querySelectorAll('tr#tr');
trs.forEach(tr => {
    const recipientId = tr.querySelector('td:first-child span').innerText.trim();

    const recipient = {
        hla_a_first: document.getElementById(`hla_a_first_${recipientId}`).innerText.trim(),
        hla_a_first_type: document.getElementById(`hla_a_first_${recipientId}_type`).innerText.trim(),
        hla_a_second: document.getElementById(`hla_a_second_${recipientId}`).innerText.trim(),
        hla_a_second_type: document.getElementById(`hla_a_second_${recipientId}_type`).innerText.trim(),

        hla_b_first: document.getElementById(`hla_b_first_${recipientId}`).innerText.trim(),
        hla_b_first_type: document.getElementById(`hla_b_first_${recipientId}_type`).innerText.trim(),
        hla_b_second: document.getElementById(`hla_b_second_${recipientId}`).innerText.trim(),
        hla_b_second_type: document.getElementById(`hla_b_second_${recipientId}_type`).innerText.trim(),

        hla_drb1_first: document.getElementById(`hla_drb1_first_${recipientId}`).innerText.trim(),
        hla_drb1_first_type: document.getElementById(`hla_drb1_first_${recipientId}_type`).innerText.trim(),
        hla_drb1_second: document.getElementById(`hla_drb1_second_${recipientId}`).innerText.trim(),
        hla_drb1_second_type: document.getElementById(`hla_drb1_second_${recipientId}_type`).innerText.trim(),

        hla_drb_first: document.getElementById(`hla_drb_first_${recipientId}`).innerText.trim(),
        hla_drb_first_type: document.getElementById(`hla_drb_first_${recipientId}_type`).innerText.trim(),
        hla_drb_second: document.getElementById(`hla_drb_second_${recipientId}`).innerText.trim(),
        hla_drb_second_type: document.getElementById(`hla_drb_second_${recipientId}_type`).innerText.trim(),

        hla_dqb1_first: document.getElementById(`hla_dqb1_first_${recipientId}`).innerText.trim(),
        hla_dqb1_first_type: document.getElementById(`hla_dqb1_first_${recipientId}_type`).innerText.trim(),
        hla_dqb1_second: document.getElementById(`hla_dqb1_second_${recipientId}`).innerText.trim(),
        hla_dqb1_second_type: document.getElementById(`hla_dqb1_second_${recipientId}_type`).innerText.trim(),
    };

    const hla_a_point = calculateLocusScore(recipient.hla_a_first, recipient.hla_a_first_type, recipient.hla_a_second, recipient.hla_a_second_type, hal_a_list);
    const hla_b_point = calculateLocusScore(recipient.hla_b_first, recipient.hla_b_first_type, recipient.hla_b_second, recipient.hla_b_second_type, hal_b_list);
    const hla_drb1_point = calculateLocusScore(recipient.hla_drb1_first, recipient.hla_drb1_first_type, recipient.hla_drb1_second, recipient.hla_drb1_second_type, hal_drb1_list);
    const hla_drb_point = scoreHlaDrb(recipient.hla_drb_first, recipient.hla_drb_second, donor.hla_drb_first, donor.hla_drb_second);
    const hla_dqb1_point = calculateLocusScore(recipient.hla_dqb1_first, recipient.hla_dqb1_first_type, recipient.hla_dqb1_second, recipient.hla_dqb1_second_type, hal_dqb1_list);

    const self_hla_a_point_div = document.getElementById(`hla_a_${recipientId}_point`);
    const self_hla_b_point_div = document.getElementById(`hla_b_${recipientId}_point`);
    const self_hla_drb1_point_div = document.getElementById(`hla_drb1_${recipientId}_point`);
    const self_hla_drb_point_div = document.getElementById(`hla_drb_${recipientId}_point`);
    const self_hla_dqb1_point_div = document.getElementById(`hla_dqb1_${recipientId}_point`);

    self_hla_a_point_div.innerText = hla_a_point;
    self_hla_b_point_div.innerText = hla_b_point;
    self_hla_drb1_point_div.innerText = hla_drb1_point;
    self_hla_drb_point_div.innerText = hla_drb_point;
    self_hla_dqb1_point_div.innerText = hla_dqb1_point;

    const total_point = ((hla_a_point + hla_b_point + hla_drb1_point + hla_dqb1_point + hla_drb_point) / 5).toFixed(2);

    const withouthla = parseFloat(tr.querySelector('td:nth-child(6) span').innerText);

    const pointCell = tr.querySelector('td:nth-child(7) span');
    if (pointCell) {
        pointCell.innerText = total_point;
    }

    const totalCell = tr.querySelector('td:nth-child(8) span');
    if (totalCell) {
        totalCell.innerText = (parseFloat(total_point) + withouthla).toFixed(2);
    }
});