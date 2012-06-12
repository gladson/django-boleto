#-*- coding: utf-8 -*-
from datetime import date
# Dependendo de onde o PIL é instalado, a referência aos módulos é feita no
# pacote PIL ou diretamente através dos nomes dos módulos 
try:
    import Image, ImageDraw
except ImportError,e:
    from PIL import Image, ImageDraw

def modulo_10(num):
    numtotal10=str()
    fator = 2
    for i in range(len(str(num))).__reversed__():
        numeros = int(num[i])
        parcial10 = numeros * fator
        numtotal10 = numtotal10+ "%s" %parcial10
        if fator == 2:
            fator = 1
        else:
            fator = 2
    soma = 0
    for i in range(len(numtotal10)).__reversed__():
        numeros = int(numtotal10[i])
        soma=soma+numeros
    resto = soma % 10
    digito = 10 - resto
    if resto == 0:
        digito = 0
    return digito      
                
def modulo_11(num,base=9,r=0):
    soma=0
    fator=2
    for i in range(len(str(num))).__reversed__():
        numeros = int(num[i])
        parcial10 = numeros * fator
        soma = soma+parcial10
        if fator == base:
            fator = 1
        fator=fator+1
    if r == 0:
        soma = soma * 10
        digito = soma % 11
        if digito == 10:
            digito = 0
        return digito     
    if r == 1:
        resto = soma % 11
        return resto

def montar_linha_digitavel(linha):
    """
    Monta a linha que o cliente pode utilizar para digitar se o c�digo de barras
    n�o puder ser lido
     Posi��o    Conte�do
     1 a 3    N�mero do banco
     4        C�digo da Moeda - 9 para Real
     5        Digito verificador do C�digo de Barras
     6 a 19   Valor (12 inteiros e 2 decimais)
     20 a 44  Campo Livre definido por cada banco
    """

    p1 = linha[0:4]
    p2 = linha[19:24]        
    p3 = modulo_10("%s%s"%(p1,p2))
    p4 = "%s%s%s" %(p1,p2,p3)
    p5 = p4[0:5]
    p6 = p4[5:]
    campo1 = "%s.%s" %(p5,p6)

    p1 = linha[24:34]
    p2 = modulo_10(p1)
    p3 = "%s%s" %(p1,p2)
    p4 = p3[0:5]
    p5 = p3[5:]
    campo2 = "%s.%s" %(p4,p5)

    p1 = linha[34:44]
    p2 = modulo_10(p1)
    p3 = "%s%s" %(p1,p2)
    p4 = p3[0:5]
    p5 = p3[5:]
    campo3 = "%s.%s" %(p4,p5)
    campo4 = linha[4]        
    campo5 = linha[5:19]

    return "%s %s %s %s %s" %(campo1,campo2,campo3,campo4,campo5)
        

def fator_vencimento(data):
    data = data.split("/")
    ano = data[2]
    mes = data[1]
    dia = data[0]
    tempo = abs(date(1997,10,07) - date(int(ano),int(mes),int(dia)))
    return tempo.days

def formatar_numero(numero,loop,insert,tipo="geral"):
    if tipo == "geral":
        numero = numero.replace(",","").replace('.','')
        while len(numero) < loop:
            numero="%s%s" %(insert,numero)
    if tipo == "valor":
        numero = numero.replace(",","").replace('.','')
        while len(numero) < loop:
            numero = "%s%s" %(insert,numero)
    if tipo == "convenio":
        while len(numero) < loop:
            numero = "%s%s" %(numero,insert)
    return numero

def gerar_codigo_banco(numero):
    parte1 = numero[0:4]
    parte2 = modulo_11(parte1)
    return "%s-%s" %(parte1,parte2)

def gerar_codigo_barras(valor, posX=0, posY=0, height = 50):
    """
    Gera a imagem do c�digo de barras do valor especificado, retornando
    um objeto PIL.Image
    """

    # padr�o 2 por 5 intercalado ( utilizado em boletos banc�rios )
    padrao = ('00110', '10001', '01001', '11000', '00101',
              '10100', '01100', '00011', '10010', '01010')
    
    # criando imagem
    imagem = Image.new('RGB',(750,80),'white')
    draw = ImageDraw.Draw(imagem)

    # verificando se o conteudo para gerar barra � impar, se for, 
    # adiciona 0 no inicial para fazer intercala��o em seguida dos pares 
    
    if (len(valor) % 2) != 0:
        valor= '0' + valor
        
    # faz intercala��o dos pares
    l=''
    for i in range(0,len(valor),2):
        p1=padrao[int(valor[i])]
        p2=padrao[int(valor[i+1])]
        for p in range(0,5):
            l+=p1[:1] + p2[:1]
            p1=p1[1:]
            p2=p2[1:]
            
    # gerando espa�os e barras 
    barra=True
    b=''
    
    # P = preto 
    # B = banco
    
    for i in range(0,len(l)):
        if l[i] == '0':
            if barra: 
                b+='P'
                barra=False
            else:
                b+='B'
                barra=True
        else:
            if barra:
                b+='PPP'
                barra=False
            else:
                b+='BBB'
                barra=True
                
    # concatena inicio e fim
    b='PBPB' + b + 'PPPBP'
    
    # P = preto 
    # B = banco 
    
    # percorre toda a string b e onde for P pinta de preto, onde for B pinta de banco 
    
    for i in range(0,len(b)):
        if b[i] == 'P':
            draw.line((posX,posY,posX,posY + height),'black')
        else:
            draw.line((posX,posY,posX,posY + height),'white')
        posX+=1
    return imagem
