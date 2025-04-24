from rest_framework import serializers  #  Asegura que importaste `serializers`
from facturacion import models
from django.contrib.auth.models import User

class ClienteSerializer(serializers.ModelSerializer):  # cla Usa `serializers.ModelSerializer`
    class Meta:
        model = models.Cliente
        fields = ('id', 'nombre', 'apellido', 'cedula', 'telefono')
        
class FacturaSerializer(serializers.ModelSerializer):  # cla Usa `serializers.ModelSerializer`
    class Meta:
        model = models.Factura
        fields = ('id', 'nrFactura', 'monto', 'descripcion', 'id_cliente', 'id_estatus', 'fecha', 'tasa')
        
class PagosSerializer(serializers.ModelSerializer):  # cla Usa `serializers.ModelSerializer`
    class Meta:
        model = models.Pago
        fields = ('id','id_factura', 'monto', 'fecha', 'metodo_pago', 'id_moneda', 'id_usuario')

class MonedasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Moneda
        fields = ('id', 'nombre_moneda')

class tipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetodosPago
        fields = ('id', 'tipoPago')

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('id', 'user', 'tipo_usuario')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_active']  