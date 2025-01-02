function creaQRdb() {
    $(`#confirma_crea_QR_db`).removeClass("hidden");
    $(`#inicia_crea_QR_db`).addClass("hidden");
}

function confirmaCreaQRdb() {
    $.post('/_crea_QR', {
        token: token
    }, function(data) {
    $(`#confirma_crea_QR_db`).addClass("hidden");
    $(`#inicia_crea_QR_db`).removeClass("hidden");
    $(`#panel_novo_QR_creado`).removeClass("hidden");
    $(`#panel_ver_QR_creado`).html(data);
    }).fail(function(data) {
        errorMsg(data);
    });
}

function cancelaCreaQRdb() {
    $(`#confirma_crea_QR_db`).addClass("hidden");
    $(`#inicia_crea_QR_db`).removeClass("hidden");
}

function iniciaAsignaQRinv() {
    listadoQRnoasignados = muestralistadoAsignaQRinv();

    $(`#confirma_asignar_QR`).removeClass("hidden");
    $(`#inicia_asignar_QR`).addClass("hidden");
}

function muestralistadoAsignaQRinv() {
    $.post('/_listado_elementos_sin_QR', {
        token: token
    }, function(data) {
        $(`#confirma_asignar_QR`).removeClass("hidden");
        $(`#inicia_asignar_QR`).addClass("hidden");
        $(`#panel_exterior_listado_elementos_sin_QR`).html(data);
    }).fail(function(data) {
        errorMsg(data);
    });
}

function preseleccionaElementoAsignarQR(id_tabla_request, id_en_tabla_request) {
    $(`#elemento${id_en_tabla_request}tabla${id_tabla_request}`).toggleClass("selected");
    $(`#boton_asignar_QR_inhabilitado`).toggleClass("hidden");
    $(`#boton_asignar_QR_habilitado`).toggleClass("hidden");
    $(`#tabla_seleccionada_asignar_QR`).val(id_tabla_request);
    $(`#elemento_seleccionado_asignar_QR`).val(id_en_tabla_request);
    console.log($(`#tabla_seleccionada_asignar_QR`).val());
    console.log($(`#elemento_seleccionado_asignar_QR`).val());
    console.log($(`#elemento${id_en_tabla_request}tabla${id_tabla_request}`).hasClass("selected"));
}

function confirmaAsignaQRinv(token_QR_request) {
    $.post('/_asigna_QR_inv', {        
        token_QR_request:token_QR_request,
        tabla_request:$(`#tabla_seleccionada_asignar_QR`).val(),
        id_en_tabla_request:$(`#elemento_seleccionado_asignar_QR`).val(),
        token: token
    }, function(data) {
        console.log(data);
        $(`#confirma_asignar_QR`).addClass("hidden");
        $(`#inicia_asignar_QR`).removeClass("hidden");
        preseleccionaElementoAsignarQR($(`#tabla_seleccionada_asugnar_QR`).val(), $(`#elemento_seleccionado_asignar_QR`).val())
        $(`#panel_exterior_listado_elementos_sin_QR`).html();
    }).fail(function(data) {
        errorMsg(data);
    });
}

function cancelaAsignaQRinv() {
    $(`#confirma_asignar_QR`).addClass("hidden");
    $(`#inicia_asignar_QR`).removeClass("hidden");
    $(".elemento_lista_sin_QR").each(function() {
        $(this).removeClass("selected");
        $(`#boton_asignar_QR_inhabilitado`).removeClass("hidden");
        $(`#boton_asignar_QR_habilitado`).addClass("hidden");
    });
}


// function actualizaQRdb(id_QR) {
//     $.post('/_actualiza_QR_db', {
//         id_traballo: id_QR,
//         valores: $(`#formularioQR${id_QR} .edited`).not(".vinculado").serialize(),
//         token: token
//     }, function(data) {
//         finalizaActualizarCambios(`QR${id_QR}`)
//     }).fail(function(data) {
//         errorMsg(data);
//     });
// }

// function borraQR(id_QR) {
//     if (!confirm("Está seguro de que desexa borrar o QR?")) {
//         return undefined
//     }
//     $.post('/_borra_QR_db', {
//         id_QR: id_QR,
//         token: token
//     }, function(data) {
//         window.location.replace(`/`);
//     }).fail(function(data) {
//         errorMsg(data);
//     });
// }
