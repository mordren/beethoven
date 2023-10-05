import datetime
import io
from user.models import UserProfile
from django.shortcuts import render, redirect
from analiseProcessos.forms import analiseForm
from .models import AnaliseProcesso, AnaliseProcessoResposta, AnaliseProcessoSV, Questao, Semana
from django.views.generic.edit import CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from .util.report import imprimirPDF
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

#As semanas serão realizados pelo updateModels
#As análises de processos, serão feitas através da pagina 'listSem/ + portaria' por exemplo listSem/OIVA
#Depois que inserir quantos foram os processos, quem abre a página é listProc


#listar todas as análises na semana.
class listSem(View):
    def get(self, request, portaria):  
        user = UserProfile.objects.filter(user=request.user).first()
        semana = Semana.objects.filter(empresa=user.empresa, portaria=portaria)
        return render(request, 'atividades/listSem.html', {'semanas':semana, 'portaria':portaria})    

#Listagem dos procedimentos, passa a semana para listar todos os procedimentos.
class listProc(LoginRequiredMixin ,View):
    def get(self, request, semana):
        #aqui precisa fazer uma seleção do usário/empresa
        data = {}
        semana = Semana.objects.get(id=int(semana))
        data['semana'] = semana
        data['analises'] = AnaliseProcesso.objects.filter(semana=semana)
        return render(request, 'atividades/listProc.html', data)     

#Criação de todas as análises críticas necessárias para aquela semana.
@login_required
def criaAnalisesProcessos(request):
    semana = Semana.objects.get(id=request.POST.get('semana_hidden'))
    processos = int(request.POST.get('processos'))
    #Se o usuário inserir 0, quer dizer que aquele período não teve inspeções
    if processos > 0:         
        nAnalises = round((int(processos)*0.05)+0.5)
        #inserir usuário da sessão:        
        user = request.user            
        analises = []
        for i in range(nAnalises):
            analise = AnaliseProcesso.objects.create(semana=semana, user=user)
            analises.append(analise)
            Semana.objects.filter(id=semana.id).update(processos=processos,analises=nAnalises) 
        return redirect('listProc-view', semana.id)     
    #é salvado a analise zerada e retorna para lista.
    else:
        Semana.objects.filter(id=request.POST.get('semana_hidden')).update(realizado= True)
        return redirect('listSem-view' , semana.portaria)
   
#Procedimento para realização do Cadastro
class RealizaAnaliseProcesso(View):
    def get(self, request, id):
        analise = AnaliseProcesso.objects.get(id=id)
        if analise.realizado:
            formularios = AnaliseProcessoResposta.objects.filter(analiseProcesso = analise)
            return render(request, 'atividades/updProc_edt.html', {'formulario':formularios, 'os':analise.OS, 'observacoes':analise.observacoes})
        else:
            formularios = Questao.objects.filter(portaria = analise.semana.portaria)       
        return render(request, 'atividades/updProc_cad.html', {'formulario':formularios})
    
    def post(self, request, id):
        analise = AnaliseProcesso.objects.get(id=id)       
        nc = 'Não'
        # melhorar o desempenho do primeiro registro, pensar como fazer isso.
        if not analise.realizado:             
            formularios = Questao.objects.filter(portaria = analise.semana.portaria)
            for formulario in formularios:
                form = AnaliseProcessoResposta.objects.create()                        
                form.analiseProcesso = analise
                form.resposta = request.POST.get(formulario.titulo)
                if form.resposta == 'R':
                    nc = 'Sim'
                form.quest = formulario                
                form.save()    
        else:
            respostas = AnaliseProcessoResposta.objects.filter(analiseProcesso=analise)
            for resposta in respostas:               
                if request.POST.get(resposta.quest.titulo) == 'R':
                    nc = 'Sim'
                AnaliseProcessoResposta.objects.filter(id=resposta.id).update(resposta=request.POST.get(resposta.quest.titulo))
        AnaliseProcesso.objects.filter(id=id).update(OS=request.POST.get('OS'), data=datetime.date.today(), realizado = True, NC = nc, observacoes=request.POST.get('observacoes'))
        analises = AnaliseProcesso.objects.filter(semana=analise.semana)
        #faz análise se existe processos em aberto ainda: tirar daqui      
        for ana in analises:
            realizado = ana.realizado        
        if(realizado):
            Semana.objects.filter(id=analise.semana.id).update(realizado= True,data=datetime.date.today())
        return redirect('listProc-view', semana=analise.semana.id)

