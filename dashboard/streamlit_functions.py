import streamlit as st
import pandas as pd
import numpy as np
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_variables import *

# Setup all data required for analysis
# General Setup
desafio_details_df = pd.read_csv(details_path)
desafio_priceav_df = pd.read_csv(price_path)
desafio_df = pd.merge(desafio_details_df, desafio_priceav_df, on="airbnb_listing_id")
desafio_df = desafio_df.drop_duplicates()
desafio_df = desafio_df.fillna(value=0)
desafio_df["booked_on"] = desafio_df["booked_on"].str.replace("blank", "")
desafio_df["booked_on"] = pd.to_datetime(desafio_df["booked_on"], format = "%Y-%m-%d %H:%M:%S")
desafio_df["date"] = pd.to_datetime(desafio_df["date"], format = "%Y-%m-%d")
# Qustion 1 setup
listing_count = desafio_details_df[["airbnb_listing_id", "suburb"]].groupby("suburb").count().sort_values(by="airbnb_listing_id").reset_index()
# Question 2 setup
revenue_by_booking = desafio_df[["airbnb_listing_id", "booked_on", "date", "suburb", "price_string"]].groupby(["airbnb_listing_id", "booked_on", "date", "suburb"]).sum().reset_index()
revenue_by_booking = revenue_by_booking[revenue_by_booking.booked_on != ""]
revenue_by_id = revenue_by_booking[["airbnb_listing_id", "suburb", "price_string"]].groupby(["airbnb_listing_id", "suburb"]).sum().reset_index()
average_revenue_by_neighborhood = revenue_by_id[["suburb", "price_string"]].groupby("suburb").mean().sort_values(by="price_string").reset_index()
average_revenue_by_neighborhood["price_string"] = average_revenue_by_neighborhood["price_string"].round(decimals=2)
# Question 3 setup
numerical_relations = desafio_df[["airbnb_listing_id", "suburb", "booked_on", "date", "number_of_bedrooms", "number_of_bathrooms", "number_of_reviews", "star_rating", "is_superhost", "price_string"]].groupby(["airbnb_listing_id", "suburb", "booked_on", "date", "number_of_bedrooms", "number_of_bathrooms", "number_of_reviews", "star_rating",]).sum().sort_values(by="price_string").reset_index()
numerical_relations = numerical_relations[numerical_relations.booked_on != ""]
revenue_and_feature = numerical_relations[["airbnb_listing_id", "suburb", "number_of_bedrooms", "number_of_bathrooms", "number_of_reviews", "star_rating", "is_superhost", "price_string"]].groupby(["airbnb_listing_id", "suburb", "number_of_bedrooms", "number_of_bathrooms", "number_of_reviews", "star_rating", "is_superhost"]).sum().reset_index()
le = preprocessing.LabelEncoder()
revenue_and_feature["suburb_encoded"] = le.fit_transform(revenue_and_feature["suburb"])
revenue_by_bedroom = revenue_and_feature[["number_of_bedrooms", "price_string"]].groupby("number_of_bedrooms").mean().reset_index()
revenue_by_bedroom["price_string"] = revenue_by_bedroom["price_string"].round(2)
listing_by_bedroom = revenue_and_feature[["number_of_bedrooms", "airbnb_listing_id"]].groupby("number_of_bedrooms").count().reset_index()
revenue_by_bathroom = revenue_and_feature[["number_of_bathrooms", "price_string"]].groupby("number_of_bathrooms").mean().reset_index()
revenue_by_bathroom["price_string"] = revenue_by_bathroom["price_string"].round(2)
listing_by_bathroom = revenue_and_feature[["airbnb_listing_id", "number_of_bathrooms"]].groupby("number_of_bathrooms").count().reset_index()

# Defining all graphs to be used on pages
def listing_count_bar():
    """Barplot for count listings by neighborhood"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=listing_count["suburb"], y=listing_count["airbnb_listing_id"], color="blue");
    graph.set(xlabel="Bairros", ylabel="Contagem de anúncios")
    plt.xticks(rotation=30)
    st.pyplot(figure)

def revenue_by_neighborhood():
    """Barplot for average revenue by neighborhood"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=average_revenue_by_neighborhood["suburb"], y=average_revenue_by_neighborhood["price_string"], color="blue");
    graph.set(xlabel="Bairros", ylabel="Faturamento médio")
    plt.xticks(rotation=30)
    st.pyplot(figure)

def revenue_corr_matrix():
    """Correlation between feature and total revenue"""
    figure = plt.figure(figsize=(2.5,2.5))
    corr = revenue_and_feature.corr()
    x = corr[["price_string"]]
    graph = sns.heatmap(x, annot=True, cmap="Blues");
    st.pyplot(figure)

def bedroom_revenue():
    """Average revenue by number of bedrooms"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=revenue_by_bedroom["number_of_bedrooms"], y=revenue_by_bedroom["price_string"], color="blue");
    graph.set(xlabel="Número de Quartos", ylabel="Faturamento médio")
    st.pyplot(figure)

def bedroom_count():
    """Listing count by number of bedrooms"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=listing_by_bedroom["number_of_bedrooms"], y=listing_by_bedroom["airbnb_listing_id"], color="blue");
    graph.set(xlabel="Número de quartos", ylabel="Contagem de listings")
    st.pyplot(figure)

