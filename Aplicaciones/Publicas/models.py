from django.db import models


class Obra(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    ESTADOS_CHOICES = [
        ('planeado', 'Planeado'),
        ('en_construccion', 'En Construcción'),
        ('finalizado', 'Finalizado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='planeado')
    presupuesto_asignado = models.DecimalField(max_digits=15, decimal_places=2)
    constructor = models.ForeignKey('Constructor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

from django.db import models

class Constructor(models.Model):
    nombre_empresa = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='archivos_constructores/', blank=True, null=True)  # NUEVO CAMPO

    def __str__(self):
        return self.nombre_empresa


class Presupuesto(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    monto_asignado = models.DecimalField(max_digits=10, decimal_places=2)
    monto_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Nuevo campo

    def __str__(self):
        return f"Presupuesto para {self.obra.nombre}"

from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
