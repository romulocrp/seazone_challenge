import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_functions import *

st.set_page_config(page_title=title,
                page_icon="img/seazone_logo.png",
                layout="centered")
st.sidebar.image("/home/romulo/Documentos/projetos_ds/desafio_seazone/analise_streamlit/img/seazone_logo.png",
                  width=200)
st.sidebar.header("Opções")
#    st.sidebar.markdown("Selecione o que quer ver:")
menu = st.sidebar.radio("", ("Início", "Dados", "Questão 1", "Questão 2", "Questão 3", "Questão 4"))
st.sidebar.markdown("---")
st.sidebar.markdown("Rômulo Peixoto | Janeiro 2022 romulolespaul@gmail.com https://github.com/romulocrp")

if menu == "Início":
    set_initial_page()
elif menu == "Dados":
    set_data_page()
elif menu=="Questão 1":
    set_questao_1_page()
elif menu=="Questão 2":
    set_questao_2_page()
elif menu=="Questão 3":
    set_questao_3_page()    
elif menu == "Questão 4":
    set_questao_4_page()
