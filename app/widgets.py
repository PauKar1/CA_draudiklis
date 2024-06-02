from django import forms

class DeductibleSelect(forms.RadioSelect):
    template_name = 'widgets/deductible_select.html'
