
import pandas as pd
import numpy as np
from backend import *

# List of countries with double billing files
countries_with_double_billing_files = ['Thailand','China',  'Philippines','Taiwan', 'Malaysia' ]


# Function to clean and merge inputs for countries with double inputs
def clean_merge_inputs_of_countries_with_double_inputs(df1, Billing1, Billing2, country ): 
    # to remove leading and trailing characters, cause problems while mapping
    df1['Material Number'] = df1['Material Number'].astype(str).str.strip()
    
    Billing1.columns = Billing1.columns.str.replace(r'\s+', '')# In case column names have leading spaces
    Billing2.columns = Billing2.columns.str.rstrip(' ') # In case column names have right leading spaces
    Billing2.columns = Billing2.columns.str.lstrip(' ')# In case column names have left leading spaces
    
    Billing1['TRIM(BPLITM)'] =Billing1['TRIM(BPLITM)'].astype(str).str.strip() # To remove leading and trailing spaces
    Billing1 = Billing1[['TRIM(BPLITM)', 'BPUPRC/10000', 'BPAN8']] # Getting only the required columns of JDE 8.12

    #Customized conditions for each country
    if country == 'Thailand':
        # Filter data based on conditions
        df1 = df1[(df1['Target MRC'] == 4940)]
        Billing1 = Billing1[(Billing1['BPAN8'] == 4941)] # Tailand's MRC is 4941 in JDE
        
        Billing2 = Billing2[(Billing2['Bill-To Party'] == 4940)] # SAP MARS Bill-to Party is 4940 for Thailand
        Billing2['Material'] = Billing2['Material'].astype(str).str.strip() # remove leading and trailing characters, cause problems while mapping
        Billing2 = Billing2 [['Material', 'PCR/EA']] # Getting only the required columns of SAP Mars
        
        df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['TRIM(BPLITM)'], how='left') # Merging with JDE on related columns
        df1 = pd.merge(df1, Billing2, left_on= ['Material Number'], right_on=['Material'], how='left') # Merging with SAp Mars on related columns

        #if the value of 'ICP Sourcing Location' is equal to 'RDC001', it selects the 'Billing_ICP' value from the SAP_Mars else JDE 8.12 
        df1['Billing_ICP']= np.where(df1['ICP Sourcing Location']=='RDC001', df1['PCR/EA'], df1['BPUPRC/10000'] )
        
        df1 = df1.drop(['TRIM(BPLITM)', 'BPAN8', 'BPUPRC/10000', 'PCR/EA', 'Material' ], axis=1) # Dropping the not required columns
        df1 = df1.drop_duplicates()
        
    elif country == 'China':
        df1 = df1[(df1['Target MRC'] == 3435)]
        Billing1 = Billing1[(Billing1['BPAN8'] == 34352)] # Billing1 for China is JDE 8.12( BPAN=34352)

        
        Billing2 = Billing2[(Billing2['Customer'] == 90116)] # Billing2 for China is P01 where Customer is 90116 
        Billing2['Material'] = Billing2['Material'].astype(str).str.strip() # remove leading and trailing characters, cause problems while mapping
        
        Billing2 = Billing2 [['Material', 'Amount']] # Getting only the required columns of P01
        
        df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['TRIM(BPLITM)'], how='left') # Merging with JDE on related columns
        df1 = pd.merge(df1, Billing2, left_on= ['Material Number'], right_on=['Material'], how='left') # Merging with P01 on related columns
        
        #if the value of 'ICP Sourcing Location' is equal to 'DPY010', it selects the 'Billing_ICP' value from the P01 else gets it from JDE 8.12 
        df1['Billing_ICP'] = np.where(df1['ICP Sourcing Location']=='DPY010', df1['Amount'], df1['BPUPRC/10000'] )
        
        df1 = df1.drop(['TRIM(BPLITM)', 'BPAN8', 'BPUPRC/10000', 'Amount', 'Material' ], axis=1)# Dropping the not required columns
        df1 = df1.drop_duplicates()

    elif country == 'Philippines':
        df1 = df1[(df1['Target MRC'] == 4360)] 
        Billing1 = Billing1[(Billing1['BPAN8'] == 4360)] # Philippines' MRC is 4941 in JDE

        
        Billing2 = Billing2[(Billing2['Bill-To Party'] == 4360)] # SAP MARS Bill-to Party is 4360 for Philipinnes
        Billing2['Material'] = Billing2['Material'].astype(str).str.strip() # remove leading and trailing characters, cause problems while mapping        
        Billing2 = Billing2 [['Material', 'PCR/EA']]# Getting only the required columns of SAP Mars
        
        df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['TRIM(BPLITM)'], how='left') # Merging with JDE on related columns
        df1 = pd.merge(df1, Billing2, left_on= ['Material Number'], right_on=['Material',], how='left') # Merging with Sap Mars on related columns
        
        #if the value of 'ICP Sourcing Location' is equal to 'RDC001', it selects the 'Billing_ICP' value from  SAP_Mars else gets it from JDE 8.12 
        df1['Billing_ICP'] = np.where(df1['ICP Sourcing Location']=='RDC001', df1['PCR/EA'], df1['BPUPRC/10000'] )
        
        df1 = df1.drop(['TRIM(BPLITM)', 'BPAN8', 'BPUPRC/10000', 'PCR/EA', 'Material' ], axis=1) # Dropping the not required columns
        df1 = df1.drop_duplicates()


    elif country == 'Malaysia':
        df1 = df1[(df1['Target MRC'] == 4131)]
        Billing1 = Billing1[(Billing1['BPAN8'] == 4132)] # Malaysia's MRC is 4941 in JDE

        
        Billing2 = Billing2[(Billing2['Bill-To Party'] == 4131)] # SAP MARS Bill-to Party is 4940 for Malaysia
        
        Billing2 = Billing2 [['Material', 'PCR/EA']]
        
        df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['TRIM(BPLITM)'], how='left')
        df1 = pd.merge(df1, Billing2, left_on= ['Material Number'], right_on=['Material',], how='left')
        
        df1['Billing_ICP'] = np.where(df1['ICP Sourcing Location']=='RDC001', df1['PCR/EA'], df1['BPUPRC/10000'] )
        
        df1 = df1.drop(['TRIM(BPLITM)', 'BPAN8', 'BPUPRC/10000', 'PCR/EA', 'Material' ], axis=1)

    elif country == 'Taiwan':
        df1 = df1[(df1['Target MRC'] == 4890)]
        Billing1 = Billing1[(Billing1['BPAN8'] == 4890)]

        
        Billing2 = Billing2[(Billing2['Bill-To Party'] == 4890)] # SAP MARS Bill-to Party is 4940 for Taiwan
        
        Billing2 = Billing2 [['Material', 'PCR/EA']]
        
        df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['TRIM(BPLITM)'], how='left')
        df1 = pd.merge(df1, Billing2, left_on= ['Material Number'], right_on=['Material',], how='left')
        
        df1['Billing_ICP'] = np.where(df1['ICP Sourcing Location']=='RDC001', df1['PCR/EA'], df1['BPUPRC/10000'] )
        
        df1 = df1.drop(['TRIM(BPLITM)', 'BPAN8', 'BPUPRC/10000', 'PCR/EA', 'Material' ], axis=1)

    else:
        print("This country's Target MRC code is not defined in the code")
    
    
    return df1

