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
    document.getElementById('tabla-region-1').getElementsByTagName('tbody')[0].innerHTML = '';
    document.getElementById('tabla-region-2').getElementsByTagName('tbody')[0].innerHTML = '';
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
    const Rx = parseFloat(document.getElementById('rx').value);
    const Ry = parseFloat(document.getElementById('ry').value);

    const audio = document.getElementById('audio-siiuuu');
    audio.play().then(() => {
        console.log('Audio reproducido correctamente');
    }).catch(error => {
        console.error('Error al reproducir el audio:', error);
    });

    document.getElementById('loading').style.display = 'block';

    fetch('/calcular_puntos_elipse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ Xc, Yc, Rx, Ry })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';

        const puntosBorde = data.puntos_borde;
        const region1 = data.region1;
        const region2 = data.region2;
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
                        label: 'Borde',
                        data: puntosBorde.map(p => ({ x: p[0], y: p[1] })),
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
                        label: 'Relleno',
                        data: puntosRelleno.map(p => ({ x: p[0], y: p[1] })),
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
                aspectRatio: Rx / Ry // Ajustar la proporción para que la elipse se vea correctamente
            }
        });

        // Llenar tabla de la Región 1
        const tablaRegion1 = document.getElementById('tabla-region-1').getElementsByTagName('tbody')[0];
        tablaRegion1.innerHTML = '';
        region1.slice(1).forEach((punto, index) => { // Ignorar el primer punto
            const row = tablaRegion1.insertRow();
            row.insertCell(0).innerText = index + 1; // Ajustar el índice para que comience en 1
            row.insertCell(1).innerText = region1[index][2]; // Pk del punto anterior
            row.insertCell(2).innerText = punto[0];
            row.insertCell(3).innerText = punto[1];
        });

        // Llenar tabla de la Región 2
        const tablaRegion2 = document.getElementById('tabla-region-2').getElementsByTagName('tbody')[0];
        tablaRegion2.innerHTML = '';
        region2.forEach((punto, index) => {
            const row = tablaRegion2.insertRow();
            row.insertCell(0).innerText = index;
            row.insertCell(1).innerText = punto[2];
            row.insertCell(2).innerText = punto[0];
            row.insertCell(3).innerText = punto[1];
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
    });
});