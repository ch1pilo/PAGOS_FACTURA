from rest_framework.routers import DefaultRouter
from facturacion import api, views
from django.urls import path, include
from django.shortcuts import render
from django.dispatch import receiver 
from django.db.models.signals import post_save  
from django.contrib.auth.models import User


router = DefaultRouter()
router.register(r'cliente', api.ClienteViewset, basename='cliente')  # Ruta para MyViewSet
router.register(r'factura', api.FacturaViewset, basename='factura')  # Ruta para AnotherViewSet
router.register(r'pagos', api.PagosViewset, basename='pagos')
router.register(r'moneda', api.MonedaViewset, basename='moneda')
router.register(r'tiposPagos', api.tipoPagosViewset, basename='tiposPagos')
router.register(r'tipoUser', api.ProfileViewset, basename='tipoUser')
router.register(r'usuarios', api.UserViewSet, basename='usuarios')
router.register(r'departamento', api.DepartamentoViewSet, basename='departamento')


urlpatterns = [
    path('departamento/<int:departamento_id>/facturas/', views.departamento_required, name='lista_facturas'),
    path('api/login/', views.LoginAPI.as_view(), name="login"),
    path('formulario/', views.mostrar_formulario, name='mostrar_formulario'),
    path('tipoUser/', views.tipoUser, name='tipoUser'),
    path('departamento/', views.departamento, name='departamento'),
    path('datosFactura/', views.datosFactura, name='datosFactura'),
    path("generarFactura/", views.generarFactura, name='generarFactura'),
    path("datosFacturasCliente/", views.datosFacturasCliente, name='datosFacturasCliente'),
    path("datosFacturaPagar/", views.datosFacturaPagar, name='datosFacturaPagar'),
    path("efectuarPago/", views.datosFacturaPagarPagos, name='datosFacturaPagarPagos'),
    path("pagogenerado/", views.pagogenerado, name='pagogenerado'),
    path("repostePagados/", views.repostePagados, name='repostePagados'),
    path("datosPagados/", views.datosDelPago, name='datosDelPago'),
    path("facturas_pagadas_cliente/", views.facturas_pagadas_cliente, name='facturas_pagadas_cliente'),
    path("detalles_de_pago/", views.detalles_de_pago, name='detalles_de_pago'),
    path("pagos_de_factura_pagada/", views.pagos_de_factura_pagada, name='pagos_de_factura_pagada'),
    path("registrarCliente/", views.registrarCliente, name='registrarCliente'),
    path("registrarClientes/", views.registrarClientes, name='registrarClientes'),
    path("tienda/", views.tienda, name='tienda'),
    path("vistaTienda/", views.vistaTienda, name='vistaTienda'),
    path("usuarios/", views.usuarios, name='usuarios'),
    path("editarUsuario/", views.editarUsuario, name='editarUsuario'),
    path("usuarioEditado/", views.usuarioEditado, name='usuarioEditado'),
    path("registrarUsuario/", views.registrarUsuario, name='registrarUsuario'),
    path("formulariousuario/", views.formulariousuario, name='formulariousuario'),
    path("tasa/", views.tasa, name='tasa'),
    path("ActualizarTasa/", views.ActualizarTasa, name='ActualizarTasa'),



    path("", include(router.urls)),
]                                     