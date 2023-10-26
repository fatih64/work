import streamlit as st
import pandas as pd
import numpy as np

dict_of_countries = {'Argentina': 'AR', 'Australia': 'AU', 'Canada': 'CA', 'Chile': 'CL', 'China': 'CN', 'Colombia': 'CO', 'Costa Rica': 'CR', 'Ecuador': 'EC', 'GMED': 'GMED', 'Hong Kong': 'HK',
 'Hungary': 'HU', 'India': 'IN', 'Japan': 'JP', 'South Korea': 'KR', 'Malaysia': 'MY', 'Mexico': 'MX', 'New Zealand': 'NZ', 'Peru': 'PE', 'Philippines': 'PH', 'Puerto Rico': 'PR', 'RDC': 'SG',
 'Russia': 'RU', 'Singapore': 'SG', 'Slovenia': 'SI', 'Taiwan': 'TW', 'Thailand': 'TH', 'Turkey': 'TR', 'US': 'US', 'Uruguay': 'UY'}

parameter_list = ['Material Number', 'Item Type', 'PII Holding', 'Location Code','Mfg Sourcing Location', 'Country Code', 'Target MRC', 'Material Grp code','Source System Code', 'Implant/Instrument', 'ICP Sourcing Location']

billing_variables = {'Target_MRC_code': 4471, 'Target_MRC_Column_in_ERP': 'BPAN8', 'Material_Number_Column_in_ERP': 'TRIM(BPLITM)', 'Billing_price_ICP_Column': 'BPUPRC/10000'}

target_MRC_list = {'Argentina':[28901],'Australia': [2960],'Canada':[3350], 'Costa Rica':[2160], 'Chile':[2891], 'South Korea': [2450], 'Mexico':[4160], 'New Zealand': [2950], 'RDC': [4474], 
                   'Singapore':[4471], 'Thailand': [4941], 'China':[3435],'Slovenia':[450], 'Hungary':[480], 'Turkey': [470], 'Malaysia':[4131], 'Hong Kong': [3850],
                   'Philippines':[4360], 'Taiwan':[4890], 'Japan':[4090], 'Peru':[2892],'Uruguay':[2893],'Colombia':[2115], 'Russia': [4466], 'India': [8086, 38721], 'Ecuador':['NA'], 'Puerto Rico':[1757], 
                   'GMED':[75352] , 'US':[90126]}

sourcing_location_list = {'Argentina':['GMD001'],'Australia':['GMD001'], 'Canada':['GMD001'],'Chile':['NOT DEFINED'],'South Korea': ['GMD001'], 'Mexico':['GMD001'], 
                          'New Zealand': ['GMD001'], 'RDC': '', 'Singapore': '', 'India' : ['GMD001'], 'Tailand' : ['GMD001','RDC001'], 'Uruguay' : ['GMD001'] }



 # These are 

countries_with_double_billing_files = ['Thailand','China', 'Philippines','Taiwan','Malaysia']

def cleaning_billing_data_jde_812(df, Target_MRC_Code): 
    df = df[df['BPAN8'].isin (Target_MRC_Code)]   
    df['TRIM(BPLITM)'] = df['TRIM(BPLITM)'].astype(str).str.strip()
    df = df[['TRIM(BPLITM)', 'BPUPRC/10000', 'BPAN8' ]]    
    df = df.drop_duplicates()
    return df

def merge_inputs(df1, df2): 
    # to remove leading and trailing characters, cause problems while mapping
    df1['Material Number'] = df1['Material Number'].astype(str).str.strip() 
    
    #df1 = pd.merge(df1, df2, left_on= ['Material Number','Target MRC'], right_on=['TRIM(BPLITM)','BPAN8'], how='left')
    df1 = pd.merge(df1, df2, left_on= ['Material Number'], right_on=['TRIM(BPLITM)'], how='left')
    
    df1 = df1.drop(['TRIM(BPLITM)', 'BPAN8'], axis=1)
    df1 = df1.rename(columns={'BPUPRC/10000': 'Billing_ICP'})
    df1 = df1.drop_duplicates()
    return df1


