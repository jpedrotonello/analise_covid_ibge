import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve


# Importando bases de dados
respostas = pd.read_excel('C:/Users/tonel/Desktop/teste Einstein/dicionario.xlsx', 'Respostas')
df_052020 = pd.read_csv('PNAD_COVID_052020/PNAD_COVID_052020.csv')
df_062020 = pd.read_csv('PNAD_COVID_062020/PNAD_COVID_062020.csv')
df_072020 = pd.read_csv('PNAD_COVID_072020/PNAD_COVID_072020.csv')
df_082020 = pd.read_csv('PNAD_COVID_082020/PNAD_COVID_082020.csv')
df_092020 = pd.read_csv('PNAD_COVID_092020/PNAD_COVID_092020.csv')
df_102020 = pd.read_csv('PNAD_COVID_102020/PNAD_COVID_102020.csv')
df_112020 = pd.read_csv('PNAD_COVID_112020/PNAD_COVID_112020.csv')

def get_answers(df, codigo_variavel):
    mask = respostas['Cod variável'] == codigo_variavel
    tabela_respostas = respostas[mask][['categoria', 'descrição']]
    dict_resp = dict(zip(tabela_respostas['categoria'], tabela_respostas['descrição']))
    return [dict_resp.get(i) for i in df[codigo_variavel]]

get_dataset = lambda df: pd.DataFrame({
    'idade': list(df['A002']),
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
    
    'testou_covid': get_answers(df, 'B008'),
    'resultado': get_answers(df, 'B009B'),
    'diabetes': get_answers(df, 'B0101'),
    'hipertensao': get_answers(df, 'B0102'),
    'doenca_respiratoria': get_answers(df, 'B0103'),
    'doenca_coracao': get_answers(df, 'B0104'),
    'depressao': get_answers(df, 'B0105'),
    'cancer': get_answers(df, 'B0106'),
    
    'atividade_empresa': get_answers(df, 'C007D'),
    })

dataset = get_dataset(df_072020)
for df in [df_082020, df_092020, df_102020, df_112020]:
    dataset = pd.concat([dataset, get_dataset(df)], axis=0)

mask = (dataset['testou_covid'] == 'Sim')
df_testados = dataset[mask]


X = pd.DataFrame({'idade': list(df_testados['idade'])
, 'diabetes': [int(i) for i in list(df_testados['diabetes'] == 'Sim')]
, 'hipertensao': [int(i) for i in list(df_testados['hipertensao'] == 'Sim')]
, 'doenca_respiratoria': [int(i) for i in list(df_testados['doenca_respiratoria'] == 'Sim')]
, 'doenca_coracao': [int(i) for i in list(df_testados['doenca_coracao'] == 'Sim')]
, 'depressao': [int(i) for i in list(df_testados['depressao'] == 'Sim')]
, 'cancer': [int(i) for i in list(df_testados['cancer'] == 'Sim')]

, 'febre': [int(i) for i in list(df_testados['febre'] == 'Sim')]
, 'tosse': [int(i) for i in list(df_testados['tosse'] == 'Sim')]
, 'dor_garganta': [int(i) for i in list(df_testados['dor_garganta'] == 'Sim')]
, 'dificuldade_respirar': [int(i) for i in list(df_testados['dificuldade_respirar'] == 'Sim')]
, 'dor_cabeça': [int(i) for i in list(df_testados['dor_cabeça'] == 'Sim')]
, 'dor_peito': [int(i) for i in list(df_testados['dor_peito'] == 'Sim')]
, 'náusea': [int(i) for i in list(df_testados['náusea'] == 'Sim')]
, 'nariz_entupido': [int(i) for i in list(df_testados['nariz_entupido'] == 'Sim')]
, 'fadiga': [int(i) for i in list(df_testados['fadiga'] == 'Sim')]
, 'dor_olhos': [int(i) for i in list(df_testados['dor_olhos'] == 'Sim')]
, 'olfato_paladar': [int(i) for i in list(df_testados['olfato_paladar'] == 'Sim')]
, 'dor_muscular': [int(i) for i in list(df_testados['dor_muscular'] == 'Sim')]
, 'diarreia': [int(i) for i in list(df_testados['diarreia'] == 'Sim')]
})

y = df_testados['resultado'] == 'Positivo'

classifier = xgb.XGBClassifier(max_depth=6, n_trees = 500)
classifier.fit(X, y)

def plot_roc_curve(fper, tper):
    plt.plot(fper, tper, color='red', label='ROC')
    plt.plot([0, 1], [0, 1], color='green', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic Curve')
    plt.legend()
    plt.show()

prob = classifier.predict_proba(X)
prob = prob[:, 1]
fper, tper, thresholds = roc_curve(list(y), prob)
plot_roc_curve(fper, tper)

feature_importances = pd.DataFrame({'nome_variavel': X.columns
,'importancia': classifier.feature_importances_, })

feature_importances = feature_importances.sort_values(by='importancia', ascending=False)
sns.barplot(data = feature_importances,
            y='nome_variavel', x='importancia', color = 'blue')
