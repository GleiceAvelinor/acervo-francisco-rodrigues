import streamlit as st
import sqlite3
import pandas as pd
import io
import math
from PIL import Image
from datetime import datetime


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as PDFImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


st.set_page_config(page_title="Acervo Francisco Rodrigues", layout="wide", page_icon="🏛️")


st.markdown("""
    <style>
    .stDownloadButton>button { width: 100%; background-color: #27ae60 !important; color: white !important; font-weight: bold; border-radius: 10px; }
    div[data-testid="stExpander"] { border: 1px solid #27ae60; border-radius: 10px; margin-bottom: 10px; }
    .footer-text { text-align: center; color: grey; font-size: 0.9em; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)


def init_db():
    conn = sqlite3.connect("biblioteca_web.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS livros 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, autor TEXT, 
                      isbn TEXT, editora TEXT, categoria TEXT, capa BLOB, data TEXT)''')
    conn.commit()
    return conn

conn = init_db()


def gerar_pdf_inventario(dados_df):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, margin=1.5*cm)
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("<b>INVENTÁRIO DE ACERVO - FRANCISCO RODRIGUES</b>", estilos['Title']),
        Paragraph(f"<font color=grey size=8>Administradora:Edneia Rosendo</font>", estilos['Normal']),
        Spacer(1, 12)
    ]
    tabela_dados = [["CAPA", "DETALHES DO LIVRO", "ISBN / DATA"]]
    for _, r in dados_df.iterrows():
        try:
            img = PDFImage(io.BytesIO(r['capa']), width=1.8*cm, height=2.5*cm) if r['capa'] else "S/ Capa"
        except: img = "Erro Imagem"
        info = Paragraph(f"<b>{r['titulo']}</b><br/>{r['autor']}<br/><i>{r['categoria']}</i>", estilos['Normal'])
        isbn_data = Paragraph(f"{r['isbn'] if r['isbn'] else 'N/A'}<br/>{r['data']}", estilos['Normal'])
        tabela_dados.append([img, info, isbn_data])
    
    t = Table(tabela_dados, colWidths=[2.8*cm, 10.5*cm, 4.2*cm])
    t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('BACKGROUND', (0,0), (-1,0), colors.darkgreen), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elementos.append(t)
    doc.build(elementos)
    return output.getvalue()

st.sidebar.title("🏛️ Gestão do Acervo")
with st.sidebar.form("form_cadastro", clear_on_submit=True):
    st.subheader("📥 Novo Livro")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    isbn = st.text_input("ISBN")
    editora = st.text_input("Editora")
    categoria = st.selectbox("Categoria", ["Psicologia", "Religião", "Política", "Ficção", "Técnico", "Biografia", "Outros"])
    arquivo_capa = st.file_uploader("Foto da Capa", type=["jpg", "png", "jpeg"])
    if st.form_submit_button("ADICIONAR AO ACERVO"):
        if titulo and autor:
            capa_bytes = arquivo_capa.getvalue() if arquivo_capa else None
            conn.execute("INSERT INTO livros (titulo, autor, isbn, editora, categoria, capa, data) VALUES (?,?,?,?,?,?,?)",
                         (titulo, autor, isbn, editora, categoria, capa_bytes, datetime.now().strftime("%d/%m/%Y %H:%M")))
            conn.commit()
            st.rerun()



query = "SELECT * FROM livros ORDER BY id DESC"
df_total = pd.read_sql(query, conn)


st.title("🏛️ Acervo Francisco Rodrigues")
busca = st.text_input("🔍 Pesquisar no acervo...", placeholder="Busque por título, autor ou categoria")

if not df_total.empty:
    
    if busca:
        df_filtrado = df_total[df_total.apply(lambda r: busca.lower() in str(r).lower(), axis=1)]
    else:
        df_filtrado = df_total

    
    itens_por_pagina = 10
    total_itens = len(df_filtrado)
    total_paginas = math.ceil(total_itens / itens_por_pagina)
    
    col_pag1, col_pag2 = st.columns([1, 4])
    with col_pag1:
        pagina_atual = st.number_input("Página", min_value=1, max_value=total_paginas if total_paginas > 0 else 1, step=1)
    
    st.write(f"Total: **{total_itens}** livros | Página **{pagina_atual}** de **{total_paginas}**")
    
    
    inicio = (pagina_atual - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina
    df_pagina = df_filtrado.iloc[inicio:fim]

   
    for _, row in df_pagina.iterrows():
        with st.expander(f"📖 {row['titulo'].upper()} - {row['autor']}"):
            c1, c2 = st.columns([1, 4])
            with c1: 
                if row['capa']: st.image(row['capa'], width='stretch')
                else: st.write("🖼️ Sem capa")
            with c2:
                st.write(f"**Editora:** {row['editora']} | **ISBN:** {row['isbn']}")
                st.write(f"**Categoria:** {row['categoria']} | **Data:** {row['data']}")
                if st.button("🗑️ Remover", key=f"del_{row['id']}"):
                    conn.execute("DELETE FROM livros WHERE id=?", (int(row['id']),))
                    conn.commit()
                    st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.metric("Livros Encontrados", total_itens)
    st.sidebar.download_button("📥 BAIXAR INVENTÁRIO (PDF)", gerar_pdf_inventario(df_filtrado), "Acervo.pdf", "application/pdf")

else:
    st.info("O acervo está vazio.")


st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
    <div style='color: grey; font-size: 0.85em;'>
        👨‍💻 Desenvolvido por:<br>
        <b>Gleice Avelino</b><br>
        v1.0 - | &copy; 2026 Todos os direitos reservados.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="footer-text">
        Desenvolvido por <b>Gleice Avelino</b> | &copy; 2026 Todos os direitos reservados.
    </div>
    """, unsafe_allow_html=True)