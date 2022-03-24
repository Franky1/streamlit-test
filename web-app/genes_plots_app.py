import streamlit as st
from pathlib import Path
import base64
from helper_functions import plot_gene_start, get_reference_files, get_legend_filepath
import plotly.io as pio



def bottom_infos():

    st.sidebar.markdown("""---""")

    devname = """App created by <b>Florian Bernard</b>."""
    github = """[![Github](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/FlorianBrnrd)"""
    twitter = """[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://twitter.com/florianbrnrd)"""

    full = devname + """<br>""" + github + '     ' + twitter
    st.sidebar.markdown(full, unsafe_allow_html=True)


def download_plotly_static(fig, gene, generef):

    st.sidebar.markdown('### 3. Save plot:')

    if generef is not None:
        name_template=f'<b>{gene} ({generef}) </b>'
    else:
        name_template=f'<b>{gene}</b>'

    # modify layout for pdf + add title
    _fig = fig.update_layout(margin=dict(l=100, r=100, b=100, t=100), title_text=name_template, title_font_size=30,
                             title_font_family='Roboto', title_font_color='black')

    #pio.kaleido.scope.chromium_args += ('--single-process')
    pio.kaleido.scope.chromium_args = tuple([arg for arg in pio.kaleido.scope.chromium_args if arg != "--disable-dev-shm-usage"])


    # create pdf file and store in memory as bytes for st.download_button
    #plot_bytes = _fig.to_image(format="pdf", engine="kaleido", width=1000, height=700 , scale=1)
    plot_bytes = _fig.to_image(format="png", width=1200, height=900 , scale=2)
    st.sidebar.download_button('📥 Download', plot_bytes, file_name='test.png')


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
                header {visibility: hidden;}
                .appview-container .main .block-container {max-width: 1000px; padding-top: 1rem; padding-right: 1.5rem; padding-left: 1.5rem; padding-bottom: 2rem;}
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


def display_gene_infos(gene, refgene):

    gene_header = '<div style="background: ghostwhite; font-size: 16px; padding: 10px; border-radius: 10px; border: 1px solid lightgray; margin: 10px;">' \
                  f'<b>Input gene:</b> {refgene} ({gene})<br>' \
                  '<b>Genomic location:</b> chromosome X : 124058688 - 27465858' \
                  '</div>'

    st.markdown(gene_header, unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)


def show_legend():

    st.write('#')
    legend_header = '<span style="font-size:150%; font-weight: bold;">Figure legend:</span>'
    st.markdown(legend_header, unsafe_allow_html=True)
    st.write('##')

    cols = st.columns([0.22,0.03,0.75])

    with cols[0]:

        legendfile = get_legend_filepath()
        header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=180>"
        st.markdown(header_html.format(img_to_bytes(legendfile)), unsafe_allow_html=True)

    with cols[2]:

        legend_txt = 'Each alignment start position observed was plotted at the corresponding genomic position with ' \
                     'the number of supporting reads. The dots are colored according to the observed trans-splicing ' \
                     'events with red indicating a majority of SL reads, green a majority of endogenous hairpin reads ' \
                     'and blue reads with no evidence for either. '
        #st.write(legend_txt)
        legend_html = f'<span style="font-size:120%;">{legend_txt}</span>'
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

        display_gene_infos(gene, refgene)

        # generate and show gene plot
        gene_plot = plot_gene_start(dataset, gene, genes, exons, ATGPOSITIONS, show_atg=atg_option)
        config = {'displayModeBar': False}
        st.plotly_chart(gene_plot, use_container_width=True, config=config)


        # add legend below
        show_legend()

        # show only if plot was generated
        #download_plotly_static(gene_plot, gene, refgene)

    # show app/labs infos
    #show_biorxiv()
    #show_lab()
    bottom_infos()


if __name__ == '__main__':

    main()
