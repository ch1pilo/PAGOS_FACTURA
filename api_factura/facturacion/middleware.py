# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from facturacion import models

class DepartamentoAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # URLs que no requieren verificación
        exempt_urls = [
            reverse('login'),
            reverse('logout'),
            reverse('registrar_usuario'),
        ]
        
        if request.path in exempt_urls:
            return None
            
        if not request.user.is_authenticated:
            return redirect('login')
            
        if request.user.is_superuser:
            return None
            
        try:
            profile = request.user.profile
            if profile.tipo_usuario == 'admin':
                return None
                
            # Verificar si la vista requiere acceso a un departamento específico
            if hasattr(view_func, 'departamento_required'):
                if profile.departamento.id != view_kwargs.get('departamento_id'):
                    return redirect('acceso_denegado')
                    
        except models.Profile.DoesNotExist:
            return redirect('acceso_denegado')
            
        return None