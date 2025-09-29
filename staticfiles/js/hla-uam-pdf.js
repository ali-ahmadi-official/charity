function selectOptionByText(selectElement, targetText) {
    const options = Array.from(selectElement.options);
    const match = options.find(opt => opt.text.trim() === targetText.trim());
    if (match) {
        selectElement.value = match.value;
        selectElement.style.border = "1px solid #f97316";
    } else {
        selectElement.value = '';
    }
}

document.querySelectorAll('.file-input').forEach(input => {
    const type = input.dataset.type;
    const fileInfo = document.querySelector(`.file-info[data-type="${type}"]`);
    const fileName = document.querySelector(`.file-name[data-type="${type}"]`);
    const removeBtn = document.querySelector(`.remove-file[data-type="${type}"]`);

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (file && !file.name.endsWith('.pdf')) {
            alert('لطفاً فقط فایل PDF انتخاب کنید!');
            input.value = '';
            return;
        }
        fileName.textContent = file.name;
        fileInfo.style.display = 'flex';
        removeBtn.style.display = 'flex';
    });

    removeBtn.addEventListener('click', () => {
        input.value = '';
        fileInfo.style.display = 'none';
        fileName.textContent = '';
    });
});

document.getElementById('pcr_based_input').addEventListener('change', function () {
    const file = this.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/extract-info/', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('full_name').value = data.full_name || '';
            document.getElementById('national_code').value = data.national_code || '';
            document.getElementById('gender').value = data.gender || '';
            document.getElementById('age').value = data.age || '';
            document.getElementById('blood_group').value = data.blood_group || '';

            document.getElementById('full_name').style.border = "1px solid #f97316";
            document.getElementById('national_code').style.border = "1px solid #f97316";
            document.getElementById('gender').style.border = "1px solid #f97316";
            document.getElementById('age').style.border = "1px solid #f97316";
            document.getElementById('blood_group').style.border = "1px solid #f97316";

            document.getElementById('api-message').style.display = 'flex';
        })
        .catch(err => {
            console.error('❌ خطا در دریافت اطلاعات از API:', err);
            alert('مشکلی در خواندن فایل PDF پیش آمد.');
        });
});

document.getElementById('pcr_based_input').addEventListener('change', function () {
    const file = this.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/extract-hla/', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            const hla_a_1 = document.getElementById('id_hla_a_1');
            const hla_a_2 = document.getElementById('id_hla_a_2');
            const hla_b_1 = document.getElementById('id_hla_b_1');
            const hla_b_2 = document.getElementById('id_hla_b_2');
            const hla_drb1_1 = document.getElementById('id_hla_drb1_1');
            const hla_drb1_2 = document.getElementById('id_hla_drb1_2');
            const hla_drb_1 = document.getElementById('id_hla_drb_1');
            const hla_drb_2 = document.getElementById('id_hla_drb_2');
            const hla_dqb1_1 = document.getElementById('id_hla_dqb1_1');
            const hla_dqb1_2 = document.getElementById('id_hla_dqb1_2');

            selectOptionByText(hla_a_1, data.A?.[0] || '');
            selectOptionByText(hla_a_2, data.A?.[1] || '');
            selectOptionByText(hla_b_1, data.B?.[0] || '');
            selectOptionByText(hla_b_2, data.B?.[1] || '');
            selectOptionByText(hla_drb1_1, data.DRB1?.[0] || '');
            selectOptionByText(hla_drb1_2, data.DRB1?.[1] || '');
            selectOptionByText(hla_drb_1, data.DRB?.[0] || '');
            selectOptionByText(hla_drb_2, data.DRB?.[1] || '');
            selectOptionByText(hla_dqb1_1, data.DQB1?.[0] || '');
            selectOptionByText(hla_dqb1_2, data.DQB1?.[1] || '');
        })
        .catch(err => {
            console.error('❌ خطا در دریافت اطلاعات از API:', err);
            alert('مشکلی در خواندن فایل PDF پیش آمد.');
        });
});