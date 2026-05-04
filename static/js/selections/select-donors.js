const selectedCadaverDonors = [];

async function fetchCadaverDonors() {
    const input = document.getElementById('search-input-1').value;
    const response = await fetch(`/cadaver-donor-api/?full_name=${input}`);
    const data = await response.json();
    const resultsDiv = document.getElementById('results-1');
    resultsDiv.innerHTML = '';

    if (data.length === 0) {
        resultsDiv.innerHTML = `
            <tr>
                <td colspan="5" class="align-middle text-center">
                    <span class="text-secondary text-xs font-weight-bold">موردی یافت نشد</span>
                </td>
            </tr>
        `;
    } else {
        data.forEach(cadaverDonor => {
            const checkboxHtml = `
                <tr>
                    <td class="align-middle text-center">
                        <input type="checkbox" id="cadaverDonor-${cadaverDonor.id}" name="selected_cadaverDonor" value="${cadaverDonor.id}" onchange='handleCadaverDonorSelection(this, ${JSON.stringify(cadaverDonor)})'>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.id}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.full_name}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.national_code}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.phone_number}</span>
                    </td>
                </tr>
            `;
            resultsDiv.innerHTML += checkboxHtml;
        });
    }
}

function handleCadaverDonorSelection(checkbox, cadaverDonor) {

    if (checkbox.checked) {
        if (!selectedCadaverDonors.some(r => r.id === cadaverDonor.id)) {
            selectedCadaverDonors.push(cadaverDonor);
        }
    } else {
        const index = selectedCadaverDonors.findIndex(r => r.id === cadaverDonor.id);
        if (index > -1) {
            selectedCadaverDonors.splice(index, 1);
        }
    }
    updateSelectedCadaverDonorsTable();
}

function updateSelectedCadaverDonorsTable() {
    const selectedsDiv = document.getElementById('selecteds-1');
    selectedsDiv.innerHTML = '';

    if (selectedCadaverDonors.length === 0) {
        selectedsDiv.innerHTML = `
            <tr>
                <td colspan="4" class="align-middle text-center">
                    <span class="text-secondary text-xs font-weight-bold">اهداکننده ایی انتخاب نشده است...</span>
                </td>
            </tr>
        `;
    } else {
        selectedCadaverDonors.forEach(cadaverDonor => {
            const rowHtml = `
                <tr>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.id}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.full_name}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.national_code}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${cadaverDonor.phone_number}</span>
                    </td>
                </tr>
            `;
            selectedsDiv.innerHTML += rowHtml;
        });
    }
}

const selectedLivingDonors = [];

async function fetchLivingDonors() {
    const input = document.getElementById('search-input-2').value;
    const response = await fetch(`/living-donor-api/?full_name=${input}`);
    const data = await response.json();
    const resultsDiv = document.getElementById('results-2');
    resultsDiv.innerHTML = '';

    if (data.length === 0) {
        resultsDiv.innerHTML = `
            <tr>
                <td colspan="5" class="align-middle text-center">
                    <span class="text-secondary text-xs font-weight-bold">موردی یافت نشد</span>
                </td>
            </tr>
        `;
    } else {
        data.forEach(livingDonor => {
            const checkboxHtml = `
                <tr>
                    <td class="align-middle text-center">
                        <input type="checkbox" id="livingDonor-${livingDonor.id}" name="selected_livingDonor" value="${livingDonor.id}" onchange='handleLivingDonorSelection(this, ${JSON.stringify(livingDonor)})'>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.id}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.full_name}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.national_code}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.phone_number}</span>
                    </td>
                </tr>
            `;
            resultsDiv.innerHTML += checkboxHtml;
        });
    }
}

function handleLivingDonorSelection(checkbox, livingDonor) {

    if (checkbox.checked) {
        if (!selectedLivingDonors.some(r => r.id === livingDonor.id)) {
            selectedLivingDonors.push(livingDonor);
        }
    } else {
        const index = selectedLivingDonors.findIndex(r => r.id === livingDonor.id);
        if (index > -1) {
            selectedLivingDonors.splice(index, 1);
        }
    }
    updateSelectedLivingDonorsTable();
}

function updateSelectedLivingDonorsTable() {
    const selectedsDiv = document.getElementById('selecteds-2');
    selectedsDiv.innerHTML = '';

    if (selectedLivingDonors.length === 0) {
        selectedsDiv.innerHTML = `
            <tr>
                <td colspan="4" class="align-middle text-center">
                    <span class="text-secondary text-xs font-weight-bold">اهداکننده ایی انتخاب نشده است...</span>
                </td>
            </tr>
        `;
    } else {
        selectedLivingDonors.forEach(livingDonor => {
            const rowHtml = `
                <tr>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.id}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.full_name}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.national_code}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${livingDonor.phone_number}</span>
                    </td>
                </tr>
            `;
            selectedsDiv.innerHTML += rowHtml;
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateSelectedLivingDonorsTable();
    updateSelectedCadaverDonorsTable();
});

function submitSelection() {
    const selectedcad = selectedCadaverDonors.map(cadaverDonor => cadaverDonor.id);
    const selectedliv = selectedLivingDonors.map(livingDonor => livingDonor.id);
    const cadaverDonorsString = selectedcad.join(',');
    const livingDonorsString = selectedliv.join(',');

    let pk = document.querySelector('.pk').innerHTML;

    const targetUrl = `/recipients/${pk}/special-analysis/?some_cadaver_donors=${cadaverDonorsString}&some_living_donors=${livingDonorsString}`;
    window.location.href = targetUrl;
}
