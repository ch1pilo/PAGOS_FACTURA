from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from facturacion import models, serializers
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Todos los usuarios
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]  # Requiere autenticación para el acceso
    
class ClienteViewset(viewsets.ModelViewSet):  # 🔹 Debe ser una clase, no una función
    queryset = models.Cliente.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ClienteSerializer
    

class MonedaViewset(viewsets.ModelViewSet):
    queryset = models.Moneda.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.MonedasSerializer

class tipoPagosViewset(viewsets.ModelViewSet):
    queryset = models.MetodosPago.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.tipoPagoSerializer

class FacturaViewset(viewsets.ModelViewSet):  # 🔹 Debe ser una clase, no una función
    serializer_class = serializers.FacturaSerializer
    queryset = models.Factura.objects.all()         
    def create(self, request, *args, **kwargs):
        # Obtener los datos enviados en el cuerpo de la solicitud
        serializer = self.get_serializer(data=request.data)
        
        # Validar los datos
        serializer.is_valid(raise_exception=True)
        
        # Guardar el registro en la base de datos
        self.perform_create(serializer)
        
        # Responder con los datos creados
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        cliente_id = self.request.query_params.get('id_cliente')
        if cliente_id:
            return models.Factura.objects.filter(id_cliente=cliente_id)
        return models.Factura.objects.all()

class ProfileViewset(viewsets.ModelViewSet):
    serializer_class = serializers.profileSerializer
    queryset = models.Profile.objects.all()
    def create(self, request, *args, **kwargs):
        # Obtener los datos enviados en el cuerpo de la solicitud
        serializer = self.get_serializer(data=request.data)
        
        # Validar los datos
        serializer.is_valid(raise_exception=True)
        
        # Guardar el registro en la base de datos
        self.perform_create(serializer)
        
        # Responder con los datos creados
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.query_params.get('user')
        if (user):
            return models.Profile.object.filter(user = user)
        else:
            return models.Profile.objects.all()
    

class PagosViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PagosSerializer
    queryset = models.Pago.objects.all()  # Define el conjunto de datos por defecto

    def create(self, request, *args, **kwargs):
        # Obtener los datos enviados en el cuerpo de la solicitud
        serializer = self.get_serializer(data=request.data)
        
        # Validar los datos
        serializer.is_valid(raise_exception=True)
        
        # Guardar el registro en la base de datos
        self.perform_create(serializer)
        
        # Responder con los datos creados
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        facturaId = self.request.query_params.get('id_factura')
        pagoMID = self.request.query_params.get('metodo_pago')
        monedaId = self.request.query_params.get('id_moneda')
        usuarioId = self.request.query_params.get('id_usuario')
        if facturaId and pagoMID and monedaId and usuarioId:
            return models.Pago.objects.filter(
                facturaId=facturaId,
                pagoMID=pagoMID,
                monedaId=monedaId,
                usuarioId=usuarioId
            )
        else:
            return models.Pago.objects.all()
        

class DepartamentoViewSet(viewsets.ModelViewSet):
    
    def create(self, request, *args, **kwargs):
        # Obtener los datos enviados en el cuerpo de la solicitud
        serializer = self.get_serializer(data=request.data)
        
        # Validar los datos
        serializer.is_valid(raise_exception=True)
        
        # Guardar el registro en la base de datos
        self.perform_create(serializer)
        
        # Responder con los datos creados
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):    
        Departamento = self.request.query_params.get('id')