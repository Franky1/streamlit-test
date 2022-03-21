import pandas as pd
import streamlit as st

filepath1 = 'https://github.com/FlorianBrnrd/streamlit-test/blob/f031dde0cf1f0265aff6fe1ac8a2df50a08ec501/web-app/src/exon_coordinates.tsv'
filepath2 = './src/exon_coordinates.tsv'
filepath3 = 'src/exon_coordinates.tsv'
filepath4 = '/src/exon_coordinates.tsv' 


for path in [filepath1,filepath2,filepath3,filepath4]:
    
    if 'github' in path:
        st.write(path)
        s = requests.get(path).content
        table = pd.read_csv(s, sep='\t')
   
    else:
        st.write(path)
        table = pd.read_csv(path, sep='\t')
        st.write(table)

