from datetime import datetime
import json
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from facturacion import models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Crear perfil automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        models.Profile.objects.create(user=instance)

# Guardar perfil automáticamente
@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.profile.save()

# Vista para mostrar el formulario de login
def mostrar_formulario(request):
    return render(request, 'registration/login.html')


# API de login
class LoginAPI(APIView):
    def post(self, request):
        usuario = request.data.get('usuario')  # Captura el usuario
        contra = request.data.get('con')  # Captura la contraseña

        user = authenticate(username=usuario, password=contra)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Autenticación exitosa'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

# Redirección según el tipo de usuario
@login_required
def tipoUser(request):
    try:
        user_profile = models.Profile.objects.get(user=request.user)
        if user_profile.tipo_usuario == "admin":
            departamento = models.Departamentos.objects.all()
            dic = {'depar': departamento}
            return render(request, 'index.html', dic)
        
        return render(request, 'index.html')
    except models.Profile.DoesNotExist:
        return render(request, 'index.html')

# Vista para procesar departamento
def departamento(request):
    if request.method == 'POST' or request.method == 'GET':
        depaar = request.POST.get('departamento') if request.method == 'POST' else request.GET.get('departamento')

        try:
            # Busca el departamento
            departamento = models.Departamentos.objects.get(departamento=depaar)

            # Obtiene todos los clientes
            todos_clientes = [cliente.nombre for cliente in models.Cliente.objects.all()]
            todos_pagos = models.Pago.objects.all()
            # Filtra las facturas y clasifica
            clientes_adeudados = []
            clientes_pagados = []

            facturas = models.Factura.objects.filter(idDepartamento=departamento)
            for factura in facturas:
                cliente = factura.id_cliente
                monto_restar = 0
                 
                for m in todos_pagos:
                    print(f'{factura.id} = {m.id_factura_id} el montno del pago es: {m.monto} y el de la factura es: {factura.monto}')
                    if factura.id == m.id_factura_id:
                        monto_restar +=  (factura.monto - m.monto) - factura.monto
                print (f'el monto de la factura a cobrar es: {monto_restar}')
                monotEvaluar = factura.monto + monto_restar
                print(monotEvaluar)
                if monotEvaluar > 0:
                    if cliente.nombre not in clientes_adeudados:
                        clientes_adeudados.append(cliente.nombre)
                elif monotEvaluar == 0 or monotEvaluar <= 0:
                    if cliente.nombre not in clientes_pagados:
                        clientes_pagados.append(cliente.nombre)

            # Serializa las listas como JSON y envía al contexto
            contexto = {
                'todos_clientes': json.dumps(todos_clientes),
                'clientes_adeudados': json.dumps(clientes_adeudados),
                'clientes_pagados': json.dumps(clientes_pagados),
                'departamento': depaar,
            }

            return render(request, 'cliente.html', contexto)

        except models.Departamentos.DoesNotExist:
            return redirect('tipoUser')

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def datosFactura(request):
        if request.method == 'POST' or request.method == 'GET':
            departaemnto = request.POST.get('departamento') if request.method == 'POST' else request.GET.get('departamento')
            cliete = request.POST.get('cliente')
            fecha = datetime.now()
            fecha_formateada = fecha.strftime("%Y-%m-%d")
            paraFactura = str(fecha_formateada)
            segundos = str(fecha.second)
            nrFactura = f"Factura Nº {cliete[0]}{paraFactura[2]}{paraFactura[3]}{paraFactura[8]}{paraFactura[9]}{paraFactura[5]}{paraFactura[6]}{segundos}"
            tasa = models.Tasa.objects.all()
            tasaActual = 0
            for t in tasa:
                tasaActual = t
                
            dic = {
                'tasa' : tasaActual,
                'cliente' : cliete,
                'depar' : departaemnto,
                'nrFactura' : nrFactura,
                'fecha' : fecha_formateada
            }
            return render (request, 'factura.html', dic)
            
