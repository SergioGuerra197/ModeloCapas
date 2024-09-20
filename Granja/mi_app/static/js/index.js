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
        // Mostrar el modal
        $('#infoModal').modal('show');

        },
        error: function(error) {
            console.log('Error al obtener los datos del cliente:', error);
        }
    });
}