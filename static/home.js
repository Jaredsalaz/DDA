// Botón de limpiar
document.getElementById('clear-button').addEventListener('click', function() {
    // Limpiar los campos del formulario
    document.getElementById('formulario').reset();

    // Limpiar la gráfica
    if (window.myChart) {
        window.myChart.destroy();
        window.myChart = null;
    }

    // Limpiar las tablas
    const tablas = ['tabla-puntos-ab', 'tabla-puntos-bc', 'tabla-puntos-ca'];
    tablas.forEach(tablaId => {
        const tbody = document.getElementById(tablaId).getElementsByTagName('tbody')[0];
        tbody.innerHTML = '';
    });

    // Limpiar el texto del caso determinado
    document.getElementById('caso-determinado').textContent = '';
});

// Animaciones de las cortinas de bienvenida
document.addEventListener('DOMContentLoaded', function() {
    const curtainLeft = document.getElementById('curtain-left');
    const curtainRight = document.getElementById('curtain-right');
    const formContainer = document.getElementById('form-container');

    // Espera 3 segundos y luego oculta las cortinas
    setTimeout(() => {
        curtainLeft.style.animation = 'curtainOpen 2s forwards';
        curtainRight.style.animation = 'curtainOpen 2s forwards';
        setTimeout(() => {
            curtainLeft.style.display = 'none';
            curtainRight.style.display = 'none';
            formContainer.style.display = 'block';

            // Añadir animaciones de rebote a los elementos del formulario
            const formGroups = document.querySelectorAll('.form-group');
            const submitButton = document.querySelector('.form-submit-btn');
            const loading = document.getElementById('loading');
            const grafica = document.getElementById('grafica');
            const casoDeterminado = document.getElementById('caso-determinado');
            const tablaPuntosAb = document.getElementById('tabla-puntos-ab');
            const tablaPuntosBc = document.getElementById('tabla-puntos-bc');
            const tablaPuntosCa = document.getElementById('tabla-puntos-ca');

            formGroups.forEach((group, index) => {
                group.style.opacity = 1;
                group.style.animationDelay = `${3 + index * 0.5}s`;
            });

            submitButton.style.opacity = 1;
            submitButton.style.animationDelay = '3.5s';

            loading.style.opacity = 1;
            loading.style.animationDelay = '4s';

            grafica.style.opacity = 1;
            grafica.style.animationDelay = '4.5s';

            casoDeterminado.style.opacity = 1;
            casoDeterminado.style.animationDelay = '5s';

            tablaPuntosAb.style.opacity = 1;
            tablaPuntosAb.style.animationDelay = '5.5s';

            tablaPuntosBc.style.opacity = 1;
            tablaPuntosBc.style.animationDelay = '6s';

            tablaPuntosCa.style.opacity = 1;
            tablaPuntosCa.style.animationDelay = '6.5s';
        }, 2000); // Espera a que termine la animación de las cortinas
    }, 3000); // Duración de la animación de bienvenida
});

// Añade un evento 'submit' al formulario con id 'formulario'
document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault();

    const xa = parseFloat(document.getElementById('xa').value);
    const ya = parseFloat(document.getElementById('ya').value);
    const xb = parseFloat(document.getElementById('xb').value);
    const yb = parseFloat(document.getElementById('yb').value);
    const xc = parseFloat(document.getElementById('xc').value);
    const yc = parseFloat(document.getElementById('yc').value);

    const audio = document.getElementById('audio-siiuuu');
    audio.play().then(() => {
        console.log('Audio reproducido correctamente');
    }).catch(error => {
        console.error('Error al reproducir el audio:', error);
    });

    document.getElementById('loading').style.display = 'block';

    fetch('/calcular_puntos_triangulo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ xa, ya, xb, yb, xc, yc })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';

        const puntosAb = data.puntos_ab;
        const puntosBc = data.puntos_bc;
        const puntosCa = data.puntos_ca;
        const puntosRelleno = data.puntos_relleno;
        const casos = data.casos;

        const ctx = document.getElementById('grafica').getContext('2d');

        if (window.myChart) {
            window.myChart.destroy();
        }

        window.myChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Triángulo DDA',
                    data: [...puntosAb, ...puntosBc, ...puntosCa].map(p => ({ x: p[0], y: p[1] })),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    showLine: true,
                    fill: false,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)',
                    pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
                    pointHoverBorderWidth: 2,
                    pointStyle: 'circle'
                },
                {
                    label: 'Relleno del Triángulo',
                    data: puntosRelleno.map(p => ({ x: p[0], y: p[1] })),
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    showLine: false,
                    fill: true,
                    pointRadius: 3,
                    pointHoverRadius: 5,
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                    pointHoverBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
                    pointHoverBorderWidth: 1,
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
                                enabled: false
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
                    },
                    y: {
                        type: 'linear',
                        position: 'left'
                    }
                },
                animation: {
                    onComplete: function() {
                        document.getElementById('loading').style.display = 'none';
                    }
                }
            }
        });

        const tablas = {
            'tabla-puntos-ab': puntosAb,
            'tabla-puntos-bc': puntosBc,
            'tabla-puntos-ca': puntosCa
        };

        for (const [tablaId, puntos] of Object.entries(tablas)) {
            const tbody = document.getElementById(tablaId).getElementsByTagName('tbody')[0];
            tbody.innerHTML = '';
            puntos.forEach((punto, index) => {
                const row = tbody.insertRow();
                row.style.animation = 'fadeIn 0.5s ease-in-out';
                const cellIteracion = row.insertCell(0);
                const cellX = row.insertCell(1);
                const cellY = row.insertCell(2);
                cellIteracion.textContent = index;
                cellX.textContent = punto[0].toFixed(4);
                cellY.textContent = punto[1].toFixed(4);
            });
        }

        document.getElementById('caso-determinado').textContent = `Casos: AB - ${casos.AB}, BC - ${casos.BC}, CA - ${casos.CA}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
    });
});