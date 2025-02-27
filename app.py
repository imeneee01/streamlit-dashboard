import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
        div.bloc-container { padding-top: 4rem; }
    </style>
    """,
    unsafe_allow_html=True
)

image = Image.open('adidas-logo.jpg')

col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.image(image, width=100)

title = "<center><h1>Adidas Interactive Sales Dashboard</h1></center>"

with col2:
    st.markdown(title, unsafe_allow_html=True)

data = pd.read_excel("ventes_smartphones.xlsx")

data.columns = data.columns.str.strip()
data = data[data['TotalSales'] != "------------"]

data['TotalSales'] = pd.to_numeric(data['TotalSales'], errors='coerce')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')


col3, col4, col5 = st.columns([0.1, 0.45, 0.45])
col_filters1, col_filters2 = st.columns([0.5, 0.5])

with col_filters1:
    retailer_selected = st.selectbox("", data["Retailer"].unique(), index = None, placeholder='Select a retailer')
    filter_retailer = st.button("Get Data")

with col_filters2:
    date_selected = st.selectbox("", data["InvoiceDate"].dt.strftime('%Y-%m').unique(), index = None, placeholder='Select a date')
    filter_date = st.button("Get Data ")

if filter_retailer:
    data = data[data["Retailer"] == retailer_selected]

if filter_date:
    data = data[(data["InvoiceDate"].dt.strftime('%Y-%m') == date_selected)]


with col3:
    st.markdown("Last updated:  \n" + datetime.datetime.today().strftime('%d %B %Y'))

with col4:
    fig1 = px.bar(data, x='Retailer', y='TotalSales', title="TotalSales par Retailer")
    st.plotly_chart(fig1, use_container_width=True)

df_time = data.groupby("InvoiceDate")["TotalSales"].sum().reset_index()

with col5:
    fig2 = px.line(df_time, x="InvoiceDate", y="TotalSales", markers=True, line_shape='linear', 
                   title="Total sales per date", labels={"TotalSales": "Total Sales (€)", "InvoiceDate": "Date"})
    st.plotly_chart(fig2)

state_sales = data.groupby("State").agg({"TotalSales": "sum", "UnitsSold": "sum"}).reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=state_sales['State'], y=state_sales['TotalSales'], name='Total Sales'))
fig3.add_trace(go.Scatter(x=state_sales['State'], y=state_sales['UnitsSold'], name='Units Sold', yaxis='y2', line=dict(color='orange')))

fig3.update_layout(
    title_text='Total Sales and Units Sold by State',
    yaxis=dict(title='Total Sales'),
    yaxis2=dict(title='Units Sold', overlaying='y', side='right')
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("### Total Sales par Région et Ville avec Treemap")

fig4 = px.treemap(data, path=['Region', 'City'],
                  values='TotalSales',
                  color='Region')

st.plotly_chart(fig4)