def generarFactura(request):
    if request.method == 'GET' or request.methos == 'POST':
        depart = request.GET.get('departaentoDato')
        nrFactura = request.GET.get('factura')
        monto = request.GET.get('monto')
        fecha = request.GET.get('fecha')
        tasa = request.GET.get('tasa')
        descripcion = request.GET.get('descripcion')
        
        cliente = request.GET.get('cliente')
        estatusID = models.Estatus.objects.get(tipo_estatus = 'pendiente')
        clienteID = models.Cliente.objects.get(nombre = cliente)
        idDepartamento = models.Departamentos.objects.get(departamento = depart)
           
        dic = {
            'departamento' : idDepartamento.departamento,
        }
        enviar = models.Factura(
            nrFactura = nrFactura,
            monto = monto,
            descripcion=descripcion,
            id_cliente = clienteID,
            id_estatus = estatusID,
            fecha = fecha,
            tasa = tasa,
            idDepartamento = idDepartamento,
        ) 
        
        print(idDepartamento.departamento)
        enviar.save()
        palabra = {
            'palabra' : 'Factura',
            'departamento' : depart
        }
        return render(request, 'confirmar.html', palabra)
    else:
        dic = {
                'dep' : 'lol',
                'nom' : 'lol'
            }
        return render(request, 'lol.html', dic)
    
def datosFacturaPagar(request):
        if request.method == 'POST' or request.method == 'GET':
            usuario = request.user
            cliete = request.POST.get('factura')
            facturas = models.Factura.objects.get(nrFactura = cliete)
            fecha = facturas.fecha.strftime("%Y-%m-%d")
            moneda = models.Moneda.objects.all()
            metodo = models.MetodosPago.objects.all()
            resta = request.POST.get('resta')
            print( f'resta: {resta}')
            dic = {
                'resta' : resta,
                'metodo' : metodo,
                'moneda' : moneda,
                'fecha' : fecha,
                'usuario' : usuario,
                'factura' : facturas,
                'fecha' : fecha
            }
            return render (request, 'pagar.html', dic)

def datosFacturaPagarPagos(request):
    if request.method in ['POST', 'GET']:
        usuario = request.user
        facturanmr = request.POST.get('factura')
        facturas = models.Factura.objects.get(nrFactura=facturanmr)
        fecha = datetime.now().strftime("%Y-%m-%d")

        # Obtener todas las monedas
        monedas = models.Moneda.objects.all()

        # Crear un diccionario con cada moneda y sus métodos de pago asociados
        listaDeMonedasMetodos = {
            moneda.id: list(models.MetodosPago.objects.filter(monedaId=moneda).values("id", "tipoPago"))  # <-- Cambiado
            for moneda in monedas
        }
        
        metodosPagos = models.MetodosPago.objects.all()
        print("Factura seleccionada:", facturanmr)
        print("Monedas obtenidas:", monedas)
        print("Métodos de pago obtenidos:", metodosPagos)
        print("Lista de métodos por moneda:", listaDeMonedasMetodos)
        metodos = models.MetodosPago.objects.all()
        dic = {
            'moneda': monedas,
            'metodo': metodos,  # Todos los métodos de pago en general
            'listaMonedasMetodos': json.dumps(listaDeMonedasMetodos),  # Métodos filtrados por moneda
            'fecha': fecha,
            'usuario': usuario,
            'factura': facturas,
        }

        return render(request, 'pago.html', dic)

def datosFacturasCliente(request):
        if request.method == 'POST' or request.method == 'GET':
            departaemnto = request.POST.get('departamento') if request.method == 'POST' else request.GET.get('departamento')
            cliete = request.POST.get('cliente')
            clienteID = models.Cliente.objects.get(nombre = cliete)
            departamentoID = models.Departamentos.objects.get(departamento = departaemnto)
            facturas = models.Factura.objects.all()
            pagos = models.Pago.objects.all()
            facturaCliente = []
            for f in facturas:
                print(f'{f.nrFactura} id= {f.id_cliente_id} otro {clienteID.id} departamento= {departamentoID.id} otro {f.idDepartamento_id}')
                montoTotal = 0
                for p in pagos:
                    if f.id == p.id_factura_id:
                        montoTotal += p.monto  
                         
                    
                if f.id_cliente_id == clienteID.id and departamentoID.id == f.idDepartamento_id and (f.monto-montoTotal)>0:
                    facturaCliente.append({
                        'facturas': f,
                        'monto' : (f.monto-montoTotal)                   
                                           })
                    print(f.nrFactura)
                    
            dic = {
                'cliente' : cliete,
                'f' : facturaCliente,
            }
            return render (request, 'listaFacturas.html', dic)
        
