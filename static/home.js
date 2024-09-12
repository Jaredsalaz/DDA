
//boton de limpiar 
document.getElementById('clear-button').addEventListener('click', function() {
    // Limpiar los campos del formulario
    document.getElementById('formulario').reset();

    // Limpiar la gráfica
    if (window.myChart) {
        window.myChart.destroy();
        window.myChart = null;
    }

    // Limpiar la tabla
    const tbody = document.getElementById('tabla-puntos').getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';

    // Limpiar el texto del caso determinado
    document.getElementById('caso-determinado').textContent = '';
});

//animaciones de las cortinas de bienvenida
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
            const tablaPuntos = document.getElementById('tabla-puntos');

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

            tablaPuntos.style.opacity = 1;
            tablaPuntos.style.animationDelay = '5.5s';
        }, 2000); // Espera a que termine la animación de las cortinas
    }, 3000); // Duración de la animación de bienvenida
});

// Añade un evento 'submit' al formulario con id 'formulario'
document.getElementById('formulario').addEventListener('submit', function(event) {
    // Previene el comportamiento por defecto del formulario (recargar la página)
    event.preventDefault();

    // Obtiene los valores de los campos de entrada del formulario
    const x0 = document.getElementById('x0').value;
    const y0 = document.getElementById('y0').value;
    const x1 = document.getElementById('x1').value;
    const y1 = document.getElementById('y1').value;

    // Reproduce un sonido al enviar el formulario
    const audio = document.getElementById('audio-siiuuu');
    audio.play().then(() => {
        console.log('Audio reproducido correctamente');
    }).catch(error => {
        console.error('Error al reproducir el audio:', error);
    });

    // Muestra una animación de carga
    document.getElementById('loading').style.display = 'block';

    // Envía una solicitud POST al servidor para calcular los puntos
    fetch('/calcular_puntos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ x0, y0, x1, y1 }) // Envía los valores como JSON
    })
    .then(response => response.json()) // Convierte la respuesta a JSON
    .then(data => {
        // Oculta la animación de carga
        document.getElementById('loading').style.display = 'none';

        // Procesa los datos recibidos
        const puntos = data.puntos;
        const pendiente = data.pendiente;
        const caso = data.caso; // Nuevo campo para el caso determinado
        const ctx = document.getElementById('grafica').getContext('2d');

        // Destruye cualquier instancia previa de Chart.js para evitar superposiciones
        if (window.myChart) {
            window.myChart.destroy();
        }

        // Crea una nueva gráfica con los puntos calculados
        window.myChart = new Chart(ctx, {
            type: 'scatter', // Cambia el tipo a 'scatter' para manejar mejor los puntos individuales
            data: {
                datasets: [{
                    label: 'Línea DDA',
                    data: puntos.map(p => ({ x: p[0], y: p[1] })), // Datos de los puntos
                    borderColor: 'rgba(75, 192, 192, 1)', // Color de la línea
                    borderWidth: 2, // Ancho de la línea
                    showLine: true, // Mostrar la línea entre los puntos
                    fill: false, // No rellenar debajo de la línea
                    pointRadius: 5, // Radio de los puntos
                    pointHoverRadius: 7, // Radio de los puntos al pasar el ratón
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)', // Color de fondo de los puntos
                    pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)', // Color de fondo de los puntos al pasar el ratón
                    pointHoverBorderColor: 'rgba(255, 99, 132, 1)', // Color del borde de los puntos al pasar el ratón
                    pointHoverBorderWidth: 2, // Ancho del borde de los puntos al pasar el ratón
                    pointStyle: 'circle' // Estilo de los puntos
                }]
            },
            options: {
                plugins: {
                    tooltip: {
                        callbacks: {
                            // Formato de la etiqueta del tooltip
                            label: function(context) {
                                return `Punto (${context.raw.x.toFixed(4)}, ${context.raw.y.toFixed(4)})`;
                            }
                        }
                    },
                    zoom: {
                        pan: {
                            enabled: true, // Habilita el paneo
                            mode: 'xy' // Paneo en ambas direcciones
                        },
                        zoom: {
                            wheel: {
                                enabled: false // Habilita el zoom con la rueda del ratón
                            },
                            pinch: {
                                enabled: true // Habilita el zoom con pellizco
                            },
                            mode: 'xy' // Zoom en ambas direcciones
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'linear', // Tipo de escala lineal para el eje x
                        position: 'bottom' // Posición del eje x en la parte inferior
                    },
                    y: {
                        type: 'linear', // Tipo de escala lineal para el eje y
                        position: 'left' // Posición del eje y en la parte izquierda
                    }
                },
                animation: {
                    onComplete: function() {
                        // Oculta la animación de carga al completar la animación de la gráfica
                        document.getElementById('loading').style.display = 'none';
                    }
                }
            }
        });

        // Actualiza la tabla de puntos con los nuevos datos
        const tbody = document.getElementById('tabla-puntos').getElementsByTagName('tbody')[0];
        tbody.innerHTML = ''; // Limpia el contenido previo de la tabla
        puntos.forEach((punto, index) => {
            const row = tbody.insertRow(); // Inserta una nueva fila
            row.style.animation = 'fadeIn 0.5s ease-in-out'; // Añade una animación de entrada
            const cellIteracion = row.insertCell(0); // Celda para el índice
            const cellX = row.insertCell(1); // Celda para la coordenada x
            const cellY = row.insertCell(2); // Celda para la coordenada y
            const cellPendiente = row.insertCell(3); // Celda para la pendiente
            cellIteracion.textContent = index; // Asigna el índice a la celda
            cellX.textContent = punto[0].toFixed(4); // Asigna la coordenada x a la celda
            cellY.textContent = punto[1].toFixed(4); // Asigna la coordenada y a la celda
            cellPendiente.textContent = pendiente.toFixed(4); // Asigna la pendiente a la celda
        });

        // Muestra el caso determinado en el elemento con id 'caso-determinado'
        document.getElementById('caso-determinado').textContent = `Caso: ${caso}`;
    })
    .catch(error => {
        console.error('Error:', error);
        // Oculta la animación de carga en caso de error
        document.getElementById('loading').style.display = 'none';
    });
});