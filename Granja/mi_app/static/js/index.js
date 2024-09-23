// Funcion cargar información detallada del cliente
function loadClienteInfo(cedula) {
    // Realizar la solicitud AJAX para obtener los datos del cliente
    $.ajax({
        url: '/cliente/' + cedula + '/',  // La URL que obtiene los datos del cliente según su cédula
        type: 'GET',
        success: function(response) {
            // Llenar los campos del modal con los datos del cliente
            $('#modal-cedula').text(response.cedula);
            $('#modal-nombre').text(response.nombre);
            $('#modal-apellidos').text(response.apellidos);
            $('#modal-direccion').text(response.direccion);
            $('#modal-telefono').text(response.telefono);

            $('#cerdos-list').empty();
            // Mostrar el modal
            
            if (response.cerdos.length > 0) {
                response.cerdos.forEach(function(cerdo) {
                    $('#cerdos-list').append(
                        '<li class="list-group-item">' +
                        '<strong>ID:</strong> ' + cerdo.id + '<br>' +
                        '<strong>Edad:</strong> ' + cerdo.edad + ' años<br>' +
                        '<strong>Peso:</strong> ' + cerdo.peso + ' kg<br>' +
                        '<strong>Raza:</strong> ' + cerdo.raza +
                        '</li>'
                    );
                });
                console.log(response)
        } else {
            // Si no hay cerdos asociados
            $('#cerdos-list').append('<li class="list-group-item">No hay porcinos registrados para este cliente.</li>');
        }
        
        $('#infoModal').modal('show');


        },
        error: function(error) {
            console.log('Error al obtener los datos del cliente:', error);
        }
    });
}



// Funcion para editar cliente 
function setEditarCliente(cedula) {
    // Realizar una solicitud AJAX para obtener los datos del cliente
    $.ajax({
        url: '/cliente/' + cedula + '/',  // La URL que obtiene los datos del cliente según la cédula
        type: 'GET',
        success: function(response) {
            // Llenar los campos del modal con los datos del cliente
            $('#modal-cedula-mod').val(response.cedula);
            $('#modal-nombre-mod').val(response.nombre);
            $('#modal-apellidos-mod').val(response.apellidos);
            $('#modal-direccion-mod').val(response.direccion);
            $('#modal-telefono-mod').val(response.telefono);
            
            // Cambiar la acción del formulario para que apunte a la vista de actualización
            $('#formEditarCliente').attr('action', '/actualizar_cliente/' + response.cedula + '/');
            
            // Mostrar el modal
            $('#editarClienteModal').modal('show');
        },
        error: function(error) {
            console.log('Error al obtener los datos del cliente:', error);
        }
    });
}

// Funcion para eliminar cliente 
function setEliminarCliente(cedula) {
    // Establecer la URL de eliminación en el botón de confirmación del modal
    document.getElementById('confirmarEliminarBtn').href = '/eliminar_cliente/' + cedula + '/';
}

function setClienteCedula(cedula){
    document.getElementById('cliente_cedula').value = cedula;
    console.log(cedula)
}

