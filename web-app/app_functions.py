import os
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import base64
import plotly.io as pio



def isoform_to_gene(isoform):

    match = re.search(r"\w+.\d+", isoform)

    if match is not None:
        return match.group(0)
    else:
        return None

@st.cache(show_spinner=False)
def get_gene_ref(genes, GENES):

    GENESNAME = genes[genes['CDS'].isin(GENES)]
    GENESNAME['name'] = GENESNAME.apply(lambda x: x['name'] if x['name']==x['name'] else x['CDS'], axis=1)
    GENESNAME = GENESNAME.iloc[GENESNAME.name.str.lower().argsort()]
    GENESNAME = GENESNAME.set_index('CDS')['name'].to_dict()

    return GENESNAME


@st.cache(show_spinner=False)
def get_atg_position(atg):

    # convert transcript name to gene name
    atg['gene'] = atg['transcript'].apply(lambda x: isoform_to_gene(x))

    # create dict
    ATGPOSITIONS = {}
    for gene, positions in atg.groupby('gene'):
        pos = list(set(positions['CDS_start']))
        ATGPOSITIONS[gene] = pos

    return ATGPOSITIONS


@st.cache(show_spinner=False)
def get_reference_files():

    path = os.getcwd()

    exons = pd.read_csv(f'{path}/web-app/src/exon_coordinates.tsv', sep='\t')
    genes = pd.read_csv(f'{path}/web-app/src/genes_coordinates.tsv', sep='\t')
    dataset = pd.read_csv(f'{path}/web-app/src/SL_&_mimic_positions.tsv', sep='\t')
    atg = pd.read_csv(f'{path}/web-app/src/CDS_start_positions.tsv', sep='\t')

    GENES = list(set(dataset['gene']))

    GENESNAME = get_gene_ref(genes, GENES)

    ATGPOSITIONS = get_atg_position(atg)

    return genes, exons, dataset, GENES, GENESNAME, ATGPOSITIONS


def get_legend_filepath():

    path = os.getcwd()
    filepath = f'{path}/web-app/src/legend.png'

    return filepath


def overlapping_exons(start, end, exon):

    x, y = exon
    if x <= start <= y or x <= end <= y:
        return False
    else:
        return True


def plotly_gene_structure(fig, gene, genes_coord, exons_coord):

    # Select exons for gene of interest and remove duplicates
    exons_coord = exons_coord.loc[exons_coord['gene'] == gene].drop_duplicates(['start', 'end']).sort_values('start')

    #### DRAW LINE FIRST

    # get start / end coordinates for the gene
    gene_start = genes_coord.loc[genes_coord['CDS'] == gene, 'start'].values[0]
    gene_end = genes_coord.loc[genes_coord['CDS'] == gene, 'end'].values[0]

    # Calculate isoform length
    gene_length = gene_end - gene_start

    # Create gene line to be plotted
    fig.add_shape(type="line", x0=gene_start, y0=0.5, x1=gene_end, y1=0.5,
                  line=dict(color="black", width=1.5),
                  row=1, col=1)

    #### THEN DRAW EXONS

    # Process exons
    exons_set = []

    for _, exon in exons_coord.iterrows():

        start = exon['start']
        end = exon['end']

        set_size = len(exons_set)

        if set_size == 0:
            exons_set.append((start, end))

        else:
            if all([overlapping_exons(start, end, exons_set[n]) for n in range(set_size)]):
                exons_set.append((start, end))


    strand = exons_coord['strand'].unique()[0]


    l = gene_length + gene_length*0.2
    arrow_size = 0.02*l

    for i, exon in enumerate(exons_set):

        start, end = exon
        length = abs(start-end)

        # bleu fleche vers la gauche (antisense strand last exon)
        if strand == '-' and i == 0:

            if arrow_size <= length:

                xn = start+(arrow_size)

                fig.add_shape(type="path", path= f' M{start},0.5 L{xn},1 H{end} V0, H{xn} Z',
                              fillcolor="LightSkyBlue",
                              line=dict(color="black", width=2),
                              row=1, col=1)

            else:


                fig.add_shape(type="path", path= f' M{start},0.5 L{end},1 V0 Z',
                              fillcolor="LightSkyBlue",
                              line=dict(color="black", width=2),
                              row=1, col=1)


        elif strand == '-' and i > 0:

            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor="LightSkyBlue",
                          row=1, col=1)

        # sense strand last exon
        elif strand == '+' and i+1 == len(exons_set):


            if arrow_size <= length:

                xn = end-(arrow_size)

                fig.add_shape(type="path", path= f' M{start},0 V1 H{xn} L{end},0.5 L{xn},0 Z',
                              fillcolor="LightPink",
                              line=dict(color="black", width=2),
                              row=1, col=1)
            else:

                fig.add_shape(type="path", path= f' M{start},0  V1 L{end},0.5 Z',
                              fillcolor="LightSkyBlue",
                              line=dict(color="black", width=2),
                              row=1, col=1)

        # sense strand
        elif strand == '+' and i < len(exons_set):

            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor="LightPink",
                          row=1, col=1)

        # unknown strand
        else:

            fig.add_shape(type="rect", x0=start, y0=0, x1=end, y1=1,
                          line=dict(color="black", width=2), fillcolor="grey",
                          row=1, col=1)


    return gene_start, gene_end, gene_length


