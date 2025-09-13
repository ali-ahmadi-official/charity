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