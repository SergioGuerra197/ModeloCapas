function loadPorcinoInfo(idporcinos) {
    // Realizar la solicitud AJAX para obtener los datos del cliente
    $.ajax({
        url: 'porcino/profile/' + idporcinos + '/',  // La URL que obtiene los datos del cliente según su cédula
        type: 'GET',
        success: function(response) {
            // Llenar los campos del modal con los datos del cliente
            $('#modal-idporcino').text(response.idporcinos);
            $('#modal-edad').text(response.edad);
            $('#modal-peso').text(response.peso);
            $('#modal-raza').text(response.razas_idrazas);
            $('#modal-alimentacion').text(response.clientes_cedula);
            $('#modal-idpropietario').text(response.clientes_cedula);
        
        $('#infoModal').modal('show');


        },
        error: function(error) {
            console.log('Error al obtener los datos del porcino:', error);
        }
    });
}

function setEliminarPorcino(idporcinos) {
    // Establecer la URL de eliminación en el botón de confirmación del modal
    document.getElementById('confirmarEliminarBtn').href = '/porcino/delete/' + idporcinos + '/';
}