def plot_gene_start(dataset, gene, genes_coord, exons_coord, ATGPOSITION, show_atg=True):

    fig = make_subplots(rows=2, cols=1, row_heights=[2, 10], shared_xaxes=True, vertical_spacing=0.02)


    # plot gene model ---------------------------------
    start, end, length = plotly_gene_structure(fig, gene, genes_coord, exons_coord)

    # lock y axis range on gene model subplot and remove axis/grid/etc
    fig.update_yaxes(fixedrange=True, range=[-1, 2], row=1, col=1)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, row=1, col=1)


    # plot gene data points ---------------------------------

    gene_data = dataset[dataset['gene'] == gene]

    x = list(gene_data['position'])
    y = list(gene_data['total'])

    r = [i/100*255 for i in list(gene_data['%SL'])]
    g = [i/100*255 for i in list(gene_data['%hairpin'])]
    b = [i/100*255 for i in list(gene_data['%unidentified'])]
    col = list(zip(r, g, b))
    col = [f'rgb({r},{g},{b})' for r,g,b in [i for i in col] ]

    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color=col, size=10)), row=2, col=1)

    # plot ATG ---------------------------------

    if show_atg:
        if gene in ATGPOSITION:

            ATG = ATGPOSITION[gene]

            for _atg in ATG:

                fig.add_vline(x=_atg, line_width=1.5, line_dash="dot", line_color="black", row=2, col=1, layer='below')

    # add custom hovering infos ---------------------------------

    cstm = np.stack((gene_data['%SL1'], gene_data['%SL2'], gene_data['%hairpin']), axis=-1)

    hovertemplate = ('<b>Position:</b> %{x}<br>'
                     '<b>Reads:</b> %{y}<br>'+
                     '<br>'+
                     '<b>SL1:</b> %{customdata[0]}%<br>' +
                     '<b>SL2:</b> %{customdata[1]}%<br>' +
                     '<b>Hairpin:</b> %{customdata[2]}%<br>' +
                     '<extra></extra>')

    fig.update_traces(customdata=cstm, hovertemplate=hovertemplate, row=2, col=1)

    # add x and y axis labels ---------------------------------

    fig['layout']['yaxis2']['title']='<b>Number of reads</b>'
    fig['layout']['xaxis2']['title']='<b>genomic start position (bp)</b>'

    # plots settings ---------------------------------

    _start = start - (length*0.1)
    _end = end + (length*0.1)
    fig.update_layout(xaxis_range=[_start, _end], width=900, height=500, margin=dict(l=0, r=0, b=0, t=0))

    fig.update_yaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='black', mirror=True,
                     showgrid=True, gridwidth=0.5, gridcolor='lightgrey',
                     tickformat=',', ticksuffix='</b>', tickfont=dict(size=14, color='black',family='Roboto'),
                     ticks = "outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='black',family='Roboto'))

    fig.update_xaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='black', mirror=True,
                     showgrid=True, gridwidth=0.5, gridcolor='lightgrey',
                     tickformat=',', ticksuffix='bp', tickfont=dict(size=14, color='black', family='Roboto'),
                     ticks = "outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='black', family='Roboto'))

    fig.update_layout(plot_bgcolor="rgb(255,255,255,255)")

    return fig


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
    # pio.kaleido.scope.chromium_args = tuple([arg for arg in pio.kaleido.scope.chromium_args if arg != "--disable-dev-shm-usage"])

    # set explicit headless parameters for chromium (not sure if all are needed)
    pio.kaleido.scope.chromium_args = (
        "--headless",
        "--no-sandbox",
        "--single-process",
        "--disable-gpu",
        # "--disable-dev-shm-usage",
        # "--disable-setuid-sandbox",
        # "--disable-features=NetworkService",
        # "--window-size=1920x1080",
        # "--disable-features=VizDisplayCompositor"
    )  # tuple with chromium args

    # create pdf file and store in memory as bytes for st.download_button
    #plot_bytes = _fig.to_image(format="pdf", engine="kaleido", width=1000, height=700 , scale=1)
    plot_bytes = _fig.to_image(format="png", width=1200, height=900 , scale=2)
    st.sidebar.download_button('???? Download', plot_bytes, file_name='test.png')


