window.onload = () => {

    const ctx = document.getElementById('chart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Risk', 'Confidence'],
            datasets: [{
                label: 'Analysis',
                data: [
                    parseFloat(document.querySelectorAll('.progress-circle')[0].innerText),
                    parseFloat(document.querySelectorAll('.progress-circle')[1].innerText)
                ],
                backgroundColor: ['#ef4444', '#22c55e']
            }]
        },
        options: {
            plugins: {
                legend: { labels: { color: "white" } }
            },
            scales: {
                y: { ticks: { color: "white" } },
                x: { ticks: { color: "white" } }
            }
        }
    });

};