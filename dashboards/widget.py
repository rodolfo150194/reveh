from django import forms
from django.template.loader import render_to_string


class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("pages/form/popupplus.html", {'field': name})
        return html+popupplus

class SelectMultipleWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(SelectMultipleWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("pages/form/popupplus.html", {'field': name})
        return html+popupplus