#-*- coding: utf-8 -*-
from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render_to_response
from boleto import bancos
from boleto.util import gerar_codigo_barras
from io import StringIO
from boleto.bancos import BoletoBancoDoBrasil, BoletoBancoReal,\
            BoletoBradesco, BoletoCaixaEconomica, BoletoCaixaEconomicaSIGCB

def boleto_bb(request):           
    dados = dict()

    dados['nosso_numero'] = '87654'
    dados['numero_documento'] = '27.030195.10'
    
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = (date.today() + timedelta(5)
                               ).strftime("%d/%m/%Y")       # data vencimento demonstra￧￣o, data atual + 5 dias
    
    dados['data_documento'] = date.today().strftime("%d/%m/%Y")
    dados['data_processamento'] = date.today().strftime("%d/%m/%Y")
    dados['valor_boleto'] = 2950.00
    dados['taxa_boleto'] = 2.95

    # Dados da sua conta - BANCO DO BRASIL 
    dados['agencia'] = '2806'
    dados['conta'] = '99999'

    # Dados personalizados - BANCO DO BRASIL 
    dados['convenio'] = '7777777'
    dados['contrato'] = '999999'
    dados['carteira'] = '18'
    dados['variacao_carteira'] = '-019'

    # Informações do seu cliente 
    dados['sacado'] = 'Nome do seu Cliente'
    dados['endereco1'] = 'Endereço do seu Cliente'
    dados['endereco2'] = 'Cidade - Estado -  CEP: 00000-000'

    # Informações para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Compra na Loja Nonononono'
    dados['demonstrativo2'] = """Mensalidade referente a nonon nonooon nononon """
    dados['demonstrativo3'] = 'PyBoletos'

    # Instruções para o Caixa 
    dados['instrucoes1'] = '- Sr. Caixa, cobrar multa de 2% após o vencimento'
    dados['instrucoes2'] = '- Receber até 10 dias após o vencimento'
    dados['instrucoes3'] = '- Em caso de dúvidas entre em contato conosco: opencode@gmail.com '
    dados['instrucoes4'] = '- Emitido pelo sistema PyBoletos '


    # Dados opcionais de acordo com o banco ou cliente 
    dados['quantidade'] = '10'
    dados['valor_unitario'] = '10'
    dados['aceite'] = "N";        
    dados['especie'] = 'R$'
    dados['especie_doc'] = 'DM'


    # Deus Dados     
    dados['identificacao'] = ' PyBoletos '
    dados['cpf_cnpj'] = ''
    dados['endereco'] = 'Coloque o endereço da sua empresa aqui'
    dados['cidade_uf'] = 'Cidade / Estado'
    dados['cedente'] = 'Coloque a Razã Social da sua empresa aqui'

    dados_resposta = BoletoBancoDoBrasil.get_dados(7,2,dados)

    return render_to_response("boletos/bancodobrasil.html", dados_resposta)    

