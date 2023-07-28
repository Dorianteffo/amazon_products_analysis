import pandas as pd 
import numpy as np 

def cleaning_data(df) : 
    """ 
    To clean the ratings, no_of_ratings, discount_price, actual_price columns, 
    create the manufacturer and discount_percentage columns,
    convert the actual_price and discount_price currencies to Us dollars, 
    
    paramters : the uncleaned dataframe 
    return : a clean dataframe with only the top 10 manufacturers in terms of popularity

    You can also find this data cleaning process on the notebook (.ipynb), with the EDA
    
    """

    df.dropna(inplace=True)#drop row with Nan value
    df.drop('Unnamed: 0',axis=1, inplace=True)#drop the first column

    #clean the ratings column
    dirty_value = ['Get', 'FREE', '₹68.99', '₹65', '₹70','₹100','₹99', '₹2.99']
    df['ratings'] = df['ratings'].replace(dirty_value, '0')
    df['ratings'] = df['ratings'].astype('float')

    #clean the no_of_ratings column
    df['no_of_ratings'] = df['no_of_ratings'].replace(',','', regex = True)
    df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce').fillna('0')
    df['no_of_ratings'] = df['no_of_ratings'].astype('float')

    #clean the discount_price column
    df.loc[df['discount_price'].str.contains('₹')==True, 'discount_price'] = df.loc[df['discount_price'].str.contains('₹')==True, 'discount_price'].apply(lambda x:x.strip('₹'))
    df.loc[df['discount_price'].str.contains(',')==True,'discount_price'] = df.loc[df['discount_price'].str.contains(',')==True,'discount_price'].apply(lambda x:x.replace(',',''))
    df['discount_price'] = df['discount_price'].astype('float')

    #clean the actual_price column
    df.loc[df['actual_price'].str.contains('₹')==True, 'actual_price'] = df.loc[df['actual_price'].str.contains('₹')==True, 'actual_price'].apply(lambda x:x.strip('₹'))
    df.loc[df['actual_price'].str.contains(',')==True,'actual_price'] = df.loc[df['actual_price'].str.contains(',')==True,'actual_price'].apply(lambda x:x.replace(',',''))
    df['actual_price'] = df['actual_price'].astype('float')

    #convert the actual_price and discount_price column to Us dollars 
    #1₹ = 0.012$
    df['discount_price'] = df['discount_price']*0.012
    df['actual_price'] = df['actual_price']*0.012

    #create the manufacturer column
    df.insert(1, 'manufacturer', df['name'].apply(lambda x:x.split(' ')[0]))

    #create the discount_percentage column
    df['discount_percentage'] = np.where(df['actual_price']!=0,round((df['actual_price']-df['discount_price'])/df['actual_price'],2),0)

    #take only the TOP10 manufacturers
    top10_manufacturer= df['manufacturer'].value_counts()[:10].index.tolist()
    df = df[df['manufacturer'].isin(top10_manufacturer)]

    return df