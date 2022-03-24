import os
import re
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import streamlit as st


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





def generate_plot(dataset, gene, genes_coord, exons_coord, ATGPOSITION, show_atg=True):



    fig = make_subplots(rows=2, cols=1, row_heights=[2, 10], shared_xaxes=True, vertical_spacing=0.02)


    # gene model
    plotly_gene_structure(fig, gene, genes_coord, exons_coord)

    # lock y axis range on gene model subplot
    fig.update_yaxes(fixedrange=True, range=[-1, 2], row=1, col=1)

    # remove x axis border on top subplot
    fig.update_xaxes(visible=False, row=1, col=1)

    # remove y axis border on top subplot
    fig.update_yaxes(visible=False, row=1, col=1)



    # ATG ---------------------------------
    if show_atg:
        if gene in ATGPOSITION:

            ATG = ATGPOSITION[gene]

            for _atg in ATG:

                fig.add_vline(x=_atg, line_width=2, line_dash="dash", line_color="black")



    ###### gene data points
    gene_data = dataset[dataset['gene'] == gene]

    x = list(gene_data['position'])
    y = list(gene_data['total'])

    r = [i/100*255 for i in list(gene_data['%SL'])]
    g = [i/100*255 for i in list(gene_data['%hairpin'])]
    b = [i/100*255 for i in list(gene_data['%unidentified'])]
    col = list(zip(r, g, b))
    col = [f'rgb({r},{g},{b})' for r,g,b in [i for i in col] ]


    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color=col, size=10))
                  , row=2, col=1)










    cstm = np.stack((gene_data['%SL1'], gene_data['%SL2'], gene_data['%hairpin']), axis=-1)

    hovertemplate = ('<b>Position:</b> %{x}<br>'
                     '<b>Reads:</b> %{y}<br>'+
                     '<br>'+
                     '<b>SL1:</b> %{customdata[0]}%<br>' +
                     '<b>SL2:</b> %{customdata[1]}%<br>' +
                     '<b>Hairpin:</b> %{customdata[2]}%<br>' +
                     '<extra></extra>')

    fig.update_traces(customdata=cstm, hovertemplate=hovertemplate, row=2, col=1)

    fig['layout']['yaxis2']['title']='<b>Number of reads</b>'
    fig['layout']['xaxis2']['title']='<b>genomic start position (bp)</b>'

    x0 = min(x)
    x1 = max(x)
    length = x1-x0
    start = x0-(0.1*length)
    end = x1+(0.1*length)

    fig.update_layout(xaxis_range=[start, end], width=900, height=500, margin=dict(l=0, r=0, b=0, t=0))


    fig.update_xaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='black', mirror=True)
    fig.update_yaxes(zeroline=False, showline=True, linewidth=1.2, linecolor='black', mirror=True)
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')
    fig.update_layout(plot_bgcolor="rgb(255,255,255,255)")


    fig.update_yaxes(tickformat=',', ticksuffix='</b>', tickfont=dict(size=14, color='black',family='Roboto'),
                     ticks = "outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='black',family='Roboto'))

    fig.update_xaxes(tickformat=',', ticksuffix='bp', tickfont=dict(size=14, color='black', family='Roboto'),
                     ticks = "outside", tickcolor='black', ticklen=5,
                     title_font=dict(size=16, color='black', family='Roboto'))

    return fig