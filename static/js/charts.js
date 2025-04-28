document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('baptismChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: baptismChartData,
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true }
                }
            }
        });
    }
});