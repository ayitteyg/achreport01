document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById("baptismChart").getContext("2d");

    const data = {
        labels: ['Church A', 'Church B', 'Church C'],
        datasets: [{
            label: 'Baptisms',
            data: [12, 19, 7],
            backgroundColor: '#0d6efd',
        }]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
});