def clean_merge_inputs_for_US(df1, Billing1, Billing2, UOM_Input): 
    
    df1['Material Number'] = df1['Material Number'].astype(str).str.strip() # to remove leading and trailing characters, cause problems while mapping
    Billing1['Material'] = Billing1['Material'].astype(str).str.strip()# to remove leading and trailing characters, cause problems while mapping
    Billing1 = Billing1.rename(columns={'Material': 'Material1'}) # Renaming not to confuse, Material from P01
    Billing2['Material'] = Billing2['Material'].astype(str).str.strip() # to remove leading and trailing characters, cause problems while mapping
    UOM_Input['Material'] = UOM_Input['Material'].astype(str).str.strip() # to remove leading and trailing characters, cause problems while mapping
    UOM_Input = UOM_Input.rename(columns={'Material': 'Material_UoM'}) # Renaming not to confuse, Material in UoM Input

    #US P01 DPY010
    Billing1 = Billing1[(Billing1['Customer'] == 90126)] # P01 Customer is 90126 for US
    Billing1.columns = Billing1.columns.str.replace(r'\s+', '')# In case column names have spaces

    Billing1 = pd.merge(Billing1,UOM_Input, left_on= ['Material1'], right_on=['Material_UoM'], how='left') # Merging P01 and UoM mapping file
    Billing1['Numerator'].fillna(1, inplace=True) # Replace NaN (no match) with 1 in the 'T' column
        
    # Calculating 'Price per eaches', dividing Amount to numerator
    Billing1['Numerator'] = Billing1['Numerator'].astype(float)
    Billing1['Amount'] = Billing1['Amount'].astype(float)

    Billing1['Price per eaches'] = (Billing1['Amount'] / Billing1['Numerator']).round(2)
    Billing1 = Billing1 [['Material1', 'Price per eaches']]

    # GMED  1225 ICP Report
    Billing2 = Billing2 [['Material', 'Amount']]
    Billing2 = Billing2.rename(columns={'Amount': 'Amount_Billing2'}) # Renaming not to confuse, Amount from GMED 1225 ICP reportt
    Billing2 = Billing2.drop_duplicates()
    
    df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['Material1'], how='left') # Merging with P01 on related columns
    df1 = pd.merge(df1, Billing2, left_on= ['Material Number'], right_on=['Material'], how='left') # Merging with GMED1225 ICP report on related columns
    
   
    #if the value of 'Material' is not null in GMED 1225 ICP report, the 'Billing_ICP' value comes from there, else gets it from P01 
    df1['Billing_ICP'] = np.where(df1['Material'].notnull(), df1['Amount_Billing2'], df1['Price per eaches'])

    
    df1 = df1.drop(['Material', 'Amount_Billing2', 'Price per eaches', 'Material1' ], axis=1)# Dropping the not required columns
    df1 = df1.drop_duplicates()    

    return df1

