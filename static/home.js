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
    for (let i = 1; i <= 8; i++) {
        const tbody = document.getElementById(`tabla-octante-${i}`).getElementsByTagName('tbody')[0];
        tbody.innerHTML = '';
    }
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
        }, 2000); // Espera a que termine la animación de las cortinas
    }, 3000); // Duración de la animación de bienvenida
});

// Añade un evento 'submit' al formulario con id 'formulario'
document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault();

    const Xc = parseFloat(document.getElementById('xc').value);
    const Yc = parseFloat(document.getElementById('yc').value);
    const r = parseFloat(document.getElementById('r').value);

    const audio = document.getElementById('audio-siiuuu');
    audio.play().then(() => {
        console.log('Audio reproducido correctamente');
    }).catch(error => {
        console.error('Error al reproducir el audio:', error);
    });

    document.getElementById('loading').style.display = 'block';

    fetch('/calcular_puntos_circulo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ Xc, Yc, r })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';

        const puntos = data.puntos;
        const octantes = data.octantes;
        const puntosRelleno = data.puntos_relleno;

        const ctx = document.getElementById('grafica').getContext('2d');

        if (window.myChart) {
            window.myChart.destroy();
        }

        window.myChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Octante 1',
                        data: [],
                        borderColor: 'rgba(255, 99, 132, 1)', // Rojo
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                        pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)',
                        pointHoverBorderColor: 'rgba(255, 99, 132, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 2',
                        data: [],
                        borderColor: 'rgba(54, 162, 235, 1)', // Azul
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                        pointHoverBackgroundColor: 'rgba(54, 162, 235, 1)',
                        pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 3',
                        data: [],
                        borderColor: 'rgba(255, 255, 255, 1)', // Blanco
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                        pointHoverBackgroundColor: 'rgba(255, 255, 255, 1)',
                        pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 4',
                        data: [],
                        borderColor: 'rgba(153, 102, 255, 1)', // Púrpura
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(153, 102, 255, 1)',
                        pointHoverBackgroundColor: 'rgba(153, 102, 255, 1)',
                        pointHoverBorderColor: 'rgba(153, 102, 255, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 5',
                        data: [],
                        borderColor: 'rgba(255, 206, 86, 1)', // Amarillo
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(255, 206, 86, 1)',
                        pointHoverBackgroundColor: 'rgba(255, 206, 86, 1)',
                        pointHoverBorderColor: 'rgba(255, 206, 86, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 6',
                        data: [],
                        borderColor: 'rgba(255, 159, 64, 1)', // Naranja
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(255, 159, 64, 1)',
                        pointHoverBackgroundColor: 'rgba(255, 159, 64, 1)',
                        pointHoverBorderColor: 'rgba(255, 159, 64, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 7',
                        data: [],
                        borderColor: 'rgba(255, 0, 0, 1)', // Rojo
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(255, 0, 0, 1)',
                        pointHoverBackgroundColor: 'rgba(255, 0, 0, 1)',
                        pointHoverBorderColor: 'rgba(255, 0, 0, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Octante 8',
                        data: [],
                        borderColor: 'rgba(75, 192, 192, 1)', // Teal
                        borderWidth: 2,
                        showLine: false,
                        fill: false,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                        pointHoverBackgroundColor: 'rgba(75, 192, 192, 1)',
                        pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
                        pointHoverBorderWidth: 2,
                        pointStyle: 'circle'
                    },
                    {
                        label: 'Relleno',
                        data: [],
                        borderColor: 'rgba(0, 206, 41, 0.505)', // Verde
                        borderWidth: 1,
                        showLine: false,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                        pointBackgroundColor: 'rgba(0, 206, 41, 0.505)',
                        pointHoverBackgroundColor: 'rgba(0, 206, 41, 0.505)',
                        pointHoverBorderColor: 'rgba(0, 206, 41, 0.505)',
                        pointHoverBorderWidth: 1,
                        pointStyle: 'circle'
                    }
                ]
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
                                enabled: true, // Habilitar el zoom con la rueda del ratón
                                speed: 0.1 // Ajustar la velocidad del zoom
                            },
                            pinch: {
                                enabled: true // Habilitar el zoom con el gesto de pellizco
                            },
                            mode: 'xy'
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        ticks: {
                            stepSize: 1 // Ajuste para que los puntos se dibujen por píxel
                        }
                    },
                    y: {
                        type: 'linear',
                        position: 'left',
                        ticks: {
                            stepSize: 1 // Ajuste para que los puntos se dibujen por píxel
                        }
                    }
                },
                animation: {
                    duration: 0 // Desactivar la animación predeterminada
                },
                aspectRatio: 1 // Mantener la proporción 1:1 para evitar el efecto de elipse
            }
        });

        // Animar el dibujo del círculo octante por octante
        const drawOctant = (octantIndex) => {
            const points = octantes[octantIndex];
            let pointIndex = 0;
            const drawNextPoint = () => {
                if (pointIndex < points.length) {
                    window.myChart.data.datasets[octantIndex].data.push({ x: points[pointIndex][0], y: points[pointIndex][1] });
                    window.myChart.update();
                    pointIndex++;
                    setTimeout(drawNextPoint, 5); // Añadir un retraso de 100ms entre cada punto
                } else if (octantIndex < 7) {
                    drawOctant(octantIndex + 1);
                } else {
                    // Animar el dibujo del relleno del círculo punto por punto
                    let fillIndex = 0;
                    const drawNextFillPoint = () => {
                        if (fillIndex < puntosRelleno.length) {
                            window.myChart.data.datasets[8].data.push({ x: puntosRelleno[fillIndex][0], y: puntosRelleno[fillIndex][1] });
                            window.myChart.update();
                            fillIndex++;
                            setTimeout(drawNextFillPoint, 1); // Añadir un retraso de 100ms entre cada punto
                        }
                    };
                    drawNextFillPoint();
                }
            };
            drawNextPoint();
        };

        drawOctant(0);

        const octantHeaders = [
            ["N", "Pk", "Xk+1", "Yk-1"],
            ["Y", "X"],
            ["X", "-Y"],
            ["-Y", "X"],
            ["-Y", "-X"],
            ["-X", "-Y"],
            ["-X", "Y"],
            ["Y", "-X"]
        ];

        for (let i = 0; i < 8; i++) {
            const thead = document.getElementById(`tabla-octante-${i + 1}`).getElementsByTagName('thead')[0];
            const tbody = document.getElementById(`tabla-octante-${i + 1}`).getElementsByTagName('tbody')[0];
            thead.innerHTML = '';
            tbody.innerHTML = '';

            const headerRow = thead.insertRow();
            octantHeaders[i].forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });

            puntos.forEach((punto, index) => {
                // Filtrar puntos con valores .5
                if (punto[0] % 1 !== 0 || punto[1] % 1 !== 0) {
                    return;
                }

                const row = tbody.insertRow();
                row.style.animation = 'fadeIn 0.5s ease-in-out';
                if (i === 0) {
                    const cellIteracion = row.insertCell(0);
                    const cellPk = row.insertCell(1);
                    const cellX = row.insertCell(2);
                    const cellY = row.insertCell(3);
                    cellIteracion.textContent = index;
                    cellPk.textContent = punto[2];
                    cellX.textContent = punto[0] + 1;
                    cellY.textContent = punto[1];
                } else {
                    const cellX = row.insertCell(0);
                    const cellY = row.insertCell(1);
                    if (i === 1) {
                        cellX.textContent = punto[1];
                        cellY.textContent = punto[0];
                    } else if (i === 2) {
                        cellX.textContent = punto[0];
                        cellY.textContent = -punto[1];
                    } else if (i === 3) {
                        cellX.textContent = -punto[1];
                        cellY.textContent = punto[0];
                    } else if (i === 4) {
                        cellX.textContent = -punto[1];
                        cellY.textContent = -punto[0];
                    } else if (i === 5) {
                        cellX.textContent = -punto[0];
                        cellY.textContent = -punto[1];
                    } else if (i === 6) {
                        cellX.textContent = -punto[0];
                        cellY.textContent = punto[1];
                    } else if (i === 7) {
                        cellX.textContent = punto[1];
                        cellY.textContent = -punto[0];
                    }
                }
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
    });
});