def filter_dataframe(mitek_country, parameter_list, country_parameters):
    for parameter in parameter_list:      
        
        if (country_parameters[parameter].isna()).any():
            filter_values = ['Nothing to filter']  
        else:
            filter_values = str(country_parameters[parameter].tolist()[0]).split(',')
            filter_values = [element.strip() for element in filter_values]

        if 'Nothing to filter' in filter_values:
            mitek_country = mitek_country
        else:
            mitek_country = mitek_country[mitek_country[parameter].isin(filter_values)]
    
    return mitek_country


def before_comparison(Mitek, parameters_df, billing_df, country, country_code,Target_MRC_Code):

    Billing_price = cleaning_billing_data_jde_812(billing_df,Target_MRC_Code)  

    if country == 'RDC': # Since it is a part of SG and based on "PII Holding" column
        mitek_country = Mitek[Mitek['PII Holding'] == country]
        country_parameters = parameters_df[parameters_df['INV Loc'] == country]
        #sourcing_location_code = 'GMD001'

        filtered_data = filter_dataframe(mitek_country, parameter_list, country_parameters)
        report_df= merge_inputs(filtered_data, Billing_price)
        #report_df =  filtered_data[filtered_data['ICP Sourcing Location'] == sourcing_location_code]
    else:    

        mitek_country = Mitek[Mitek['Country Code'] == country_code]
        country_parameters = parameters_df[parameters_df['INV Loc'] == country]
        #sourcing_location_code = 'GMD001'

        filtered_data = filter_dataframe(mitek_country, parameter_list, country_parameters)
        report_df= merge_inputs(filtered_data, Billing_price)
        #report_df =  filtered_data[filtered_data['ICP Sourcing Location'] == sourcing_location_code]

    return report_df


def comparisons(report_df):
   
    #Comparison-1:creation of "Target ICP vs. ERP"

    report_df['ERP Standard Cost in Eaches'] = report_df['ERP Standard Cost in Eaches'].astype(float)
    report_df['Target ICP'] = report_df['Target ICP'].astype(float)

    report_df['Target ICP vs. ERP'] = (report_df['ERP Standard Cost in Eaches'] - report_df['Target ICP']).round(2)
    

    # Creation of "Difference Target ICP to ERP STD"
    report_df['Difference Target ICP to ERP STD'] = np.where(report_df['Target ICP vs. ERP'] == 0, 'Correct',
                            np.where(report_df['Target ICP vs. ERP'] == 0.01, 'Correct',
                                    np.where(report_df['Target ICP vs. ERP'] == -0.01, 'Correct', 'Incorrect')))

    #Comparison-2 :Creation of "Erp Std To Billing Diff", NEED TO standardize the naming of the columns
    report_df['ERP Standard Cost in Eaches'] = report_df['ERP Standard Cost in Eaches'].astype(float)
    report_df['Billing_ICP'] = report_df['Billing_ICP'].astype(float)

    report_df['Erp Std To Billing Diff'] = (report_df['Billing_ICP'] - report_df['ERP Standard Cost in Eaches']).round(2)
    


    # Creation of "Erp Std To Billing Diff Comment"
    report_df['Erp Std To Billing Diff Comment'] = np.where(report_df['Erp Std To Billing Diff'] == 0, 'Correct',
                            np.where(report_df['Erp Std To Billing Diff'] == 0.01, 'Correct',
                                    np.where(report_df['Erp Std To Billing Diff'] == -0.01, 'Correct', 'Incorrect')))
                                    #Comparison-3 : Creation of "Target ICP to Billing Diff"
    report_df['Target ICP to Billing Diff'] = (report_df['Target ICP'] - report_df['Billing_ICP']).round(2)


    # Creation of "Target ICP to Billing Diff Comment"
    report_df['Target ICP to Billing Diff Comment'] = np.where(report_df['Target ICP to Billing Diff'] == 0, 'Correct',
                            np.where(report_df['Target ICP to Billing Diff'] == 0.01, 'Correct',
                                    np.where(report_df['Target ICP to Billing Diff'] == -0.01, 'Correct', 'Incorrect')))
    
    return report_df

