import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import os
from PIL import Image
import tempfile

st.set_page_config(
    page_title="Ferramentas de edição de PDFs",
    page_icon="📎",
    layout="centered"
)

st.title("Ferramentas de edição de PDFs")

# Lista de tarefas estilo iLovePDF
pdf_options = [
    "Selecione a ação...",
    "Juntar PDFs",
    "Dividir PDF (intervalo de páginas)",
    "Extrair páginas específicas",
    "Rotacionar páginas",
    "Adicionar senha ao PDF",
    "Remover senha do PDF",
    "Compactar PDF",
    "Converter PDF para imagens",
    "Converter imagens para PDF"
]

option = st.selectbox("Escolha a ação que deseja realizar:", pdf_options)

if option != "Selecione a ação...":

    if option == "Juntar PDFs":
        st.header("Juntar PDFs")
        pdfs = st.file_uploader("Envie os arquivos PDF que deseja juntar", type="pdf", accept_multiple_files=True)
        if st.button("Juntar"):
            if pdfs:
                writer = PdfWriter()
                for pdf in pdfs:
                    reader = PdfReader(pdf)
                    for page in reader.pages:
                        writer.add_page(page)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("PDFs unidos com sucesso!")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Unificado", f, file_name="merged.pdf")

    elif option == "Dividir PDF (intervalo de páginas)":
        st.header("Dividir PDF")
        pdf = st.file_uploader("Envie o PDF", type="pdf")
        start = st.number_input("Página inicial", 1, 100, 1)
        end = st.number_input("Página final", 1, 100, 1)
        if st.button("Dividir"):
            if pdf and end >= start:
                reader = PdfReader(pdf)
                writer = PdfWriter()
                for i in range(start - 1, end):
                    writer.add_page(reader.pages[i])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("PDF dividido com sucesso!")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Dividido", f, file_name="split.pdf")

    elif option == "Extrair páginas específicas":
        st.header("Extrair Páginas")
        pdf = st.file_uploader("Envie o PDF", type="pdf")
        pages = st.text_input("Digite as páginas a extrair (ex: 1,3,5)")
        if st.button("Extrair"):
            if pdf and pages:
                page_nums = [int(p.strip()) - 1 for p in pages.split(",")]
                reader = PdfReader(pdf)
                writer = PdfWriter()
                for i in page_nums:
                    writer.add_page(reader.pages[i])
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("Páginas extraídas com sucesso!")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Extraído", f, file_name="extracted.pdf")

    elif option == "Rotacionar páginas":
        st.header("Rotacionar Páginas")
        pdf = st.file_uploader("Envie o PDF", type="pdf")
        angle = st.selectbox("Ângulo de rotação", [90, 180, 270])
        if st.button("Rotacionar"):
            if pdf:
                reader = PdfReader(pdf)
                writer = PdfWriter()
                for page in reader.pages:
                    page.rotate(angle)
                    writer.add_page(page)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("Páginas rotacionadas com sucesso!")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Rotacionado", f, file_name="rotated.pdf")

    elif option == "Adicionar senha ao PDF":
        st.header("Adicionar Senha")
        pdf = st.file_uploader("Envie o PDF", type="pdf")
        senha = st.text_input("Digite a senha desejada")
        if st.button("Proteger PDF"):
            if pdf and senha:
                reader = PdfReader(pdf)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                writer.encrypt(senha)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("Senha adicionada com sucesso!")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Protegido", f, file_name="protected.pdf")

    elif option == "Remover senha do PDF":
        st.header("Remover Senha")
        pdf = st.file_uploader("Envie o PDF protegido", type="pdf")
        senha = st.text_input("Digite a senha atual")
        if st.button("Remover Senha"):
            if pdf and senha:
                reader = PdfReader(pdf)
                reader.decrypt(senha)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("Senha removida com sucesso!")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Desprotegido", f, file_name="unlocked.pdf")

    elif option == "Compactar PDF":
        st.header("Compactar PDF")
        st.info("Aviso: Essa compressão apenas remove metadados duplicados.")
        pdf = st.file_uploader("Envie o PDF", type="pdf")
        if st.button("Compactar"):
            if pdf:
                reader = PdfReader(pdf)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                # Simples reescrita, compressão real depende de compressão de imagens internas
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    writer.write(tmp.name)
                    st.success("PDF compactado (modo básico).")
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF Compactado", f, file_name="compressed.pdf")

    elif option == "Converter PDF para imagens":
        st.header("Converter PDF em Imagens")
        pdf = st.file_uploader("Envie o PDF", type="pdf")
        if st.button("Converter"):
            if pdf:
                import fitz  # PyMuPDF
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(pdf.read())
                    pdf_doc = fitz.open(tmp_pdf.name)
                    for i, page in enumerate(pdf_doc):
                        pix = page.get_pixmap()
                        output_image = f"page_{i+1}.png"
                        pix.save(output_image)
                        with open(output_image, "rb") as f:
                            st.download_button(f"Baixar página {i+1}", f, file_name=output_image)
                    st.success("Conversão concluída!")

    elif option == "Converter imagens para PDF":
        st.header("Converter Imagens em PDF")
        imagens = st.file_uploader("Envie as imagens", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        if st.button("Converter"):
            if imagens:
                imgs = [Image.open(img).convert("RGB") for img in imagens]
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    imgs[0].save(tmp.name, save_all=True, append_images=imgs[1:])
                    with open(tmp.name, "rb") as f:
                        st.download_button("Baixar PDF", f, file_name="images_to_pdf.pdf")
                st.success("Conversão concluída!")
