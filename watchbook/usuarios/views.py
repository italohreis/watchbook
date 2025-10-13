from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormularioCadastro
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroAssistidoForm
from catalogo.models import Obra

class RegistrarObraAssistida(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request, obra_id):
        obra = get_object_or_404(Obra, pk=obra_id)
        form = RegistroAssistidoForm(request.POST)

        if form.is_valid():
            novo_registro = form.save(commit=False)
            novo_registro.usuario = request.user
            novo_registro.obra = obra
            novo_registro.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'buscar-obras'))

class CadastrarUsuario(CreateView):
    form_class = FormularioCadastro
    template_name = 'usuarios/cadastrar.html'
    success_url = reverse_lazy('login') 