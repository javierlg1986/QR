function creaQRdb() {
    $(`#confirma_crea_QR_db`).removeClass("hidden");
    $(`#inicia_crea_QR_db`).addClass("hidden");
}

function confirmaCreaQRdb() {
    $.post('/_crea_QR_db', {
        token: token
    }, function(data) {
    $(`#confirma_crea_QR_db`).addClass("hidden");
    $(`#inicia_crea_QR_db`).removeClass("hidden");
    creaQRimagen();
    }).fail(function(data) {
        errorMsg(data);
    });
}

function cancelaCreaQRdb() {
    $(`#confirma_crea_QR_db`).addClass("hidden");
    $(`#inicia_crea_QR_db`).removeClass("hidden");
}

function creaQRimagen(token_QR) {
    $.post('/_crea_QR_imagen/'+token_QR, {
        token: token
    }, function(data) {
    $(`#confirma_crea_QR_db`).addClass("hidden");
    $(`#inicia_crea_QR_db`).removeClass("hidden");
    }).fail(function(data) {
        errorMsg(data);
    });
}

function asignaQRinv() {
    $.post('/_lista_QR_no_asignados', {
        token: token
    }, function(data) {
    $(`#confirma_asignar_QR`).removeClass("hidden");
    $(`#inicia_asignar_QR`).addClass("hidden");
    creaQRimagen();
    }).fail(function(data) {
        errorMsg(data);
    });
}


function muestralistadoAsignaQRinv() {
}

function confirmaAsignaQRinv() {
}

function cancelaAsignaQRinv() {
    $(`#confirma_asignar_QR`).addClass("hidden");
    $(`#inicia_asignar_QR`).removeClass("hidden");
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