def boleto_real(request):
    dados = dict()

    dados['taxa_boleto'] = 2.95
    
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = (date.today() + timedelta(5)
                               ).strftime("%d/%m/%Y")       # data vencimento demonstra￧￣o, data atual + 5 dias   
    
    dados["data_documento"] = date.today().strftime("%d/%m/%Y")
    dados["data_processamento"] = date.today().strftime("%d/%m/%Y")

    dados['valor_boleto'] = 2950.00        
    
    
    dados['nosso_numero'] = '0000000123456'                     #Nosso numero sem o DV - REGRA: M￡ximo de 13 caracteres!
    dados['numero_documento'] = '1234567'                       # Num do pedido ou do documento 
    

    # Dados do seu cliente 
    dados['sacado'] = 'Nome do seu Cliente'
    dados['endereco1'] = 'Endere￧o do seu Cliente'
    dados['endereco2'] = 'Cidade - Estado -  CEP: 00000-000'


    # Informa￧￵es para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Compra na Loja Nonononono'
    dados['demonstrativo2'] = 'Mensalidade referente a nonon nonooon nononon'
    dados['demonstrativo3'] = ' PyBoletos '


    # Instru￧￵es para o caixa 
    dados['instrucoes1'] = '- Sr. Caixa, cobrar multa de 2% ap￳s o vencimento'
    dados['instrucoes2'] = '- Receber at￩ 10 dias ap￳s o vencimento'
    dados['instrucoes3'] = '- Em caso de d￺vidas entre em contato conosco: opencode@gmail.com'
    dados['instrucoes4'] = '- Emitido pelo sistema PyBoletos'


    # Dados opcionais de acordo com o Banco ou cliente 
    dados['quantidade'] = ''
    dados['valor_unitario'] = ''
    dados['aceite'] = 'N'        
    dados['especie'] = 'R$'
    dados['especie_doc'] = ''


  
    # Dados da sua conta - Banco real
    dados['agencia'] = '1234'    #Num da agencia, sem digito
    dados['conta'] = '0012345'      # Num da conta, sem digito

    
    # Dados Personalizados - banco real
    dados['carteira'] = '57'            # C￳digo da Carteira: 

    # Seus Dados 
    dados['identificacao'] = 'PyBoletos'
    dados['cpf_cnpj'] = ''
    dados['endereco'] = 'Coloque o endere￧o da sua empresa aqui'
    dados['cidade_uf'] = 'Cidade / Estado'
    dados['cedente'] = 'Coloque a Raz￣o Social da sua empresa aqui'

    dados_resposta = BoletoBancoReal.get_dados(dados)

    return render_to_response("boletos/bancoreal.html", dados_resposta)   

def boleto_caixa(request): 
    dados = dict()
    dados['taxa_boleto'] = 2.95
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = (date.today() + timedelta(5)
                               ).strftime("%d/%m/%Y")       # data vencimento demonstra￧￣o, data atual + 5 dias   
    
    dados["data_documento"] = date.today().strftime("%d/%m/%Y")
    dados["data_processamento"] = date.today().strftime("%d/%m/%Y")

    dados['valor_boleto'] = 2950.00


    dados['inicio_nosso_numero'] = '80'         # Carteira SR: 80, 81 ou 82  -  
                                                # Carteira CR: 90 (Confirmar com gerente qual usar)

    dados['nosso_numero'] = '19525086'          # Nosso numero sem o DV - REGRA: M￡ximo de 8 caracteres!
    dados['numero_documento'] = '27.030195.10'    # Num do pedido ou do documento

    # Dados do seu cliente 
    dados['sacado'] = 'Nome do seu Cliente'
    dados['endereco1'] = 'Endere￧o do seu Cliente'
    dados['endereco2'] = 'Cidade - Estado -  CEP: 00000-000'


    # Informa￧￵es para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Compra na Loja Nonononono'
    dados['demonstrativo2'] = 'Mensalidade referente a nonon nonooon nononon'
    dados['demonstrativo3'] = ' PyBoletos '


    # Instru￧￵es para o caixa 
    dados['instrucoes1'] = '- Sr. Caixa, cobrar multa de 2% ap￳s o vencimento'
    dados['instrucoes2'] = '- Receber at￩ 10 dias ap￳s o vencimento'
    dados['instrucoes3'] = '- Em caso de d￺vidas entre em contato conosco: opencode@gmail.com'
    dados['instrucoes4'] = '&nbsp; Emitido pelo sistema PyBoletos'


    # Dados opcionais de acordo com o Banco ou cliente 
    dados['quantidade'] = ''
    dados['valor_unitario'] = ''
    dados['aceite'] = ''        
    dados['especie'] = 'R$'
    dados['especie_doc'] = ''


    # Dados da sua conta - CAIXA ECONOMICA FEDERAL 
    dados['agencia'] = '1565'  # Num da agencia, sem digito
    dados['conta'] = '13877'   # Num da conta, sem digito
    dados['conta_dv'] = '4'    # Digito do Num da conta

    # Dados personalizados - CAIXA ECONOMICA FEDERAL 
    dados['conta_cedente'] = '87000000414'  # ContaCedente do Cliente, sem digito (Somente N￺meros)
    dados['conta_cedente_dv'] = '3'         # Digito da ContaCedente do Cliente
    dados['carteira'] = 'SR'                # C￳digo da Carteira: pode ser SR (Sem Registro) ou CR (Com Registro) 
                                            #                                - (Confirmar com gerente qual usar)

    # Seus Dados 
    dados['identificacao'] = 'PyBoletos'
    dados['cpf_cnpj'] = ''
    dados['endereco'] = 'Coloque o endere￧o da sua empresa aqui'
    dados['cidade_uf'] = 'Cidade / Estado'
    dados['cedente'] = 'Coloque a Raz￣o Social da sua empresa aqui'

    dados_resposta = BoletoCaixaEconomica.get_dados(dados)

    return render_to_response("boletos/caixaeconomica.html", dados_resposta)   

