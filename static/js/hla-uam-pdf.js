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

document.getElementById('class_i_input').addEventListener('change', function () {
    const file = this.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/extract/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        // پر کردن فیلدها با داده‌های برگشتی
        document.getElementById('first_name').value = data.first_name || '';
        document.getElementById('last_name').value = data.last_name || '';
        document.getElementById('national_code').value = data.national_code || '';
        document.getElementById('gender').value = data.gender || '';
        document.getElementById('pregnancies_number').value = data.pregnancies_number ?? '';
        document.getElementById('age').value = data.age || '';
        document.getElementById('blood_group').value = data.blood_group || '';

        document.getElementById('first_name').style.border = "1px solid #f97316";
        document.getElementById('last_name').style.border = "1px solid #f97316";
        document.getElementById('national_code').style.border = "1px solid #f97316";
        document.getElementById('gender').style.border = "1px solid #f97316";
        document.getElementById('pregnancies_number').style.border = "1px solid #f97316";
        document.getElementById('age').style.border = "1px solid #f97316";
        document.getElementById('blood_group').style.border = "1px solid #f97316";

        document.getElementById('api-message').style.display = 'flex';
    })
    .catch(err => {
        console.error('❌ خطا در دریافت اطلاعات از API:', err);
        alert('مشکلی در خواندن فایل PDF پیش آمد.');
    });
});