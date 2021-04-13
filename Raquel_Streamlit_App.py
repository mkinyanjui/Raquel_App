import streamlit as st
import pandas as pd
import numpy as np
import base64
st.beta_set_page_config(layout='wide')


def main():

    st.title('Automated Excel Process')

    """
    Created by Mark Kinyanjui

    """

    """
    ### Step 1: Import Data
    """

    df = st.file_uploader(
        'Import dataset - make sure the $ is removed from both tabs')

    if df is not None:
        df_enrollment = pd.read_excel(df, sheet_name='Enrollments')
        df_payroll = pd.read_excel(df, sheet_name='Payroll')
        """
        ### Step 2: Merging the data & results
        """
        df_enrollment = df_enrollment.groupby(
            ['NAME', 'COMPANY CODE', 'HOME DEPARTMENT', 'POSITION ID', 'DEDUCTION CODE', 'EMPLOYEE STATUS']).sum('ENROLLMENT AMOUNT').reset_index()

        df_payroll = df_payroll.groupby(['NAME', 'COMPANY CODE', 'HOME DEPARTMENT',
                                         'POSITION ID', 'DEDUCTION CODE']).sum('DEDUCTION AMOUNT').reset_index()

        st.text(
            'Changing Payroll Deduction Code AC1 to match Enrollment Deduction Code ACC')
        # PAYROLL CHANGE ACC TO AC1
        df_payroll = df_payroll.replace(to_replace='AC1', value='ACC')
        df_enrollment = df_enrollment.replace(to_replace='AC1', value='ACC')

        # Merge the data
        clean = pd.merge(df_enrollment, df_payroll, how='left', left_on=[
                         'POSITION ID', 'DEDUCTION CODE'], right_on=['POSITION ID', 'DEDUCTION CODE'])
        clean = clean[['NAME_x', 'COMPANY CODE_x', 'HOME DEPARTMENT_x', 'POSITION ID',
                       'DEDUCTION CODE', 'EMPLOYEE STATUS', 'ENROLLMENT AMOUNT', 'DEDUCTION AMOUNT']]

        clean.columns = ['NAME', 'COMPANY CODE', 'HOME DEPARTMENT',
                         'POSITION ID', 'DEDUCTION CODE', 'EMPLOYEE STATUS', 'ENROLLMENT  AMOUNT', 'PAYROLL DEDUCTION']
        st.write(clean)
        """
        ### Step 3: Download the Data
        The below link allows you to download the data for further use
        """
        if df is not None:
            clean_exp = clean.to_csv(index=False)
            # When no file name is given, pandas returns the CSV as a string, nice.
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(clean_exp.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
            st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
