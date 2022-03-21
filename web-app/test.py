import pandas as pd
import streamlit as st
import os

filepath2 = 'src/exon_coordinates.tsv'
filepath3 = 'src/exon_coordinates.tsv'
filepath4 = '/src/exon_coordinates.tsv' 


st.write(os.getcwd())

for path in [filepath2,filepath3,filepath4]:

    st.write(path)
    table = pd.read_csv(path, sep='\t')
    st.write(table)