def comparison_in_USD(report_df, country_fx):
   
    #Comparison-1:creation of "Target ICP vs. ERP"

    report_df['ERP Standard Cost in Eaches'] = report_df['ERP Standard Cost in Eaches'].astype(float)
    report_df['Target ICP'] = report_df['Target ICP'].astype(float)

    report_df['Target ICP vs. ERP'] = (report_df['ERP Standard Cost in Eaches'] - report_df['Target ICP']).round(2)
    report_df['Target ICP vs. ERP Standard (Converted To USD @ FBP Rates)'] = (report_df['Target ICP vs. ERP'] * country_fx).round(2)

    # Creation of "Difference Target ICP to ERP STD"
    report_df['Difference Target ICP to ERP STD'] = np.where(report_df['Target ICP vs. ERP Standard (Converted To USD @ FBP Rates)'] == 0, 'Correct',
                            np.where(report_df['Target ICP vs. ERP Standard (Converted To USD @ FBP Rates)'] == 0.01, 'Correct',
                                    np.where(report_df['Target ICP vs. ERP Standard (Converted To USD @ FBP Rates)'] == -0.01, 'Correct', 'Incorrect')))

    #Comparison-2 :Creation of "Erp Std To Billing Diff", NEED TO standardize the naming of the columns
    report_df['ERP Standard Cost in Eaches'] = report_df['ERP Standard Cost in Eaches'].astype(float)
    report_df['Billing_ICP'] = report_df['Billing_ICP'].astype(float)

    report_df['Erp Std To Billing Diff'] = (report_df['Billing_ICP'] - report_df['ERP Standard Cost in Eaches']).round(2)
    report_df['Billing ICP (Converted To USD @ FBP Rates)'] = (report_df['Erp Std To Billing Diff']*country_fx).round(2)


    # Creation of "Erp Std To Billing Diff Comment"
    report_df['Erp Std To Billing Diff Comment'] = np.where(report_df['Billing ICP (Converted To USD @ FBP Rates)'] == 0, 'Correct',
                            np.where(report_df['Billing ICP (Converted To USD @ FBP Rates)'] == 0.01, 'Correct',
                                    np.where(report_df['Billing ICP (Converted To USD @ FBP Rates)'] == -0.01, 'Correct', 'Incorrect')))
                                    
    #Comparison-3 : Creation of "Target ICP to Billing Diff"
    report_df['Target ICP to Billing Diff'] = (report_df['Target ICP'] - report_df['Billing_ICP']).round(2)
    report_df['Target ICP to Billing Diff in USD'] = (report_df['Target ICP to Billing Diff']*country_fx).round(2)


    # Creation of "Target ICP to Billing Diff Comment"
    report_df['Target ICP to Billing Diff Comment'] = np.where(report_df['Target ICP to Billing Diff in USD'] == 0, 'Correct',
                            np.where(report_df['Target ICP to Billing Diff in USD'] == 0.01, 'Correct',
                                    np.where(report_df['Target ICP to Billing Diff in USD'] == -0.01, 'Correct', 'Incorrect')))
    
    return report_df

def summary(pivot_table):

    # initialize data of summary.
    data = {'Total': [pivot_table.iloc[2][2], pivot_table.iloc[2][1], pivot_table.iloc[2][0]],
            'ICP Available and Correct': [pivot_table.iloc[25][2], pivot_table.iloc[25][1], pivot_table.iloc[25][0]],
            'ICP Not Available or Incorrect': [pivot_table.iloc[28][2], pivot_table.iloc[28][1], pivot_table.iloc[28][0]],
            '% Available and Correct': [str(100*pivot_table.iloc[25][2] / pivot_table.iloc[2][2])+'%', str(100*pivot_table.iloc[25][1] / pivot_table.iloc[2][1])+'%', str(100*pivot_table.iloc[25][0] / pivot_table.iloc[2][0])+'%']}
    # Creates pandas DataFrame.
    summary = pd.DataFrame(data, index=['Data Lines',
                                'Total Inventory Units',
                                'Total SGD Inventory Valuation'
                                ])  
    return summary


def country_fx_rate(fx, country):
        
    return float(fx[fx.iloc[:, 1]==country.upper()].iloc[:,3])








