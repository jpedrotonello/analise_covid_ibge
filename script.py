import pandas as pd

respostas = pd.read_excel('C:/Users/tonel/Desktop/teste Einstein/dicionario.xlsx', 'Respostas')

df = pd.read_csv('C:/Users/tonel/Desktop/teste Einstein/PNAD_COVID_082020/PNAD_COVID_082020.csv')

def get_answers(df, codigo_variavel):
    mask = respostas['Cod variável'] == codigo_variavel
    tabela_respostas = respostas[mask][['categoria', 'descrição']]
    dict_resp = dict(zip(tabela_respostas['categoria'], tabela_respostas['descrição']))
    return [dict_resp.get(i) for i in df[codigo_variavel]]

dataset = pd.DataFrame({'idade': list(df['A002']),
    'renda': list(df['C01012']),
    'faixa_renda': get_answers(df, 'C01011'),
    'aposentadoria_pensao': list(df['D0013']),
    'aux_emergenciais': list(df['D0053']),
    
    'febre': get_answers(df, 'B0011'),
    'tosse': get_answers(df, 'B0012'),
    'dor_garganta': get_answers(df, 'B0013'),
    'dificuldade_respirar': get_answers(df, 'B0014'),
    'dor_cabeça': get_answers(df, 'B0015'),
    'dor_peito': get_answers(df, 'B0016'),
    'náusea': get_answers(df, 'B0017'),
    'nariz_entupido': get_answers(df, 'B0018'),
    'fadiga': get_answers(df, 'B0019'),
    'dor_olhos': get_answers(df, 'B00110'),
    'olfato_paladar': get_answers(df, 'B00111'),
    'dor_muscular': get_answers(df, 'B00112'),
    'diarreia': get_answers(df, 'B00113'),
    'foi_estabelecimento_saude': get_answers(df, 'B002'),
    'recuperacao_em_casa': get_answers(df, 'B0031'),
    'ligou_profissional': get_answers(df, 'B0032'),
    'remedio_conta_propria': get_answers(df, 'B0033'),
    'remedio_orientacao_medica': get_answers(df, 'B0034'),
    'recebeu_visita_sus': get_answers(df, 'B0035'),
    'recebeu_visita_particular': get_answers(df, 'B0036'),
    'outra_providencia': get_answers(df, 'B0037'),
    'testou_covid': get_answers(df, 'B008'),
    'resultado': get_answers(df, 'B009B'),
    'diabetes': get_answers(df, 'B0101'),
    'hipertensao': get_answers(df, 'B0102'),
    'doenca_respiratoria': get_answers(df, 'B0103'),
    'doenca_coracao': get_answers(df, 'B0104'),
    'depressao': get_answers(df, 'B0105'),
    'cancer': get_answers(df, 'B0106'),
    
    'domicilio': get_answers(df, 'F001'),
    'atividade_empresa': get_answers(df, 'C007D'),
    'tipo_trabalho': get_answers(df, 'C007C'), 
    'mais_de_um_trabalho': get_answers(df, 'C006'),
})
