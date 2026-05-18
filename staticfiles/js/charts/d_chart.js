function parseCountsFromPercent(data) {
    const result = {};
    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            const valueString = data[key];
            const match = valueString.match(/^(\d+)\s*\(/);
            if (match && match[1]) {
                result[key] = parseInt(match[1], 10);
            } else {
                result[key] = valueString;
            }
        }
    }
    return result;
}

function shuffleArray(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

const colors = [
    'rgba(255, 99, 132, 0.7)',   // صورتی
    'rgba(54, 162, 235, 0.7)',   // آبی
    'rgba(255, 206, 86, 0.7)',   // زرد
    'rgba(75, 192, 192, 0.7)',   // فیروزه‌ای
    'rgba(153, 102, 255, 0.7)',  // بنفش
    'rgba(255, 159, 64, 0.7)',   // نارنجی
    'rgba(199, 199, 199, 0.7)',  // خاکستری
    'rgba(83, 102, 255, 0.7)',   // آبی تیره
    'rgba(255, 99, 255, 0.7)',   // صورتی روشن
    'rgba(100, 255, 100, 0.7)',  // سبز روشن
    'rgba(255, 140, 0, 0.7)',    // نارنجی پررنگ
    'rgba(0, 200, 200, 0.7)',    // سبز آبی
    'rgba(220, 50, 120, 0.7)',   // تمشکی
    'rgba(50, 200, 150, 0.7)',   // نعنایی
    'rgba(200, 100, 200, 0.7)',  // ارکیده
    'rgba(100, 150, 250, 0.7)',  // آبی آسمانی
    'rgba(255, 100, 50, 0.7)',   // قرمز-نارنجی
    'rgba(50, 200, 80, 0.7)',    // سبز چمنی
    'rgba(200, 180, 100, 0.7)',  // زرد قهوه‌ای
    'rgba(180, 100, 80, 0.7)'    // قهوه‌ای مایل به قرمز
];

function barChartCreator(data, elementId, label) {
    if (data) {
        const labels = Object.keys(data);
        const values = Object.values(data);

        const total = values.reduce((sum, value) => sum + value, 0);
        const percentValues = values.map(value => total ? (value / total * 100) : 0);

        const barCtx = document.getElementById(elementId).getContext('2d');
        const barChart = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label + ' (%)',
                    data: percentValues,
                    backgroundColor: shuffleArray(colors),
                    borderColor: '#ffffff',
                    borderWidth: 1,
                    rawValues: values
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function (value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const dataset = context.dataset;
                                const index = context.dataIndex;
                                const rawValue = dataset.rawValues[index];
                                const percentValue = context.parsed.y;
                                return `${context.label}: ${rawValue} (${percentValue.toFixed(1)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
}

function pieChartCreator(data, elementId) {
    if (data) {
        const labels = Object.keys(data);
        const values = Object.values(data);

        const total = values.reduce((sum, value) => sum + value, 0);
        const percentValues = values.map(value => total ? (value / total * 100) : 0);

        const pieCtx = document.getElementById(elementId).getContext('2d');
        const pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: percentValues,
                    backgroundColor: shuffleArray(colors),
                    borderColor: '#ffffff',
                    borderWidth: 1,
                    rawValues: values
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const dataset = context.dataset;
                                const index = context.dataIndex;
                                const rawValue = dataset.rawValues[index];
                                const percentValue = context.parsed;
                                return `${context.label}: ${rawValue} (${percentValue.toFixed(1)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
}

let results = JSON.parse(document.getElementById('results').textContent);

pieChartCreator(parseCountsFromPercent(results['gender_status']), 'gender_status');
pieChartCreator(parseCountsFromPercent(results['age_status']), 'age_status');
pieChartCreator(parseCountsFromPercent(results['blood_group_status']), 'blood_group_status');

barChartCreator(parseCountsFromPercent(results['hla_a']), 'hla_a', 'HLA A');
barChartCreator(parseCountsFromPercent(results['hla_b']), 'hla_b', 'HLA B');

barChartCreator(parseCountsFromPercent(results['hla_drb1']), 'hla_drb1', 'HLA DRB1');
barChartCreator(parseCountsFromPercent(results['hla_drb']), 'hla_drb', 'HLA DRB');
barChartCreator(parseCountsFromPercent(results['hla_dqb1']), 'hla_dqb1', 'HLA DQB1');