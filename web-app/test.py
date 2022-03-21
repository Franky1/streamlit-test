import pandas as pd
import streamlit as st
import os

filepath2 = '/app/streamlit-test/web-app/src/exon_coordinates.tsv'


for path in [filepath2]:

    st.write(path)
    table = pd.read_csv(path, sep='\t')
    if len(table)>10:
        st.write('yay!')
    
    

