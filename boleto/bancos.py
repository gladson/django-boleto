# -*- coding: utf-8
from datetime import date
from djboleto.boleto import util
from django.conf import settings

class Boleto(object):
    
    @staticmethod
    def get_dados(dados):
        dados["settings"] = settings
        
class BoletoBancoDoBrasil(Boleto):
    
    @staticmethod
    def get_dados(formatconvenio,formatnnumero,dados):        
        """
         Retorna dados do boleto          
        """
        Boleto.get_dados(dados)
        
        dados['codigobanco']= '001'
        dados['nummoeda'] = '9'         
        dados['livre_zeros'] = '000000'

        fator_vencimento = util.fator_vencimento(dados["data_vencimento"])  
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = util.formatar_numero(str(vtotal),10,0,'valor')
        agencia = util.formatar_numero(dados["agencia"],4,0)   
        conta = util.formatar_numero(dados["conta"],8,0)

        boleto = dict()
        boleto = dados
        boleto['codigobancodv'] = util.gerar_codigo_banco(dados['codigobanco'])
        boleto['agenciaconta'] = "%s-%s / %s-%s" %(agencia,util.modulo_11(agencia),conta,util.modulo_11(conta))
        boleto['valor'] = vtotal.replace('.',',')
        
        # Carteira 18 com Conv�nio de 8 d�gitos
        if formatconvenio == 8:            
            convenio = util.formatar_numero(dados['convenio'],8,0,'convenio')
            
            # Noss� numero de at� 9 d�gitos 
            nossonumero = util.formatar_numero(dados['nosso_numero'],9,0)
            boleto['nossonumero'] = nossonumero
            boleto['convenio'] = convenio
   
            dv = util.modulo_11("%s%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                    dados['nummoeda'],
                                                    fator_vencimento,
                                                    valor,
                                                    dados['livre_zeros'],
                                                    convenio,
                                                    nossonumero,
                                                    dados['carteira']))
                                                    
            linha = "%s%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                           dados['nummoeda'],
                                           dv,
                                           fator_vencimento,
                                           valor,
                                           dados['livre_zeros'],
                                           convenio,
                                           nossonumero,
                                           dados['carteira'])
            boleto['codigobarra'] = linha 
            boleto['linhadigitavel'] = util.montar_linha_digitavel(linha)
              
            # Montando o nosso numero que aparecer� no boleto
            nossonumero = "%s%s-%s" %(convenio,nossonumero, util.modulo_11("%s%s"%(convenio,nossonumero)))
            boleto['nossonumeroformatado'] = nossonumero
            return  boleto                                   
                        
        # Carteira 18 com Conv�nio de 7 d�gitos
        if formatconvenio == 7:            
            convenio = util.formatar_numero(dados['convenio'],7,0,'convenio')
            
            # Noss� numero de at� 10 d�gitos 
            nossonumero = util.formatar_numero(dados['nosso_numero'],10,0)
            boleto['convenio'] = convenio
            boleto['nossonumero'] = nossonumero
            
            dv = util.modulo_11("%s%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                      dados['nummoeda'],
                                                      fator_vencimento,
                                                      valor,
                                                      dados['livre_zeros'],
                                                      convenio,
                                                      nossonumero,
                                                      dados['carteira']))
          
            
            linha = "%s%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                           dados['nummoeda'],
                                           dv,
                                           fator_vencimento,
                                           valor,
                                           dados['livre_zeros'],
                                           convenio,
                                           nossonumero,
                                           dados['carteira'])

            boleto['codigobarra'] = linha 
            boleto['linhadigitavel'] = util.montar_linha_digitavel(linha)            
            # Montando o nosso numero que aparecer� no boleto
            nossonumero = "%s%s" %(convenio,nossonumero)
            boleto['nossonumeroformatado'] = nossonumero
                                    
            return boleto     
        
        # Carteira 18 com Conv�nio de 6 d�gitos 
        if formatconvenio == 6:            
            convenio = util.formatar_numero(dados['convenio'],6,0,'convenio')            
            if formatnnumero == 1:                
                # Noss� numero de at� 5 d�gitos 
                nossonumero = util.formatar_numero(dados['nosso_numero'],5,0)   
                boleto['nossonumero'] = nossonumero             
                dv = util.modulo_11("%s%s%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                          dados['nummoeda'],
                                                          fator_vencimento,
                                                          valor,
                                                          convenio,
                                                          nossonumero,
                                                          agencia,
                                                          conta,                                                          
                                                          dados['carteira']))

                linha = "%s%s%s%s%s%s%s%s%s%s" %( dados['codigobanco'],
                                                  dados['nummoeda'],
                                                  dv,
                                                  fator_vencimento,
                                                  valor,
                                                  convenio,                                                 
                                                  nossonumero,
                                                  agencia,
                                                  conta,
                                                  dados['carteira'])
                boleto['codigobarra'] = linha 
                boleto['linhadigitavel'] = util.montar_linha_digitavel(linha)   
                # montando o nosso numero que aparecer� no boleto
                nossonumero = "%s%s-%s" %(convenio,
                                          nossonumero,
                                          util.modulo_11("%s%s" %(convenio,
                                                                  nossonumero))) 
                boleto['nossonumeroformatado'] = nossonumero                
                return  boleto
                                                                                  
                
            if formatnnumero == 2:
                
                # Nosso n�mero de at� 17 d�gitos
                
                nservico = '21'
                nossonumero = util.formatar_numero(dados['nosso_numero'],17,0)
                boleto['nossonumero'] = nossonumero  
                
                dv = util.modulo_11("%s%s%s%s%s%s%s"%(dados['codigobanco'],
                                                          dados['nummoeda'],
                                                          fator_vencimento,
                                                          valor,
                                                          convenio,
                                                          nossonumero,
                                                          nservico))
                
                linha = "%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                             dados['nummoeda'],
                                             dv,
                                             fator_vencimento,
                                             valor,
                                             convenio,                                                 
                                             nossonumero,
                                             nservico)
                boleto['codigobarra'] = linha                
                boleto['linhadigitavel'] = util.montar_linha_digitavel(linha)   
                boleto['nossonumeroformatado'] = nossonumero
                return boleto
            
