from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ObraForm, ConstructorForm, PresupuestoForm
from .models import Obra, Constructor, Presupuesto
from django.contrib import messages
from django.urls import reverse
from django.db.models import Sum  # Import Sum from django.db.models
from django.http import JsonResponse


def pagina_principal(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    return render(request, 'inicio.html')

def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('inicio')
        messages.error(request, 'Error en el registro. Por favor, corrige los errores.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

def inicio_sesion(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {username}!')
                return redirect('inicio')
            messages.error(request, 'Credenciales inválidas.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    messages.success(request, '¡Sesión cerrada exitosamente!')
    return redirect('inicio_sesion')


@login_required
def inicio(request):
    obras_en_progreso = Obra.objects.filter(estado='en_construccion').count()
    obras_finalizadas = Obra.objects.filter(estado='finalizado').count()
    obras_planeadas = Obra.objects.filter(estado='planeado').count()
    presupuesto_total = Presupuesto.objects.all().aggregate(Sum('monto_asignado'))['monto_asignado__sum'] or 0
    gasto_actual = 0  # Reemplaza con la lógica real para calcular el gasto actual

    return render(request, 'inicio.html', {
        'obras_en_progreso': obras_en_progreso,
        'obras_finalizadas': obras_finalizadas,
        'obras_planeadas': obras_planeadas,
        'presupuesto_total': presupuesto_total,
        'gasto_actual': gasto_actual,
    })


@login_required
def lista_obras(request):
    obras = Obra.objects.all()
    return render(request, 'obra.html', {'obras': obras})


@login_required
def detalle_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    return render(request, 'obra.html', {'obra_detalle': obra})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Obra
from .forms import ObraForm  # Importamos el formulario

@login_required
def crear_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Obra creada exitosamente.')
            return redirect('lista_obras')
        else:
            messages.error(request, '❌ Error al crear la obra. Por favor, verifica los datos.')

    else:
        form = ObraForm()

    obras = Obra.objects.all()
    return render(request, 'obra.html', {'form': form, 'obras': obras})


@login_required
def editar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)

    if request.method == 'POST':
        form = ObraForm(request.POST, instance=obra)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Obra actualizada correctamente.")
            return redirect('lista_obras')
        else:
            messages.error(request, '❌ Error al actualizar la obra. Por favor, verifica los datos.')

    else:
        form = ObraForm(instance=obra)

    return render(request, 'obra.html', {'form': form, 'obra': obra, 'obras': Obra.objects.all()})



@login_required
def eliminar_obra(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    
    if request.method == 'POST':
        obra.delete()
        messages.success(request, '🗑️ Obra eliminada correctamente.')
        return redirect('lista_obras')
    
    return redirect('lista_obras')


@login_required
def lista_constructores(request):
    constructores = Constructor.objects.all()
    return render(request, 'empresa.html', {'constructores': constructores})


@login_required
def agregar_constructor(request):
    if request.method == 'POST':
        form = ConstructorForm(request.POST, request.FILES)  # Asegurar que se procesen archivos
        if form.is_valid():
            form.save()
            messages.success(request, 'Constructor agregado correctamente.')
            return redirect('lista_constructores')
        else:
            messages.error(request, 'Error al agregar el constructor. Por favor, corrige los errores.')
    else:
        form = ConstructorForm()

    return render(request, 'constructor.html', {'form': form})

@login_required
def editar_constructor(request, pk):
    constructor = get_object_or_404(Constructor, pk=pk)
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre_empresa = request.POST.get('nombre_empresa')
            especialidad = request.POST.get('especialidad')
            contacto = request.POST.get('contacto')

            # Validar que todos los campos requeridos estén presentes
            if not all([nombre_empresa, especialidad, contacto]):
                raise ValueError("Todos los campos son requeridos")

            # Actualizar los datos del constructor
            constructor.nombre_empresa = nombre_empresa
            constructor.especialidad = especialidad
            constructor.contacto = contacto
            constructor.save()

            # Manejar las obras asignadas si se enviaron en el formulario
            obras_seleccionadas = request.POST.getlist('obras')
            if obras_seleccionadas:
                constructor.obras.set(obras_seleccionadas)

            messages.success(request, '✅ Contratista actualizado exitosamente.')
            return redirect('lista_constructores')

        except ValueError as e:
            messages.error(request, f'❌ Error: {str(e)}')
        except Exception as e:
            messages.error(request, '❌ Error al actualizar el contratista. Por favor, verifica los datos.')
            print(f"Error: {str(e)}")  # Para debugging

    # Si es GET o hubo un error, mostrar el formulario con los datos actuales
    obras_disponibles = Obra.objects.all()
    return render(request, 'constructor.html', {
        'constructor': constructor,
        'obras_disponibles': obras_disponibles,
        'obras_asignadas': constructor.obras.all()
    })

@login_required
def eliminar_constructor(request, pk):
    constructor = get_object_or_404(Constructor, pk=pk)
    if request.method == 'POST':
        constructor.delete()
        return redirect('lista_constructores')
    return render(request, 'contructor.html', {'constructor': constructor})




from django.shortcuts import render, redirect, get_object_or_404
from .models import Presupuesto, Obra
from django.contrib.auth.decorators import login_required

def lista_presupuestos(request):
    presupuestos = Presupuesto.objects.all()
    obras = Obra.objects.all()
    return render(request, 'asignarpresupuesto.html', {'presupuestos': presupuestos, 'obras': obras})







from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Obra, Presupuesto

@login_required
def asignar_presupuesto(request):
    if request.method == 'POST':
        obra_id = request.POST.get('obra')
        monto_asignado = request.POST.get('monto_asignado')

        # Verificar si los datos son válidos
        if not obra_id or not monto_asignado:
            return JsonResponse({'success': False, 'error': 'Datos incompletos'}, status=400)

        obra = get_object_or_404(Obra, id=obra_id)

        # Crear el presupuesto
        Presupuesto.objects.create(
            obra=obra,
            monto_asignado=monto_asignado
        )

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Verifica si es una petición AJAX
            return JsonResponse({'success': True})

        return redirect('lista_presupuestos')

    return redirect('lista_presupuestos')




@login_required
def editar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    
    if request.method == "POST":
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Presupuesto actualizado correctamente.")
            return redirect('lista_presupuestos')  # Cambiado a 'lista_presupuestos' en vez de 'gestion_presupuestos'
        else:
            messages.error(request, "❌ Error al actualizar el presupuesto.")
    else:
        form = PresupuestoForm(instance=presupuesto)
    
    return render(request, 'asignarpresupuesto.html', {'presupuestos': Presupuesto.objects.all(), 'form': form, 'editar_presupuesto': presupuesto})




@login_required
def eliminar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    
    if request.method == 'POST':
        presupuesto.delete()

    return redirect('lista_presupuestos')





      

@login_required
def gestion(request):
    return render(request, 'gestion.html')





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Presupuesto
from .forms import PresupuestoForm

# Vista para listar presupuestos
def gestion_presupuestos(request):
    presupuestos = Presupuesto.objects.all()
    form = PresupuestoForm()
    return render(request, 'asignarpresupuesto.html', {'presupuestos': presupuestos, 'form': form})

# Vista para editar presupuesto
def editar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if request.method == "POST":
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            messages.success(request, "Presupuesto actualizado correctamente.")
            return redirect('gestion_presupuestos')
        else:
            messages.error(request, "Error al actualizar el presupuesto.")
    else:
        form = PresupuestoForm(instance=presupuesto)
    
    return render(request, 'asignarpresupuesto.html', {'presupuestos': Presupuesto.objects.all(), 'form': form, 'editar_presupuesto': presupuesto})

# Vista para eliminar presupuesto
def eliminar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    presupuesto.delete()
    messages.success(request, "Presupuesto eliminado correctamente.")
    return redirect('gestion_presupuestos')


from django.shortcuts import render
from django.db.models import Sum
from .models import Obra

def informe(request):
    obras_en_progreso = Obra.objects.filter(estado='en_construccion').count()
    obras_finalizadas = Obra.objects.filter(estado='finalizado').count()
    obras_planeadas = Obra.objects.filter(estado='planeado').count()

    presupuesto_total = Obra.objects.aggregate(Sum('presupuesto_asignado'))['presupuesto_asignado__sum'] or 0

    return render(request, 'informe.html', {
        'obras_en_progreso': obras_en_progreso,
        'obras_finalizadas': obras_finalizadas,
        'obras_planeadas': obras_planeadas,
        'presupuesto_total': presupuesto_total
    })



@login_required
def gestion(request):
    obras = Obra.objects.all()
    constructores = Constructor.objects.all()
    presupuestos = Presupuesto.objects.all()
    return render(request, 'gestion.html', {
        'obras': obras,
        'constructores': constructores,
        'presupuestos': presupuestos
    })


@login_required
def contactos(request):
    return render(request, 'contactos.html')




from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactoForm
from django.conf import settings

def contactos(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            mensaje = form.cleaned_data["mensaje"]

            asunto = f"Nuevo mensaje de {nombre}"
            cuerpo_mensaje = f"Nombre: {nombre}\nCorreo: {email}\nMensaje:\n{mensaje}"

            try:
                send_mail(asunto, cuerpo_mensaje, settings.DEFAULT_FROM_EMAIL, ['destinatario@ejemplo.com'])
                messages.success(request, "Mensaje enviado correctamente.")
                return redirect("contactos")  # Redirige después de enviar
            except Exception as e:
                messages.error(request, f"Error al enviar el mensaje: {e}")

    else:
        form = ContactoForm()

    return render(request, "contactos.html", {"form": form})
