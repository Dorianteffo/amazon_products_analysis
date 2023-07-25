import pandas as pd 
import streamlit as st 
import plotly.express as px
import numpy as np 

st.set_page_config(page_title= "Amazon product",
                    page_icon="📊",
                    layout="wide")



#title
st.write('# 📊Amazon products analysis')
st.write('## ')

df = pd.read_csv('Amazon-Products.csv')
def cleaning_data(df) : 

    df.dropna(inplace=True)#drop row with Nan value
    df.drop('Unnamed: 0',axis=1, inplace=True)


    dirty_value = ['Get', 'FREE', '₹68.99', '₹65', '₹70','₹100','₹99', '₹2.99']
    df['ratings'] = df['ratings'].replace(dirty_value, '0')
    df['ratings'] = df['ratings'].astype('float')

    df['no_of_ratings'] = df['no_of_ratings'].replace(',','', regex = True)
    df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce').fillna('0')
    df['no_of_ratings'] = df['no_of_ratings'].astype('float')

 
    df.loc[df['discount_price'].str.contains('₹')==True, 'discount_price'] = df.loc[df['discount_price'].str.contains('₹')==True, 'discount_price'].apply(lambda x:x.strip('₹'))
    df.loc[df['discount_price'].str.contains(',')==True,'discount_price'] = df.loc[df['discount_price'].str.contains(',')==True,'discount_price'].apply(lambda x:x.replace(',',''))
    df['discount_price'] = df['discount_price'].astype('float')


    df.loc[df['actual_price'].str.contains('₹')==True, 'actual_price'] = df.loc[df['actual_price'].str.contains('₹')==True, 'actual_price'].apply(lambda x:x.strip('₹'))
    df.loc[df['actual_price'].str.contains(',')==True,'actual_price'] = df.loc[df['actual_price'].str.contains(',')==True,'actual_price'].apply(lambda x:x.replace(',',''))
    df['actual_price'] = df['actual_price'].astype('float')

    df.insert(1, 'manufacturer', df['name'].apply(lambda x:x.split(' ')[0]))

    df['discount_percentage'] = np.where(df['actual_price']!=0,round((df['actual_price']-df['discount_price'])/df['actual_price'],2),0)

    top10_manufacturer= df.groupby('manufacturer',as_index=False).size().sort_values('size',ascending=False).iloc[:10]['manufacturer'].to_list() 
    df = df[df['manufacturer'].isin(top10_manufacturer)]

    return df

df = cleaning_data(df)



#sidebar 
st.sidebar.write('## Filter')
manufactur = st.sidebar.multiselect("Select a manufacturer:", 
                                    options = df['manufacturer'].unique())

df_selection = df.query(
    " manufacturer == @manufactur"
)


st.dataframe(df_selection)