import pandas as pd
import streamlit as st
import plotly.express as px
import base64
import datetime as dt
import locale

meses_pt = {
    "january": "janeiro",
    "february": "fevereiro",
    "march": "março",
    "april": "abril",
    "may": "maio",
    "june": "junho",
    "july": "julho",
    "august": "agosto",
    "september": "setembro",
    "october": "outubro",
    "november": "novembro",
    "december": "dezembro"
}

st.set_page_config(page_title="Dashboard RH", layout="wide")

url = "https://docs.google.com/spreadsheets/d/1OjO4JRwkaSy053tCm1Jls9ncc2uE8yREvQqqz0UBMGk/gviz/tq?tqx=out:csv"
df = pd.read_csv(url, on_bad_lines='skip')

df_adms = df.copy()
df_saidas = df.copy()

data_30dias = dt.datetime.today() - dt.timedelta(days=30)
data_90dias = dt.datetime.today() - dt.timedelta(days=90)
data_atual = dt.datetime.now()

mes_atual = data_atual.strftime("%B")
mes_atual_port = meses_pt[mes_atual]

mes_anterior = data_30dias.strftime('%B')
mes_anterior_port = meses_pt[mes_anterior]

anterior = mes_anterior + str(data_30dias.year)
atual = mes_atual + str(data_atual.year)

col_img, col_title = st.columns([1, 12])

with col_img:
    st.image('logo_base.png', width=80)
with col_title:
    st.title("Dashboard RH")

col1, col2, col3 = st.columns(3)

with col1:
    cargos = df["Função"].dropna().unique().tolist()
    cargos.insert(0, "BASE27")
    filtro_funcao = st.selectbox("Função:", cargos)

with col2:
    supervisao = df["SUPERVISÃO"].dropna().unique().tolist()
    supervisao.insert(0, "BASE27")
    filtro_sup = st.selectbox("Supervisão:", supervisao)
    
with col3:
    periodos = [mes_anterior_port.upper(), mes_atual_port.upper()]
  
    filtro_periodo = st.selectbox("Período:", periodos)


if filtro_funcao != "BASE27":
    df = df[df["Função"] == filtro_funcao]
    df_adms = df_adms[df_adms["Função"] == filtro_funcao]
    df_saidas = df_saidas[df_saidas["Função"] == filtro_funcao]  
if filtro_sup != "BASE27":
    df = df[df["SUPERVISÃO"] == filtro_sup]
    df_adms = df_adms[df_adms["SUPERVISÃO"] == filtro_sup]
    df_saidas = df_saidas[df_saidas["SUPERVISÃO"] == filtro_sup]  
if filtro_periodo == mes_anterior.upper():
    df_adms = df_adms[df_adms["PERIODO ADMISSAO"] == anterior]
    df_saidas = df_saidas[df_saidas["PERÍODO DEMISSÃO"] == anterior]
if filtro_periodo == mes_atual.upper():
    df_adms = df_adms[df_adms["PERIODO ADMISSAO"] == atual]
    df_saidas = df_saidas[df_saidas["PERÍODO DEMISSÃO"] == atual]
   


df_ativos= df[df["Demissão"].isna()]

ativos = df_ativos["Nome do Funcionário"].count()

df["Admissão"] = pd.to_datetime(df["Admissão"],  format="%d/%m/%Y", errors="coerce")
df["Demissão"] = pd.to_datetime(df["Demissão"], format="%d/%m/%Y", errors="coerce")


admissões = 0
saidas = 0

adm_geral = 0
saidas_geral = 0

adm_90d = 0
saidas_90d = 0

media_meses = 0

if ativos > 0:
    media_meses = df["TEMPO EMPRESA"].mean()

idade = 0

if ativos > 0:  
    idade = df_ativos["IDADE"].mean()

for i in range(df['Nome do Funcionário'].count()):
    if df["Admissão"].iloc[i] > data_30dias:
        admissões += 1
    if df["Admissão"].iloc[i] > data_90dias:
        adm_90d += 1
    if df["Demissão"].iloc[i] > data_30dias:
        saidas += 1
    if df["Demissão"].iloc[i] > data_90dias:
        saidas_90d += 1

admissões = 0
saidas = 0

for i in range(df_adms['Nome do Funcionário'].count()):
    admissões += 1
for i in range(df_saidas['Nome do Funcionário'].count()):
    saidas += 1

turnover_periodo = 0
turnover_90d = 0

if ativos > 0:
    turnover_periodo = (((admissões + saidas) / 2) / ativos) * 100  
    turnover_90d = (((adm_90d + saidas_90d) / 2) / ativos) * 100

if filtro_periodo == mes_anterior.upper():
    faltas = df["FALTAS ANTERIOR"].sum()
    atestados = df["ATESTADOS ANTERIOR"].sum()
