import streamlit as st
import pandas as pd
import numpy as np

# PIVOT Table - Part 1
def pivot_table1(report_df2):
    # PIVOT Table


    # Create the pivot table without totals
    pivot_table1 = report_df2.pivot_table(
        index='Difference Target ICP to ERP STD', 
        values=[ 'Gross Inventory Quantity (Subledger)', 'Material Number',
        'ERP Standard Cost Valuation in Local Currency (Subledger)'],
        aggfunc={
            'Gross Inventory Quantity (Subledger)': 'sum',
            'Material Number': 'count',       
            'ERP Standard Cost Valuation in Local Currency (Subledger)': 'sum'
            
        }
    )
    # Ensure that both options always appear in the pivot table's index
    options = ['Correct', 'Incorrect']
    pivot_table1 = pivot_table1.reindex(options, fill_value=0)  

    # Round the values to 0 decimal places
    pivot_table1 = pivot_table1.round()

    # Calculate the total values
    total_row = pd.Series({
        'Gross Inventory Quantity (Subledger)': pivot_table1['Gross Inventory Quantity (Subledger)'].sum(),
        'Material Number': pivot_table1['Material Number'].sum(),
        'ERP Standard Cost Valuation in Local Currency (Subledger)': pivot_table1['ERP Standard Cost Valuation in Local Currency (Subledger)'].sum()
    }, name='Total')

    # Repeat a specific row (replace 'Specific Row' with the actual row label)
    correct_row = pivot_table1.loc['Correct']

    # Calculate the percentage row for the specific row
    percentage_correct_row = (correct_row / total_row * 100).round(2)
    percentage_correct_row.name = 'Correct(%)'



    # Create an empty row with empty values
    empty_row = pd.Series({
        'Gross Inventory Quantity (Subledger)': '',
        'Material Number': '',
        'ERP Standard Cost Valuation in Local Currency (Subledger)': ''
    }, name='')

    # Repeat a specific incorrect row (replace 'Incorrect Row' with the actual label of the incorrect row)
    
    try:
        incorrect_row = pivot_table1.loc['Incorrect']
    except KeyError:
        incorrect_row =  pd.Series({
        'Gross Inventory Quantity (Subledger)': 0,
        'Material Number': 0,
        'ERP Standard Cost Valuation in Local Currency (Subledger)': 0
    }, name='Incorrect')

    # Calculate the percentage row for the incorrect row
    percentage_incorrect_row = (incorrect_row / total_row * 100).round(2)
    percentage_incorrect_row.name = 'Incorrect(%)'

    # Create an empty row with empty values
    empty_row2 = pd.Series({
        'Gross Inventory Quantity (Subledger)': '',
        'Material Number': '',
        'ERP Standard Cost Valuation in Local Currency (Subledger)': ''
    }, name='')

    # Combine the data
    combined_df1 = pd.concat([
        pivot_table1, 
        total_row.to_frame().T, 
        empty_row.to_frame().T, 
        correct_row.to_frame().T, 
        percentage_correct_row.to_frame().T,
        empty_row.to_frame().T,
        incorrect_row.to_frame().T,
        percentage_incorrect_row.to_frame().T,
        empty_row.to_frame().T
    ])

    # Reset index
    combined_df1 = combined_df1.reset_index()

    # Rename columns to match the aggregation functions
    combined_df1.columns = ['Row_Labels', 'Sum ERP Standard Cost Valuation in Local Currency (Subledger)', 'Sum of Gross Inventory Quantity (Subledger)', 
                        'Count of Material Number', ]


    return combined_df1



    # PIVOT Table-Part2
   
