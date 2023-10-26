import streamlit as st
import pandas as pd
from pivot import *
from backend import *
from custumized_functions import *
import xlsxwriter
import io

import numpy as np
from PIL import Image
import openpyxl
from openpyxl_image_loader import SheetImageLoader 

import plotly.express as px
import plotly.graph_objects as go





st.set_page_config(page_title="3 Way Match", layout="wide")


# st.markdown("""
# <style>
# .main {
#     background-color: #F5F5F5;
# }
# </style>
# """, 
# unsafe_allow_html=True
# )

header = st.container()
dataset = st.container()
reports = st.container()
summary = st.container()
download = st.container()

##-----SIDEBAR, DATA UPLOADING and VARIABLE SELECTION-----
with st.sidebar:
    image = Image.open('depuy_logo.jpg')

    st.image(image)

    st.title("Please enter your inputs here!")

    #Uploading Mtek raw data
    mitek_file = st.file_uploader("Upload the raw Mitek Data!") 
    if mitek_file is None:
        st.text ("")
    else:
        mitek = pd.read_excel(mitek_file, engine = 'openpyxl')

    st.markdown("""------------------------------------------------------------""")

    # Country and country_code
    country = st.selectbox(
    'For which country would you like to create the report?',
    ( ['Argentina', 'Australia', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'GMED', 'Hong Kong',
 'Hungary', 'India', 'Japan', 'South Korea', 'Malaysia', 'Mexico', 'New Zealand', 'Peru', 'Philippines', 'Puerto Rico', 'RDC',
 'Russia', 'Singapore', 'Slovenia', 'Taiwan', 'Thailand', 'Turkey', 'US', 'Uruguay']))
    country_code =  dict_of_countries[country]
    country_Target_MRC = target_MRC_list[country]
    
   
    st.markdown("""------------------------------------------------------------""")

    #Uploading parameters file
    parameters_file = st.file_uploader("Upload the Parameters File!") 
    if parameters_file is None:
        st.text ("")
    else:
        parameters = pd.read_excel(parameters_file, engine = 'openpyxl', header =1)

    st.markdown("""------------------------------------------------------------""")

    #Uploading Billing1 file
    Billing1_file = st.file_uploader("Upload the Billing File!") 
    if Billing1_file is None:
        st.text ("")
    else:
        Billing1 = pd.read_excel(Billing1_file, engine = 'openpyxl')
    
    st.markdown("""------------------------------------------------------------""")

     #Uploading Billing2 or UOM files
    Billing2_file = None
    Additional_file_for_UOM = None
    
    
    if country in countries_with_double_billing_files :
        st.text ("The second billing file:")
        Billing2_file = st.file_uploader("Upload the 2. Billing File!") 
        if Billing2_file is None:
            st.text ("")
        else:
            Billing2 = pd.read_excel(Billing2_file, engine = 'openpyxl')

    elif country in ['US']:
        st.text ("The second billing file:")
        Billing2_file = st.file_uploader("Upload the 2. Billing File: GMED 1225 ICP report!") 
        if Billing2_file is None:
            st.text ("")
        else:
            Billing2 = pd.read_excel(Billing2_file, engine = 'openpyxl')

        st.text ("Additional file for UOM:")
        Additional_file_for_UOM = st.file_uploader("Upload additional file for UOM!") 
        if Additional_file_for_UOM  is None:
            st.text ("")
        else:
            Additional_UOM_file  = pd.read_excel(Additional_file_for_UOM , engine = 'openpyxl')
    elif country in ['Puerto Rico']:
        st.text ("Additional file for UOM:")
        Additional_file_for_UOM = st.file_uploader("Upload additional file for UOM!") 
        if Additional_file_for_UOM  is None:
            st.text ("")
        else:
            Additional_UOM_file  = pd.read_excel(Additional_file_for_UOM , engine = 'openpyxl')

    

    st.markdown("""------------------------------------------------------------""")

    #Uploading rates file
    rates_file = st.file_uploader("Upload the rates Data!") 
    if rates_file is None:
        st.text ("")
    else:
        fx_rates = pd.read_excel(rates_file, engine = 'openpyxl')

    st.markdown("""------------------------------------------------------------""")

    #Fx rates of the specific country
    if country == 'RDC':
        country_fx_rate = country_fx_rate(fx_rates, 'Singapore')
    elif country == 'Puerto Rico':
        country_fx_rate = country_fx_rate(fx_rates, 'US')
    elif country == 'GMED'  or country == 'Slovenia':
        country_fx_rate = country_fx_rate(fx_rates, 'US')
    else:
        country_fx_rate = country_fx_rate(fx_rates, country)

    # getting screenshot from 2nd sheet of mitek file
    # pxl_doc = openpyxl.load_workbook('data/Mitek 06.23 Master Tableau data.xlsx')
    # sheet = pxl_doc['Tableau Screenshot']

    #     #calling the image_loader
    # image_loader = SheetImageLoader(sheet)

    #     #get the image (put the cell you need instead of 'A1')
    # screenshot = image_loader.get('A1')
    screenshot = st.file_uploader(label="Upload the screenshot", type=['jpg', 'png'])

    #Function to Read and Manupilate Images
    def load_image(img):
        im = Image.open(img)
        image = np.array(im)
        return image

    if screenshot is not None:
    #     # Perform your Manupilations (In my Case applying Filters)
        screenshot = load_image(screenshot)
        st.image(screenshot)
        st.write("Image Uploaded Successfully")
    else:
        st.write("Make sure your image is in JPG/PNG Format.")   

    st.markdown("""------------------------------------------------------------""")     

    



   