def clean_merge_inputs_for_Puerto_Rico(df1, Billing1,  UOM_Input): 

    df1['Material Number'] = df1['Material Number'].astype(str).str.strip()
    Billing1['Material Number'] = Billing1['Material Number'].astype(str).str.strip()
    Billing1['UOM'] = Billing1['UOM'].astype(str).str.strip()
    UOM_Input['Alternative Unit of Measure'] = UOM_Input['Alternative Unit of Measure'].astype(str).str.strip()    
    UOM_Input['Material'] = UOM_Input['Material'].astype(str).str.strip()

    

    #Creating a new column to vlookup with UOM conversion file
    Billing1['Material+UOM'] =  Billing1['UOM'].astype(str) + Billing1['Material Number'].astype(str)
    #Creating a new column to vlookup with Billing 
    UOM_Input['Material+UOM2'] =  UOM_Input['Alternative Unit of Measure'].astype(str) + UOM_Input['Material']

    # merge USROTC and UoM conversion table
    Billing1 = pd.merge(Billing1,UOM_Input, left_on= ['Material+UOM'], right_on=['Material+UOM2'], how='left')

    #create a new column which is amount per UOM
    Billing1['Numerator'] = Billing1['Numerator'].astype(float)
    Billing1['List Price'] = Billing1['List Price'].astype(float)
        
    Billing1['Price per eaches'] = (Billing1['List Price'] / Billing1['Numerator']).round(2)
    Billing1 = Billing1 [['Material Number', 'Price per eaches']]
    
    df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['Material Number'], how='left')
    
    
    #df1 = df1.drop(['Material_'], axis=1)
    df1 = df1.rename(columns={'Price per eaches': 'Billing_ICP'})


    return df1







def clean_merge_inputs_for_GMED(df1, Billing1): 
    # to remove leading and trailing characters, cause problems while mapping
    df1['Material Number'] = df1['Material Number'].astype(str).str.strip()
    Billing1['Material'] = Billing1['Material'].astype(str).str.strip()
    Billing1.columns = Billing1.columns.str.replace(r'\s+', '')# In case column names have spaces
    
               
    Billing1 = Billing1[(Billing1['Customer'] == 75352)] # P01 Customer is 75352 for GMED --> Confirm this, 75352 seems belongs to China
    
    Billing1 = Billing1 [['Material', 'Amount']]
    
    df1 = pd.merge(df1, Billing1, left_on= ['Material Number'], right_on=['Material'], how='left')

    #There is a UoM logic like this for GMED
    df1['Amount'] = df1['Amount'].astype(float)
    df1 = df1[df1['Target ICP'] != 'Total']
    df1['Target ICP'] = df1['Target ICP'].astype(float)
    try:
        df1['Amount'] = df1['Amount'] / (df1['Amount']/df1['Target ICP'])

    except ZeroDivisionError:
        df1['Amount']
    
    
    df1 = df1.drop(['Material'], axis=1)
    df1 = df1.rename(columns={'Amount': 'Billing_ICP'})
    
   
    return df1



def before_comparison_countries_with_double_inputs(Mitek, parameters_df, billing_df, country, country_code, Billing2_df):

    Mitek = clean_merge_inputs_of_countries_with_double_inputs(Mitek, billing_df, Billing2_df, country )

    mitek_country = Mitek[(Mitek['Country Code'] == country_code) ]
    country_parameters = parameters_df[parameters_df['INV Loc'] == country]
    

    filtered_data = filter_dataframe(mitek_country, parameter_list, country_parameters)
    report_df =  filtered_data

    return report_df

def before_comparison_for_US(Mitek, parameters_df, billing_df, country, country_code, UOM_Input, Billing2_df):

    Mitek = clean_merge_inputs_for_US(Mitek, billing_df,  Billing2_df, UOM_Input)

    mitek_country = Mitek[(Mitek['PII Holding'] == country_code) ]
    country_parameters = parameters_df[parameters_df['INV Loc'] == country]
    

    filtered_data = filter_dataframe(mitek_country, parameter_list, country_parameters)
    report_df =  filtered_data

    return report_df


def before_comparison_for_Puerto_Rico(Mitek, parameters_df, billing_df, country, country_code, UOM_Input):

    Mitek = clean_merge_inputs_for_Puerto_Rico(Mitek, billing_df, UOM_Input )

    mitek_country = Mitek[(Mitek['Country Code'] == country_code) ]
    country_parameters = parameters_df[parameters_df['INV Loc'] == country]
    

    filtered_data = filter_dataframe(mitek_country, parameter_list, country_parameters)
    report_df =  filtered_data

    return report_df





def before_comparison_for_GMED(Mitek, parameters_df, billing_df, country, country_code):

    Mitek = clean_merge_inputs_for_GMED(Mitek, billing_df)

    mitek_country = Mitek[(Mitek['PII Holding'] == country_code) ]
    country_parameters = parameters_df[parameters_df['INV Loc'] == country]
    

    filtered_data = filter_dataframe(mitek_country, parameter_list, country_parameters)
    report_df =  filtered_data

    return report_df
