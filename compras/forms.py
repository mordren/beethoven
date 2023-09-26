import datetime
from django.forms import ModelForm, Form
from django import forms
from user.models import UserProfile
from .models import Compra

class comprasForm(Form):
    class Meta:
        model = Compra
        
    ap = (('A','A'),('R', 'R'),('NA', 'NA') )
    descricao = forms.CharField(label='Descrição:')
    #responsavelCompra = forms.CharField(label='Responsável pela Compra:')
    #date = forms.DateField(initial=datetime.date.today().strftime('%d/%m/%y'))
    #pegar os dados, criar um para a lista de fornecedores.
    
    empresaContratada = forms.CharField(label='Empresa Contratada:')
    responsavelAnuencia = forms.CharField(label='Responsável pela Anuência da Compra')
    integridade = forms.ChoiceField(choices=ap, help_text='Se os mesmo estão íntegros, bem lacrados nas suas embalagens e funcionando:')
    labRBC = forms.ChoiceField( choices=ap, help_text='Verificar se o certificado foi feito por laboratório da RBC:')
    metodologia = forms.ChoiceField(choices=ap, help_text='VVerificar se foi usada a metodologia correta na calibração:')
    requisitosNorma = forms.ChoiceField(choices=ap, help_text='Verificar se foi usada a metodologia correta na calibração:')
    metodologia = forms.ChoiceField(choices=ap, help_text='Verificar atendimento aos requisitos solicitados:')
    calibracao = forms.ChoiceField(choices=ap, help_text='Verificar se o equipamento calibrado foi aprovado')
    observacoes = forms.CharField(widget=forms.Textarea(attrs={"rows":"7"}), label='Observações:')
    dataRecebimento = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    
    #essas coisas aqui é para mudar o help_text e colocar como descricação abaixo do input.
    def __init__(self, *args, **kwargs):
        super(comprasForm, self).__init__(*args, **kwargs)            
        #self.fields['observacoes'].required = False  
    
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})
    
    def iniciar(self,compras):
        #Para o update, traz todos os dados necessários para usuário atualizar.
        self.fields['dataRecebimento'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
        self.fields['descricao'].initial = compras.descricao
        #self.fields['responsavelCompra'].initial = compras.responsavelCompra.user.first_name
        self.fields['empresaContratada'].initial = compras.empresaContratada
        self.fields['responsavelAnuencia'].initial = compras.responsavelAnuencia
        self.fields['integridade'].initial = compras.integridade
        self.fields['labRBC'].initial = compras.labRBC
        self.fields['metodologia'].initial = compras.metodologia
        self.fields['requisitosNorma'].initial = compras.requisitosNorma
        self.fields['calibracao'].initial = compras.calibracao
        self.fields['observacoes'].initial = compras.observacoes
        self.fields['dataRecebimento'].initial = datetime.date.today().strftime('%d/%m/%y')
        return self
    
    def save(self, user):
        #faço assim para salvar, porque não dá pra fazer de forma automática
        #como é muita coisa preferi trazer pra cá o save, não sei se é o correto. Mas form é também view.
        compra = Compra()
        user = UserProfile.objects.filter(user=user).first()
        compra.date = datetime.date.today()
        compra.descricao = self.cleaned_data.get('descricao')    
        compra.responsavelCompra = user
        compra.empresaContratada = self.cleaned_data.get('empresaContratada')
        compra.responsavelAnuencia = self.cleaned_data.get('responsavelAnuencia')
        compra.integridade = self.cleaned_data.get('integridade')
        compra.labRBC = self.cleaned_data.get('labRBC')
        compra.metodologia = self.cleaned_data.get('metodologia')
        compra.requisitosNorma = self.cleaned_data.get('requisitosNorma')
        compra.calibracao = self.cleaned_data.get('calibracao')
        compra.observacoes = self.cleaned_data.get('observacoes')
        compra.save()
        return compra
    
    def create(self):
        self.fields['dataRecebimento'].widget = forms.widgets.HiddenInput()
        self.fields['dataRecebimento'].widget = forms.widgets.HiddenInput()
