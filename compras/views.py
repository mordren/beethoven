import io
from django.shortcuts import render
from django.views.generic.edit import View, DeleteView
from django.views.generic.list import ListView
from compras.models import Compra
from compras.util.report import imprimirPDF
from .forms import comprasForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse

# Create your views here.
class CadCompra(View):
    def get(self, request):
        form = comprasForm()
        form.create()
        return render(request, 'compras/cadCompra.html', {'form':form})

    def post(self, request):
        form = comprasForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(request.user)
        return redirect('listCompra-view')

class ListCompra(ListView):
    model = Compra
    
class DeleteCompra(DeleteView):
    model = Compra
    sucess_url = reverse_lazy('listCompra-view')

@login_required(login_url='login/')
def compraDelete(request, id):
    compra = get_object_or_404(Compra, id=id)
    #nesse eu envio uma pessoa para criar uma instância lá no template, para decidir se vou deletar.        
    compra.delete()
    return redirect('listCompra-view')

class UpdateCompra(View):
    def get(self, request,id):
        compra = Compra.objects.get(id=id)     
        form = comprasForm().iniciar(compra) 
        return render(request, 'compras/cadCompra.html', {'form':form})
    
    def post(self, request, id):
        post = request.POST                
        analise = Compra.objects.get(id=id)
        #verificar se existe reprova e etc;
        Compra.objects.filter(id=id).update(descricao=post.get('descricao'),empresaContratada=post.get('empresaContratada'),responsavelAnuencia=post.get('responsavelAnuencia'),integridade=post.get('integridade'),requisitosNorma=post.get('requisitosNorma'),metodologia=post.get('metodologia'),requisitos=post.get('requisitos'), calibracao=post.get('calibracao'), observacoes=post.get('observacoes'), dataRecebimento=post.get('dataRecebimento'))
        return redirect('listCompra-view')

def report(request,id):
    compra = Compra.objects.get(id=id)    
    buffer = io.BytesIO() 
    imprimirPDF(buffer,compra,request.user)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"Compras: { compra.descricao } - { compra.date} .pdf")