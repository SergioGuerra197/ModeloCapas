function setEliminarPorcino(idporcinos) {
    // Establecer la URL de eliminación en el botón de confirmación del modal
    document.getElementById('confirmarEliminarBtn').href = '/porcino/delete/' + idporcinos + '/';
}