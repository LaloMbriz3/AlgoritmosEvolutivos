// const declara referencias que no se reasignan; el DOM se busca por su id HTML.
const botonGenerar = document.getElementById("generarHorario");
const selectorGrupo = document.getElementById("selectorGrupo");
const contenedorHorarios = document.getElementById("contenedorHorarios");
const sesionesElemento = document.getElementById("sesiones");
const penalizacionElemento = document.getElementById("penalizacion");
const mensaje = document.getElementById("mensaje");


// Actualiza el texto de estado que se muestra debajo de los controles.
function mostrarMensaje(texto) {

    mensaje.textContent = texto;

}


// Construye una tarjeta interactiva con el detalle de una sesión programada.
function crearClase(clase) {

    // createElement crea nodos HTML y las propiedades siguientes definen su contenido.
    const elemento = document.createElement("div");

    elemento.className = "clase";

    // Las comillas invertidas crean una plantilla multilínea; ${...} inserta valores.
    elemento.innerHTML = `
        <div class="materia">
            ${clase.materia}
        </div>

        <div class="profesor">
            ${clase.profesor}
        </div>

        <div class="salon">
            ${clase.salon}
        </div>

        <div class="horario-clase">
            ${clase.hora_inicio} - ${clase.hora_fin}
        </div>
    `;


    // addEventListener asocia una función que se ejecuta cuando ocurre el evento.
    elemento.addEventListener("click", function () {

        alert(
            // Las plantillas interpoladas y + concatenan el texto mostrado en la alerta.
            `Materia: ${clase.materia}\n` +
            `Profesor: ${clase.profesor}\n` +
            `Salón: ${clase.salon}\n` +
            `Grupo: ${clase.grupo}\n` +
            `Horario: ${clase.hora_inicio} - ${clase.hora_fin}`
        );

    });


    return elemento;

}


// Agrupa las sesiones por grupo y construye una tabla de días y horas para cada uno.
function mostrarHorario(clases) {

    contenedorHorarios.innerHTML = "";


    // La estructura por grupo permite renderizar cada horario de forma independiente.
    const grupos = {};

    // forEach ejecuta una función flecha por cada elemento de la lista.
    clases.forEach(clase => {

        if (!grupos[clase.grupo_id]) {

            grupos[clase.grupo_id] = {
                nombre: clase.grupo,
                clases: []
            };

        }

        grupos[clase.grupo_id].clases.push(clase);

    });


    // Object.entries convierte propiedades del objeto en pares [clave, valor].
    Object.entries(grupos).forEach(
        ([grupoId, grupo]) => {

            // La destructuración asigna los dos valores del par a variables con nombre.
            const seccion = document.createElement("section");

            seccion.className = "grupo";

            // dataset escribe el atributo data-grupo, que luego usa el filtro.
            seccion.dataset.grupo = grupoId;


            const titulo = document.createElement("h2");

            titulo.textContent =
                `Grupo ${grupo.nombre}`;


            seccion.appendChild(titulo);


            const tabla = document.createElement("table");

            tabla.className = "horario-tabla";


            // La tabla estática se inserta como HTML; luego se completa el tbody con nodos.
            tabla.innerHTML = `
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Lunes</th>
                        <th>Martes</th>
                        <th>Miércoles</th>
                        <th>Jueves</th>
                        <th>Viernes</th>
                    </tr>
                </thead>

                <tbody></tbody>
            `;


            const cuerpo =
                tabla.querySelector("tbody");


            // Debe corresponder a las horas de inicio disponibles en los bloques JSON.
            const horas = [
                "07:00",
                "08:00",
                "09:00",
                "10:00",
                "11:00",
                "12:00",
                "13:00",
                "14:00"
            ];


            const dias = [
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes"
            ];


            horas.forEach(hora => {

                const fila =
                    document.createElement("tr");


                const horaCelda =
                    document.createElement("td");

                horaCelda.className = "hora";

                horaCelda.textContent = hora;

                fila.appendChild(horaCelda);


                // El bucle anidado recorre los días para llenar cada fila horaria.
                dias.forEach(dia => {

                    const celda =
                        document.createElement("td");

                    celda.className =
                        "celda-clase";


                    // find devuelve el primer elemento que satisface la condición, o undefined.
                    const claseEncontrada =
                        grupo.clases.find(clase =>
                            clase.dia === dia &&
                            clase.hora_inicio === hora
                        );


                    if (claseEncontrada) {

                        celda.appendChild(
                            crearClase(claseEncontrada)
                        );

                    }


                    fila.appendChild(celda);

                });


                cuerpo.appendChild(fila);

            });


            seccion.appendChild(tabla);

            contenedorHorarios.appendChild(seccion);

        }
    );


    aplicarFiltro();

}


// Oculta los grupos que no coinciden con la selección actual.
function aplicarFiltro() {

    const grupoSeleccionado =
        selectorGrupo.value;


    const grupos =
        document.querySelectorAll(".grupo");


    grupos.forEach(grupo => {

        // === compara sin conversión de tipos; || acepta cualquiera de las dos condiciones.
        if (
            grupoSeleccionado === "todos" ||
            grupo.dataset.grupo === grupoSeleccionado
        ) {

            grupo.style.display = "";

        } else {

            grupo.style.display = "none";

        }

    });

}


// Solicita al servidor otra solución y actualiza la vista sin recargar la página.
// async permite usar await y hace que la función retorne una Promise.
async function generarHorario() {

    botonGenerar.disabled = true;

    botonGenerar.textContent =
        "Generando...";

    mostrarMensaje(
        "El algoritmo está buscando una nueva solución..."
    );


    try {

        // Comprueba el estado HTTP antes de interpretar la respuesta como JSON.
        // await pausa esta función hasta recibir la respuesta HTTP del servidor.
        const respuesta =
            await fetch("/generar");


        if (!respuesta.ok) {

            throw new Error(
                "No se pudo generar el horario."
            );

        }


        // json() también es asíncrono: interpreta el cuerpo de la respuesta como objeto JS.
        const resultado =
            await respuesta.json();


        mostrarHorario(
            resultado.clases
        );


        sesionesElemento.textContent =
            resultado.sesiones;


        penalizacionElemento.textContent =
            resultado.penalizacion;


        mostrarMensaje(
            "Nuevo horario generado correctamente."
        );


    // catch maneja errores de red o del procesamiento; finally siempre restaura el botón.
    } catch (error) {

        mostrarMensaje(
            "Ocurrió un error al generar el horario."
        );

        console.error(error);

    } finally {

        botonGenerar.disabled = false;

        botonGenerar.textContent =
            "Generar nuevo horario";

    }

}


// Estos listeners conectan los eventos del selector y el botón con sus manejadores.
selectorGrupo.addEventListener(
    "change",
    aplicarFiltro
);


botonGenerar.addEventListener(
    "click",
    generarHorario
);