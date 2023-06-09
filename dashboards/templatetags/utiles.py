from django import template

register = template.Library()

@register.filter(name='es_positivo_o_negativo')
def es_positivo_o_negativo(porciento_crecimiento_mensual):
    if porciento_crecimiento_mensual < 0:
        return "negativo"
    elif porciento_crecimiento_mensual > 0:
        return "positivo"
    else:
        return "cero"

@register.filter(name='obtener_primera_letra')
def obtener_primera_letra(cadena):
    primera_letra = cadena[0].upper()
    return primera_letra

