import pandas as pd

import seaborn as sns
import time
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from matplotlib.ticker import MaxNLocator, MultipleLocator, AutoMinorLocator
from matplotlib.backends.backend_pdf import PdfPages

from dna_features_viewer import GraphicFeature, GraphicRecord



###### OPEN FILES

genes_start = pd.read_csv('src/SL_&_mimic_positions.tsv', sep='\t')

genesref = pd.read_csv('src/genes_coordinates.tsv', sep='\t')


_genesfound = list(genes_start['gene'])
refname = genesref[genesref['CDS'].isin(_genesfound)]
refname['name'] = refname.apply(lambda x: x['name'] if x['name']==x['name'] else x['CDS'], axis=1)

#refname = refname.sort_values('name',ascending=True)
refname = refname.iloc[refname.name.str.lower().argsort()]
refname = refname.set_index('CDS')['name'].to_dict()
#refname = {k: v for k, v in sorted(refname.items(), key=lambda x: x[1])}

exonslist = pd.read_csv('/Users/florian/Bioinfo/Manuscript_old/Bioinformatics analysis/exon_coordinates.tsv', sep='\t')


##### FUNCTIONS

def OverlappingExons(start, end, exon):
    x, y = exon
    if x <= start <= y or x <= end <= y:
        return False
    else:
        return True


def GeneStructure(gene, return_coordinates=False):

    # Open reference files
    exonslist = pd.read_csv('exon_coordinates.tsv', sep='\t')
    geneslist = pd.read_csv('genes_coordinates.tsv', sep='\t')

    # Select exons for gene of interest and remove duplicates
    exonslist = exonslist.loc[exonslist['gene'] == gene].drop_duplicates(['start', 'end']).sort_values('start')

    # Process exons
    exons_set = []
    gene_structure = []

    for _, exon in exonslist.iterrows():

        start = exon['start']
        end = exon['end']

        set_size = len(exons_set)

        if set_size == 0:
            exons_set.append((start, end))

        else:
            if all([OverlappingExons(start, end, exons_set[n]) for n in range(set_size)]):
                exons_set.append((start, end))

    color = {'+': '#ffd1df', '-': '#95d0fc'}
    strand = exonslist['strand'].unique()[0]

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
    gene_start = geneslist.loc[geneslist['CDS'] == gene, 'start'].values[0]
    gene_end = geneslist.loc[geneslist['CDS'] == gene, 'end'].values[0]

    # Calculate isoform length
    length = gene_end - gene_start

    # Create feature to be plotted
    record = GraphicRecord(first_index=gene_start, sequence_length=length, features=gene_structure)

    if return_coordinates is False:
        return record
    else:
        return gene_start, length, record


# main function for plotting gene start representated in our dataset
# for each gene, the first aligned based of a read is considered the "start position"
# for each representated start position (X axis), we plot the number of reads (Y axis)

def gene_start_positions(gene, output=None, min_reads=None):

    # get common name
    name = f'{refname[gene]} ({gene})' if refname[gene] == refname[gene] else gene

    # plot setting ----------------------

    sns.set_style("white")
    fig = plt.figure(figsize=(8, 5), dpi=300) # constrained_layout=True

    grid = fig.add_gridspec(2, 1,
                            height_ratios=[1.5, 6],
                            top=1.05, bottom=0.08, right=0.95, left=0.08, hspace=0.1, wspace=0)

    # Gene structure ----------------------

    axis1 = fig.add_subplot(grid[0])
    axis1.grid(False)
    axis1.axis('off')

    start, length, record = GeneStructure(gene, return_coordinates=True)
    record.plot(ax=axis1)


    #### computing --------------------------

    gene_df = genes_start[genes_start['gene'] == gene]

    #### plotting --------------------------

    axis2 = fig.add_subplot(grid[1], sharex = axis1)

    x = list(gene_df['position'])
    y = list(gene_df['total'])

    r = [i/100 for i in list(gene_df['%SL'])]
    g = [i/100 for i in list(gene_df['%hairpin'])]
    b = [i/100 for i in list(gene_df['%unidentified'])]
    col= list(zip(r, g, b))

    plot = axis2.scatter(x, y ,c=col, s=50, alpha=1, edgecolor='k', linewidth=0.1)


    # ATG ------

    if gene in ATG_positions:

        ATG = ATG_positions[gene]
        _max = max(y)*1.1

        for _atg in ATG:
            axis2.vlines(_atg, 0, _max, colors='k', linestyles='dotted', zorder=-1)
            axis2.set_ylim(top=_max)

    # settings ------

    axis2.set_ylabel('number of reads', weight='bold')
    axis2.set_xlabel('genomic start position (bp)', weight='bold')
    axis2.tick_params(axis='both', left=True, top=False, right=False, bottom=True,
                      labelleft=True, labeltop=False, labelright=False, labelbottom=True)

    axis2.xaxis.set_major_locator(plt.MaxNLocator(7))
    axis2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    axis2.set_xlim(start-(0.1*length), (start+(length*1.1)))

    fig.suptitle(name, weight='bold', style='italic', size=14)

    return fig


if __name__ == '__main__':

    x = pd.DataFrame.from_dict(refname, orient='index')



