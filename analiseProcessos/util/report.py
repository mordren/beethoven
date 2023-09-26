from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
from django.conf import settings
from datetime import datetime
from user.models import UserProfile

from analiseProcessos.models import AnaliseProcesso

media_url = settings.MEDIA_ROOT


def mp(mm):
    return mm/0.352777

def imprimirPDF(link,semana,user,ncs):  
    usuario = UserProfile.objects.filter(user=user).first()
    user = usuario.user.first_name + ' ' + usuario.user.last_name
    temp = "/templates/analiseProcessos/template_" + str(usuario.empresa.nome)
    
    local = media_url
    outfile = "result.pdf"
    
    template = PdfReader(local+temp+".pdf", decompress=False).getPage(0)
    template_obj = pagexobj(template)

    canvas = Canvas(link)
    canvas.setPageSize(A4)

    xobj_name = makerl(canvas, template_obj)
    canvas.doForm(xobj_name)

    canvas.setTitle("Análise Crítica de : "+datetime.strftime(semana.inicio,"%d/%m/%Y")+' a '+datetime.strftime(semana.fim,"%d/%m/%Y"))
    linhaDaOS = 210
    colunaItem = 54
    linha = 5.3

    #data execução
    canvas.drawString(mp(51),mp(256), datetime.strftime(semana.data,"%d/%m/%Y"))
    #engenheiro pegar da sessão no método
    canvas.drawString(mp(115),mp(256), user)
    #amostrar número
    #amostragem = round(int(semana.processos*0.05)+0.5)
    canvas.drawString(mp(81),mp(250.5), str(semana.analises))
    #quantidades totais
    canvas.drawString(mp(57),mp(245.5), str(semana.processos))
    #período semana início
    canvas.drawString(mp(92),mp(240.5), datetime.strftime(semana.inicio,"%d/%m/%Y"))
    #período semana fim
    canvas.drawString(mp(155),mp(240.5), datetime.strftime(semana.fim,"%d/%m/%Y"))

    canvas.setFontSize(10)
    
    
    #ordem de serviço:
    #corrigir quando tiver mais usuários;
    i = 0
    analises = AnaliseProcesso.objects.filter(semana=semana)
    
    for analise in analises:        
        l = linha * i
        canvas.drawString(mp(25),mp(linhaDaOS-l), str(analise.OS))

        #Item da coluna
        for f in range(11):
            col = (7.1 * f) + colunaItem
            attr = getAttr(analise, f)
            canvas.drawString(mp(col),mp(linhaDaOS-l), str(attr))            
        i = i+1

        
    canvas.showPage()
    template = PdfReader(local+temp+".pdf", decompress=False).getPage(1)
    template_obj = pagexobj(template)

    canvas.setPageSize(A4)

    xobj_name = makerl(canvas, template_obj)
    canvas.doForm(xobj_name)
    
    canvas.setFontSize(12)
    if(ncs == 0):
    #não
        canvas.drawString(mp(85.5),mp(267.5),"X")
    #sim
    else:    
        canvas.drawString(mp(67.5),mp(267.5),"X")
    #RNC
    
    canvas.drawString(mp(160),mp(268),str(ncs))
    #usuario
    canvas.drawString(mp(20),mp(240), user)

    canvas.showPage()
    canvas.save()
    return canvas

def getAttr(analise, opcao):
    att = []
    att.append("crlv")
    att.append("decalque")
    att.append("vistoriaInicial")
    att.append("verificaoEscopo")
    att.append("linhaInspecao")
    att.append("opacidade")
    att.append("ruido")
    att.append("naoConformidade")
    att.append("rasurasProcessos")
    att.append("registrosFotograficos")
    att.append("filmagem")
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute(f"SELECT {att[opcao]} FROM analiseProcessos_analiseprocesso WHERE id = {analise.id} ")   
    row = cursor.fetchone()
    return row[0]