import os
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from dna_features_viewer import GraphicFeature, GraphicRecord


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


def OverlappingExons(start, end, exon):
    x, y = exon
    if x <= start <= y or x <= end <= y:
        return False
    else:
        return True


def GeneStructure(gene, genes_coord, exons_coord, return_coordinates=False):

    # Select exons for gene of interest and remove duplicates
    exons_coord = exons_coord.loc[exons_coord['gene'] == gene].drop_duplicates(['start', 'end']).sort_values('start')

    # Process exons
    exons_set = []
    gene_structure = []

    for _, exon in exons_coord.iterrows():

        start = exon['start']
        end = exon['end']

        set_size = len(exons_set)

        if set_size == 0:
            exons_set.append((start, end))

        else:
            if all([OverlappingExons(start, end, exons_set[n]) for n in range(set_size)]):
                exons_set.append((start, end))

    color = {'+': '#ffd1df', '-': '#95d0fc'}
    strand = exons_coord['strand'].unique()[0]

    i = 1
    for exon in exons_set:

        start, end = exon

        if strand == '-' and i == 1:
            strd = -1
            i += 1

        elif strand == '+' and i == len(exons_set):
            strd = +1
            i += 1

        else:
            strd = 0
            i += 1

        gene_structure.append(GraphicFeature(start=start, end=end, strand=strd, color=color[strand],
                                             thickness=25, linewidth=1.5))

    # get start / end coordinates for the gene
    gene_start = genes_coord.loc[genes_coord['CDS'] == gene, 'start'].values[0]
    gene_end = genes_coord.loc[genes_coord['CDS'] == gene, 'end'].values[0]

    # Calculate isoform length
    length = gene_end - gene_start

    # Create feature to be plotted
    record = GraphicRecord(first_index=gene_start, sequence_length=length, features=gene_structure)

    if return_coordinates is False:
        return record
    else:
        return gene_start, length, record


def gene_start_positions(dataset, gene, genes_coord, exons_coord, GENESNAME, ATGPOSITION, show_atg=True):

    # get common name

    name = f'{GENESNAME[gene]} ({gene})' if GENESNAME[gene] == GENESNAME[gene] else gene

    # plot setting ----------------------

    sns.set_style("white")
    fig = plt.figure(figsize=(15, 8), dpi=800)

    grid = fig.add_gridspec(3, 1, height_ratios=[0.8, 0.1, 4],
                            top=1.1, bottom=0.08, right=0.95, left=0.08, hspace=0.05, wspace=0)

    # Gene structure ----------------------

    axis1 = fig.add_subplot(grid[0])
    axis1.grid(False)
    axis1.axis('off')

    start, length, record = GeneStructure(gene, genes_coord, exons_coord, return_coordinates=True)
    record.plot(ax=axis1)

    #### computing --------------------------

    gene_df = dataset[dataset['gene'] == gene]

    #### plotting --------------------------

    axis2 = fig.add_subplot(grid[2], sharex=axis1)

    x = list(gene_df['position'])
    y = list(gene_df['total'])

    r = [i/100 for i in list(gene_df['%SL'])]
    g = [i/100 for i in list(gene_df['%hairpin'])]
    b = [i/100 for i in list(gene_df['%unidentified'])]
    col = list(zip(r, g, b))

    axis2.scatter(x, y, c=col, s=120, alpha=1, edgecolor=None)

    _max = max(y)*1.1

    # ATG ---------------------------------
    if show_atg:
        if gene in ATGPOSITION:

            ATG = ATGPOSITION[gene]

            for _atg in ATG:
                axis2.vlines(_atg, 0, _max, colors='k', linestyles='dotted', zorder=-1)

    # settings ----------------------------

    axis2.set_ylabel('Number of reads', weight='bold', fontsize=18, labelpad=15)
    axis2.set_xlabel('Genomic start position (bp)', weight='bold', fontsize=18, labelpad=15)

    axis2.tick_params(axis='both', left=True, top=False, right=False, bottom=True,
                      labelleft=True, labeltop=False, labelright=False, labelbottom=True)

    axis2.xaxis.set_major_locator(plt.MaxNLocator(7))
    axis2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    axis2.set_xlim(start-(0.1*length), (start+(length*1.1)))
    axis2.set_ylim(top=_max)

    return fig


def get_legend_filepath():
    path = os.getcwd()
    filepath = f'{path}/web-app/src/legend.png'
    return filepath