# CONTAINER #1 Haader and format of the PAGE
with header:
    col1, col2 = st.columns([2,1]) 
    col1.markdown(f'<h1 style="color:#B22222;font-size:48px;">{"3 Way Match Detective Check (Mitek) "}</h1>', unsafe_allow_html=True)
    col1.write("""
    3-Way Match Detective Check (Mitek) is a quarterly compliance control audit document that consist of comparing and ensuring that the ICP 
    (sourced from STRIVE and downloaded from the AGP Tool via Tableau), ERP standard cost (downloaded from Tableau), 
    and the billing price (sourced from various source system / selling MRC) are all the same value. """)
    image = Image.open('logo_JnJ.jpg')

    col2.image(image)


# CONTAINER #2 META DATA About the UPLOADED DATA
with dataset:    
    st.markdown("""------------------------------------------------------------""")
    st.header('3WM Data - Inputs')
    col1, col2, col3, col4 = st.columns([1,1,1,1]) 

    #Column # 1 Mitek metadata
    col1.subheader('Raw Data, Strive&ERP:')
    if mitek_file is None:
        col1.text ("No data is uploaded!")
    else:
        with col1:
            st.write ("Uploaded file: ", mitek_file.name )
            st.write ("Number of columns : ", mitek.shape[1] )
            st.write ("Number of rows : ", mitek.shape[0] )
     # column #2 Parameters metadata   
    col2.subheader('Parameters:')
    if parameters_file is None:
        col2.text ("No data is uploaded!")
    else:
        with col2:
            st.write ("Uploaded file: ", parameters_file.name)
            st.write ("Number of columns : ", parameters.shape[1])
            st.write ("Number of rows : ", parameters.shape[0])
    # column#3 Billing metadata
    col3.subheader('Billing Data:')
    if Billing1_file is None:
        col3.text ("No data is uploaded!")
    else:
        with col3:
            st.write ("Billing file: ", Billing1_file.name)
            #st.write ("Number of columns : ", Billing1.shape[1])
            #st.write ("Number of rows : ", Billing1.shape[0])

            if Billing2_file is None:
                st.text ("")
            else:
                st.write ("Second Billing file: ", Billing2_file.name)
            
            if Additional_file_for_UOM is None:
                st.text('')
            else:
                st.write ("Additional UOM file: ", Additional_file_for_UOM.name)


    # column#4 Billing metadata
    with col4:   
        col4.subheader('Country:') 
        st.write('You selected:', country)
        st.write('Fx rate of ', country, ' is:',country_fx_rate )
    
    
#  CONTAINER #3 REPORTING
#  
with reports:
    
    st.markdown("""------------------------------------------------------------""")
    
    st.write("Please check your inputs!")

    col1, col2= st.columns([1,1]) 
    