def bathroom_revenue():
    """Average revenue by number of bathrooms"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=revenue_by_bathroom["number_of_bathrooms"], y=revenue_by_bathroom["price_string"], color="blue");
    graph.set(xlabel="Número de banheiros", ylabel="Faturamento médio")
    st.pyplot(figure)

def bathroom_count():
    """Listing count by number of bathrooms"""
    figure = plt.figure(figsize=(5, 2.5))
    graph = sns.barplot(x=listing_by_bathroom["number_of_bathrooms"], y=listing_by_bathroom["airbnb_listing_id"], color="blue");
    graph.set(xlabel="Número de quartos", ylabel="Contagem de listings")
    st.pyplot(figure)

def date_boxplot(weekend="no"):
    """Boxplot for date distribuition and outlier vizualization"""
    dates = desafio_df[["airbnb_listing_id", "booked_on", "date"]].groupby(["airbnb_listing_id", "booked_on"], sort=False)["date"].min().sort_values().reset_index()
    dates = dates[dates.booked_on != ""]
    dates["weekday_rent"] = dates["date"].dt.dayofweek        
    dates["difference"] = (dates.date - dates.booked_on)
    dates = dates[dates.difference != "0 days"]
    dates["difference"] = dates["difference"].values.astype(np.int64)
    if weekend == "no":
        figure1 = plt.figure(figsize=(2.5, 5))
        graph1 = sns.boxplot(y=dates["difference"], orient="h");
        graph1.set(xlabel="Diferença", ylabel="")
        graph1.set_yscale("log")
        st.pyplot(figure1)
    elif weekend == "yes":
        dates_weekend = dates[dates.weekday_rent > 4]
        figure2 = plt.figure(figsize=(2.5, 5))
        graph2 = sns.boxplot(y=dates_weekend["difference"], orient="h");
        graph2.set(xlabel="Diferença", ylabel="")
        graph2.set_yscale("log")
        st.pyplot(figure2)


# Defining calculations required
def superhost_revenue(superhost="yes"):
    """Superhost revenue calculations"""
    total_superhost_revenue = 0
    total_non_superhost_revenue = 0
    superhost_count = 0
    non_superhost_count = 0
    for i in range(len(revenue_and_feature["is_superhost"])):
        if revenue_and_feature.iloc[i, 6] != 0:
            total_superhost_revenue += revenue_and_feature.iloc[i, 7]
            superhost_count += 1
        else:
            total_non_superhost_revenue += revenue_and_feature.iloc[i, 7]
            non_superhost_count += 1

    average_superhost_revenue = total_superhost_revenue / superhost_count
    average_non_superhost_revenue = total_non_superhost_revenue / non_superhost_count
    if superhost == "yes":
        return f"""Faturamento médio: {average_superhost_revenue:.2f}
        
Faturamento total: {total_superhost_revenue:.2f}
        
Número total: {superhost_count}"""

    elif superhost == "no":
        return f"""Faturamento médio: {average_non_superhost_revenue:.2f}

Faturamento total: {total_non_superhost_revenue:.2f}

Número total: {non_superhost_count}"""


def average_time_diference(weekend="no"):
    """Average time diference between booking and check-in"""
    dates = desafio_df[["airbnb_listing_id", "booked_on", "date"]].groupby(["airbnb_listing_id", "booked_on"], sort=False)["date"].min().sort_values().reset_index()
    dates = dates[dates.booked_on != ""]
    dates["weekday_rent"] = dates["date"].dt.dayofweek        
    dates["difference"] = (dates.date - dates.booked_on)
    dates = dates[dates.difference != "0 days"]
    if weekend == "no":
        mean_dates = dates["difference"].mean()
        mode = dates["difference"].mode()
        median_dates = dates["difference"].median()
        return f"""Média: {mean_dates}
        
Moda: {mode[0]}
        
Mediana: {median_dates}"""
    elif weekend == "yes":
        dates_weekend = dates[dates.weekday_rent > 4]
        mean_weekend = dates_weekend["difference"].mean()
        mode = dates_weekend["difference"].mode()
        median_weekend = dates_weekend["difference"].median()
        return f"""Média: {mean_weekend}
        
Moda: {mode[0]}
        
Mediana: {median_weekend}"""

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

def set_questao_3_page():
    """Function to define 'Questão 3' page option."""
    st.title(title)
    st.markdown(q3_explanation_1)
    revenue_corr_matrix()
    st.markdown(q3_explanation_2)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Faturamento")
        st.table(revenue_by_bedroom)
        bedroom_revenue()
    with col2:
        st.markdown("Contagem")
        st.table(listing_by_bedroom)
        bedroom_count()
        
    st.markdown(q3_explanation_3)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("Faturamento")
        st.table(revenue_by_bathroom)
        bathroom_revenue()
    with col4:
        st.markdown("Contagem")
        st.table(listing_by_bathroom)
        bathroom_count()

    st.markdown(q3_explanation_4)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("*Superhost*")
        st.markdown(superhost_revenue())
    with col6:
        st.markdown("Não *Superhost*")
        st.markdown(superhost_revenue(superhost="no"))

    st.markdown(q3_explanation_5)

    

def set_questao_4_page():
    """Function to define 'Questão 4' page option."""
    st.title(title)
    st.markdown(q4_explanation)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Todas as datas:")
        st.markdown(average_time_diference())
        date_boxplot()
    with col2:
        st.markdown("Para finais de semana:")
        st.markdown(average_time_diference(weekend="yes"))
        date_boxplot(weekend="yes")
