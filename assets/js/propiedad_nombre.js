$('.valor').each(function () {
    var h = $(this).parent().find('label').html( propiedades_nombres[cont]);
    cont++;
});