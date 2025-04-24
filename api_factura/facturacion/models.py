from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, User


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Estatus(models.Model):
    TIPO_ESTATUS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('negado', 'Negado'),
        ('devolucion', 'Devolución'),
    ]
    
    tipo_estatus = models.CharField(max_length=10, choices=TIPO_ESTATUS)

    def __str__(self):
        return self.get_tipo_estatus_display()


class Departamentos(models.Model):
    departamento = models.CharField(max_length=50)
    
    def __str__(self):
        return self.departamento
    
    
class Factura(models.Model):
    nrFactura = models.CharField(max_length=50)
    monto = models.FloatField()
    descripcion = models.CharField(max_length=200)
    id_cliente = models.ForeignKey(Cliente, related_name='Clientes', on_delete=models.CASCADE)
    id_estatus = models.ForeignKey(Estatus, on_delete=models.RESTRICT)
    fecha = models.DateTimeField()
    tasa = models.CharField(max_length=5)
    idDepartamento = models.ForeignKey(Departamentos, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nrFactura


class Moneda(models.Model):
    nombre_moneda = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_moneda

class MetodosPago(models.Model):
    tipoPago = models.CharField(max_length=50)
    monedaId = models.ForeignKey(Moneda, on_delete=models.RESTRICT)

    def __str__(self):
        return self.tipoPago

class Pago(models.Model):
    id_factura = models.ForeignKey(Factura, on_delete=models.RESTRICT)
    monto = models.FloatField()
    fecha = models.DateField()
    id_moneda = models.ForeignKey(Moneda, on_delete=models.RESTRICT)
    metodo_pago = models.CharField(max_length=30)
    id_usuario = models.ForeignKey(User, on_delete=models.RESTRICT)
    descripcion = models.CharField(max_length=200)
    def __str__(self):
        return f"Pago #{self.id} - Factura {self.id_factura}"
    
class Profile(models.Model): 
    
    tipo_usuario = models.CharField(max_length=20, default="admin") 
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con User

    def __str__(self):
        return f'{self.user.username} - {self.tipo_usuario}'

class Tasa(models.Model):
    tasa = models.CharField(max_length=5)
    def __str__(self):
        return self.tasa