# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 22:27:02 2023

@author: supak
"""

# In[] Get datasource 
import pandas as pd 

path = r'03 Python test and Dataset.xlsx'

pricing_df= pd.read_excel(path,sheet_name='pricing_project_dataset')  
platform_df= pd.read_excel(path,sheet_name='platform_number')  
fx_df= pd.read_excel(path,sheet_name='exchange_rate')  

# In[] Join table 
# rename col 
platform_df.rename(columns = {'region':'grass_region'}, inplace = True)
pricing_platform = pricing_df.merge( platform_df, on='grass_region', how='left')
# In[ Question 1 ] 

# Coverage = shopee_order / shopee platform order
pricing_platform['Coverage']=pricing_platform['shopee_order']/pricing_platform['platform order']
# q11=pricing_platform[['grass_region','Coverage']].groupby(['grass_region']).mean().reset_index()

q1=pd.DataFrame(columns=['grass_region','Coverage','Net_Competitive_ness','Total_items'])
for reg in pricing_platform['grass_region'].unique():
    temp_df=pricing_platform[pricing_platform['grass_region']==reg]
    loss_model = temp_df[temp_df['shopee_model_competitiveness_status']=='Shopee < CPT']['shopee_model_id'].nunique()
    win_model = temp_df[temp_df['shopee_model_competitiveness_status']=='Shopee > CPT']['shopee_model_id'].nunique()
    total_model =temp_df['shopee_model_id'].nunique()
    net_com=(win_model-loss_model)/total_model
    Coverage= temp_df['Coverage'].mean()
    total_item= temp_df['shopee_item_id'].nunique()
    print(reg,' : ',net_com,' from ',win_model,loss_model,total_model)
    df=pd.DataFrame([reg,Coverage,net_com,total_item]).T
    df.columns=['grass_region','Coverage','Net_Competitive_ness','Total_items']
    q1=q1.append(df)


# Net Competitive = (#Model win - # Model loss) / total model(shopee model_id)