class BoletoBancoReal(Boleto):
        
    @staticmethod
    def get_dados(dados):                
        Boleto.get_dados(dados)
        
        dados['codigobanco'] = '356'
        dados['codigobancodv'] = util.gerar_codigo_banco(dados['codigobanco'])
        dados['nummoeda'] = '9'
        
        fator_vencimento = util.fator_vencimento(dados['data_vencimento'])

        boleto = dados        
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = util.formatar_numero(str(vtotal),10,0,'valor')

        boleto['valor'] = vtotal.replace('.',',')
        
        agencia = util.formatar_numero(dados['agencia'],4,0)   
        conta = util.formatar_numero(dados['conta'],7,0)
        nossonumero = util.formatar_numero(dados['nosso_numero'],13,0)
        # Digitao - Digito de Cobranca do banco Real
        digitao_cobranca = util.modulo_10("%s%s%s" %(nossonumero,agencia,conta))
        
        linha = "%s%s0%s%s%s%s%s%s" %(dados['codigobanco'],
                                      dados['nummoeda'],
                                      fator_vencimento,
                                      valor,
                                      agencia,
                                      conta,
                                      digitao_cobranca,
                                      nossonumero)
        
        linha = BoletoBancoReal.digito_verificador_barra(linha)        
        agencia_codigo = "%s/%s/%s" %(agencia,conta,digitao_cobranca)
        boleto['codigobarra'] = linha
        boleto['linha_digitavel'] = util.montar_linha_digitavel(linha)
        boleto['agencia_codigo'] = agencia_codigo
        boleto['nossonumeroformatado'] = nossonumero
                
        return boleto
        
    @staticmethod
    def digito_verificador_barra(numero):
        pesos = '43290876543298765432987654329876543298765432'
        if len(numero) == 44:
            soma = 0
            for i in range(len(numero)):
                soma=soma+(int(numero[i]) * int(pesos[i]))
                
            num_temp = 11 - (soma % 11)
            if num_temp >= 10:
                num_temp = 1
            
            l = list(numero)    
            l[4] = str(num_temp)
            numero = str()
            for c in l:
                numero = numero+"%s" %c
                
        return numero        
    