if filtro_periodo == mes_atual.upper():
    faltas = df["FALTAS ATUAL"].sum()
    atestados = df["ATESTADOS ATUAL"].sum()

st.markdown("""
    <style>
        @keyframes float{
            0%, 100%{
                transform: translateY(0.1rem);
            }
            50%{
                transform: translateY(-0.2rem);
        }
            }
        label{
            font-weight: 600;
        }
        .subtitle{
            font-size: 14px;
            color: #8f8f8f;
            margin-top:5px;
            
        }
       .row1{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            grid-template-rows: repeat(1, 1fr);
            gap: 10px;
            margin-bottom: 40px;
        }
        .row2{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(1, 1fr);
            gap: 10px;
            margin-bottom: 30px
        }
        .row3{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(1, 1fr);
            gap: 10px;
        }
        .card{
            min-width: 175px;
            display: flex;
            flex-direction: column;
            border-radius: 10px;
            background: #262730;
            text-align: center;
            font-size: 20px;
            padding: 8px 10px;
            box-shadow: 0px 4px 12px rgba(71, 72, 89, 0.2);
            border: solid 1px #61626b;
        }
        .img{
            background-image: url("../group.png");
            width:30px;
        }
        .title{
            display: flex;
            margin: auto;
            gap: 15px;
        }
        .text{
            display: flex;
            margin: auto;
            gap: 10px;
            align-items: center;
        }
        .green{
            color:#009127;
        }
        .red{
            color:#b50000;
        }
        .blue{
            color: #1F37D8;
        }
        .orange{
            color: #E07500;   
        }
        .num{
            font-size:30px;
        }
       
        .subs{
            display:flex;
            max-width: 75%;
            flex-wrap: wrap;
            
            margin: auto;
        }
        
    </style>  
""", unsafe_allow_html=True)

icon_group = f'icons/group.png'
icon_green = f'icons/user_green.png'
icon_red = f'icons/user_red.png'
icon_clock = f'icons/clock.png'
icon_age = f'icons/age-group.png'


def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_group = get_base64_of_image(icon_group)
img_green = get_base64_of_image(icon_green)
img_red = get_base64_of_image(icon_red)
img_clock = get_base64_of_image(icon_clock)
img_age = get_base64_of_image(icon_age)

st.markdown(f"""
    <div class="row1">
        <div class="card">
            <div class="title">
                <img class="icon" src="data:image/jpeg;base64,{img_group}" width=35>
                <label>Ativos</label>
            </div>
            <label class="num">{ativos}</label>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
        <div class="card">
            <div class="title">
                <img class="icon" src="data:image/jpeg;base64,{img_green}" width=25>
                <label class="green">Adimissões</label>
            </div>
            <label class="num green">{admissões}</label>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao}) / ({filtro_periodo})</label></div>
        </div>
        <div class="card">
            <div class="title">
                <img class="icon" src="data:image/jpeg;base64,{img_red}" width=25>
                <label class="red">Saídas</label>
            </div>
           <label class="num red">{saidas}</label>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao}) / ({filtro_periodo})</label></div>
        </div>
        <div class="card">
            <div class="title">
                <img class="icon" src="data:image/jpeg;base64,{img_clock}" width=25>
                <label class="blue">Tempo médio</label>
            </div>
            <div class="text">
                <label class="num blue">{media_meses:.0f}</label>
                <label class="blue">Meses</label>
            </div>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
        <div class="card">
            <div class="title">
                <img class="icon" src="data:image/jpeg;base64,{img_age}" width=25>
                <label class="orange">Faixa Etária</label>
            </div>
            <div class="text">
                <label class="num orange">{idade:.0f}</label>
                <label class="orange">Anos</label>
            </div>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
    </div>
    <div class=row2>
        <div class="card">
            <div class="title">
                <label class="">% Turnover {filtro_periodo}</label>
            </div>
            <div class="text">
                <label class="num ">{turnover_periodo:.2f} %</label>
            </div>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
        <div class="card">
            <div class="title">
                <label class="">% Turnover 90 dias</label>
            </div>
            <div class="text">
                <label class="num ">{turnover_90d:.2f} %</label>
            </div>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
    </div>
    <div class="row3">
        <div class="card">
            <div class="title">
                <label class="">Faltas / {filtro_periodo}</label>
            </div>
            <div class="text">
                <label class="num ">{faltas:.0f}</label>
            </div>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
        <div class="card">
            <div class="title">
                <label class="">Atestados / {filtro_periodo}</label>
            </div>
            <div class="text">
                <label class="num ">{atestados:.0f}</label>
            </div>
            <div class="subs"><label class="subtitle">({filtro_sup}) / ({filtro_funcao})</label></div>
        </div>
    </div>
""", unsafe_allow_html=True)

