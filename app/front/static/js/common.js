function prevenirSalir() {
  if ($(".edited").length > 0) {
    window.onbeforeunload = function() {return 0;}
  } else {
    window.onbeforeunload = null;
  }
}

function errorMsg(data) {
  if (typeof data.responseJSON != "undefined") {
    var error = data.responseJSON.error;
  } else {
    var error = "Erro no servidor. ";
  }
  alert(error + " Se o problema persiste contacte co administrador.");
}

function openMenu() {
  $(".icons_box").removeClass("hidden");
}
function closeMenu() {
  $(".icons_box").addClass("hidden");
}

function replaceDecimalPoint(esto) {
  var value = $(esto).val();
  var replaced = value.replace(",", ".");
  replaced = replaced.replace("..", ".");
  replaced = replaced.replace(/[a-zA-Z ]/g, "");
  $(esto).val(replaced);
}

function toggleEdit(variable) {
  $(`.uploadButton${variable}`).addClass("hidden");
  $(`.edit${variable}`).toggleClass("hidden");
  $(`.label${variable}`).toggleClass("editMode")
}

function changeValue(esto) {
  let variable = $(esto).attr('id').split("value-")[1];
  let tabla_id_tabla = variable.split("-")[0];
  
  $(esto).addClass("edited");
  $(`#label-${variable}`).addClass("edited");
  $(`#upload${tabla_id_tabla}`).removeClass("hidden");

  prevenirSalir();
}

function addOnInput(value, esto) {
  let variable = getVariableBoton(esto);
  let tabla_id_tabla = variable.split("-")[0];
  let old_value = $(`#value-${variable}`).val();
  let new_value = `${old_value}${value}`;
  $(`#value-${variable}`)
    .val(new_value)
    .addClass("edited");
  $(`#label-${variable}`).addClass("edited");
  $(`#upload${tabla_id_tabla}`).removeClass("hidden");
  $(esto).addClass("clicked");
  setTimeout(() => {
    $(esto).removeClass("clicked");
  }, 200);
}

function writeOnInput(value, esto) {
  let variable = getVariableBoton(esto);
  let tabla_id_tabla = variable.split("-")[0];
  $(`#value-${variable}`)
    .val(value)
    .addClass("edited");
  $(`#label-${variable}`).addClass("edited");
  $(`#upload${tabla_id_tabla}`).removeClass("hidden");
  $(`.button-${variable}`)
    .removeClass("clicked").
    removeClass("edited");
  $(esto).addClass("edited");
  prevenirSalir();
}

function getVariableBoton(esto) {
  let clases = $(esto).attr("class").split(" ");  
  for (i in clases) {
    if (clases[i].split("button-").length > 1) {
      if (clases[i].split("button-")[1] != "") {
        return clases[i].split("button-")[1]
      }
    }
  }
};

function editInputDatalist(esto) {
  let datalist = $(esto).attr('list');
  let tabla_id_tabla = $(esto).attr("id").split("-")[1];
  let index = $(esto).attr("id").split("-")[2];
  let value = $(esto).val();
  if ($(`#${datalist}`)[0].options.namedItem(value)) {
    $(esto).removeClass("incorrect")
      .addClass("edited");
    $(`#value-${tabla_id_tabla}-${index}-vinculado`)
      .addClass("edited")
      .val($(`#${datalist}`)[0].options[value].getAttribute("campo"));
    $(`#label-${tabla_id_tabla}-${index}`).addClass("edited");
    $(`#upload${tabla_id_tabla}`).removeClass("hidden");
  } else {
    $(esto)
      .addClass("incorrect")
      .removeClass("edited");
    $(`#value-${tabla_id_tabla}-${index}-vinculado`)
      .removeClass("edited")
      .val("");
    $(`#label-${tabla_id_tabla}-${index}`).removeClass("edited");
    $(`#upload${tabla_id_tabla}`).addClass("hidden");
  }
}

function cancelaActualizarCambios(tabla_id_tabla) {
  $(`#formulario${tabla_id_tabla} input.edited, #formulario${tabla_id_tabla} textarea.edited`).each( function() {
    let apellido = $(this).attr("id").split(`${tabla_id_tabla}-`)[1];
    let variable = `${tabla_id_tabla}-${apellido}`
    
    $(this).removeClass("edited");    
    $(`#label-${variable}`).removeClass("edited");

    $(this).val($(`#text-${variable}`).text());
    
    var this_input = this;
    $(`.button.button-${variable}`).each( function() {
      $(this).removeClass("edited");
      if ($(this).text() == $(this_input).val()){
        $(this).addClass("clicked");
      }
    })
  });
  $(`#upload${tabla_id_tabla}`).addClass("hidden");
  prevenirSalir();
}

function finalizaActualizarCambios(tabla_id_tabla, formulario="") {
  if (formulario == "") {
    formulario = tabla_id_tabla
  }
  $(`#formulario${formulario} input.edited, #formulario${tabla_id_tabla} textarea.edited`).each( function() {
    let apellido = $(this).attr("id").split(`${tabla_id_tabla}-`)[1];
    let variable = `${tabla_id_tabla}-${apellido}`
    
    $(this).removeClass("edited");    
    $(`#label-${variable}`).removeClass("edited");

    $(`#text-${variable}`).text($(this).val());
    
    var this_input = this;
    $(`.button.button-${variable}`).each( function() {
      if ($(this).hasClass("edited")) {
        $(`#text-${variable}`).text($(this).text());
        $(this).removeClass("edited");
        $(this).addClass("clicked")
      }
    })
  });
  $(`#upload${tabla_id_tabla}`).addClass("hidden");
  prevenirSalir();
}


$(document).ready(function() {
  $(document).mouseup(function(e) {
    // var container = $(".icons_box");
    // if (!container.is(e.target) && container.has(e.target).length === 0) {
        closeMenu();
    // }
  });
});