def boleto_caixa_sigcb(request):
    """
     Boleto CAIXA ECONOMICA FEDERAL  ( SIGCB)
    """

    dados = dict()


    dados['taxa_boleto'] = 2.95
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = (date.today() + timedelta(5)
                               ).strftime("%d/%m/%Y")       # data vencimento demonstra￧￣o, data atual + 5 dias   
    
    dados["data_documento"] = date.today().strftime("%d/%m/%Y")
    dados["data_processamento"] = date.today().strftime("%d/%m/%Y")

    dados['valor_boleto'] = 2950.00
    dados['numero_documento'] = '27.030195.10'    # Num do pedido ou do documento
    
    # Composi￧￣o Nosso Numero - CEF SIGCB
    dados['nosso_numero1'] = '000'       # tamanho 3
    dados['nosso_numero_const1'] = '1'   # constanto 1 , 1=registrada , 2=sem registro
    dados['nosso_numero2'] = '000'       # tamanho 3
    dados['nosso_numero_const2'] = '4'   # constanto 2 , 4=emitido pelo proprio cliente
    dados['nosso_numero3'] = '000000019' # tamanho 9
    

    # Dados do seu cliente 
    dados['sacado'] = 'Nome do seu Cliente'
    dados['endereco1'] = 'Endere￧o do seu Cliente'
    dados['endereco2'] = 'Cidade - Estado -  CEP: 00000-000'


    # Informa￧￵es para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Compra na Loja Nonononono'
    dados['demonstrativo2'] = 'Mensalidade referente a nonon nonooon nononon'
    dados['demonstrativo3'] = ' PyBoletos '


    # Instru￧￵es para o caixa 
    dados['instrucoes1'] = '- Sr. Caixa, cobrar multa de 2% ap￳s o vencimento'
    dados['instrucoes2'] = '- Receber at￩ 10 dias ap￳s o vencimento'
    dados['instrucoes3'] = '- Em caso de d￺vidas entre em contato conosco: opencode@gmail.com'
    dados['instrucoes4'] = '&nbsp; Emitido pelo sistema PyBoletos'


    # Dados opcionais de acordo com o Banco ou cliente 
    dados['quantidade'] = ''
    dados['valor_unitario'] = ''
    dados['aceite'] = ''        
    dados['especie'] = 'R$'
    dados['especie_doc'] = ''


    # Dados da sua conta - CAIXA ECONOMICA FEDERAL 
    dados['agencia'] = '1234'  # Num da agencia, sem digito
    dados['conta'] = '123'     # Num da conta, sem digito
    dados['conta_dv'] = '0'    # Digito do Num da conta

    # Dados personalizados - CAIXA ECONOMICA FEDERAL 
    dados['conta_cedente'] = '123456'  # ContaCedente do Cliente, sem digito (Somente N￺meros)
    dados['carteira'] = 'SR'                # C￳digo da Carteira: pode ser SR (Sem Registro) ou CR (Com Registro) 
                                            #                                - (Confirmar com gerente qual usar)
    # Seus Dados 
    dados['identificacao'] = 'PyBoletos'
    dados['cpf_cnpj'] = ''
    dados['endereco'] = 'Coloque o endere￧o da sua empresa aqui'
    dados['cidade_uf'] = 'Cidade / Estado'
    dados['cedente'] = 'Coloque a Raz￣o Social da sua empresa aqui'

    dados_resposta = BoletoCaixaEconomicaSIGCB.get_dados(dados)

    return render_to_response("boletos/caixaeconomica.html", dados_resposta)   


    