#aqui quando eu insiro ou excluo uma análise de processos ele atualiza na semana.
@login_required
def atualizarNumerosProcessos(request):
    AnaliseProcessoSV.objects.filter(semana=request.POST.get('semana_hidden')).delete()
    Semana.objects.filter(id=request.POST.get('semana_hidden')).update(analises=0, processos=0,realizado=False)
    criaAnalisesProcessos(request, request.POST.get('semana_hidden'))
    return redirect('listSem-view')

#usei upd porque o usário não cria essas análises por OS, ele apenas diz quantas ele quer criar.
#obsoleto
class updProc(View):
    def get(self, request,id):
        analise = AnaliseProcessoSV.objects.get(id=id)
        form = analiseForm().iniciar(analise)     
        return render(request, 'atividades/updProc.html', {'form':form})
    
    def post(self, request, id):
        post = request.POST                
        analise = AnaliseProcessoSV.objects.get(id=id)
        #verificar se existe reprova e etc;
        nc = verificarNC(request)
        AnaliseProcessoSV.objects.filter(id=id).update(OS=post.get('OS'), crlv=post.get('crlv'),data=datetime.date.today(), decalque=post.get('decalque'), vistoriaInicial=post.get('vistoriaInicial'), verificaoEscopo=post.get('verificaoEscopo'),linhaInspecao=post.get('linhaInspecao'),opacidade=post.get('opacidade'),ruido=post.get('ruido'),naoConformidade=post.get('naoConformidade'),rasurasProcessos=post.get('rasurasProcessos'),registrosFotograficos=post.get('registrosFotograficos'),filmagem=post.get('filmagem'), observacoes=post.get('observacoes'), realizado= True, NC = nc ) 
        analises = AnaliseProcessoSV.objects.filter(semana=analise.semana)
        #faz análise se existe processos em aberto ainda: tirar daqui        
        for ana in analises:
            realizado = ana.realizado        
        if(realizado):
            Semana.objects.filter(id=analise.semana.id).update(realizado= True,data=datetime.date.today())
        return redirect('listProc-view', semana=analise.semana.id)
      
@login_required
def delProc(request, id):
    realizado = False
    ana = AnaliseProcesso.objects.filter(id=id).first()
    ana.delete()
    semana = Semana.objects.filter(id=ana.semana.id)
    analises = AnaliseProcesso.objects.filter(semana=ana.semana)     
    for ana in analises:
        realizado = ana.realizado    
    Semana.objects.filter(id=semana.id).update(realizado=realizado, analises=semana.analises-1)     
    return redirect('listProc-view', semana.id)

@login_required
def criarNovoProcessoIndividual(request,semana):
    semana = Semana.objects.get(id=semana)
    analise = AnaliseProcesso()
    analise.semana = semana  
    analise.save()
    Semana.objects.filter(id=semana.id).update(analises=semana.analises+1,realizado=False)
    return redirect('listProc-view', semana.id)

def report(request,id):
    semana = Semana.objects.get(id=id)    
    buffer = io.BytesIO()    
    ncs = qntdNC(semana)
    imprimirPDF(buffer,semana,request.user, ncs)
    buffer.seek(0)
    filename=semana.data
    return FileResponse(buffer, as_attachment=False, filename="Analise: "+str(semana.inicio)+" - "+str(semana.fim)+".pdf")

#esse é o home provisório do site, vou ter que ver como fazer isso de uma maneira mais desmembrada
def home(request):
    return render(request, 'user/index.html')

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
        respostas = AnaliseProcessoResposta.objects.filter(analiseProcesso=analise)
        for resposta in respostas:
            if resposta == "R":
                nc = nc+1
    return nc 

#Criar analises de processos na semana correta.
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
                analise = AnaliseProcessoSV.objects.create(semana=data['semana'])
                analises.append(analise)
                Semana.objects.get(id=id).update(processos=post.get('numProcessos'),analises=data['nAnalises'])                
            data['analises'] = analises
            return HttpResponseRedirect('./listProc/'+id)            
        else:
            #implementar tela de confirmação de semana vaga.
            #salvar a semana como vazia.
            Semana.objects.filter(id=id).update(realizado= True)
            pass     
        # aqui vou ter que inserir o usuario/empresa/e etc.
        #atualizar a semana aqui.
        return render(request, 'atividades/cadSemana.html', data)