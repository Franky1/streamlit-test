import streamlit as st
from genes_list import GENES
from pathlib import Path
import base64
# from PIL import Image

from helper_functions import plot_GeneStart, genes_start, refname
from plots.test import plotgene

GENES.sort()


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def display_image(img):
    header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=950>"
    st.markdown(header_html.format(img_to_bytes(img)), unsafe_allow_html=True)


def show_plot(gene):
    file = f'/Users/florian/Desktop/THESE/PAPIER/Fig3/plots/{gene}.png'
    display_image(img=file)


def show_legend():
    st.write('#')
    st.write('### Figure legend:')
    st.write('###')
    cols = st.columns([1, 0.1, 1.9])
    with cols[0]:
        file = f'/Users/florian/PycharmProjects/arna/legend.png'
        header_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=300>"
        st.markdown(header_html.format(img_to_bytes(file)), unsafe_allow_html=True)

    with cols[2]:
        st.write(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas nisl leo, consectetur sit amet vulputate sagittis, aliquet vitae eros. Nam maximus mauris at mauris interdum, vel malesuada risus blandit. Sed egestas blandit viverra. Donec sollicitudin vitae enim a porttitor. Aliquam lorem justo, euismod blandit aliquam consectetur, consectetur sed turpis. Ut dictum est eu accumsan fringilla. Nam dolor risus, placerat ac tellus eget, eleifend dignissim odio. Integer pulvinar ac diam id pulvinar. Nunc ut tellus ut risus posuere dignissim. Pellentesque vitae dictum nisl, vel tristique ligula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Proin tellus risus, tristique pretium ultrices vitae, pharetra vel mauris. Ut dictum sagittis consectetur. Sed ut velit sed lorem congue pellentesque sit amet ac metus. Mauris molestie sit amet nulla tempus accumsan. Etiam et sem vitae elit volutpat hendrerit.')


def helper(gene):
    name = f'{refname[gene]} ({gene})' if refname[gene] == refname[gene] else gene
    return name
    # if x == refname[x]:
    #    return x
    # else:
    #    return f'{refname[x]} ({x})'


def sidebar():
    st.sidebar.write('### 1. Chose gene to plot:')

    choice = st.sidebar.radio('input method:', options=['Type gene name', 'Select from list'])

    if choice == 'Select from list':

        refgene = st.sidebar.selectbox('Select:', options=refname.values())
        gene = [i for i, v in refname.items() if refgene == v][0]
        return gene, refgene

    elif choice == 'Type gene name':

        gene = st.sidebar.text_input('Type:', placeholder='ex: Y105E8B.1 or lev-11', )

        # CDS format
        if gene in GENES:
            refgene = refname[gene]
        # Common name
        elif gene in refname.values():
            refgene = gene
            gene = [i for i, v in refname.items() if gene == v][0]
        else:
            gene = 'Y105E8B.1'
            refgene = 'lev-11'
        return gene, refgene

    else:
        return None, None


def plot_settings():
    st.sidebar.write('### 2. Customize plot:')

    atg_option = st.sidebar.checkbox('Show known ATG positions (WS270)')
    unidentified_option = st.sidebar.checkbox('Show unidentified positions')

    return atg_option, unidentified_option


def download_plot():
    st.sidebar.write('### 3. Download .pdf plot:')

    _ = 0
    st.sidebar.download_button('📥 Download', _, file_name='test.pdf')


def paper_names():
    txt = """ """

    st.markdown(txt, unsafe_allow_html=True)
    pass


def display_dataframe(gene):
    with st.expander("Full dataframe"):
        gene_df = genes_start[genes_start['gene'] == gene]

        st.dataframe(gene_df)


def show_lab():
    st.sidebar.markdown("""---""")
    lab = """[![forthebadge](data:image/svg+xml;base64,
    PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMzcuODEiIGhlaWdodD0iMzUiIHZpZXdCb3g9IjAgMCAxMzcuODEgMzUiPjxyZWN0IGNsYXNzPSJzdmdfX3JlY3QiIHg9IjAiIHk9IjAiIHdpZHRoPSI1NC41NCIgaGVpZ2h0PSIzNSIgZmlsbD0iIzVBNUM1QyIvPjxyZWN0IGNsYXNzPSJzdmdfX3JlY3QiIHg9IjUyLjU0IiB5PSIwIiB3aWR0aD0iODUuMjciIGhlaWdodD0iMzUiIGZpbGw9IiM4RkM5NjUiLz48cGF0aCBjbGFzcz0ic3ZnX190ZXh0IiBkPSJNMTkuNTcgMjJMMTQuMjIgMjJMMTQuMjIgMTMuNDdMMTUuNzAgMTMuNDdMMTUuNzAgMjAuODJMMTkuNTcgMjAuODJMMTkuNTcgMjJaTTI0LjQ4IDIyTDIyLjk0IDIyTDI2LjE2IDEzLjQ3TDI3LjQ5IDEzLjQ3TDMwLjcyIDIyTDI5LjE3IDIyTDI4LjQ3IDIwLjAxTDI1LjE3IDIwLjAxTDI0LjQ4IDIyWk0yNi44MiAxNS4yOEwyNS41OCAxOC44MkwyOC4wNiAxOC44MkwyNi44MiAxNS4yOFpNMzcuNzggMjJMMzQuNjcgMjJMMzQuNjcgMTMuNDdMMzcuNjAgMTMuNDdRMzkuMDQgMTMuNDcgMzkuODAgMTQuMDVRNDAuNTYgMTQuNjMgNDAuNTYgMTUuNzhMNDAuNTYgMTUuNzhRNDAuNTYgMTYuMzYgNDAuMjQgMTYuODNRMzkuOTIgMTcuMzAgMzkuMzEgMTcuNTZMMzkuMzEgMTcuNTZRNDAuMDAgMTcuNzUgNDAuMzggMTguMjZRNDAuNzYgMTguNzggNDAuNzYgMTkuNTFMNDAuNzYgMTkuNTFRNDAuNzYgMjAuNzEgMzkuOTkgMjEuMzZRMzkuMjIgMjIgMzcuNzggMjJMMzcuNzggMjJaTTM2LjE1IDE4LjE1TDM2LjE1IDIwLjgyTDM3LjgwIDIwLjgyUTM4LjUwIDIwLjgyIDM4Ljg5IDIwLjQ3UTM5LjI4IDIwLjEzIDM5LjI4IDE5LjUxTDM5LjI4IDE5LjUxUTM5LjI4IDE4LjE4IDM3LjkyIDE4LjE1TDM3LjkyIDE4LjE1TDM2LjE1IDE4LjE1Wk0zNi4xNSAxNC42NkwzNi4xNSAxNy4wNkwzNy42MSAxNy4wNlEzOC4zMCAxNy4wNiAzOC42OSAxNi43NVEzOS4wOCAxNi40MyAzOS4wOCAxNS44NkwzOS4wOCAxNS44NlEzOS4wOCAxNS4yMyAzOC43MiAxNC45NVEzOC4zNiAxNC42NiAzNy42MCAxNC42NkwzNy42MCAxNC42NkwzNi4xNSAxNC42NloiIGZpbGw9IiNGRkZGRkYiLz48cGF0aCBjbGFzcz0ic3ZnX190ZXh0IiBkPSJNNzAuNzAgMjJMNjYuNzMgMjJMNjYuNzMgMTMuNjBMNzAuNzAgMTMuNjBRNzIuMDggMTMuNjAgNzMuMTUgMTQuMTJRNzQuMjIgMTQuNjMgNzQuODEgMTUuNThRNzUuMzkgMTYuNTMgNzUuMzkgMTcuODBMNzUuMzkgMTcuODBRNzUuMzkgMTkuMDcgNzQuODEgMjAuMDJRNzQuMjIgMjAuOTcgNzMuMTUgMjEuNDhRNzIuMDggMjIgNzAuNzAgMjJMNzAuNzAgMjJaTTY5LjExIDE1LjUwTDY5LjExIDIwLjEwTDcwLjYxIDIwLjEwUTcxLjY4IDIwLjEwIDcyLjM0IDE5LjQ5UTcyLjk5IDE4Ljg4IDcyLjk5IDE3LjgwTDcyLjk5IDE3LjgwUTcyLjk5IDE2LjcyIDcyLjM0IDE2LjExUTcxLjY4IDE1LjUwIDcwLjYxIDE1LjUwTDcwLjYxIDE1LjUwTDY5LjExIDE1LjUwWk04MC4wNSAxOC4yNkw4MC4wNSAxOC4yNkw4MC4wNSAxMy42MEw4Mi40MyAxMy42MEw4Mi40MyAxOC4xOVE4Mi40MyAyMC4yMCA4NC4wMiAyMC4yMEw4NC4wMiAyMC4yMFE4NS42MSAyMC4yMCA4NS42MSAxOC4xOUw4NS42MSAxOC4xOUw4NS42MSAxMy42MEw4Ny45NSAxMy42MEw4Ny45NSAxOC4yNlE4Ny45NSAyMC4xMyA4Ni45MSAyMS4xNVE4NS44NyAyMi4xNyA4NC4wMCAyMi4xN0w4NC4wMCAyMi4xN1E4Mi4xMyAyMi4xNyA4MS4wOSAyMS4xNVE4MC4wNSAyMC4xMyA4MC4wNSAxOC4yNlpNOTUuNDIgMjJMOTMuMDQgMjJMOTMuMDQgMTMuNjBMOTYuODggMTMuNjBROTguMDIgMTMuNjAgOTguODYgMTMuOThROTkuNzAgMTQuMzUgMTAwLjE2IDE1LjA2UTEwMC42MSAxNS43NiAxMDAuNjEgMTYuNzFMMTAwLjYxIDE2LjcxUTEwMC42MSAxNy42NiAxMDAuMTYgMTguMzVROTkuNzAgMTkuMDUgOTguODYgMTkuNDJROTguMDIgMTkuODAgOTYuODggMTkuODBMOTYuODggMTkuODBMOTUuNDIgMTkuODBMOTUuNDIgMjJaTTk1LjQyIDE1LjQ3TDk1LjQyIDE3LjkzTDk2LjczIDE3LjkzUTk3LjQ3IDE3LjkzIDk3Ljg0IDE3LjYxUTk4LjIxIDE3LjI5IDk4LjIxIDE2LjcxTDk4LjIxIDE2LjcxUTk4LjIxIDE2LjEyIDk3Ljg0IDE1LjgwUTk3LjQ3IDE1LjQ3IDk2LjczIDE1LjQ3TDk2LjczIDE1LjQ3TDk1LjQyIDE1LjQ3Wk0xMDUuMjkgMTguMjZMMTA1LjI5IDE4LjI2TDEwNS4yOSAxMy42MEwxMDcuNjcgMTMuNjBMMTA3LjY3IDE4LjE5UTEwNy42NyAyMC4yMCAxMDkuMjcgMjAuMjBMMTA5LjI3IDIwLjIwUTExMC44NSAyMC4yMCAxMTAuODUgMTguMTlMMTEwLjg1IDE4LjE5TDExMC44NSAxMy42MEwxMTMuMTkgMTMuNjBMMTEzLjE5IDE4LjI2UTExMy4xOSAyMC4xMyAxMTIuMTUgMjEuMTVRMTExLjExIDIyLjE3IDEwOS4yNCAyMi4xN0wxMDkuMjQgMjIuMTdRMTA3LjM3IDIyLjE3IDEwNi4zMyAyMS4xNVExMDUuMjkgMjAuMTMgMTA1LjI5IDE4LjI2Wk0xMjAuNDEgMTguOTVMMTE3LjIwIDEzLjYwTDExOS43MSAxMy42MEwxMjEuNzAgMTYuOTRMMTIzLjY5IDEzLjYwTDEyNi4wMCAxMy42MEwxMjIuNzggMTguOTlMMTIyLjc4IDIyTDEyMC40MSAyMkwxMjAuNDEgMTguOTVaIiBmaWxsPSIjRkZGRkZGIiB4PSI2NS41Mzk5OTk5OTk5OTk5OSIvPjwvc3ZnPg==)](http://www.iecb.u-bordeaux.fr/teams/DUPUY/DupuylabSite/Welcome.html) """
    st.sidebar.markdown(lab)


def show_biorxiv():
    paper = """[![forthebadge](data:image/svg+xml;base64,
    PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDIuMzk5OTk5OTk5OTk5OTgiIGhlaWdodD0iMzUiIHZpZXdCb3g9IjAgMCAyMDIuMzk5OTk5OTk5OTk5OTggMzUiPjxyZWN0IGNsYXNzPSJzdmdfX3JlY3QiIHg9IjAiIHk9IjAiIHdpZHRoPSIxMDMuNzQiIGhlaWdodD0iMzUiIGZpbGw9IiM1QTVDNUMiLz48cmVjdCBjbGFzcz0ic3ZnX19yZWN0IiB4PSIxMDEuNzQiIHk9IjAiIHdpZHRoPSIxMDAuNjYiIGhlaWdodD0iMzUiIGZpbGw9IiNDMTNCM0EiLz48cGF0aCBjbGFzcz0ic3ZnX190ZXh0IiBkPSJNMTUuNzAgMjJMMTQuMjIgMjJMMTQuMjIgMTMuNDdMMTcuNDggMTMuNDdRMTguOTEgMTMuNDcgMTkuNzUgMTQuMjFRMjAuNTkgMTQuOTYgMjAuNTkgMTYuMThMMjAuNTkgMTYuMThRMjAuNTkgMTcuNDQgMTkuNzcgMTguMTNRMTguOTUgMTguODMgMTcuNDYgMTguODNMMTcuNDYgMTguODNMMTUuNzAgMTguODNMMTUuNzAgMjJaTTE1LjcwIDE0LjY2TDE1LjcwIDE3LjY0TDE3LjQ4IDE3LjY0UTE4LjI3IDE3LjY0IDE4LjY5IDE3LjI3UTE5LjEwIDE2LjkwIDE5LjEwIDE2LjE5TDE5LjEwIDE2LjE5UTE5LjEwIDE1LjUwIDE4LjY4IDE1LjA5UTE4LjI2IDE0LjY4IDE3LjUyIDE0LjY2TDE3LjUyIDE0LjY2TDE1LjcwIDE0LjY2Wk0yNi4zNiAyMkwyNC44OCAyMkwyNC44OCAxMy40N0wyNy44OCAxMy40N1EyOS4zNSAxMy40NyAzMC4xNSAxNC4xM1EzMC45NiAxNC43OSAzMC45NiAxNi4wNUwzMC45NiAxNi4wNVEzMC45NiAxNi45MCAzMC41NCAxNy40OFEzMC4xMyAxOC4wNiAyOS4zOSAxOC4zN0wyOS4zOSAxOC4zN0wzMS4zMSAyMS45MkwzMS4zMSAyMkwyOS43MiAyMkwyOC4wMSAxOC43MUwyNi4zNiAxOC43MUwyNi4zNiAyMlpNMjYuMzYgMTQuNjZMMjYuMzYgMTcuNTJMMjcuODggMTcuNTJRMjguNjMgMTcuNTIgMjkuMDUgMTcuMTVRMjkuNDggMTYuNzcgMjkuNDggMTYuMTFMMjkuNDggMTYuMTFRMjkuNDggMTUuNDMgMjkuMDkgMTUuMDVRMjguNzAgMTQuNjggMjcuOTIgMTQuNjZMMjcuOTIgMTQuNjZMMjYuMzYgMTQuNjZaTTQwLjkzIDIyTDM1LjM1IDIyTDM1LjM1IDEzLjQ3TDQwLjg5IDEzLjQ3TDQwLjg5IDE0LjY2TDM2LjgzIDE0LjY2TDM2LjgzIDE3LjAyTDQwLjM0IDE3LjAyTDQwLjM0IDE4LjE5TDM2LjgzIDE4LjE5TDM2LjgzIDIwLjgyTDQwLjkzIDIwLjgyTDQwLjkzIDIyWk00Ni42MSAyMkw0NS4xMyAyMkw0NS4xMyAxMy40N0w0OC4zOSAxMy40N1E0OS44MiAxMy40NyA1MC42NiAxNC4yMVE1MS41MCAxNC45NiA1MS41MCAxNi4xOEw1MS41MCAxNi4xOFE1MS41MCAxNy40NCA1MC42OCAxOC4xM1E0OS44NSAxOC44MyA0OC4zNyAxOC44M0w0OC4zNyAxOC44M0w0Ni42MSAxOC44M0w0Ni42MSAyMlpNNDYuNjEgMTQuNjZMNDYuNjEgMTcuNjRMNDguMzkgMTcuNjRRNDkuMTggMTcuNjQgNDkuNjAgMTcuMjdRNTAuMDEgMTYuOTAgNTAuMDEgMTYuMTlMNTAuMDEgMTYuMTlRNTAuMDEgMTUuNTAgNDkuNTkgMTUuMDlRNDkuMTcgMTQuNjggNDguNDMgMTQuNjZMNDguNDMgMTQuNjZMNDYuNjEgMTQuNjZaTTU3LjI3IDIyTDU1Ljc4IDIyTDU1Ljc4IDEzLjQ3TDU4Ljc4IDEzLjQ3UTYwLjI2IDEzLjQ3IDYxLjA2IDE0LjEzUTYxLjg3IDE0Ljc5IDYxLjg3IDE2LjA1TDYxLjg3IDE2LjA1UTYxLjg3IDE2LjkwIDYxLjQ1IDE3LjQ4UTYxLjA0IDE4LjA2IDYwLjMwIDE4LjM3TDYwLjMwIDE4LjM3TDYyLjIyIDIxLjkyTDYyLjIyIDIyTDYwLjYzIDIyTDU4LjkyIDE4LjcxTDU3LjI3IDE4LjcxTDU3LjI3IDIyWk01Ny4yNyAxNC42Nkw1Ny4yNyAxNy41Mkw1OC43OSAxNy41MlE1OS41NCAxNy41MiA1OS45NiAxNy4xNVE2MC4zOCAxNi43NyA2MC4zOCAxNi4xMUw2MC4zOCAxNi4xMVE2MC4zOCAxNS40MyA1OS45OSAxNS4wNVE1OS42MCAxNC42OCA1OC44MyAxNC42Nkw1OC44MyAxNC42Nkw1Ny4yNyAxNC42NlpNNjcuODIgMjJMNjYuMzUgMjJMNjYuMzUgMTMuNDdMNjcuODIgMTMuNDdMNjcuODIgMjJaTTc0LjEyIDIyTDcyLjY0IDIyTDcyLjY0IDEzLjQ3TDc0LjEyIDEzLjQ3TDc3LjkzIDE5LjU0TDc3LjkzIDEzLjQ3TDc5LjQwIDEzLjQ3TDc5LjQwIDIyTDc3LjkyIDIyTDc0LjEyIDE1Ljk1TDc0LjEyIDIyWk04NS44MiAxNC42Nkw4My4xOSAxNC42Nkw4My4xOSAxMy40N0w4OS45NiAxMy40N0w4OS45NiAxNC42Nkw4Ny4zMCAxNC42Nkw4Ny4zMCAyMkw4NS44MiAyMkw4NS44MiAxNC42NloiIGZpbGw9IiNGRkZGRkYiLz48cGF0aCBjbGFzcz0ic3ZnX190ZXh0IiBkPSJNMTIwLjQ3IDIyTDExNS45MyAyMkwxMTUuOTMgMTMuNjBMMTIwLjIzIDEzLjYwUTEyMS44MyAxMy42MCAxMjIuNjcgMTQuMTlRMTIzLjUyIDE0Ljc5IDEyMy41MiAxNS43OUwxMjMuNTIgMTUuNzlRMTIzLjUyIDE2LjM5IDEyMy4yMiAxNi44N1ExMjIuOTIgMTcuMzQgMTIyLjM4IDE3LjYyTDEyMi4zOCAxNy42MlExMjMuMTEgMTcuODcgMTIzLjUxIDE4LjQxUTEyMy45MiAxOC45NCAxMjMuOTIgMTkuNzBMMTIzLjkyIDE5LjcwUTEyMy45MiAyMC44MCAxMjMuMDMgMjEuNDBRMTIyLjE0IDIyIDEyMC40NyAyMkwxMjAuNDcgMjJaTTExOC4yOCAxOC41OEwxMTguMjggMjAuMjhMMTIwLjI4IDIwLjI4UTEyMS41MiAyMC4yOCAxMjEuNTIgMTkuNDNMMTIxLjUyIDE5LjQzUTEyMS41MiAxOC41OCAxMjAuMjggMTguNThMMTIwLjI4IDE4LjU4TDExOC4yOCAxOC41OFpNMTE4LjI4IDE1LjMxTDExOC4yOCAxNi45NEwxMTkuOTEgMTYuOTRRMTIxLjExIDE2Ljk0IDEyMS4xMSAxNi4xMkwxMjEuMTEgMTYuMTJRMTIxLjExIDE1LjMxIDExOS45MSAxNS4zMUwxMTkuOTEgMTUuMzFMMTE4LjI4IDE1LjMxWk0xMzEuMDIgMjJMMTI4LjY0IDIyTDEyOC42NCAxMy42MEwxMzEuMDIgMTMuNjBMMTMxLjAyIDIyWk0xMzUuNzYgMTcuODBMMTM1Ljc2IDE3LjgwUTEzNS43NiAxNi41NSAxMzYuMzcgMTUuNTVRMTM2Ljk3IDE0LjU2IDEzOC4wMyAxNC4wMFExMzkuMTAgMTMuNDMgMTQwLjQzIDEzLjQzTDE0MC40MyAxMy40M1ExNDEuNzYgMTMuNDMgMTQyLjgyIDE0LjAwUTE0My44OCAxNC41NiAxNDQuNDkgMTUuNTVRMTQ1LjEwIDE2LjU1IDE0NS4xMCAxNy44MEwxNDUuMTAgMTcuODBRMTQ1LjEwIDE5LjA1IDE0NC40OSAyMC4wNFExNDMuODggMjEuMDQgMTQyLjgyIDIxLjYwUTE0MS43NiAyMi4xNyAxNDAuNDMgMjIuMTdMMTQwLjQzIDIyLjE3UTEzOS4xMCAyMi4xNyAxMzguMDMgMjEuNjBRMTM2Ljk3IDIxLjA0IDEzNi4zNyAyMC4wNFExMzUuNzYgMTkuMDUgMTM1Ljc2IDE3LjgwWk0xMzguMTYgMTcuODBMMTM4LjE2IDE3LjgwUTEzOC4xNiAxOC41MSAxMzguNDYgMTkuMDVRMTM4Ljc2IDE5LjYwIDEzOS4yOCAxOS45MFExMzkuNzkgMjAuMjAgMTQwLjQzIDIwLjIwTDE0MC40MyAyMC4yMFExNDEuMDYgMjAuMjAgMTQxLjU4IDE5LjkwUTE0Mi4xMCAxOS42MCAxNDIuMzkgMTkuMDVRMTQyLjY5IDE4LjUxIDE0Mi42OSAxNy44MEwxNDIuNjkgMTcuODBRMTQyLjY5IDE3LjA5IDE0Mi4zOSAxNi41NFExNDIuMTAgMTYgMTQxLjU4IDE1LjcwUTE0MS4wNiAxNS40MCAxNDAuNDMgMTUuNDBMMTQwLjQzIDE1LjQwUTEzOS43OSAxNS40MCAxMzkuMjcgMTUuNzBRMTM4Ljc2IDE2IDEzOC40NiAxNi41NFExMzguMTYgMTcuMDkgMTM4LjE2IDE3LjgwWk0xNTIuMjAgMjJMMTQ5LjgyIDIyTDE0OS44MiAxMy42MEwxNTMuNjcgMTMuNjBRMTU0LjgxIDEzLjYwIDE1NS42NSAxMy45OFExNTYuNDkgMTQuMzUgMTU2Ljk0IDE1LjA2UTE1Ny40MCAxNS43NiAxNTcuNDAgMTYuNzFMMTU3LjQwIDE2LjcxUTE1Ny40MCAxNy42MiAxNTYuOTcgMTguMzBRMTU2LjU1IDE4Ljk4IDE1NS43NSAxOS4zNkwxNTUuNzUgMTkuMzZMMTU3LjU2IDIyTDE1NS4wMiAyMkwxNTMuNTAgMTkuNzdMMTUyLjIwIDE5Ljc3TDE1Mi4yMCAyMlpNMTUyLjIwIDE1LjQ3TDE1Mi4yMCAxNy45M0wxNTMuNTIgMTcuOTNRMTU0LjI1IDE3LjkzIDE1NC42MyAxNy42MVExNTUuMDAgMTcuMjkgMTU1LjAwIDE2LjcxTDE1NS4wMCAxNi43MVExNTUuMDAgMTYuMTIgMTU0LjYzIDE1Ljc5UTE1NC4yNSAxNS40NyAxNTMuNTIgMTUuNDdMMTUzLjUyIDE1LjQ3TDE1Mi4yMCAxNS40N1pNMTY0LjA0IDIyTDE2MS4zMyAyMkwxNjQuMzggMTcuNzVMMTYxLjQ2IDEzLjYwTDE2NC4xMyAxMy42MEwxNjUuODEgMTYuMDJMMTY3LjQ3IDEzLjYwTDE3MC4wNCAxMy42MEwxNjcuMTEgMTcuNjZMMTcwLjIzIDIyTDE2Ny41MCAyMkwxNjUuNzYgMTkuNDBMMTY0LjA0IDIyWk0xNzYuODkgMjJMMTc0LjUyIDIyTDE3NC41MiAxMy42MEwxNzYuODkgMTMuNjBMMTc2Ljg5IDIyWk0xODQuNjUgMjJMMTgxLjA2IDEzLjYwTDE4My42MyAxMy42MEwxODUuOTEgMTkuMDdMMTg4LjI0IDEzLjYwTDE5MC41OSAxMy42MEwxODYuOTkgMjJMMTg0LjY1IDIyWiIgZmlsbD0iI0ZGRkZGRiIgeD0iMTE0Ljc0Ii8+PC9zdmc+)](https://www.biorxiv.org/) """

    st.sidebar.markdown(paper)


def display_paper_infos():
    st.sidebar.markdown("""---""")
    txt = """See our paper in <b>Nature</b><br>"""
    DOI = """[![DOI:10.1007/978-3-319-76207-4_15](https://zenodo.org/badge/DOI/10.1007/978-3-319-76207-4_15.svg)](https://doi.org/10.1007/978-3-319-76207-4_15)"""
    full = txt + DOI
    st.sidebar.markdown(full, unsafe_allow_html=True)
    st.sidebar.markdown("#")


def bottom_infos():
    st.sidebar.markdown("""---""")

    devname = """App created by <b>Florian Bernard</b>."""
    github = """[![Github](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/FlorianBrnrd)"""
    twitter = """[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://twitter.com/florianbrnrd)"""

    full = devname + """<br>""" + github + '     ' + twitter
    st.sidebar.markdown(full, unsafe_allow_html=True)


def main():
    st.set_page_config(layout="wide", page_title='C.elegans trans-splicing', page_icon='🔬')

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .reportview-container .main .block-container {max-width: 1000px; padding-top: 1rem; padding-right: 1.5rem; padding-left: 1.5rem; padding-bottom: 2rem;}
                </style>
                """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # get gene chosen
    gene, refgene = sidebar()

    # add settings to plot
    atg_option, unidentified_option = plot_settings()

    if gene is None:
        st.error('No gene detected')

    elif refgene != gene:
        st.write(f'### Selected gene: {refgene} ({gene})')
    else:
        st.write(f'### Selected gene: {gene}')

    # show data
    # display_dataframe(gene)

    # show corresponding plot
    # show_plot(gene)
    if gene is not None:
        x = plot_GeneStart(gene)
        st.pyplot(x)

    show_legend()

    download_plot()

    # show_biorxiv()
    # show_lab()
    bottom_infos()


if __name__ == '__main__':
    main()
