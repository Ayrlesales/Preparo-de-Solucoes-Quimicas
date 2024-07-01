import PySimpleGUI as sg

sg.theme('SystemDefault')

layout = [  
  [sg.Text('Qual a concentração? (digite apenas o número): '), 
   sg.InputText(size=(10,0), key='qualConcentracao')],
  [sg.Text('Qual o volume em mL? (digite apenas o número): '), sg.InputText(size=(10,0), key='qualVolume')], 
  [sg.Text('Qual a pureza do soluto? (digite apenas o número): '), 
   sg.InputText(size=(10,0), key='qualPurezaSoluto')],
  [sg.Text('O soluto está líquido ou sólido?'), sg.Radio('líquido', 'liquidoSolido', key='liquido'), sg.Radio('sólido', 'liquidoSolido', key='solido')],
  [sg.Text('Qual a unidade de medida?'), 
   sg.Radio('mol/L', 'unidadeMedida', key='mol'), 
   sg.Radio('N(normal - eq/L)', 'unidadeMedida', key='normal'), 
   sg.Radio('g/L(comum)', 'unidadeMedida', key='comum'), 
   sg.Radio('porcentagem', 'unidadeMedida', key='porcentagem')],
  [sg.Button('Ok'), sg.Button('Cancel')] 
]
window = sg.Window('Preparo de soluções', layout)
event, values = window.read()
qualConcentracao = float(values['qualConcentracao'])
qualPurezaSoluto = float(values['qualPurezaSoluto'])
acordoComPureza = 0

solido = values['solido']
liquido = values['liquido']
qualVolume = float(values['qualVolume'])



def calcularMol():
  global acordoComPureza
  layoutMol = [  
    [sg.Text('Qual a massa molar do soluto? (digite apenas o número): '), sg.InputText(size=(10,0), key='massaMolar')],
    [sg.Button('Ok'), sg.Button('Cancel')] 
  ]
  windowMol = sg.Window('Preparo de soluções mol/L', layoutMol)
  event, values = windowMol.read()
  massaMolar = float(values['massaMolar'])
  quantoMolEmGrama = qualConcentracao * massaMolar
  paraVolume = (qualVolume * quantoMolEmGrama) / 1000
  acordoComPureza = (paraVolume * 100) / qualPurezaSoluto

  if liquido == True:
    if event == 'Ok':
      windowMol.close()
      volumeSoluto, qualDensidade, windowDensidade = densidade()
      windowDensidade.close()
      resultado(f'pureza: {qualPurezaSoluto} \nMassa Molar do soluto: {massaMolar} \nDensidade: {qualDensidade} \nVocê deve diluir {round(volumeSoluto, 3)}mL do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao}mol/L')
  if solido == True:
    if event == 'Ok':
      windowMol.close()
      resultado(f'pureza: {qualPurezaSoluto} \nMassa Molar do soluto: {massaMolar} \nVocê deve diluir {round(acordoComPureza, 5)}g do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao}mol/L')




def calcularNormal():
  global acordoComPureza
  layoutNormal = [  
             [sg.Text('Qual a massa molar do soluto? (digite apenas o número): '), sg.InputText(size=(10,0), key='massaMolar')],
             [sg.Text('Qual o número de H+ ou HO- hionizavéis na molécula do soluto? (digite apenas o número): '), sg.InputText(size=(10,0), key='numeroIonizaveis')],
             [sg.Button('Ok'), sg.Button('Cancel')] 
  ]
  windowNormal = sg.Window('Preparo de soluções N(normal - eq/L)', layoutNormal)
  event, values = windowNormal.read()
  numeroIonizaveis = float(values['numeroIonizaveis'])
  massaMolar = float(values['massaMolar'])
  mlEmL = qualVolume / 1000
  quantoEmGrama = (qualConcentracao * massaMolar * mlEmL) / numeroIonizaveis
  acordoComPureza = (quantoEmGrama * 100) / qualPurezaSoluto

  if liquido == True:
    if event == 'Ok':
        windowNormal.close()
        volumeSoluto, qualDensidade, windowDensidade = densidade()
        windowDensidade.close()
        resultado(f'pureza: {qualPurezaSoluto} \nMassa Molar do soluto: {massaMolar} \nDensidade: {qualDensidade} \nH hionizáveis: {numeroIonizaveis} \nVocê deve diluir {round(volumeSoluto, 3)}mL do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao}N')
  if solido == True:
    if event == 'Ok':
        windowNormal.close()
        resultado(f'pureza: {qualPurezaSoluto} \nMassa Molar do soluto: {massaMolar} \nH hionizáveis: {numeroIonizaveis} \nVocê deve diluir {round(acordoComPureza, 5)}g do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao}N')




