import datetime
import io
from user.models import UserProfile
from django.shortcuts import render, redirect
from analiseProcessos.forms import analiseForm
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
class cadSem(View):
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
            Semana.objects.filter(id=id).update(realizado= True)
            pass     
        # aqui vou ter que inserir o usuario/empresa/e etc.
        #atualizar a semana aqui.
        return render(request, 'atividades/cadSemana.html', data)
    
class updProc(View):
    def get(self, request,id):
        analise = AnaliseProcesso.objects.get(id=id)
        form = analiseForm().iniciar(analise)     
        return render(request, 'atividades/updProc.html', {'form':form})

    def post(self, request, id):
        post = request.POST                
        analise = AnaliseProcesso.objects.get(id=id)
        #verificar se existe reprova e etc;
        nc = verificarNC(request)
        AnaliseProcesso.objects.filter(id=id).update(OS=post.get('OS'), crlv=post.get('crlv'),data=datetime.date.today(), decalque=post.get('decalque'), vistoriaInicial=post.get('vistoriaInicial'), verificaoEscopo=post.get('verificaoEscopo'),linhaInspecao=post.get('linhaInspecao'),opacidade=post.get('opacidade'),ruido=post.get('ruido'),naoConformidade=post.get('naoConformidade'),rasurasProcessos=post.get('rasurasProcessos'),registrosFotograficos=post.get('registrosFotograficos'),filmagem=post.get('filmagem'),realizado= True, NC = nc ) 
        analises = AnaliseProcesso.objects.filter(semana=analise.semana)
        #faz análise se existe processos em aberto ainda: tirar daqui        
        for ana in analises:
            realizado = ana.realizado        
        if(realizado):
            Semana.objects.filter(id=analise.semana.id).update(realizado= True,data=datetime.date.today())
        return redirect('listAna-view', semana=analise.semana.id)

@login_required
def cadProc(request):    
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
            analise = AnaliseProcesso.objects.create(semana=semana, user=user)
            analises.append(analise)
            Semana.objects.filter(id=id).update(processos=processos,analises=nAnalises) 
        return redirect('listAna-view', semana.id)     
    else:
        Semana.objects.filter(id=id).update(realizado= True)
        return HttpResponse('./listSem')


class listAna(LoginRequiredMixin ,View):
    def get(self, request, semana):
        #aqui precisa fazer uma seleção do usário/empresa
        data = {}
        data['semana'] = Semana.objects.get(id=int(semana))
        data['analises'] = AnaliseProcesso.objects.filter(semana=data['semana'].id)
        return render(request, 'atividades/listAna.html', data)     
    def post(self, request):
        pass

class listSem(View):
    def get(self, request):
        proc = []
        data = {}     
        user = UserProfile.objects.filter(user=request.user).first()
        semana = Semana.objects.filter(empresa=user.empresa)
        data['semanas'] = semana            
        return render(request, 'atividades/listSem.html', data)    
    def post(self, request):
        pass

def report(request,id):
    semana = Semana.objects.get(id=id)    
    buffer = io.BytesIO() 
    ncs = qntdNC(semana)
    imprimirPDF(buffer,semana,request.user, ncs)
    buffer.seek(0)
    filename=semana.data
    return FileResponse(buffer, as_attachment=False, filename="Analise: "+str(semana.inicio)+" - "+str(semana.fim)+".pdf")

def home(request):
    return render(request, 'user/index.html')

def my_logout(request):
    logout(request)
    return redirect('atividades-home-view')

def verificarNC(request):
    nc = 'Não'
    if(request.POST.get('crlv') == 'R'):
        nc = 'Sim'

    if(request.POST.get('decalque') == 'R'):
        nc = 'Sim'

    if(request.POST.get('vistoriaInicial') == 'R'):
        nc = 'Sim'

    if(request.POST.get('verificaoEscopo') == 'R'):
        nc = 'Sim'

    if(request.POST.get('linhaInspecao') == 'R'):
        nc = 'Sim'

    if(request.POST.get('opacidade') == 'R'):
        nc = 'Sim'

    if(request.POST.get('ruido') == 'R'):
        nc = 'Sim'

    if(request.POST.get('naoConformidade') == 'R'):
        nc = 'Sim'

    if(request.POST.get('rasurasProcessos') == 'R'):
        nc = 'Sim'

    if(request.POST.get('registrosFotograficos') == 'R'):
        nc = 'Sim'

    if(request.POST.get('filmagem') == 'R'):
        nc = 'Sim'

    return nc

def qntdNC(semana):
    nc = 0
    analises = AnaliseProcesso.objects.filter(semana=semana.id)
    for analise in analises:
        if(analise.crlv == 'R'):
            nc = nc+1
        if(analise.decalque == 'R'):
            nc = nc+1
        if(analise.vistoriaInicial == 'R'):
            nc = nc+1
        if(analise.verificaoEscopo == 'R'):
            nc = nc+1
        if(analise.linhaInspecao == 'R'):
            nc = nc+1
        if(analise.opacidade == 'R'):
            nc = nc+1            
        if(analise.ruido == 'R'):
            nc = nc+1
        if(analise.naoConformidade == 'R'):
            nc = nc+1
        if(analise.rasurasProcessos == 'R'):
            nc = nc+1
        if(analise.registrosFotograficos == 'R'):
            nc = nc+1
        if(analise.filmagem == 'R'):
            nc = nc+1
    
    return nc 
   
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