with col1:
    #st.button('Prepare ' + country + ' Report')

    if country in countries_with_double_billing_files:
        pre_df = before_comparison_countries_with_double_inputs(mitek, parameters, Billing1, country, country_code, Billing2)
        st.table(pre_df)

    elif country == 'US' :
        pre_df =before_comparison_for_US(mitek, parameters, Billing1, country, country_code, Additional_UOM_file,Billing2)

    elif country == 'Puerto Rico':
        pre_df = before_comparison_for_Puerto_Rico(mitek, parameters, Billing1, country, country_code, Additional_UOM_file)      
    
        
    elif country == 'GMED':
        pre_df = before_comparison_for_GMED(mitek, parameters, Billing1, country, country_code)
    else:    
        pre_df = before_comparison(mitek, parameters, Billing1, country, country_code, country_Target_MRC)
    

    
    df = comparison_in_USD(pre_df, country_fx_rate)
    if df.shape[0]==0:
        st.write("WARNING: "+ country + " doesn't have any result with these parameters.Please check your data.")
    else:
        pivot_table = pivot_table(df)  
        pivot_table1 = pivot_table1(df)
        pivot_table2 = pivot_table2(df)
        pivot_table3 = pivot_table3(df)
    #summary = summary(pivot_table)


    # Getting only the mismathes as a sub-dataframe.
    mismatches = df[(df['Difference Target ICP to ERP STD'] == 'Incorrect') | (df['Erp Std To Billing Diff Comment'] == 'Incorrect') | (df['Target ICP to Billing Diff Comment'] == 'Incorrect') ] 
    
    #Converting the type of some columns in mismatches table
    mismatches['Fiscal Year Month'] = mismatches['Fiscal Year Month'].astype(str)
    mismatches['Global Material Number'] = mismatches['Global Material Number'].astype(str)
    mismatches['Target MRC'] = mismatches['Target MRC'].astype(str)




## CONTAINER 4 Summary
with summary:
    
    st.markdown("""------------------------------------------------------------""")
    st.subheader("Pivot Tables:")
    
    #st.table(pivot_table)    
    pivot_column, pie_col = st.columns([1,1]) 

    with pivot_column:

        #Result Table-1, 'Target ICP vs.ERP Standard'
        fig1 = go.Figure(data = go.Table(
            header= dict(values = pivot_table1.columns, 
                        fill_color = '#EACCC7', 
                        align='center'), 
            cells= dict(values = [ list(pivot_table1['Row_Labels']), pivot_table1['Sum ERP Standard Cost Valuation in Local Currency (Subledger)'], pivot_table1['Sum of Gross Inventory Quantity (Subledger)'], pivot_table1['Count of Material Number']],
                        fill_color = '#E5ECF6',
                        align='center')))
        fig1.update_layout(width=800, height=300, margin = dict(l=5, r=15, b=10, t=30), title_text='Target ICP vs. Erp Std')
        st.write(fig1)

        #Result Table-2, 'Erp Std To JDE'
        fig2 = go.Figure(data = go.Table(
            header= dict(values = pivot_table2.columns, 
                        fill_color = '#FFDAB9', 
                        align='center'), 
            cells= dict(values = [ list(pivot_table2['Row_Labels']), pivot_table2['Sum ERP Standard Cost Valuation in Local Currency (Subledger)'], pivot_table2['Sum of Gross Inventory Quantity (Subledger)'], pivot_table2['Count of Material Number']],
                        fill_color = '#E5ECF6',
                        align='center')))
        fig2.update_layout(width=800, height=300, margin = dict(l=5, r=15, b=10, t=30), title_text='Erp Std vs. Billing ')
        st.write(fig2)

        #Result Table-3, 'Target ICP to JDE'
        fig3 = go.Figure(data = go.Table(
            header= dict(values = pivot_table3.columns, 
                        fill_color = '#D9D9D9', 
                        align='center'), 
            cells= dict(values = [ list(pivot_table3['Row_Labels']), pivot_table3['Sum ERP Standard Cost Valuation in Local Currency (Subledger)'], pivot_table3['Sum of Gross Inventory Quantity (Subledger)'], pivot_table3['Count of Material Number']],
                        fill_color = '#E5ECF6',
                        align='center')))
        fig3.update_layout(width=800, height=300, margin = dict(l=5, r=15, b=10, t=30), title_text='Target ICP vs. Billing ')
        st.write(fig3)

    with pie_col:
        # Pie Chart - 1
        df1 = pivot_table1.iloc[:2,[0,1]]
        
        fig_pie1 = px.pie(df1, values=df1['Sum ERP Standard Cost Valuation in Local Currency (Subledger)'], names = df1['Row_Labels'], title='Target ICP vs.ERP Standard', color=df1['Row_Labels'],
             color_discrete_map={'Correct':'#EACCC7',
                                 'Incorrect':'#C8102E'})
        fig_pie1.update_layout(width=400, height=300, margin = dict(l=15, r=5, b=10, t=30), title_text='Target ICP vs. Erp Std')
        st.plotly_chart(fig_pie1)

        # Pie Chart - 2
        df2 = pivot_table2.iloc[:2,[0,1]]
        
        fig_pie2 = px.pie(df2, values=df2['Sum ERP Standard Cost Valuation in Local Currency (Subledger)'], names = df2['Row_Labels'], title='Erp Std vs. Billing', color=df2['Row_Labels'],
             color_discrete_map={'Correct':'#FFDAB9',
                                 'Incorrect':'#C8102E'})
        fig_pie2.update_layout(width=400, height=300, margin = dict(l=15, r=5, b=10, t=30), title_text='Erp Std vs. Billing')
        st.plotly_chart(fig_pie2)

        # Pie Chart - 3
        df3 = pivot_table3.iloc[:2,[0,1]]
        
        fig_pie3 = px.pie(df3, values=df3['Sum ERP Standard Cost Valuation in Local Currency (Subledger)'], names = df3['Row_Labels'], title='Target ICP vs. Billing', color=df3['Row_Labels'],
             color_discrete_map={'Correct':'#D9D9D9',
                                 'Incorrect':'#C8102E'})
        fig_pie3.update_layout(width=400, height=300, margin = dict(l=15, r=5, b=10, t=30), title_text='Target ICP vs. Billing')
        st.plotly_chart(fig_pie3)


    st.markdown("""------------------------------------------------------------""")
    st.subheader("Mismatches:")
    st.dataframe(mismatches)

    
    st.markdown("""------------------------------------------------------------""")
    st.subheader("Summary:")
    # initialize data of summary.
    data = {'Total': [round(pivot_table.iloc[2][2]), round(pivot_table.iloc[2][1]), round(pivot_table.iloc[2][0])],
            'ICP Available and Correct': [round(pivot_table.iloc[26][2]), round(pivot_table.iloc[26][1]), round(pivot_table.iloc[26][0])],
           'ICP Not Available or Incorrect': [round(pivot_table.iloc[29][2]), round(pivot_table.iloc[29][1]), round(pivot_table.iloc[29][0])],
            '% Available and Correct': [str(round(100*pivot_table.iloc[26][2] / pivot_table.iloc[2][2], 2))+'%', str(round(100*pivot_table.iloc[26][1] / pivot_table.iloc[2][1], 2))+'%', str(round(100*pivot_table.iloc[26][0] / pivot_table.iloc[2][0], 2))+'%']
}
    # Creates pandas DataFrame.
    index1=['Data Lines','Total Inventory Units','Total SGD Inventory Valuation' ]
    summary = pd.DataFrame(data, index1)  
    #st.dataframe(summary)

   
    #st.table(summary)
    
    index=['Data Lines','Total Inventory Units','Total SGD Inventory Valuation' ]

    fig = go.Figure(data = go.Table(
        header= dict(values = summary.columns.insert(0, ' '), 
                     fill_color = '#FD8E72', 
                     align='left'), 
        cells= dict(values = [ summary.index.values.tolist(), summary['Total'], summary['ICP Available and Correct'], summary['ICP Not Available or Incorrect'], summary['% Available and Correct']],
                    fill_color = '#E5ECF6',
                    align='center')))
    fig.update_layout(width=800, height=300, margin = dict(l=5, r=5, b=10, t=30))
    st.write(fig)

    st.markdown("""------------------------------------------------------------""") 

    st.subheader("Download "+ country + " reports as Excel:")

    st.markdown("""------------------------------------------------------------""")   


