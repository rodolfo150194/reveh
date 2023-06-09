if($.trim(mensaje) != ''){
    $.each(mensaje, function (){
        Swal.fire({
            text: mensaje[cont],
            icon: "success",
            confirmButtonText: "Aceptar",
        });
    });
}
