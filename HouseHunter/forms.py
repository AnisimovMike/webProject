from django import forms


class UserForm(forms.Form):
    square = forms.IntegerField()
    address = forms.CharField()
    email_address = forms.EmailField()
    type = forms.ChoiceField(choices=(("commercial", "commercial"), ("country", "country"), ("residential", "residential")))
    price = forms.IntegerField()
    foto_link = forms.CharField(max_length=30)
    field_order = ["type", "square", "address", "email_address", "price", "foto_link"]


class LoadObject(forms.Form):
    obj_id = forms.IntegerField()
    method_type = forms.ChoiceField(choices=((1, "get"), (2, "delete")))


class AuthorizationForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    new_action = forms.CharField()