def pivot_table2(report_df2):

    # Create the pivot table without totals
    pivot_table2 = report_df2.pivot_table(
        index='Erp Std To Billing Diff Comment', 
        values=[ 'Gross Inventory Quantity (Subledger)', 'Material Number',
        'ERP Standard Cost Valuation in Local Currency (Subledger)'],
        aggfunc={
            'Gross Inventory Quantity (Subledger)': 'sum',
            'Material Number': 'count',       
            'ERP Standard Cost Valuation in Local Currency (Subledger)': 'sum'            
        },
        fill_value=0
    )
    # Ensure that both options always appear in the pivot table's index
    options = ['Correct', 'Incorrect']
    pivot_table2 = pivot_table2.reindex(options, fill_value=0)  

    # Round the values to 0 decimal places
    pivot_table2 = pivot_table2.round()

    # Calculate the total values
    total_row2 = pd.Series({
        'Gross Inventory Quantity (Subledger)': pivot_table2['Gross Inventory Quantity (Subledger)'].sum(),
        'Material Number': pivot_table2['Material Number'].sum(),
        'ERP Standard Cost Valuation in Local Currency (Subledger)': pivot_table2['ERP Standard Cost Valuation in Local Currency (Subledger)'].sum()
    }, name='Total')

    # Repeat a specific row (replace 'Specific Row' with the actual row label)
    
    try:
        correct_row2 = pivot_table2.loc['Correct']
    except KeyError:
        correct_row2 =  pd.Series({
        'Gross Inventory Quantity (Subledger)': 0,
        'Material Number': 0,
        'ERP Standard Cost Valuation in Local Currency (Subledger)': 0
    }, name='')

    # Calculate the percentage row for the specific row
    percentage_correct_row2 = (correct_row2 / total_row2 * 100).round(2)
    percentage_correct_row2.name = 'Correct(%)'



    # Create an empty row with empty values
    empty_row2 = pd.Series({
        'Gross Inventory Quantity (Subledger)': '',
        'Material Number': '',
        'ERP Standard Cost Valuation in Local Currency (Subledger)': ''
    }, name='')

    # Repeat a specific incorrect row (replace 'Incorrect Row' with the actual label of the incorrect row)
    try:
        incorrect_row2 = pivot_table2.loc['Incorrect']
    except KeyError:
        incorrect_row2 =  pd.Series({
        'Gross Inventory Quantity (Subledger)': 0,
        'Material Number': 0,
        'ERP Standard Cost Valuation in Local Currency (Subledger)': 0
    }, name='Incorrect')


    # Calculate the percentage row for the incorrect row
    percentage_incorrect_row2 = (incorrect_row2 / total_row2 * 100).round(2)
    percentage_incorrect_row2.name = 'Incorrect(%)'

    # Create an empty row with empty values
    empty_row2 = pd.Series({
        'Gross Inventory Quantity (Subledger)': '',
        'Material Number': '',
        'ERP Standard Cost Valuation in Local Currency (Subledger)': ''
    }, name='')

    # Combine the data
    combined_df2 = pd.concat([
        pivot_table2, 
        total_row2.to_frame().T, 
        empty_row2.to_frame().T, 
        correct_row2.to_frame().T, 
        percentage_correct_row2.to_frame().T,
        empty_row2.to_frame().T,
        incorrect_row2.to_frame().T,
        percentage_incorrect_row2.to_frame().T,
        empty_row2.to_frame().T
    ])

    # Reset index
    combined_df2 = combined_df2.reset_index()

    # Rename columns to match the aggregation functions
    combined_df2.columns = ['Row_Labels', 'Sum ERP Standard Cost Valuation in Local Currency (Subledger)', 'Sum of Gross Inventory Quantity (Subledger)', 
                        'Count of Material Number', ]


    return combined_df2


     # PIVOT Table-Part3
   
