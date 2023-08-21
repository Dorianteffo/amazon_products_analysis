import streamlit as st 

st.set_page_config(page_title= "Amazon_product",
                    page_icon="🏷",
                    layout="wide")

st.title('📕About')
st.markdown('#')

st.markdown('### 💡Goal')
st.markdown("""
            The main objective of this project was to advise someone who wanted to start selling products on Amazon's E-commerce platform.                                                                                                            
            To do this, we have created this web application, to display the top 10 manufacturers on Amazon and their statistics: average rating, discount percentage, number of reviews, and main categories of products sold."""
            )


st.markdown('##')
st.markdown('### 🔎Methodology')
st.markdown(f"""
            This app uses a dataset from [kaggle](https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset). And I used the streamlit library top build this entire webapp. 
            """)



st.markdown('##')
st.markdown('### 🔗Links')
col1,col2,col3 = st.columns(3)
with col1 : 
    st.markdown(f'### 🐈[Github](https://github.com/Dorianteffo/amazon_products_analysis/tree/master)')
    st.write('Source code for project')

with col2 : 
    st.markdown(f'### 💹[Kaggle](https://www.kaggle.com/code/doriancurtis/amazon-products-analysis)')
    st.write('Notebook (EDA) and dataset')

with col3 : 
    st.markdown(f'### 🗞[Medium](https://medium.com/@dorianteffo)')
    st.write('For tips in data analysis')
