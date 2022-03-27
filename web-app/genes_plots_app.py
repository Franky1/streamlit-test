from helper_functions import *


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
        download_plotly_static(gene_plot, gene, refgene)

    # show app/labs infos
    #show_biorxiv()
    #show_lab()
    bottom_infos()


if __name__ == '__main__':

    main()
