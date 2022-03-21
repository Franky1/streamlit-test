import pandas as pd
import streamlit as st
import os

filepath2 = '/app/streamlit-test/src/exon_coordinates.tsv'
filepath3 = 'app/streamlit-test/src/exon_coordinates.tsv'


st.write(os.getcwd())

for path in [filepath2,filepath3]:

    st.write(path)
    try:
        table = pd.read_csv(path, sep='\t')
        st.write(table)
    except:
        st.write('not working')
    