class BoletoBradesco(Boleto):
    
    @staticmethod
    def get_dados(dados):
        Boleto.get_dados(dados)
       
        dados['codigobanco'] = '237'
        dados['nummoeda'] = '9'
        
        boleto = dados
        
        boleto['codigobancodv'] = util.gerar_codigo_banco(dados['codigobanco'])
        fator_vencimento = util.fator_vencimento(dados['data_vencimento'])
        
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = util.formatar_numero(str(vtotal),10,0,'valor')

        boleto['valor'] = vtotal.replace('.',',')        
        agencia = util.formatar_numero(dados['agencia'],4,0)   
        conta = util.formatar_numero(dados['conta'],6,0)
        conta_dv = util.formatar_numero(dados['conta_dv'],1,0)
        
        # nosso nÃºmero (sem dv) Ã© 11 digitos
        nnum = "%s%s" %(util.formatar_numero(dados['carteira'],2,0),util.formatar_numero(dados['nosso_numero'],11,0))
        
        # dv do nosso nÃºmero
        dv_nosso_numero = BoletoBradesco.digito_verificador_nossonumero(nnum)
        
        # conta cedente (sem dv) Ã© 7 digitos        
        boleto['conta_cedente'] = util.formatar_numero(dados['conta_cedente'],7,0)
        boleto['conta_devente_dv'] = util.formatar_numero(dados['conta_cedente_dv'],1,0)
        
        boleto['nossonumero'] = nnum
        boleto['dvnossonumero'] = dv_nosso_numero
        
        # 43 numeros para o calculo do digito verificador do codigo de barras
        dv = BoletoBradesco.digito_verificador_barra("%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                                                   dados['nummoeda'],
                                                                   fator_vencimento,
                                                                   valor,
                                                                   agencia,
                                                                   nnum,
                                                                   boleto['conta_cedente'],
                                                                   '0'))

        # Numero para o codigo de barras com 44 digitos
        linha = "%s%s%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                     dados['nummoeda'],
                                     dv,
                                     fator_vencimento,
                                     valor,
                                     agencia,
                                     nnum,
                                     boleto['conta_cedente'],'0')

        nossonumero = "%s/%s-%s" %(nnum[0:2],nnum[2:],dv_nosso_numero)
        agencia_codigo = "%s-%s / %s-%s" %(agencia,dados['agencia_dv'],boleto['conta_cedente'],boleto['conta_devente_dv'])

        boleto['codigobarra'] = linha
        boleto['linha_digitavel'] = util.montar_linha_digitavel(linha)
        boleto['agencia_codigo'] = agencia_codigo
        boleto['nossonumeroformatado'] = nossonumero
        
        return boleto
    
    @staticmethod
    def digito_verificador_nossonumero(numero):
        resto2 = util.modulo_11(numero,7,1)
        digito = 11 - resto2
        if digito == 10:
            dv = 'P'
        elif digito == 11:
            dv = 0
        else:
            dv = digito
         
        return dv
       
    @staticmethod       
    def digito_verificador_barra(numero):
        resto2 = util.modulo_11(numero,9,1)
        if resto2 == 0 or resto2 == 1 or resto2 == 10:
            dv = 1
        else:
            dv = 11 - resto2
        return dv
        
class BoletoCaixaEconomica(Boleto):
    
    @staticmethod
    def get_dados(dados):
        Boleto.get_dados(dados)
                
        dados['codigobanco'] = '104'
        dados['nummoeda'] = '9'
                    
        boleto = dados
        
        fator_vencimento = util.fator_vencimento(dados["data_vencimento"])
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = util.formatar_numero(str(vtotal),10,0,'valor')
        agencia = util.formatar_numero(dados["agencia"],4,0)   
        conta = util.formatar_numero(dados["conta"],5,0)
                
        boleto['codigobancodv'] = util.gerar_codigo_banco(dados['codigobanco'])
        
        boleto['valor'] = vtotal.replace('.',',')        
        boleto['conta_cedente'] = util.formatar_numero(dados['conta_cedente'],11,0)
        boleto['conta_devente_dv'] = util.formatar_numero(dados['conta_cedente_dv'],1,0)

        nnum = "%s%s" %(dados['inicio_nosso_numero'],util.formatar_numero(dados['nosso_numero'],8,0))
        dv_nosso_numero = BoletoCaixaEconomica.digito_verificador_nossonumero(nnum)
        nossonumero_dv ="%s%s" %(nnum,dv_nosso_numero)
        boleto['nossonumero'] = nnum
        boleto['dvnossonumero'] = dv_nosso_numero
        
        ag_contacedente = "%s%s" %(agencia, boleto['conta_cedente'])
        
        # 43 numeros para o calculo do digito verificador do codigo de barras
        dv = BoletoCaixaEconomica.digito_verificador_barra("%s%s%s%s%s%s" %(dados['codigobanco'],
                                                           dados['nummoeda'],
                                                           fator_vencimento,
                                                           valor,
                                                           nnum,           
                                                           ag_contacedente))                            
                    
        # Numero para o codigo de barras com 44 digitos
        linha = "%s%s%s%s%s%s%s" %(dados['codigobanco'],
                                   dados['nummoeda'],
                                   dv,
                                   fator_vencimento,
                                   valor,
                                   nnum,
                                   ag_contacedente)        
        nossonumero = "%s-%s" %(nossonumero_dv[0:10],nossonumero_dv[10])
        agencia_codigo = "%s / %s-%s" %(agencia,boleto['conta_cedente'],boleto['conta_devente_dv'])
                
        boleto['codigobarra'] = linha
        boleto['linha_digitavel'] = util.montar_linha_digitavel(linha)
        boleto['agencia_codigo'] = agencia_codigo
        boleto['nossonumeroformatado'] = nossonumero        
        return boleto
      
    @staticmethod
    def digito_verificador_nossonumero(numero):
        resto2 = util.modulo_11(numero,9,1)
        digito = 11 - resto2
        if digito == 10 or digito == 11:
            dv = 0
        else:
            dv = digito         
        return dv
        
    @staticmethod
    def digito_verificador_barra(numero):
        resto2 = util.modulo_11(numero,9,1)
        if resto2 == 0 or resto2 == 1 or resto2 == 10:
            dv = 1
        else:
            dv = 11 - resto2
        return dv    
    