def pagogenerado(request):
    if request.method == 'POST' or request.method == 'GET':
        factura = request.POST.get('factura')
        monea = request.POST.get('moneda')
        fecha = request.POST.get('fecha')
        metodo = request.POST.get('metodo')
        monto = request.POST.get('monto')
        
        print(factura)
        print(monea)
        print(metodo)
        usu = request.user
        facturaID = models.Factura.objects.get(nrFactura = factura)
        monedaID = models.Moneda.objects.get(id = monea)
        if monedaID.nombre_moneda == 'USD':
            monto = facturaID.tasa * int(monto)
            print(monto)
        
        descripcion = request.GET.get('descripcion')
        if descripcion == None:
                descripcion = 'sin efecto'
        
        
        enviar = models.Pago(
            id_factura = facturaID,
            monto = monto,
            fecha = fecha,
            metodo_pago = metodo,
            id_moneda = monedaID,
            id_usuario = usu,
            descripcion = descripcion
            
        )
        enviar.save()
        palabra = {
            'palabra' : 'Pago',
            'departamento' : facturaID.idDepartamento
        }
        return render(request, 'confirmar.html', palabra)

def repostePagados(request):
    factura = request.POST.get('factura')
    print(f' obtenido {factura}')
    idFactura = models.Factura.objects.get(nrFactura = factura)
    print( f' factura iguaada y traida de la tabla factura que es el id {idFactura.id}')
    facturas = []
   
    pagosExisten = models.Pago.objects.all()
    for p in pagosExisten:
        print( f'si {idFactura.id} = {p.id_factura_id}')
        if idFactura.id == p.id_factura_id:
            print(f'pagos agg {p}')
            facturas.append(p)
                
    dic = {
        'pagos' : facturas,
        'nrFactura' :factura
    }
    
    return render(request, 'reportePagos.html', dic)

def datosDelPago (request):
    if request.method == 'POST' or request.method == 'GET':
        datosID = request.POST.get('datosDelPago')
        pago = models.Pago.objects.get(id = datosID)
        nrFactura = pago.id_factura
        fecha = pago.fecha.strftime("%Y-%m-%d")
        factura = models.Factura.objects.get(nrFactura = nrFactura)
        metodoPago = models.MetodosPago.objects.get(id = pago.metodo_pago )
        dic = {
            'metodoPago' : metodoPago,
            'fecha' : fecha,
            'pago' : pago,
            'factura' : factura
        }
        
        return render(request, 'detallePago.html', dic)
    
def facturas_pagadas_cliente(request):
    if request.method == 'POST' or request.method == 'GET':
        departamento = request.POST.get('departamento') if request.method == 'POST' else request.GET.get('departamento')
        cliente_nombre = request.POST.get('cliente')

        try:
            cliente = models.Cliente.objects.get(nombre=cliente_nombre)
            departamento_obj = models.Departamentos.objects.get(departamento=departamento)
        except models.Cliente.DoesNotExist:
            print(f"Cliente '{cliente_nombre}' no encontrado.")  # Depuración
            return HttpResponse("Cliente no encontrado", status=404)
        except models.Departamentos.DoesNotExist:
            print(f"Departamento '{departamento}' no encontrado.")  # Depuración
            return HttpResponse("Departamento no encontrado", status=404)

        # Filtrar las facturas completamente pagadas
        facturas = models.Factura.objects.filter(id_cliente=cliente.id, idDepartamento=departamento_obj.id)
        print(f"Facturas obtenidas: {facturas}")  # Depuración

        pagos = models.Pago.objects.filter(id_factura__in=[f.id for f in facturas])
        print(f"Pagos obtenidos: {pagos}")  # Depuración

        pagos_por_factura = {}
        for pago in pagos:
            if pago.id_factura_id not in pagos_por_factura:
                pagos_por_factura[pago.id_factura_id] = 0
            pagos_por_factura[pago.id_factura_id] += pago.monto

        print(f"Pagos acumulados por factura: {pagos_por_factura}")  # Depuración

        facturas_pagadas = []
        for factura in facturas:
            monto_total_pagado = pagos_por_factura.get(factura.id, 0)  # Obtiene monto pagado individualmente
            residuo = factura.monto - monto_total_pagado  # Calcula el residuo

            print(f'Factura {factura.id}: Monto total abonado {monto_total_pagado}')
            print(f'Residuo: {factura.monto} - {monto_total_pagado} = {residuo}')

            if factura.monto == monto_total_pagado or residuo < 0:  # Si está completamente pagada o hay excedente
                facturas_pagadas.append({'factura': factura, 'residuo': (-1)*residuo})  # Agrega el residuo a la lista

        print(f"Facturas completamente pagadas con residuo: {facturas_pagadas}")  # Depuración

        context = {
            'cliente': cliente_nombre,
            'facturas_pagadas': facturas_pagadas,
        }
        
        return render(request, 'facturasPagadas.html', context)


