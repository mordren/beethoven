from django.forms import ModelForm, Form
from django import forms
from .models import Semana

class SemanaForm(ModelForm):
    class Meta:
        model = Semana        
        fields = ['numero','processos']
        
class analiseForm(Form):
    ap = (('A','A'),('R', 'R'),('NA', 'NA') )
    OS = forms.IntegerField(label="Ordem de Serviço: ")
    crlv = forms.ChoiceField(label="CRVL", choices=ap, help_text="1)	CRLV ou CRV ou NF compra veículo – HABILITAÇÃO do condutor")
    decalque = forms.ChoiceField(choices=ap, help_text="2)	DECALQUE do número do chassi;")
    vistoriaInicial = forms.ChoiceField(label="Vistoria Incial", choices=ap, help_text="3)	FOR ADM 31 ORDEM DE SERVIÇO com a VISTORIA INICIAL;")
    verificaoEscopo = forms.ChoiceField(label="Verificação do escopo Correto", choices=ap, help_text="4)	Lista de verificação correta ao escopo, rastreável, com anotações corretas, correções conforme procedimento, com quantificáveis rastreado ao equipamento entre outros;")
    linhaInspecao = forms.ChoiceField(label="Linha de Inspeção", choices=ap, help_text="5)	Relatório da LINHA DE INSPEÇÃO, assinado por todos, aprovado, com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;")
    opacidade = forms.ChoiceField(choices=ap, help_text="6)	Relatório de OPACIDADE, ANÁLISE DE GASES quando aplicável, assinado por todos, aprovado, com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;")
    ruido = forms.ChoiceField(choices=ap, help_text="7)	Relatório de RUÍDO, quando aplicável, assinado por todos, aprovado, com número de patrimônio, rastreavel ao veículo, equipamento calibrado entre outros;")
    naoConformidade = forms.ChoiceField(label="Não conformidades", choices=ap, help_text="8)	Registro de NÃO CONFORMIDADE;")
    rasurasProcessos = forms.ChoiceField(label="Rasuras no processo", choices=ap, help_text="9)	Verificar a existência de RASURAS NOS PROCESSOS;")
    registrosFotograficos = forms.ChoiceField(label="Registros Fotográficos", choices=ap, help_text="10)	Registro fotográfico do EIXO (s) DIANTEIRO (s) e EIXO (s) TRASEIRO (s) do veículo e a banda de rodagem dos pneus dianteiros e pneus traseiros. A foto do eixo dianteiro deve ser tirada no sentido do eixo traseiro, a foto do eixo traseiro deve ser tirada no sentido do eixo dianteiro, quando houver um terceiro eixo, o registro fotográfico deve ser tirado no sentido do eixo traseiro; Registro fotográfico do Para todos os veículos com PARA-CHOQUE homologados, um (1) registro fotográfico da plaqueta de homologação do pára-choque; Registro fotográfico do transversal do PINO-REI e de sua MESA LIMPOS ou QUINTA RODA, quando aplicável; Registro fotográfico das LATERAIS DOS VEÍCULOS com as FAIXAS REFLETIVAS, quando aplicáveis; Registro fotográfico ALÍVIO DE PESO no eixo direcional em veículos pesados, quando aplicável; Registro fotográfico da TRASEIRA DO VEÍCULO na linha de inspeção mecanizada, que tenha possibilidade de leitura da PLACA de licença no RELATÓRIO DE INSPEÇÃO.Obs. Os registros fotográficos devem conter data e hora.")
    filmagem = forms.ChoiceField(choices=ap, help_text="11)	Filmagem de todas as etapas de inspeção, verificar calibragem de pneus, ensaio de regloscopio, verificação do sistema de sinalização, ensaio de opacidade e ruído, dentre outros, a filmagem deve conter data e horas no formato (DD/MM/AAAA) e (hh:mm:ss).")
    observacoes = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
     
    def __init__(self, *args, **kwargs):
        super(analiseForm, self).__init__(*args, **kwargs)
        self.fields['observacoes'].required = False
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})
    
    def iniciar(self, analise):
        self.fields['OS'].initial = analise.OS
        self.fields['crlv'].initial = analise.crlv
        self.fields['decalque'].initial = analise.decalque
        self.fields['vistoriaInicial'].initial = analise.vistoriaInicial
        self.fields['linhaInspecao'].initial = analise.linhaInspecao
        self.fields['opacidade'].initial = analise.opacidade
        self.fields['ruido'].initial = analise.ruido
        self.fields['rasurasProcessos'].initial = analise.rasurasProcessos
        self.fields['registrosFotograficos'].initial = analise.registrosFotograficos        
        self.fields['observacoes'].initial = analise.observacoes
        return self
        