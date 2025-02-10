from django.urls import path
from . import views
from .views import informe, contactos

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('inicio-sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio/', views.inicio, name='inicio'),
    path('obras/', views.lista_obras, name='lista_obras'),
    path('obras/<int:pk>/', views.detalle_obra, name='detalle_obra'),
    path('obras/crear/', views.crear_obra, name='crear_obra'),
    path('obra/editar/<int:pk>/', views.editar_obra, name='editar_obra'),
    path('obras/<int:pk>/eliminar/', views.eliminar_obra, name='eliminar_obra'),
    
    path('constructores/', views.lista_constructores, name='lista_constructores'),
    path('constructores/agregar/', views.agregar_constructor, name='agregar_constructor'),
    path('constructores/<int:pk>/editar/', views.editar_constructor, name='editar_constructor'),
    path('constructores/<int:pk>/eliminar/', views.eliminar_constructor, name='eliminar_constructor'),
    
    # Define solo una vez la ruta para la lista de presupuestos
    path('presupuestos/', views.lista_presupuestos, name='lista_presupuestos'),
 

    path('presupuestos/asignar/', views.asignar_presupuesto, name='asignar_presupuesto'),
    path('presupuestos/editar/<int:pk>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:pk>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
    
    path('gestion/', views.gestion, name='gestion'),
    path('informe/', informe, name='informe'),
    path('contactos/', views.contactos, name='contactos'),
    
]
