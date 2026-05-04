const selectedRecipients = [];

async function fetchRecipients() {
    const input = document.getElementById('search-input').value;
    const response = await fetch(`/recipient-api/?full_name=${input}`);
    const data = await response.json();
    const resultsDiv = document.getElementById('results');
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
        data.forEach(recipient => {
            const checkboxHtml = `
                <tr>
                    <td class="align-middle text-center">
                        <input type="checkbox" id="recipient-${recipient.id}" name="selected_recipient" value="${recipient.id}" onchange='handleRecipientSelection(this, ${JSON.stringify(recipient)})'>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.id}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.full_name}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.national_code}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.phone_number}</span>
                    </td>
                </tr>
            `;
            resultsDiv.innerHTML += checkboxHtml;
        });
    }
}

function handleRecipientSelection(checkbox, recipient) {

    if (checkbox.checked) {
        if (!selectedRecipients.some(r => r.id === recipient.id)) {
            selectedRecipients.push(recipient);
        }
    } else {
        const index = selectedRecipients.findIndex(r => r.id === recipient.id);
        if (index > -1) {
            selectedRecipients.splice(index, 1);
        }
    }
    updateSelectedRecipientsTable();
}

function updateSelectedRecipientsTable() {
    const selectedsDiv = document.getElementById('selecteds');
    selectedsDiv.innerHTML = '';

    if (selectedRecipients.length === 0) {
        selectedsDiv.innerHTML = `
            <tr>
                <td colspan="4" class="align-middle text-center">
                    <span class="text-secondary text-xs font-weight-bold">گیرنده‌ای انتخاب نشده است...</span>
                </td>
            </tr>
        `;
    } else {
        selectedRecipients.forEach(recipient => {
            const rowHtml = `
                <tr>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.id}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.full_name}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.national_code}</span>
                    </td>
                    <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${recipient.phone_number}</span>
                    </td>
                </tr>
            `;
            selectedsDiv.innerHTML += rowHtml;
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateSelectedRecipientsTable();
});

function submitSelection() {
    const selectedIds = selectedRecipients.map(recipient => recipient.id);
    const recipientsString = selectedIds.join(',');
    
    let pk = document.querySelector('.pk').innerHTML;
    let status = document.querySelector('.status').innerHTML;

    const targetUrl = `/${status}/${pk}/special-analysis/?some_recipients=${recipientsString}`;
    window.location.href = targetUrl;
}
