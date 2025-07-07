
// ✳️ توابع عمومی امتیازدهی

function mismatchPoint(type1, type2) {
    if (type1 === type2) return 4;
    if ((type1 === "COMMON" && type2 === "INTERMEDIATE") || (type1 === "INTERMEDIATE" && type2 === "COMMON")) return 2;
    if ((type1 === "INTERMEDIATE" && type2 === "UNCOMMON") || (type1 === "UNCOMMON" && type2 === "INTERMEDIATE")) return 2;
    if ((type1 === "COMMON" && type2 === "UNCOMMON") || (type1 === "UNCOMMON" && type2 === "COMMON")) return 0;
    return 0;
}

function calculateLocusScore(r1, r1_type, r2, r2_type, donorList, locus) {
    if (locus === "hla_drb") {
        let matches = 0;
        [r1, r2].forEach(r => {
            if (donorList.some(d => d.value === r)) matches++;
        });
        return matches === 2 ? 5 : matches === 1 ? 3 : 0;
    }

    function scoreOneAllele(rec, recType) {
        const match = donorList.find(d => d.value === rec);
        if (match) return 5;
        const scores = donorList.map(d => mismatchPoint(recType, d.type));
        return Math.max(...scores);
    }

    return scoreOneAllele(r1, r1_type) + scoreOneAllele(r2, r2_type);
}

function scoreHlaDrb(rec1, rec2, donor1, donor2) {
    let score = 0;

    const isNone = val => !val || val.trim().toLowerCase() === "None";

    const donorEmpty1 = isNone(donor1);
    const donorEmpty2 = isNone(donor2);

    // هر donor خالی = ۵ امتیاز
    if (donorEmpty1) score += 5;
    if (donorEmpty2) score += 5;

    // اگر هر دو پر بودن → بررسی تطابق
    if (!donorEmpty1 && !donorEmpty2) {
        const matches = [rec1, rec2].filter(r => r === donor1 || r === donor2).length;
        if (matches === 2) return 10;
        if (matches === 1) return 5;
        return 0;
    }

    // اگه فقط یکی خالی و یکی match داریم → ۱۰ امتیاز
    const matches = [rec1, rec2].filter(r => r === donor1 || r === donor2).length;
    if ((donorEmpty1 || donorEmpty2) && matches === 1) return 10;

    return score;
}

// ✳️ شروع محاسبه برای تمام گیرنده‌ها

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

// گرفتن همه گیرنده‌ها
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

    const hla_a_point = calculateLocusScore(recipient.hla_a_first, recipient.hla_a_first_type, recipient.hla_a_second, recipient.hla_a_second_type, hal_a_list, "hla_a");
    const hla_b_point = calculateLocusScore(recipient.hla_b_first, recipient.hla_b_first_type, recipient.hla_b_second, recipient.hla_b_second_type, hal_b_list, "hla_b");
    const hla_drb1_point = calculateLocusScore(recipient.hla_drb1_first, recipient.hla_drb1_first_type, recipient.hla_drb1_second, recipient.hla_drb1_second_type, hal_drb1_list, "hla_drb1");
    const hla_drb_point = scoreHlaDrb(recipient.hla_drb_first, recipient.hla_drb_second, donor.hla_drb_first, donor.hla_drb_second);
    const hla_dqb1_point = calculateLocusScore(recipient.hla_dqb1_first, recipient.hla_dqb1_first_type, recipient.hla_dqb1_second, recipient.hla_dqb1_second_type, hal_dqb1_list, "hla_dqb1");

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

    // نمایش در جدول HTML — ستون ششم با تگ <span>
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

function sortTableByColumn(columnIndex) {
    const table = document.getElementById('myTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const valA = a.cells[columnIndex].textContent.trim();
        const valB = b.cells[columnIndex].textContent.trim();

        // اگر مقدار عددی بود، به عدد تبدیل کن و مقایسه عددی انجام بده
        const numA = parseFloat(valA);
        const numB = parseFloat(valB);
        if (!isNaN(numA) && !isNaN(numB)) {
            return numB - numA; // از بیشتر به کمتر
        }

        // در غیر این صورت، مقایسه رشته‌ای انجام بده
        return valA.localeCompare(valB, 'fa'); // مرتب‌سازی فارسی
    });

    // پاک کردن tbody و اضافه‌کردن ردیف‌ها
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}

const black = document.querySelector('.black');
function showDiv(id) {
    hideAllDivs();
    document.getElementById(id).style.display = 'grid';
    black.style.display = 'flex';
}

function hideAllDivs() {
    const divs = document.querySelectorAll('.hidden-div');
    divs.forEach(div => div.style.display = 'none');
    black.style.display = 'none';
}