def pagos_de_factura_pagada(request):
    if request.method == 'POST' or request.method == 'GET':
        numero_factura = request.POST.get('factura')

        try:
            factura = models.Factura.objects.get(nrFactura=numero_factura)
        except models.Factura.DoesNotExist:
            return HttpResponse("Factura no encontrada", status=404)

        # Obtener los pagos relacionados con esta factura
        pagos = models.Pago.objects.filter(id_factura=factura.id)

        context = {
            'factura': factura,
            'pagos': pagos,
        }
        return render(request, 'pagosPorFacturaPagada.html', context)


def detalles_de_pago(request):
    if request.method == 'POST' or request.method == 'GET':
        pago_id = request.POST.get('factura')
        idFactura = models.Factura.objects.get(nrFactura = pago_id)
        print (idFactura.id)
        try:
            # Obtenemos el pago seleccionado
            pago = models.Pago.objects.all()
        except models.Pago.DoesNotExist:
            return HttpResponse("Pago no encontrado", status=404)

        # Obtenemos detalles relacionados al pago
        pagos = []
        for p in pago:
            if p.id_factura == idFactura:
                pagos.append(p)
        context = {
            'pagos' : pagos
        }
        return render(request, 'pagosYaPagados.html', context)


def registrarCliente(request):
    if request.method == 'POST' or request.method == 'GET':
        departamento = request.POST.get('departamento')
        print(departamento)
        dic = {
            'departamento' : departamento
        }
        return render(request, 'registrarCliente.html', dic)

def registrarClientes(request):
    if request.method == "POST" or request.method == "GET":
        nombre = request.POST.get('nombre')
        print(nombre)
        apellido = request.POST.get('apellido')
        ci = request.POST.get('cedula')
        tel = request.POST.get('numero')

        enviar = models.Cliente(
            nombre = nombre,
            apellido = apellido,
            cedula = ci,
            telefono = tel
        )

        enviar.save()
        departamento = request.POST.get('departamento')
        print(departamento)
        palabra = {
            'palabra' : 'Cliente',
            'departamento' : departamento 
        }

        return render(request, 'confirmar.html', palabra )
    
def vistaTienda(request):
    return render(request, 'tiendas.html')

def tasa(request):
    return render(request, 'actualizaTasa.html')


def ActualizarTasa(request):
    if request.method == 'POST' or request.method == 'GET':
        tasaActual = request.POST.get('tasa')
        
        tasa = models.Tasa(
            tasa = tasaActual
        )
        
        tasa.save()
        dic = {
            'palabra' : 'Tasa'
        }
        return render ( request, 'confirmar.html', dic)
def tienda(request):
     if request.method == 'POST' or request.method == 'GET':
        nombre = request.POST.get('nombre')
        print(nombre)
        enviar = models.Departamentos(
            departamento = nombre
        )
        enviar.save()
        dic= {
            'palabra' : 'Tienda'
        }
        return render(request, 'confirmar.html', dic)
    
def usuarios(request):
    return render (request, 'usuarios.html')

def formulariousuario(request):
    return render(request, 'registrarUsuario.html')

def editarUsuario(request):
    usuario = request.user
    print(usuario)
    dic = {
        'usuario' : usuario
    }
    return render(request, 'editarUsuario.html', dic)

def usuarioEditado (request):
    if request.method == 'POST':
        usu = request.user
        contraseña = request.POST.get('contraseña')
        usuario = request.POST.get('nombre')

        if contraseña:
            usu.set_password(contraseña)
            update_session_auth_hash(request, usu)  # Mantiene la sesión activa después de cambiar la contraseña

        if usuario:
            usu.username = usuario
            
        usu.save()

        dic = {'palabra': 'Actualizado'}
        return render(request, 'confirmar.html', dic)
        
        
def registrarUsuario (request):
    if request.method == 'POST':
        usuario = request.POST.get('nombre')
        contraseña = request.POST.get('contraseña')

        if usuario and contraseña:
            email = f"{usuario}@{usuario}.com"  # Generar correo ficticio

            nuevo_usuario = User.objects.create(
                username=usuario,
                email=email
            )
            nuevo_usuario.set_password(contraseña)  # Guardar contraseña de manera segura
            nuevo_usuario.save()

            dic = {
                'palabra' : 'Usuario'
            }
            return render(request, "confirmar.html", dic)  # Redirige a la página de perfil

    return render(request, "registrar_usuario.html")   
            
