import re

import mammoth
import streamlit as st


st.set_page_config(page_title="Conversor DOCX → HTML", page_icon="🚀")

st.markdown(
    """
<style>
.stApp {
    background-color: #091424 !important;
}
h1 {
    color: #EB008B !important;
    font-weight: 650 !important;
}
.stButton > button, .stDownloadButton > button {
    background-color: #3D3D3D !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 600 !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #FF42B3 !important;
}
textarea {
    background-color: #2A0046 !important;
    color: #FFFFFF !important;
    border: 1px solid #EB008B !important;
    border-radius: 8px !important;
}
.stFileUploader {
    background-color: #2A0046 !important;
    padding: 12px !important;
    border-radius: 8px !important;
    border: 1px solid #EB008B !important;
}
.stFileUploader div[data-testid="stFileUploaderDropzone"] {
    background-color: #3C0061 !important;
    border: 2px dashed #EB008B !important;
}
.stFileUploader button:hover {
    background-color: #FF42B3 !important;
    color: #FFFFFF !important;
}
</style>
""",
    unsafe_allow_html=True,
)


def ajustar_html_para_papoca(html: str) -> str:
    html = re.sub(r"<h1>(.*?)</h1>", r'<h1 class="h1style">\1</h1>', html, flags=re.DOTALL)
    html = re.sub(r"<h2>(.*?)</h2>", r'<h2 class="h2style">\1</h2>', html, flags=re.DOTALL)
    html = re.sub(r"<h3>(.*?)</h3>", r'<h3 class="h3style">\1</h3>', html, flags=re.DOTALL)

    html = re.sub(
        r'<a(?=[^>]*\sid="[^"]+")(?![^>]*\shref=)[^>]*>.*?</a>',
        "",
        html,
        flags=re.DOTALL,
    )

    html = re.sub(
        r"<strong>\s*(<a[^>]*>.*?</a>)\s*</strong>",
        r"\1",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<a([^>]*)>\s*<strong>(.*?)</strong>\s*</a>",
        r"<a\1>\2</a>",
        html,
        flags=re.DOTALL,
    )

    def adicionar_target(match: re.Match) -> str:
        atributos = match.group(1)
        if "target=" in atributos:
            return match.group(0)
        return f'<a{atributos} target="_blank">'

    html = re.sub(r"<a([^>]*)>", adicionar_target, html)

    return html


def converter_docx_para_html(arquivo_docx):
    arquivo_docx.seek(0)
    resultado = mammoth.convert_to_html(arquivo_docx)
    html_ajustado = ajustar_html_para_papoca(resultado.value)
    return html_ajustado, resultado.messages


st.title("🚀 Conversor de Word (.docx) para HTML - PAPOCA")
st.write(
    "Envie um arquivo **.docx** e copie o código HTML gerado para usar no WordPress."
)

uploaded_file = st.file_uploader("Escolha um arquivo .docx", type=["docx"])

if uploaded_file:
    st.info(f"📄 Arquivo selecionado: **{uploaded_file.name}**")

    if st.button("Converter para HTML"):
        html, mensagens = converter_docx_para_html(uploaded_file)

        if html:
            st.success("✅ Conversão concluída!")
            st.subheader("📑 Código HTML (copie e cole no WordPress)")
            st.text_area("HTML gerado:", html, height=400)

            nome_base = uploaded_file.name.rsplit(".", 1)[0]
            nome_html = f"{nome_base}.txt"

            st.download_button(
                label="Baixar HTML como arquivo .txt",
                data=html,
                file_name=nome_html,
                mime="text/plain",
            )
        else:
            st.warning("⚠️ Conversão falhou ou gerou HTML vazio.")
