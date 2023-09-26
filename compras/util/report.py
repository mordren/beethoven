from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
from django.conf import settings
from datetime import datetime
from user.models import UserProfile
from compras.models import Compra

media_url = settings.MEDIA_ROOT

def mp(mm):
    return mm/0.352777

def imprimirPDF(link,compra,user):  
    usuario = UserProfile.objects.filter(user=user).first()
    
    temp = "/templates/compras/template_" + str(usuario.empresa.nome)
    
    local = media_url
    outfile = "result.pdf"
    
    template = PdfReader(local+temp+".pdf", decompress=False).getPage(0)
    template_obj = pagexobj(template)

    canvas = Canvas(link)
    canvas.setPageSize(A4)

    xobj_name = makerl(canvas, template_obj)
    canvas.doForm(xobj_name)
    
    canvas.setFontSize(10)

    canvas.setTitle("Análise Crítica de : ")
    #data execução
    canvas.drawString(mp(177),mp(240), datetime.strftime(compra.date,"%d/%m/%Y"))
    #responsável pela compra
    canvas.drawString(mp(105),mp(240), compra.responsavelAnuencia)
    #descrição 
    canvas.drawString(mp(15),mp(240), compra.descricao)
    #Empresa contratada
    canvas.drawString(mp(15),mp(225), compra.empresaContratada)
    #Funcionário anuência
    canvas.drawString(mp(105),mp(225), compra.responsavelAnuencia)
    
    if compra.integridade == "A":
        #integros SIM
        canvas.drawString(mp(21),mp(202), 'x')
    elif compra.integridade == "R":
        #integros NÃO 
        canvas.drawString(mp(35),mp(202), 'x')
    #integros NA
    else:
        canvas.drawString(mp(50.5),mp(202), 'x')
    
    if compra.requisitosNorma == "A":
        #norma SIM
        canvas.drawString(mp(21),mp(185.5), 'x')
    elif compra.requisitosNorma == "R":
        #norma NÃO 
        canvas.drawString(mp(35),mp(185.5), 'x')
    else:
        #norma NA
        canvas.drawString(mp(50.5),mp(185.5), 'x')
    
    if compra.labRBC == "A":
        #RBC SIM
        canvas.drawString(mp(21),mp(169), 'x')
    elif compra.labRBC == "R":
        #RBC NÃO 
        canvas.drawString(mp(35),mp(169), 'x')
    else:
        #RBC NA
        canvas.drawString(mp(50.5),mp(169), 'x')
    
    if compra.metodologia == "A":
        #metodologia SIM
        canvas.drawString(mp(21),mp(152.5), 'x')    
    elif compra.metodologia == "R":
        #metodologia NÃO 
        canvas.drawString(mp(35),mp(152.5), 'x')
    else:
        #metodologia NA
        canvas.drawString(mp(50.5),mp(152.5), 'x')
    
    if compra.requisitos == "A":
        #requisitos SIM
        canvas.drawString(mp(21),mp(136), 'x')
    elif compra.requisitos == "R":
        #requisitos NÃO 
        canvas.drawString(mp(34),mp(136), 'x')
    else:
        #requisitos NA
        canvas.drawString(mp(50.5),mp(136), 'x')
        
    if compra.calibracao == "A":    
        #calibracao SIM
        canvas.drawString(mp(21),mp(120), 'x')
    elif compra.calibracao == "R":
        #calibracao NÃO 
        canvas.drawString(mp(34),mp(120), 'x')
    else:
        #calibracao NA
        canvas.drawString(mp(50.5),mp(120), 'x')
 
    #observações
    #canvas.drawString(mp(13),mp(76), compra.observacoes)
    
    canvas.drawString(mp(42), mp(107), datetime.strftime(compra.date,"%d/%m/%Y"))
    
    textObject = canvas.beginText(mp(12.8),mp(92))
    for line in compra.observacoes.splitlines(False):
        textObject.textLine(line.rstrip())
    canvas.drawText(textObject)
    
    #responsável 
    responsavel = compra.responsavelCompra.user.first_name + ' ' + compra.responsavelCompra.user.last_name
    canvas.drawString(mp(12.5),mp(51), responsavel)
 
    canvas.showPage()
    canvas.save()
    return canvas