def pivot_table3(report_df2):
    # Create the pivot table without totals
    pivot_table3 = report_df2.pivot_table(
        index='Target ICP to Billing Diff Comment', 
        values=[ 'Gross Inventory Quantity (Subledger)', 'Material Number',
        'ERP Standard Cost Valuation in Local Currency (Subledger)'],
        aggfunc={
            'Gross Inventory Quantity (Subledger)': 'sum',
            'Material Number': 'count',       
            'ERP Standard Cost Valuation in Local Currency (Subledger)': 'sum'
            
        }
    )
    # Ensure that both options always appear in the pivot table's index
    options = ['Correct', 'Incorrect']
    pivot_table3 = pivot_table3.reindex(options, fill_value=0)  

    # Round the values to 0 decimal places
    pivot_table3 = pivot_table3.round()

    # Calculate the total values
    total_row3 = pd.Series({
        'Gross Inventory Quantity (Subledger)': pivot_table3['Gross Inventory Quantity (Subledger)'].sum(),
        'Material Number': pivot_table3['Material Number'].sum(),
        'ERP Standard Cost Valuation in Local Currency (Subledger)': pivot_table3['ERP Standard Cost Valuation in Local Currency (Subledger)'].sum()
    }, name='Total')

    
    # Repeat a specific row (replace 'Specific Row' with the actual row label)
    try:
        correct_row3 = pivot_table3.loc['Correct']
    except KeyError:
        correct_row3 =  pd.Series({
        'Gross Inventory Quantity (Subledger)': 0,
        'Material Number': 0,
        'ERP Standard Cost Valuation in Local Currency (Subledger)': 0
    }, name='')

    # Calculate the percentage row for the specific row
    percentage_correct_row3 = (correct_row3 / total_row3 * 100).round(2)
    percentage_correct_row3.name = 'Correct(%)'



    # Create an empty row with empty values
    empty_row3 = pd.Series({
        'Gross Inventory Quantity (Subledger)': '',
        'Material Number': '',
        'ERP Standard Cost Valuation in Local Currency (Subledger)': ''
    }, name='')

    # Repeat a specific incorrect row (replace 'Incorrect Row' with the actual label of the incorrect row)
    try:
        incorrect_row3 = pivot_table3.loc['Incorrect']
    except KeyError:
        incorrect_row3 =  pd.Series({
        'Gross Inventory Quantity (Subledger)': 0,
        'Material Number': 0,
        'ERP Standard Cost Valuation in Local Currency (Subledger)': 0
    }, name='Incorrect')


    # Calculate the percentage row for the incorrect row
    percentage_incorrect_row3 = (incorrect_row3 / total_row3 * 100).round(2)
    percentage_incorrect_row3.name = 'Incorrect(%)'

    # Create an empty row with empty values
    empty_row3 = pd.Series({
        'Gross Inventory Quantity (Subledger)': '',
        'Material Number': '',
        'ERP Standard Cost Valuation in Local Currency (Subledger)': ''
    }, name='')

    # Combine the data
    combined_df3 = pd.concat([
        pivot_table3, 
        total_row3.to_frame().T, 
        empty_row3.to_frame().T, 
        correct_row3.to_frame().T, 
        percentage_correct_row3.to_frame().T,
        empty_row3.to_frame().T,
        incorrect_row3.to_frame().T,
        percentage_incorrect_row3.to_frame().T,
        empty_row3.to_frame().T
    ])

    # Reset index
    combined_df3 = combined_df3.reset_index()

    # Rename columns to match the aggregation functions
    combined_df3.columns = ['Row_Labels', 'Sum ERP Standard Cost Valuation in Local Currency (Subledger)', 'Sum of Gross Inventory Quantity (Subledger)', 
                        'Count of Material Number' ]

    return combined_df3


def pivot_table(report_df2):
    combined_df1 = pivot_table1(report_df2)
    combined_df2 = pivot_table2(report_df2)
    combined_df3 = pivot_table3(report_df2)
    header2 = pd.Series({
    'Row_Labels':'',
    'Sum ERP Standard Cost Valuation in Local Currency (Subledger)': 'ERP Std to JDE',
    'Count of Material Number': '',
    'Sum of Gross Inventory Quantity (Subledger)': ''
    }, name='')

    header3 = pd.Series({
        'Row_Labels':'',
        'Sum ERP Standard Cost Valuation in Local Currency (Subledger)': 'Target ICP to JDE',
        'Count of Material Number': '',
        'Sum of Gross Inventory Quantity (Subledger)': ''
    }, name='')

    # Concatenate the DataFrames vertically with spaces between them
    result = pd.concat([combined_df1, header2.to_frame().T, combined_df2, header3.to_frame().T, combined_df3], axis=0, ignore_index=True)
    result.set_index('Row_Labels', inplace=True)
    result.columns = pd.MultiIndex.from_tuples(zip(['Target ICP vs.ERP Standard', '', ''], result.columns))
    

    return result