with download:
    column1, column2= st.columns([1,1]) 
    
    with column1:        
        
        # buffer to use for excel writer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
            #summary.to_excel(writer, sheet_name='Summary', index=False)
            pivot_table.to_excel(writer, sheet_name='Pivots', index=True)
             
            df.to_excel(writer, sheet_name='Tableau Download', index=False)
            Billing1.to_excel(writer, sheet_name='Billing_ICPs', index=False)
            if Billing2_file != None:
                Billing2.to_excel(writer, sheet_name='Billing2', index=False)
            if Additional_file_for_UOM != None:
                Additional_UOM_file.to_excel(writer, sheet_name='Additional_UOM_file', index=False)
            fx_rates.to_excel(writer, sheet_name='FBP 2023 Rates', index=False)


            workbook  = writer.book
            worksheet = workbook.add_worksheet('Tableau-Screenshot')
            worksheet.insert_image('A1', 'Tableau_Screenshot.png')   
           

            writer.save()

            download2 = st.download_button(
                label="Download report as Excel",
                data=buffer,
                file_name= country +'.xlsx',
                mime='application/vnd.ms-excel'    
    )
            
    with column2:
        
        
        # buffer to use for excel writer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    
            mismatches.to_excel(writer, sheet_name='Mismatches', index=False)    
            workbook  = writer.book              

            writer.save()

            download2 = st.download_button(
                label="Download mismatches as Excel",
                data=buffer,
                file_name= country+'_Mismatches.xlsx',
                mime='application/vnd.ms-excel'    
    )
    
    st.markdown("""------------------------------------------------------------""")

