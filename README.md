# Seazone Challenge
![repo cover](img/seazone_logo.png?raw=true)
## Introduction
On 01/11/2022 Seazone realesed their proposed challenge to participants on their recruitment program. The challenge goal is to evaluate candidates skills on data analysis given the following two data sets:
- [desafio_details.csv](/datasets/desafio_details.csv)
- [desafio_pricesav.csv](/datasets/desafio_pricesav.csv)

Also there are some questions required to answer, given by the recruiters:
- Order neighborhood by growing number of listings.
- Order neighborhood by growing revenue.
- Is there any relationship between an ad charateristics and its revenue? If so, which? Explain.
- What is the average advance notice for bookings? Is this number greater for weekends?

All these questions should be answered and delivered as a GitHub repository link and a PDF with the required analysis.

## Datasets
All datasets provided by recruiters for the challenge, column information is inside the folder.

## Notebook
In this file is all analysis made for the challenge, it is a more didatic way to explain all code used to answer question and provide deep analysis on the matter.

## Dashboard
The dashboard directory is a more resumed way to view all answers, lacks text explanation which is provided by other delivereables, but is faster to get access to graphs and numbers delivered by the analysis. All results from the notebook are here.

In order to use the dashboard download the latest version of Streamlit on the python environment is required by the following line:
`pip install streamlit`

To launch the app just using the command line:
`streamlit run path/to/file/streamlit_main.py`
