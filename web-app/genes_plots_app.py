import streamlit as st
from pathlib import Path
import base64
from helper_functions import gene_start_positions, get_reference_files, get_legend_filepath


def bottom_infos():

    st.sidebar.empty()

    st.sidebar.markdown("""---""")

    devname = """App created by <b>Florian Bernard</b>."""
    github = """[![Github](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/FlorianBrnrd)"""
    twitter = """[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://twitter.com/florianbrnrd)"""

    full = devname + """<br>""" + github + '     ' + twitter
    st.sidebar.markdown(full, unsafe_allow_html=True)






def download_plot():
    st.sidebar.write('### 3. Download .pdf plot:')

    #_ = 0
    #st.sidebar.download_button('📥 Download', _, file_name='test.pdf')





def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded






def app_settings():

    st.set_page_config(layout="wide", page_title='C.elegans trans-splicing', page_icon='🔬')

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .reportview-container .main .block-container {max-width: 1000px; padding-top: 1rem; padding-right: 1.5rem; padding-left: 1.5rem; padding-bottom: 2rem;}
                </style>
                """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def chose_gene(GENES, GENESNAME):

    st.sidebar.write('### 1. Chose gene to plot:')

    choice = st.sidebar.radio('input method:', options=['Type gene name', 'Select from list'])

    if choice == 'Select from list':

        refgene = st.sidebar.selectbox('Select:', options=GENESNAME.values())
        gene = [i for i, v in GENESNAME.items() if refgene == v][0]
        return gene, refgene

    elif choice == 'Type gene name':

        gene = st.sidebar.text_input('Type:', placeholder='ex: Y105E8B.1 or lev-11', )

        # CDS format
        if gene in GENES:
            refgene = GENESNAME[gene]
        # Common name
        elif gene in GENESNAME.values():
            refgene = gene
            gene = [i for i, v in GENESNAME.items() if gene == v][0]
        else:
            gene = 'Y105E8B.1'
            refgene = 'lev-11'
        return gene, refgene

    else:
        return None, None


def plot_settings():

    st.sidebar.write('### 2. Customize plot:')

    atg_option = st.sidebar.checkbox('Show known ATG positions (WS270)')

    return atg_option


def show_legend():

    st.write('#')
    st.write('### Figure legend:')
    st.write('###')

    cols = st.columns([0.25,0.05,0.7])

    with cols[0]:

        legendfile = get_legend_filepath()
        header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=200>"
        st.markdown(header_html.format(img_to_bytes(legendfile)), unsafe_allow_html=True)

    with cols[2]:


        legend_txt = 'Each alignment start position observed was plotted at the corresponding genomic position with the number of '
                     'supporting reads. The dots are colored according to the observed trans-splicing events '
                     'with red indicating a majority of SL reads, green a majority of endogenous hairpin reads '
                     'and blue reads with no evidence for either.'

        legend_html = f'<span style="font-size:200%; font-weight: bold;">{legend_txt}</span>'
        st.markdown(legend_html, unsafe_allow_html=True)




def main():

    # general settings
    app_settings()


    # open ref files and cache them
    genes, exons, dataset, GENES, GENESNAME, ATGPOSITIONS = get_reference_files()

    # chose gene to plot
    gene, refgene = chose_gene(GENES, GENESNAME)

    # chose plot settings
    atg_option = plot_settings()

    if gene is None:
        st.error('No gene detected')

    else:
        if refgene != gene:
            st.write(f'### Selected gene: {refgene} ({gene})')
        else:
            st.write(f'### Selected gene: {gene}')

        # generate gene plot
        gene_plot = gene_start_positions(dataset, gene, genes, exons, GENESNAME, ATGPOSITIONS, show_atg=atg_option)

        # show plot with streamlit
        st.pyplot(gene_plot)
        # add legend below
        show_legend()

        # show only if plot was generated
        download_plot()

    # show app/labs infos
    #show_biorxiv()
    #show_lab()
    bottom_infos()


if __name__ == '__main__':

    main()
