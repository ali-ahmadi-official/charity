function sortTableByColumn(columnIndex) {
    const table = document.getElementById('myTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const valA = a.cells[columnIndex].textContent.trim();
        const valB = b.cells[columnIndex].textContent.trim();

        const numA = parseFloat(valA);
        const numB = parseFloat(valB);
        if (!isNaN(numA) && !isNaN(numB)) {
            return numB - numA; // از بیشتر به کمتر
        }

        return valA.localeCompare(valB, 'fa'); // مرتب‌سازی فارسی
    });

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

const first_sort = document.getElementById('first_sort');
const second_sort = document.getElementById('second_sort');
const third_sort = document.getElementById('third_sort');

first_sort.addEventListener('click', () => {
    first_sort.classList.add('active-sort');
    second_sort.classList.remove('active-sort');
    third_sort.classList.remove('active-sort');
});

second_sort.addEventListener('click', () => {
    second_sort.classList.add('active-sort');
    third_sort.classList.remove('active-sort');
    first_sort.classList.remove('active-sort');
});

third_sort.addEventListener('click', () => {
    third_sort.classList.add('active-sort');
    first_sort.classList.remove('active-sort');
    second_sort.classList.remove('active-sort');
});