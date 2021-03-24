/* Comprueba si una cadena es vacía o contiene espacios en blanco */
function isEmpty(str) {
    return (!str || !/\S/.test(str));
}

/* Esta función se ejecuta cuando se clickea en el botón Guardar/Save
 * en el diálogo de creación de la DB */
function onButtonSaveClicked() {
    if(isEmpty(databaseName.text)) {
        databaseName.hasError = true;
    } else {
        // Emito la señal con los datos de la DB
        create(databaseName.text, dbLocation.text, dbFilename.text);
        close();
    }
}
