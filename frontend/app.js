// Consultar todos los registros
function consulta_general() {
    let url = "http://127.0.0.1:5000/";
    fetch(url)
        .then(response => response.json())
        .then(data => visualizar(data))
        .catch(error => console.log(error));

    const visualizar = (data) => {
        console.log(data);
        let b = "";
        for (let i = 0; i < data.baul.length; i++) {
            b += `
                <tr>
                    <td>${data.baul[i].id_baul}</td>
                    <td>${data.baul[i].Plataforma}</td>
                    <td>${data.baul[i].usuario}</td>
                    <td>${data.baul[i].clave}</td>
                    <td>
                        <a href="edit.html?id=${data.baul[i].id_baul}">Editar</a>
                        <button onclick="eliminar(${data.baul[i].id_baul})">Eliminar</button>
                    </td>
                </tr>
            `;
        }
        document.getElementById('data').innerHTML = b;
    };
}

// Eliminar un registro
function eliminar(id) {
    let url = `http://127.0.0.1:5000/eliminar/${id}`;
    fetch(url, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(res => visualizar(res));

    const visualizar = (res) => {
        swal("Mensaje", `Registro ${res.mensaje} exitosamente`, "success").then(() => {
            window.location.reload();
        });
    };
}

// Registrar un nuevo registro
function registrar() {
    let url = "http://127.0.0.1:5000/registro/";
    let plat = document.getElementById("plataforma").value;
    let usua = document.getElementById("usuario").value;
    let clav = document.getElementById("clave").value;
    let data = { plataforma: plat, usuario: usua, clave: clav };
    console.log(data);
    fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(res => res.json())
        .catch(error => console.error("Error:", error))
        .then(response => visualizar(response));

    const visualizar = (response) => {
        console.log("Success:", response);
        if (response.mensaje === "Error") {
            swal("Mensaje", "Error en el registro", "error");
        } else {
            swal("Mensaje", "Registro agregado exitosamente", "success").then(() => {
                window.location.href = "index.html";
            });
        }
    };
}

// Consultar un registro individual
function consulta_individual(id) {
    let url = `http://127.0.0.1:5000/consulta_individual/${id}`;
    fetch(url)
        .then(response => response.json())
        .then(data => visualizar(data))
        .catch(error => console.log(error));

    const visualizar = (data) => {
        console.log(data);
        document.getElementById("idbaul").value = data.baul.id_baul;
        document.getElementById("plataforma").value = data.baul.Plataforma;
        document.getElementById("usuario").value = data.baul.usuario;
        document.getElementById("clave").value = data.baul.clave;
    };
}

// Modificar un registro
function modificar(id) {
    let url = `http://127.0.0.1:5000/actualizar/${id}`;
    let plat = document.getElementById("plataforma").value;
    let usua = document.getElementById("usuario").value;
    let clav = document.getElementById("clave").value;
    let data = { plataforma: plat, usuario: usua, clave: clav };
    console.log(data);
    fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(res => res.json())
        .catch(error => console.error("Error:", error))
        .then(response => visualizar(response));

    const visualizar = (response) => {
        console.log("Success:", response);
        if (response.mensaje === "Error") {
            swal("Mensaje", "Error en el registro", "error");
        } else {
            swal("Mensaje", "Registro actualizado exitosamente", "success").then(() => {
                window.location.href = "index.html";
            });
        }
    };
}