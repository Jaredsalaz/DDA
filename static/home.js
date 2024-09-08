document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault();
    const x0 = document.getElementById('x0').value;
    const y0 = document.getElementById('y0').value;
    const x1 = document.getElementById('x1').value;
    const y1 = document.getElementById('y1').value;

    // Mostrar animación de carga
    document.getElementById('loading').style.display = 'block';

    fetch('/calcular_puntos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ x0, y0, x1, y1 })
    })
    .then(response => response.json())
    .then(data => {
        const puntos = data.puntos;
        const pendiente = data.pendiente;
        const caso = data.caso; // Nuevo campo para el caso determinado
        const ctx = document.getElementById('grafica').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: puntos.map((_, index) => index),
                datasets: [{
                    label: 'Línea DDA',
                    data: puntos.map(p => ({ x: p[0], y: p[1] })),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)',
                    pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
                    pointHoverBorderWidth: 2,
                    pointStyle: 'circle'
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Punto (${context.raw.x.toFixed(4)}, ${context.raw.y.toFixed(4)})`;
                            }
                        }
                    },
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'xy'
                        },
                        zoom: {
                            wheel: {
                                enabled: true
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'xy'
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    }
                },
                animation: {
                    onComplete: function() {
                        // Ocultar animación de carga
                        document.getElementById('loading').style.display = 'none';
                    }
                }
            }
        });

        const tbody = document.getElementById('tabla-puntos').getElementsByTagName('tbody')[0];
        tbody.innerHTML = '';
        puntos.forEach((punto, index) => {
            const row = tbody.insertRow();
            row.style.animation = 'fadeIn 0.5s ease-in-out';
            const cellIteracion = row.insertCell(0);
            const cellX = row.insertCell(1);
            const cellY = row.insertCell(2);
            const cellPendiente = row.insertCell(3);
            cellIteracion.textContent = index;
            cellX.textContent = punto[0].toFixed(4);
            cellY.textContent = punto[1].toFixed(4);
            cellPendiente.textContent = pendiente.toFixed(4);
        });

        // Mostrar el caso determinado
        document.getElementById('caso-determinado').textContent = `Caso: ${caso}`;
    })
    .catch(error => {
        console.error('Error:', error);
        // Ocultar animación de carga en caso de error
        document.getElementById('loading').style.display = 'none';
    });
});