def calcularComum():
  global acordoComPureza
  quantoEmGrama = (qualConcentracao * qualVolume) / 1000
  acordoComPureza = (quantoEmGrama * 100) / qualPurezaSoluto

  if liquido == True:
        volumeSoluto, qualDensidade, windowDensidade = densidade()
        windowDensidade.close()
        resultado(f'pureza: {qualPurezaSoluto} \nDensidade: {qualDensidade} \nVocê deve diluir {round(volumeSoluto, 3)}mL do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao}g/L')
  if solido == True:
        resultado(f'pureza: {qualPurezaSoluto} \nVocê deve diluir {round(acordoComPureza, 5)}g do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao}g/L')




def calcularPorcentagem():
  global acordoComPureza
  layoutPorcentagem = [             
    [sg.Text('Qual a unidade de medida em porcentagem?'), sg.Radio('%m/m', 'porcento', key='%m/m'), sg.Radio('%v/v', 'porcento', key='%v/v'), sg.Radio('%m/v', 'porcento', key='%m/v')],
    [sg.Button('Ok'), sg.Button('Cancel')] 
  ]
  windowPorcentagem = sg.Window('Preparo de soluções %', layoutPorcentagem)
  event, values = windowPorcentagem.read()
  mm = values['%m/m']
  vv = values['%v/v']
  mv = values['%m/v']

  if mm == True:
    if event == 'Ok':
        windowPorcentagem.close()
        if liquido == True:
            quantoEmGrama = (qualConcentracao * qualVolume) / 100
            acordoComPureza = (quantoEmGrama * 100) / qualPurezaSoluto
            volumeSoluto, qualDensidade, windowDensidade = densidade()
            windowDensidade.close()
            resultado(f'pureza: {qualPurezaSoluto} \nDensidade: {qualDensidade} \nVocê deve diluir {round(volumeSoluto, 3)}mL do soluto em {qualVolume}mL de solvente para ter uma solução {qualConcentracao} %m/m')
        if solido == True:
            quantoEmGrama = (qualConcentracao * qualVolume) / 100
            acordoComPureza = (quantoEmGrama * 100) / qualPurezaSoluto
            resultado(f'pureza: {qualPurezaSoluto} \nVocê deve diluir {round(acordoComPureza, 5)}g do soluto em {qualVolume}mL de solvente para ter uma solução {qualConcentracao} %m/m')  
  
  if vv == True:
    if event == 'Ok':
        windowPorcentagem.close()
        if solido == True:
            volumeSoluto, qualDensidade, windowDensidade = densidade()
            windowDensidade.close()
            quantoEmVolume = (qualConcentracao * qualVolume) / 100
            acordoComPureza = (quantoEmVolume * 100) / qualPurezaSoluto
            gramaSoluto = acordoComPureza * qualDensidade
            resultado(f'pureza: {qualPurezaSoluto} \nDensidade: {qualDensidade} \nVocê deve diluir {round(gramaSoluto, 5)}g do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao} %v/v')
        if liquido == True:
            quantoEmVolume = (qualConcentracao * qualVolume) / 100
            acordoComPureza = (quantoEmVolume * 100) / qualPurezaSoluto
            resultado(f'pureza: {qualPurezaSoluto} \nVocê deve diluir {round(acordoComPureza, 3)}mL do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao} %v/v')
  
  if mv == True:
    if event == 'Ok':
        windowPorcentagem.close()
        if liquido == True:
            volumeSoluto, qualDensidade, windowDensidade = densidade()
            windowDensidade.close()
            quantoEmGrama = (qualConcentracao * qualVolume) / 100
            acordoComPureza = (quantoEmGrama * 100) / qualPurezaSoluto
            volumeSoluto = acordoComPureza / qualDensidade
            resultado(f'pureza: {qualPurezaSoluto} \nDensidade: {qualDensidade} \nVocê deve diluir {round(volumeSoluto, 3)}mL do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao} %m/v')
        if solido == True:
            layoutCristalizacao = [
                [sg.Text('O soluto tem água de cristalização?'), sg.Radio('Sim', 'cistalizacao', key='sim'), sg.Radio('Não', 'cistalizacao', key='nao')],
                [sg.Button('Ok'), sg.Button('Cancel')] 
            ]
            windowCristalizacao = sg.Window('Preparo de soluções %', layoutCristalizacao)
            event, values = windowCristalizacao.read()
            sim = values['sim']
            nao = values['nao']
            massaMolar = '-'
            moleculasAguaCristalizacao = '-'
            if sim == True:
                windowCristalizacao.close()
                layoutMassaMolar = [
                    [sg.Text('Qual a massa molar do soluto? (digite apenas o número): '), sg.InputText(size=(10,0), key='massaMolar')],
                    [sg.Text('Número de moléculas de água de cristalização? (digite apenas o número): '), sg.InputText(size=(10,0), key='moleculasAguaCristalizacao')],
                    [sg.Button('Ok'), sg.Button('Cancel')] 
                ]
                windowMassaMolar = sg.Window('Preparo de soluções %', layoutMassaMolar)
                event, values = windowMassaMolar.read()
                massaMolar = float(values['massaMolar'])
                moleculasAguaCristalizacao = float(values['moleculasAguaCristalizacao'])
                massaAgua = 18.015
                gramasAguas = massaAgua * moleculasAguaCristalizacao
                subtraiAguaComposto = massaMolar - gramasAguas
                quantoEmGrama = (qualConcentracao * qualVolume) / 100
                composto = (quantoEmGrama * massaMolar) / subtraiAguaComposto
                acordoComPureza = (composto * 100) / qualPurezaSoluto
            if nao == True:
                quantoEmGrama = (qualConcentracao * qualVolume) / 100
                acordoComPureza = (quantoEmGrama * 100) / qualPurezaSoluto
            resultado(f'pureza: {qualPurezaSoluto} \nMassa Molar: {massaMolar} \nMolecula de Cristalização: {moleculasAguaCristalizacao} \nVocê deve diluir {round(acordoComPureza, 5)}g do soluto em um balão de {qualVolume}mL para ter uma solução {qualConcentracao} %m/v')




