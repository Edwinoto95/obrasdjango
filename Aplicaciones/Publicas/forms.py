from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Obra, Constructor, Presupuesto ,Contacto
from django.core.exceptions import ValidationError

# Formulario personalizado para la creación de usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        label='Correo Electrónico'
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise ValidationError("El correo electrónico debe contener '@'.")
        return email

# Formulario de autenticación de usuario
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico o nombre de usuario'}),
        label='Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )

# Formulario para agregar una nueva obra
class ObraForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha de Inicio'
    )

    class Meta:
        model = Obra
        fields = ['nombre', 'ubicacion', 'fecha_inicio', 'estado', 'presupuesto_asignado', 'constructor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la obra'}),
            'ubicacion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ubicación de la obra', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'presupuesto_asignado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Presupuesto asignado', 'step': '0.01'}),
            'constructor': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_presupuesto_asignado(self):
        presupuesto = self.cleaned_data.get('presupuesto_asignado')
        if presupuesto <= 0:
            raise ValidationError("El presupuesto asignado debe ser un valor positivo.")
        return presupuesto

# Formulario para agregar un constructor
class ConstructorForm(forms.ModelForm):
    class Meta:
        model = Constructor
        fields = ['nombre_empresa', 'especialidad', 'contacto', 'archivo']  # Agregado archivo
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa constructora'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialidad de la empresa'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono o correo de contacto'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'})  # Nuevo campo
        }
# Formulario para agregar un presupuesto a una obra
class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['obra', 'monto_asignado']
        widgets = {
            'obra': forms.Select(attrs={'class': 'form-control'}),
            'monto_asignado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto asignado', 'step': '0.01'}),
        }

    def clean_monto_asignado(self):
        monto = self.cleaned_data.get('monto_asignado')
        if monto <= 0:
            raise ValidationError("El monto asignado debe ser un valor positivo.")
        return monto




from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
