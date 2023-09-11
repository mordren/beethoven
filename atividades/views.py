import datetime
import io
from django.shortcuts import render, redirect
from atividades.forms import analiseForm
from .models import AnaliseProcesso, Semana
from django.views.generic.edit import CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from .util.report import imprimirPDF
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class cadSemana(View):
    def get(self, request,id):
        model = Semana.objects.get(id=id)
        form = ""
        return render(request, 'atividades/cadSemana.html', {'semana':model, "form":form})
            
    def post(self, request,id):
        data = {}          
        post = request.POST
        
        #faz a busca no banco para verificar os dados da semana
        if int(post.get('numProcessos')) > 0:
            data['semana'] = Semana.objects.get(id=id)
            data['processos'] = post.get('numProcessos')
            data['form'] = analiseForm()
            data['nAnalises'] = round((int(data['processos'])*0.05)+0.5)
            #inserir usuário da sessão:        
            data['user'] = 'João'            
            analises = []
            for i in range(data['nAnalises']):
                analise = AnaliseProcesso.objects.create(semana=data['semana'])
                analises.append(analise)
                Semana.objects.get(id=id).update(processos=post.get('numProcessos'),analises=data['nAnalises'])                
            data['analises'] = analises
            return HttpResponseRedirect('./listAna/'+id)            
        else:
            #implementar tela de confirmação de semana vaga.
            #salvar a semana como vazia.
            Semana.objects.filter(id=id).update(realizado=True)
            pass     
        # aqui vou ter que inserir o usuario/empresa/e etc.
        #atualizar a semana aqui.
        return render(request, 'atividades/cadSemana.html', data)
    
class cadProc(View):
    def get(self, request,id):
        analise = AnaliseProcesso.objects.get(id=id)
        form = analiseForm().iniciar(analise)     
        return render(request, 'atividades/cadProc.html', {'form':form})

    def post(self, request, id):
        post = request.POST                
        analise = AnaliseProcesso.objects.get(id=id)
        #verificar se existe reprova e etc;
        AnaliseProcesso.objects.filter(id=id).update(OS=post.get('OS'), crlv=post.get('crlv'),data=datetime.date.today(), decalque=post.get('decalque'), vistoriaInicial=post.get('vistoriaInicial'), verificaoEscopo=post.get('verificaoEscopo'),linhaInspecao=post.get('linhaInspecao'),opacidade=post.get('opacidade'),ruido=post.get('ruido'),naoConformidade=post.get('naoConformidade'),rasurasProcessos=post.get('rasurasProcessos'),registrosFotograficos=post.get('registrosFotograficos'),filmagem=post.get('filmagem'),realizado=True) 
        analises = AnaliseProcesso.objects.filter(semana=analise.semana)
        #faz análise se existe processos em aberto ainda: tirar daqui        
        for ana in analises:
            realizado = ana.realizado        
        if(realizado):
            Semana.objects.filter(id=analise.semana.id).update(realizado=True,data=datetime.date.today())
        return redirect('listAna-view', semana=analise.semana.numero)

def cadProcessos(request):    
    post = request.POST
    id = int(request.POST.get('semana_hidden'))
    processos = int(request.POST.get('processos'))
    if processos > 0:
        semana = Semana.objects.get(id=id)               
        nAnalises = round((int(processos)*0.05)+0.5)
        #inserir usuário da sessão:        
        user = request.user            
        analises = []
        for i in range(nAnalises):
            analise = AnaliseProcesso.objects.create(semana=semana, user=user,)
            analises.append(analise)
            Semana.objects.filter(id=id).update(processos=processos,analises=nAnalises)      
        return HttpResponseRedirect('./listAna/'+str(id))  
    else:
        Semana.objects.filter(id=id).update(realizado=True)
        return HttpResponse('./listSemana')


class listAna(LoginRequiredMixin ,View):
    def get(self, request, semana):
        #aqui precisa fazer uma seleção do usário/empresa
        data = {}
        data['semana'] = Semana.objects.get(id=int(semana))
        data['analises'] = AnaliseProcesso.objects.filter(semana=data['semana'].id)
        return render(request, 'atividades/listAna.html', data)     

    def post(self, request):
        pass

class listaSemana(View):
    def get(self, request):
        proc = []
        data = {}
        semana = Semana.objects.all()        
        data['semanas'] = semana            
        return render(request, 'atividades/listSemana.html', data)    
    def post(self, request):
        pass

def report(request,id):
    semana = Semana.objects.get(id=id)    
    buffer = io.BytesIO()   
    print(request.user)
    imprimirPDF(buffer,semana,str(request.user))
    buffer.seek(0)
    filename=semana.data
    return FileResponse(buffer, as_attachment=True, filename="Analise: "+str(semana.inicio)+" - "+str(semana.fim)+".pdf")  

def home(request):
    return render(request, 'atividades/index.html')

def my_logout(request):
    logout(request)
    return redirect('atividades-home-view')

""""
def cadastroAnalise(request):
    if request.method == "POST":
        form = request.POST
        processos = form.get('numProcessos')
        semana = form.get('selSemana')             
        return render(request, "controleProcessos",{'html':processos})           
    else:
        sem = Semana.objects.filter(realizado=False)
        return render(request, 'atividades/cadastroAnalise.html', {'semanas':sem})
    
class controleProcesso(CreateView):
    model = controleProcesso
    fields = ['OS','crlv','decalque','vistoriaInicial','linhaInspecao','opacidade','ruido','naoConformidade', 'rasurasProcessos', 'registrosFotograficos', 'filmagem']

class cadOS(UpdateView):
    model = Semana.objects.filter(realizado=False)
    fields = ['numero']
    

class atividadesView(CreateView):
    model = analiseProcessos
   fields = ['data','crlv','decalque','vistoriaInicial','linhaInspecao','opacidade','ruido','naoConformidade', 'rasurasProcessos', 'registrosFotograficos', 'filmagem', 'OS']
    success_url = reverse_lazy('atividades') 
 
def atividadesV(request):
    model = analiseProcessos
    return render(request, 'atividades/analiseprocessos_form.html',  {'object_list':model})
"""