def densidade():
  layoutDensidade = [
    [sg.Text('Qual a densidade? (digite apenas números): '), 
     sg.InputText(size=(10,0), key='qualDensidade')],
    [sg.Button('Ok'), sg.Button('Cancel')]
  ]
  windowDensidade = sg.Window('Densidade', layoutDensidade)
  event, values = windowDensidade.read()
  qualDensidade = float(values['qualDensidade'])
  volumeSoluto = acordoComPureza / qualDensidade

  if event == 'OK':
    windowDensidade.close()

  return volumeSoluto, qualDensidade, windowDensidade 


def resultado(texto):
  layoutResultado = [
    [sg.Multiline(size=(80, 5), key='output', autoscroll=True)],
    [sg.Button('Ok')]
  ]
  windowResultado = sg.Window('Resultado', layoutResultado, finalize=True)
  windowResultado['output'].update(value=texto)
  windowResultado.read()


mol = values['mol']
normal = values['normal']
comum = values['comum']
porcentagem = values['porcentagem']


if mol == True:
  if event == 'Ok': 
    window.close()
    calcularMol()
if normal == True:
  if event == 'Ok': 
    window.close()
    calcularNormal()
if comum == True:
  if event == 'Ok': 
    window.close()
    calcularComum()
if porcentagem == True:
  if event == 'Ok': 
    window.close()
    calcularPorcentagem()
