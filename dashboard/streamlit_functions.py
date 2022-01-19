import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_variables import *

# Setup all data required for analysis
desafio_details_df = pd.read_csv(details_path)
desafio_priceav_df = pd.read_csv(price_path)
desafio_df = pd.merge(desafio_details_df, desafio_priceav_df, on="airbnb_listing_id")
desafio_df = desafio_df.drop_duplicates()
desafio_df = desafio_df.fillna(value=0)
desafio_df["booked_on"] = desafio_df["booked_on"].str.replace("blank", "")
desafio_df["booked_on"] = pd.to_datetime(desafio_df["booked_on"], format = "%Y-%m-%d %H:%M:%S")
desafio_df["date"] = pd.to_datetime(desafio_df["date"], format = "%Y-%m-%d")
listing_count = desafio_details_df[["airbnb_listing_id", "suburb"]].groupby("suburb").count().sort_values(by="airbnb_listing_id").reset_index()
revenue_by_booking = desafio_df[["airbnb_listing_id", "booked_on", "date", "suburb", "price_string"]].groupby(["airbnb_listing_id", "booked_on", "date", "suburb"]).sum().reset_index()
revenue_by_booking = revenue_by_booking[revenue_by_booking.booked_on != ""]
revenue_by_id = revenue_by_booking[["airbnb_listing_id", "suburb", "price_string"]].groupby(["airbnb_listing_id", "suburb"]).sum().reset_index()
average_revenue_by_neighborhood = revenue_by_id[["suburb", "price_string"]].groupby("suburb").mean().sort_values(by="price_string").reset_index()
average_revenue_by_neighborhood["price_string"] = average_revenue_by_neighborhood["price_string"].round(decimals=2)

# Defining all graphs to be used on pages
def listing_count_bar():
    """Barplot for count listings by neighborhood"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=listing_count["suburb"], y=listing_count["airbnb_listing_id"], color="black");
    graph.set(xlabel="Bairros", ylabel="Contagem de anúncios")
    plt.xticks(rotation=30)
    st.pyplot(figure)

def revenue_by_neighborhood():
    """Barplot for average revenue by neighborhood"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=average_revenue_by_neighborhood["suburb"], y=average_revenue_by_neighborhood["price_string"], color="black");
    graph.set(xlabel="Bairros", ylabel="Faturamento médio")
    plt.xticks(rotation=30)
    st.pyplot(figure)

# Defining calculations required
def average_time_diference(weekend="no"):
    dates = desafio_df[["airbnb_listing_id", "booked_on", "date"]].groupby(["airbnb_listing_id", "booked_on"], sort=False)["date"].min().sort_values().reset_index()
    dates = dates[dates.booked_on != ""]
    dates["weekday_rent"] = dates["date"].dt.dayofweek        
    dates["difference"] = (dates.date - dates.booked_on)
    dates = dates[dates.difference != "0 days"]
    if weekend == "no":
        return dates["difference"].mean()
    elif weekend == "yes":
        dates_weekend = dates[dates.weekday_rent > 4]
        return dates_weekend["difference"].mean()

def average_std_time_diference(weekend="no"):
    dates = desafio_df[["airbnb_listing_id", "booked_on", "date"]].groupby(["airbnb_listing_id", "booked_on"], sort=False)["date"].min().sort_values().reset_index()
    dates = dates[dates.booked_on != ""]
    dates["weekday_rent"] = dates["date"].dt.dayofweek        
    dates["difference"] = (dates.date - dates.booked_on)
    dates = dates[dates.difference != "0 days"]
    dates["int_diff"] = dates["difference"].values.astype(np.int64)
    dates["int_diff_var"] = dates["int_diff"].var()
    dates["int_diff_var"] = pd.to_timedelta(dates["int_diff_var"], unit="hours")
    if weekend == "no":
        return dates["int_diff_var"].sum()
    elif weekend == "yes":
        dates_weekend = dates[dates.weekday_rent > 4]
        return dates_weekend["int_diff_var"].sum()

# Defining pages and its organization
def set_initial_page():
    """Funtion to define 'Início' page option."""
    st.title(title)
    st.markdown(subtitle)
    st.markdown(intro)

def set_data_page():
    """Function to define 'Dados' page option."""
    st.title(title)
    st.markdown(data_intro)
    st.markdown(details_explanation)
    st.markdown("4.691 entradas | 8 colunas")
    st.write(desafio_details_df.drop("Unnamed: 0", axis=1).head(5))
    st.markdown(price_explanation)
    st.markdown("354.520 entradas | 5 colunas")
    st.write(desafio_priceav_df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1).head(5))
    st.markdown(desafio_df_explanation)
    st.markdown("289.919 entradas | 13 colunas")
    st.write(desafio_df.drop(["Unnamed: 0_x", "Unnamed: 0_y"], axis=1).head(5))
    st.markdown(data_final)

def set_questao_1_page():
    """Function to define 'Questão 1' page option."""
    st.title(title)
    st.markdown(q1_explanation)
    col1, col2 = st.columns(2)
    with col1:
        listing_count_bar()
    with col2:
        st.table(listing_count)

def set_questao_2_page():
    """Function to define 'Questão 2' page option."""
    st.title(title)
    st.markdown(q2_explanation)
    col1, col2 = st.columns(2)
    with col1:
        revenue_by_neighborhood()
    with col2:
        st.table(average_revenue_by_neighborhood)

def set_questao_4_page():
    st.title(title)
    st.markdown(q4_explanation_1)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Todas as datas:")
        st.write(average_time_diference())
        st.write(average_std_time_diference())
    with col2:
        st.markdown("Para finais de semana:")
        st.write(average_time_diference(weekend="yes"))
        st.write(average_std_time_diference(weekend="yes"))