def img_to_bytes(img_path):

    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def app_settings():

    st.set_page_config(layout="wide", page_title='C.elegans trans-splicing', page_icon='????')

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

        gene = st.sidebar.text_input('Type name (ex: Y105E8B.1 or lev-11):', value='lev-11')

        # CDS format
        if gene in GENES:
            refgene = GENESNAME[gene]

        # Common name
        elif gene in GENESNAME.values():
            refgene = gene
            gene = [i for i, v in GENESNAME.items() if gene == v][0]

        else:
            gene = None
            refgene = None

        st.session_state['input'] = True
        return gene, refgene

    else:
        return None, None


def display_error():

    gene_header = ("<div style=\"background: #ffe2e0; font-size: 16px; padding: 10px; border-radius: 10px; "
                   "border: 1px solid DarkRed; margin: 10px;\"><div style=\"color: darkred;\"><strong>Requested "
                   "gene plot cannot be generated.</strong></div><br />This error can appear because:<br />- The "
                   "name entered is invalid<br />- The requested gene was not detected in our sequencing "
                   "experiments.<br /><br />Please verify the informations entered and contact the authors if "
                   "necessary.</div>")

    st.markdown(gene_header, unsafe_allow_html=True)




def plot_settings():

    st.sidebar.write('### 2. Customize plot:')

    atg_option = st.sidebar.checkbox('Show known ATG positions (WS270)', value=True)

    return atg_option


def display_gene_infos(gene, refgene):

    cols = st.columns(3)
    with cols[0]:

        gene_header = '<div style="background: ghostwhite; font-size: 18px; padding: 10px; border-radius: 5px; border: 1px solid lightgray; margin: 10px;">' \
                      f'<b>Gene:</b> {refgene} ({gene})<br></div>'


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

        legend_html = f'<span style="font-size:120%;">{legend_txt}</span>'
        st.markdown(legend_html, unsafe_allow_html=True)


def show_title():

    txt = 'Nanopore direct-cDNA sequencing reveals ubiquity of trans-splicing of <i>C. elegans</i> messengers.'
    txt2 = 'Florian Bernard, Delphine Dargere, Oded Rechavi, Denis Dupuy.'

    legend_html = f'<span style="font-size:140%;"><b>{txt}</b></span><br><span style="font-size:110%;">{txt2}</span>'
    st.markdown(legend_html, unsafe_allow_html=True)





