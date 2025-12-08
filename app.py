import streamlit as st
import mammoth


st.set_page_config(page_title="Conversor DOCX → HTML", page_icon="🚀")

# ---------------------------------------------------
# Estilo (CSS)
# ---------------------------------------------------
st.markdown("""
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
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Função de conversão
# ---------------------------------------------------
def converter_docx_para_html(arquivo_docx):
    arquivo_docx.seek(0)
    resultado = mammoth.convert_to_html(arquivo_docx)
    return resultado.value, resultado.messages

# ---------------------------------------------------
# App Principal
# ---------------------------------------------------
st.title("🚀 Conversor de Word (.docx) para HTML - PAPOCA")
st.write("Envie um arquivo **.docx** e copie o código HTML gerado para usar no WordPress.")

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