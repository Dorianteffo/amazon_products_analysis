import pandas as pd 
import streamlit as st 
import plotly.express as px
import numpy as np 

st.set_page_config(page_title= "Amazon_product",
                    page_icon="🏷",
                    layout="wide")


#data cleaning 
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

    df['discount_price'] = df['discount_price']*0.012
    df['actual_price'] = df['actual_price']*0.012

    df.insert(1, 'manufacturer', df['name'].apply(lambda x:x.split(' ')[0]))

    df['discount_percentage'] = np.where(df['actual_price']!=0,round((df['actual_price']-df['discount_price'])/df['actual_price'],2),0)

    top10_manufacturer= df.groupby('manufacturer',as_index=False).size().sort_values('size',ascending=False).iloc[:10]['manufacturer'].to_list() 
    df = df[df['manufacturer'].isin(top10_manufacturer)]

    return df

df = cleaning_data(df)


#title
st.title('📊Dashboard')
st.markdown('##')


#sidebar 
st.sidebar.write('# `FILTERS`')
st.sidebar.write('## Dashboard parameter')
manufactur = st.sidebar.selectbox("Select a manufacturer:", 
                                    options = df.groupby('manufacturer',as_index=False)['discount_price'].sum().sort_values('discount_price',ascending=False).manufacturer
                                    )

df_selection = df.query(
    " manufacturer == @manufactur"
)

#the subcategory parameter
st.sidebar.write('## Subcategory parameter')
subcategory_parameter = st.sidebar.selectbox('Select a category:',
                                             options = df_selection['main_category'].unique()
                                             )

total_revenue = round(df_selection['discount_price'].sum(),0)
avg_ratings = round(df_selection['ratings'].mean(),1)
star_rating = '⭐'* int(round(avg_ratings,0))
avg_discount = round(df_selection['discount_percentage'].mean()*100,2)

col1, col2, col3  = st.columns(3)
with col1 : 
    st.subheader('Total Sales:')
    st.subheader(f'US $ {total_revenue:,}')
with col2 : 
    st.subheader('Average Rating:')
    st.subheader(f'{avg_ratings} {star_rating} ')
with col3 : 
    st.subheader('Average Discount:')
    st.subheader(f'{avg_discount} %')


st.markdown('---')

# barchart category sales
sales_by_category = df_selection.groupby('main_category',as_index=False)['discount_price'].sum()
fig_category_sales = px.bar(
    sales_by_category, x='main_category',
      y='discount_price', 
      template='simple_white'
      )
fig_category_sales.update_layout(title = "Sales by category",
                                 xaxis_title = "Category",
                                 yaxis_title = "Sales (US $)")



# barchart subcategory sales 
sales_by_subcategory = df.groupby(['main_category','sub_category'],as_index=False)['discount_price'].sum()
fig_subcategory_sales = px.bar(     sales_by_subcategory[sales_by_subcategory['main_category']==subcategory_parameter], 
                                    x='discount_price',
                                    y='sub_category',
                                    orientation = "h", 
                                    template='simple_white'
                                )
fig_subcategory_sales.update_layout(title = "Top subcategory",
                                 xaxis_title = "Sales (US $)",
                                 yaxis_title = "Subcategory"
                                 )



left, right = st.columns(2)
left.plotly_chart(fig_category_sales)
right.plotly_chart(fig_subcategory_sales)


st.markdown('##')

#the scatterplot
fig_discount_reviews = px.scatter(df_selection, 
                                  x="discount_percentage", 
                                  y="no_of_ratings", 
                                  trendline="ols", 
                                   template="simple_white"
                                   )
fig_discount_reviews.update_yaxes(range=[0,8000])
fig_discount_reviews.update_layout(title = "Relationship between the number of reviews and discount percent",
                 yaxis_title = "Number of reviews",
                 xaxis_title = "Discount percentage")

st.plotly_chart(fig_discount_reviews)