class BoletoCaixaEconomicaSIGCB(Boleto):    
    
    @staticmethod
    def get_dados(dados):
        Boleto.get_dados(dados)
                
        dados['codigobanco'] = '104'
        dados['nummoeda'] = '9'
        
        boleto = dados
        fator_vencimento = util.fator_vencimento(dados["data_vencimento"])
        vtotal = "%.2f" %(float(dados['valor_boleto']+dados['taxa_boleto']))        
        valor = util.formatar_numero(str(vtotal),10,0,'valor')
        agencia = util.formatar_numero(dados["agencia"],4,0)   
        conta = util.formatar_numero(dados["conta"],5,0)
                
        boleto['codigobancodv'] = util.gerar_codigo_banco(dados['codigobanco'])
        
        boleto['valor'] = vtotal.replace('.',',')        
        boleto['conta_cedente'] = util.formatar_numero(dados['conta_cedente'],6,0)
        boleto['conta_cedente_dv'] = BoletoCaixaEconomicaSIGCB.digito_verificador_cedente(boleto['conta_cedente'])

        nnum = "%s%s%s%s%s%s%s" %(boleto['conta_cedente'],
                                  boleto['conta_cedente_dv'],
                                  util.formatar_numero(dados['nosso_numero1'],3,0),
                                  util.formatar_numero(dados['nosso_numero_const1'],1,0),
                                  util.formatar_numero(dados['nosso_numero2'],3,0),
                                  util.formatar_numero(dados['nosso_numero_const2'],1,0),
                                  util.formatar_numero(dados['nosso_numero3'],9,0)
                                  )
                                  
        dv_nosso_numero = BoletoCaixaEconomicaSIGCB.digito_verificador_nossonumero(nnum)
        nossonumero_dv ="%s%s" %(nnum,dv_nosso_numero)
        boleto['nossonumero'] = nnum
        boleto['dvnossonumero'] = dv_nosso_numero
        
        ag_contacedente = "%s%s" %(agencia, boleto['conta_cedente'])
        
        # 43 numeros para o calculo do digito verificador do codigo de barras
        dv = BoletoCaixaEconomicaSIGCB.digito_verificador_barra("%s%s%s%s%s" %(dados['codigobanco'],
                                                           dados['nummoeda'],
                                                           fator_vencimento,
                                                           valor,
                                                           nossonumero_dv))                            
             
        # Numero para o codigo de barras com 44 digitos
        linha = "%s%s%s%s%s%s" %(dados['codigobanco'],
                                   dados['nummoeda'],
                                   dv,
                                   fator_vencimento,
                                   valor,
                                   nossonumero_dv)
        
        nnum2 = "%s%s%s%s%s" %(util.formatar_numero(dados['nosso_numero_const1'],1,0),
                               util.formatar_numero(dados['nosso_numero_const2'],1,0),
                               util.formatar_numero(dados['nosso_numero1'],3,0),
                               util.formatar_numero(dados['nosso_numero2'],3,0),
                               util.formatar_numero(dados['nosso_numero3'],9,0))
                               
        nossonumero = "%s%s" %(nnum2,BoletoCaixaEconomicaSIGCB.digito_verificador_nossonumero(nnum2))
        agencia_codigo = "%s / %s-%s" %(agencia,boleto['conta_cedente'],boleto['conta_cedente_dv'])
                
        boleto['codigobarra'] = linha
        boleto['linha_digitavel'] = util.montar_linha_digitavel(linha)
        boleto['agencia_codigo'] = agencia_codigo
        boleto['nossonumeroformatado'] = nossonumero
  
        return boleto
      
    @staticmethod
    def digito_verificador_nossonumero(numero):
        resto2 = util.modulo_11(numero,9,1)
        digito = 11 - resto2
        if digito == 10 or digito == 11:
            dv = 0
        else:
            dv = digito         
        return dv
    
    @staticmethod
    def digito_verificador_cedente(numero):
        digito = util.modulo_11(numero,9,0)
        if digito == 10 or digito == 11:
            digito = 0
        dv = digito
        return dv    

    @staticmethod
    def digito_verificador_barra(numero):
        resto2 = util.modulo_11(numero,9,1)
        if resto2 == 0 or resto2 == 1 or resto2 == 10:
            dv = 1
        else:
            dv = 11 - resto2
        return dv