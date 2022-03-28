import streamlit

from helper_functions import *


def main():

    # general settings
    app_settings()

    # initialization for showing example gene on session start
    if 'input' not in st.session_state:
        st.session_state['input'] = False

    show_title()

    st.write(st.session_state['input'])
    # open ref files and cache them
    genes, exons, dataset, GENES, GENESNAME, ATGPOSITIONS = get_reference_files()

    # chose gene to plot
    gene, refgene = chose_gene(GENES, GENESNAME)

    # chose plot settings
    atg_option = plot_settings()

    # checking gene name input
    if gene is None and refgene is None and st.session_state['input'] == False:
        gene = 'lev-11'
        refgene = 'Y105E8B.1'

    elif gene is None and refgene is None and st.session_state['input'] == True:
        display_error()

    if gene is not None and refgene is not None:

        display_gene_infos(gene, refgene)

        # generate and show gene plot
        gene_plot = plot_gene_start(dataset, gene, genes, exons, ATGPOSITIONS, show_atg=atg_option)
        config = {'displayModeBar': False}
        st.plotly_chart(gene_plot, use_container_width=True, config=config)

        # add legend below
        show_legend()

        # show only if plot was generated
        download_plotly_static(gene_plot, gene, refgene)

    st.write(st.session_state['input'])

    # show app/labs infos
    #show_biorxiv()
    #show_lab()
    bottom_infos()


if __name__ == '__main__':

    main()
