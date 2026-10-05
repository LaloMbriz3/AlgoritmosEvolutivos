const botonGenerar = document.getElementById("generarHorario");
const selectorGrupo = document.getElementById("selectorGrupo");
const contenedorHorarios = document.getElementById("contenedorHorarios");
const sesionesElemento = document.getElementById("sesiones");
const penalizacionElemento = document.getElementById("penalizacion");
const mensaje = document.getElementById("mensaje");


function mostrarMensaje(texto) {

    mensaje.textContent = texto;

}


function crearClase(clase) {

    const elemento = document.createElement("div");

    elemento.className = "clase";

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


    elemento.addEventListener("click", function () {

        alert(
            `Materia: ${clase.materia}\n` +
            `Profesor: ${clase.profesor}\n` +
            `Salón: ${clase.salon}\n` +
            `Grupo: ${clase.grupo}\n` +
            `Horario: ${clase.hora_inicio} - ${clase.hora_fin}`
        );

    });


    return elemento;

}


function mostrarHorario(clases) {

    contenedorHorarios.innerHTML = "";


    const grupos = {};

    clases.forEach(clase => {

        if (!grupos[clase.grupo_id]) {

            grupos[clase.grupo_id] = {
                nombre: clase.grupo,
                clases: []
            };

        }

        grupos[clase.grupo_id].clases.push(clase);

    });


    Object.entries(grupos).forEach(
        ([grupoId, grupo]) => {

            const seccion = document.createElement("section");

            seccion.className = "grupo";

            seccion.dataset.grupo = grupoId;


            const titulo = document.createElement("h2");

            titulo.textContent =
                `Grupo ${grupo.nombre}`;


            seccion.appendChild(titulo);


            const tabla = document.createElement("table");

            tabla.className = "horario-tabla";


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


                dias.forEach(dia => {

                    const celda =
                        document.createElement("td");

                    celda.className =
                        "celda-clase";


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


function aplicarFiltro() {

    const grupoSeleccionado =
        selectorGrupo.value;


    const grupos =
        document.querySelectorAll(".grupo");


    grupos.forEach(grupo => {

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


async function generarHorario() {

    botonGenerar.disabled = true;

    botonGenerar.textContent =
        "Generando...";

    mostrarMensaje(
        "El algoritmo está buscando una nueva solución..."
    );


    try {

        const respuesta =
            await fetch("/generar");


        if (!respuesta.ok) {

            throw new Error(
                "No se pudo generar el horario."
            );

        }


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


selectorGrupo.addEventListener(
    "change",
    aplicarFiltro
);


botonGenerar.addEventListener(
    "click",
    generarHorario
);