def boleto_bradesco(request):
    dados = dict()

    dados['taxa_boleto'] = 2.95
    
    #dados['data_vencimento'] = 'DD/MM/AAAA'                 # Informar data vencimento
    dados['data_vencimento'] = (date.today() + timedelta(5)
                               ).strftime("%d/%m/%Y")       # data vencimento demonstra￧￣o, data atual + 5 dias   
    
    dados["data_documento"] = date.today().strftime("%d/%m/%Y")
    dados["data_processamento"] = date.today().strftime("%d/%m/%Y")

    dados['valor_boleto'] = 2950.00        
    
    
    dados['nosso_numero'] = '75896452'                          #Nosso numero sem o DV - REGRA: M￡ximo de 11 caracteres!
    dados['numero_documento'] = dados['nosso_numero']           # Num do pedido ou do documento = Nosso numero


    # Dados do seu cliente 
    dados['sacado'] = 'Nome do seu Cliente'
    dados['endereco1'] = 'Endere￧o do seu Cliente'
    dados['endereco2'] = 'Cidade - Estado -  CEP: 00000-000'


    # Informa￧￵es para o cliente 
    dados['demonstrativo1'] = 'Pagamento de Compra na Loja Nonononono'
    dados['demonstrativo2'] = 'Mensalidade referente a nonon nonooon nononon'
    dados['demonstrativo3'] = ' PyBoletos '


    # Instru￧￵es para o caixa 
    dados['instrucoes1'] = '- Sr. Caixa, cobrar multa de 2% ap￳s o vencimento'
    dados['instrucoes2'] = '- Receber at￩ 10 dias ap￳s o vencimento'
    dados['instrucoes3'] = '- Em caso de d￺vidas entre em contato conosco: opencode@gmail.com'
    dados['instrucoes4'] = '- Emitido pelo sistema PyBoletos'


    # Dados opcionais de acordo com o Banco ou cliente 
    dados['quantidade'] = '001'
    dados['valor_unitario'] = str("%s" %"%.2f" %(dados['valor_boleto']+dados['taxa_boleto'])).replace('.',',')
    dados['aceite'] = ''        
    dados['especie'] = 'R$'
    dados['especie_doc'] = 'DS'


  
    # Dados da sua conta - Bradesco
    dados['agencia'] = '1172'    #Num da agencia, sem digito
    dados['agencia_dv'] = '0'    #Digito do Num da agencia
    dados['conta'] = '0403005'      # Num da conta, sem digito
    dados['conta_dv'] = '2'       # Digito do Num da conta

    
    # Dados Personalizados - Bradesco
    dados['conta_cedente'] = '0403005'  # ContaCedente do Cliente, sem digito (Somente N￺meros)
    dados['conta_cedente_dv'] = '2'     # Digito da ContaCedente do Cliente
    dados['carteira'] = '06'            # C￳digo da Carteira: pode ser 06 ou 03

    # Seus Dados 
    dados['identificacao'] = 'PyBoletos'
    dados['cpf_cnpj'] = ''
    dados['endereco'] = 'Coloque o endere￧o da sua empresa aqui'
    dados['cidade_uf'] = 'Cidade / Estado'
    dados['cedente'] = 'Coloque a Raz￣o Social da sua empresa aqui'
    
    dados_resposta = BoletoBradesco.get_dados(dados)

    return render_to_response("boletos/bradesco.html", dados_resposta)   

def imagem_barras(request):
    codigo = request.GET["codigo"]
    
    # codigo de barra completo em dígitos
    # formato que deseja salvar a imagem (PNG,GIF)
    tipo='GIF'
    # retornando uma imagem a partir do código de barra
    image = gerar_codigo_barras(codigo)

    response = HttpResponse(mimetype = "image/"+tipo)        
    image.save(response, tipo)        
    return response
