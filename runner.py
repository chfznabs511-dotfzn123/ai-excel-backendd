# runner.py # For executing Python code or data operations

import pandas as pd
import numpy as np
import io
import traceback

# Import all allowed libraries so they are in the execution scope
import scipy
import dask
import pyjanitor
import stringcase
import unidecode
import statsmodels
import pingouin
import sklearn
from fuzzywuzzy import fuzz
from textblob import TextBlob
import re
import matplotlib
import seaborn
import plotly
import missingno
import requests
from bs4 import BeautifulSoup
import cvxpy
import networkx
import openpyxl
import xlsxwriter
import xlrd
import xlwt
import pyxlsb
import openpyxl_styles
import dateutil
import pytz

def execute_code(code: str, sheet_data: dict) -> dict:
    """
    Executes a string of Python code in a controlled environment.

    Args:
        code: The Python script to execute.
        sheet_data: A dictionary where keys are sheet names and values are sheet
                    data in a JSON-serializable format (from pandas.DataFrame.to_dict).

    Returns:
        A dictionary containing the result of the execution.
        On success: {'status': 'success', 'data': modified_sheet_data}
        On error: {'status': 'error', 'message': error_message}
    """
    try:
        # 1. Prepare the execution environment
        # Create a dictionary of pandas DataFrames from the input JSON data
        dfs = {
            name: pd.DataFrame(data['cells'])
            for name, data in sheet_data.items()
            if 'cells' in data and data['cells']
        }

        # The 'globals' dictionary for the exec environment.
        # We only expose specific, safe libraries and the data.
        execution_globals = {
            'dfs': dfs,
            'pd': pd,
            'np': np,
            'scipy': scipy,
            'dask': dask,
            'pyjanitor': pyjanitor,
            'stringcase': stringcase,
            'unidecode': unidecode,
            'statsmodels': statsmodels,
            'pingouin': pingouin,
            'sklearn': sklearn,
            'fuzz': fuzz,
            'TextBlob': TextBlob,
            're': re,
            'matplotlib': matplotlib,
            'seaborn': seaborn,
            'plotly': plotly,
            'missingno': missingno,
            'requests': requests,
            'BeautifulSoup': BeautifulSoup,
            'cvxpy': cvxpy,
            'networkx': networkx,
            'openpyxl': openpyxl,
            'xlsxwriter': xlsxwriter,
            'xlrd': xlrd,
            'xlwt': xlwt,
            'pyxlsb': pyxlsb,
            'openpyxl_styles': openpyxl_styles,
            'dateutil': dateutil,
            'pytz': pytz,
        }

        # 2. Execute the code
        # The 'code' string is executed within the context of 'execution_globals'.
        # Any modifications the code makes to the 'dfs' dictionary will be
        # reflected in the 'execution_globals' dictionary.
        exec(code, execution_globals)

        # 3. Extract and format the results
        # Retrieve the modified DataFrames from the execution context.
        modified_dfs = execution_globals['dfs']

        # Convert the DataFrames back to a JSON-serializable format.
        # We replace NaN with None (which becomes null in JSON) for compatibility.
        output_data = {}
        for name, df in modified_dfs.items():
            # Convert all data to strings to ensure JSON compatibility and
            # match the frontend's data model. Replace NaN with empty strings.
            output_df = df.astype(str).replace('nan', '')
            output_data[name] = {
                'cells': output_df.values.tolist()
            }
            
        return {'status': 'success', 'data': output_data}

    except Exception as e:
        # If an error occurs during execution, capture it and return a
        # formatted error message.
        error_type = type(e).__name__
        error_message = str(e)
        traceback_str = traceback.format_exc()
        
        # Log the full traceback to the server console for debugging
        print("--- CODE EXECUTION ERROR ---")
        print(traceback_str)
        print("----------------------------")
        
        # Return a user-friendly error
        return {
            'status': 'error',
            'message': f"Execution failed with {error_type}: {error_message}"
        }
