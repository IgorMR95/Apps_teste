import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from streamlit_drawable_canvas import st_canvas
import graphviz
from wordcloud import WordCloud
import streamlit.components.v1 as components
import json
import streamlit as st
import json
import streamlit.components.v1 as components
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io

st.set_page_config(page_title="Visual Law: Ferramentas", layout="wide")
st.title("Ferramentas de Visual Law")

st.markdown("""
Use essas ferramentas visuais para deixar seus documentos jurídicos mais claros e compreensíveis.

**Passos Simples:**
1. Escolha o que você deseja criar no menu abaixo.
2. Preencha os campos com suas informações.
3. Veja a visualização e baixe se quiser!
""")

# Escolha da ferramenta
opcao = st.selectbox("O que deseja criar?", [
    "Selecione",
    "Linha do Tempo",
    "Gráfico",
    "Fluxograma",
    "Nuvem de Palavras"
])

# Função para baixar imagem

def baixar_figura(fig, nome):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button("Baixar imagem", buf.getvalue(), f"{nome}.png", "image/png")

# Linha do tempo
# Linha do tempo


if opcao == "Linha do Tempo":
    st.title("Gerador de Linha do Tempo")

    st.markdown("""
    ## Como funciona
    Crie facilmente uma linha do tempo visual com datas, títulos e descrições de eventos.  
    A linha do tempo pode ser visualizada diretamente abaixo e capturada como imagem usando as instruções abaixo.

    ### Como preencher corretamente
    - **Data**: escolha a data do evento
    - **Título**: escreva um nome curto para o evento (por exemplo: Sentença publicada)
    - **Descrição**: detalhe o que aconteceu nesse evento

    ### Como salvar a imagem
    - Após gerar a linha do tempo, use o botão do seu navegador para **imprimir ou salvar como PDF**
    - Ou use a tecla **Print Screen** e cole em um editor de imagem ou Word para salvar como imagem
    """)

    # Entrada dos eventos
    st.subheader("Adicionar Eventos")
    eventos = []
    qtd = st.number_input("Quantos eventos deseja adicionar?", min_value=1, max_value=20, value=3)

    for i in range(qtd):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input(f"Data do Evento {i+1}", key=f"data_{i}")
        with col2:
            titulo = st.text_input(f"Título do Evento {i+1}", key=f"titulo_{i}")
        descricao = st.text_area(f"Descrição do Evento {i+1}", key=f"desc_{i}")
        eventos.append({
            "start": str(data),
            "content": f"<b>{titulo}</b><br><small>{descricao}</small>",
            "title": descricao
        })

    # Geração
    if st.button("Gerar Linha do Tempo"):
        html = f"""
        <link href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" type="text/css" />
        <script src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
        <div id="visualization"></div>
        <script>
        const container = document.getElementById('visualization');
        const items = {json.dumps(eventos)};
        const options = {{
            height: '450px',
            editable: false,
            margin: {{
                item: 20
            }},
            stack: true
        }};
        new vis.Timeline(container, items, options);
        </script>
        """
        components.html(html, height=500)
        st.success("Linha do tempo gerada. Use Print Screen ou botão de impressão do navegador para salvar.")


# Gráfico simples


if opcao == "Gráfico":
    st.title("Criador Simples de Gráficos")

    st.markdown("""
    ## Como usar este gerador de gráficos
    1. Escolha o tipo de gráfico que deseja.
    2. Preencha os dados com nomes e valores.
    3. Personalize as cores, textos e aparência.
    4. Gere o gráfico e baixe se quiser.

    ### Exemplos de uso
    - Comparar valores de indenizações
    - Mostrar evolução de prazos ou processos
    - Ilustrar dados de uma petição

    **Dica**: insira nomes simples (ex: "2023", "Recurso", "Valor A") e valores numéricos.
    """)

    # Escolha do tipo
    tipo = st.radio("Tipo de gráfico que deseja criar:", ["Barras", "Linha", "Área"])

    # Número de itens
    qtd = st.number_input("Quantos itens você quer comparar?", min_value=1, max_value=20, value=3)

    # Coleta de dados
    nomes, valores = [], []
    st.subheader("Preencha seus dados")

    for i in range(qtd):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input(f"Nome do item {i+1}", key=f"nome_{i}")
        with col2:
            valor = st.number_input(f"Valor do item {i+1}", key=f"valor_{i}")
        nomes.append(nome)
        valores.append(valor)

    # Personalização visual
    st.subheader("Personalize a aparência do gráfico")

    # Cores
    cor_primaria = st.color_picker("Cor principal (linhas/barras)", "#0F62FE")
    cor_fundo = st.color_picker("Cor de fundo do gráfico", "#FFFFFF")

    # Estética
    mostrar_grid = st.checkbox("Mostrar linhas de grade", value=True)
    mostrar_valores = st.checkbox("Exibir valores nos pontos (rótulos)", value=True)

    # Títulos e Rótulos
    st.markdown("### Textos no gráfico")
    titulo = st.text_input("Título do gráfico", "")
    rotulo_x = st.text_input("Texto para o eixo X", "Categorias")
    rotulo_y = st.text_input("Texto para o eixo Y", "Valores")

    # Fonte
    tamanho_titulo = st.slider("Tamanho do título", 10, 30, 16)
    tamanho_rotulos = st.slider("Tamanho dos rótulos dos eixos", 8, 20, 12)

    # Estilo extra (para linha/área)
    espessura_linha = st.slider("Espessura da linha (gráficos de linha/área)", 1, 10, 2)
    tamanho_marcador = st.slider("Tamanho dos marcadores (linha/área)", 2, 15, 6)

    # Função para baixar gráfico
    def baixar_figura(fig, nome):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor=cor_fundo)
        st.download_button("Baixar imagem", buf.getvalue(), f"{nome}.png", "image/png")

    # Geração do gráfico
    if st.button("Gerar Gráfico"):
        df = pd.DataFrame({"Nome": nomes, "Valor": valores})

        for idx in [1, 2]:  # Gera gráfico 1 e 2
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor(cor_fundo)
            ax.set_facecolor(cor_fundo)
            ax.grid(mostrar_grid)
            ax.set_title(titulo, fontsize=tamanho_titulo)
            ax.set_xlabel(rotulo_x, fontsize=tamanho_rotulos)
            ax.set_ylabel(rotulo_y, fontsize=tamanho_rotulos)

            if tipo == "Barras":
                if idx == 1:
                    bars = ax.bar(df["Nome"], df["Valor"], color=cor_primaria)
                    if mostrar_valores:
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}',
                                    ha='center', va='bottom', fontsize=10)
                else:
                    bars = ax.barh(df["Nome"], df["Valor"], color=cor_primaria)
                    if mostrar_valores:
                        for bar in bars:
                            width = bar.get_width()
                            ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.1f}',
                                    va='center', ha='left', fontsize=10)

            elif tipo == "Linha":
                ax.plot(df["Nome"], df["Valor"], marker="o", markersize=tamanho_marcador,
                        linewidth=espessura_linha, color=cor_primaria,
                        linestyle="solid" if idx == 1 else "dashed")
                if mostrar_valores:
                    for i, val in enumerate(df["Valor"]):
                        ax.text(i, val, f'{val:.1f}', ha='center', va='bottom', fontsize=10)

            elif tipo == "Área":
                ax.fill_between(df["Nome"], df["Valor"], color=cor_primaria, alpha=0.3 if idx == 1 else 0.15)
                ax.plot(df["Nome"], df["Valor"], marker="o", markersize=tamanho_marcador,
                        linewidth=espessura_linha, linestyle="solid" if idx == 1 else "dashed",
                        color=cor_primaria)
                if mostrar_valores:
                    for i, val in enumerate(df["Valor"]):
                        ax.text(i, val, f'{val:.1f}', ha='center', va='bottom', fontsize=10)

            st.subheader(f"Gráfico {idx}")
            st.pyplot(fig)
            baixar_figura(fig, f"grafico_{idx}")


elif opcao == "Fluxograma":
    st.header("Fluxograma")
    
    with st.expander(" Como usar (clique para abrir)"):
        st.markdown("""
        ### 1) Fluxo simples (uma linha)
        Escreva todo o processo numa linha só, conectando os passos com `->`.

        **Exemplo de texto:**
        ```
        Início -> Análise -> Decisão -> Fim
        ```
        **Visualização:**
        """)
        dot_simples = '''
        digraph G {
            rankdir=LR;
            node [style=filled, fillcolor="#0F62FE", shape=box];
            "Início" -> "Análise" -> "Decisão" -> "Fim";
        }
        '''
        st.graphviz_chart(dot_simples, use_container_width=True)

        st.markdown("""
        ---
        ### 2) Fluxo com ramificações (várias linhas)
        Para criar ramificações basta escrever o item que você quer ter uma ramificação e escrever na linha abaixo.

        **Exemplo de texto:**
        ```
        Início -> Análise -> Decisão Favorável -> Fim
        Análise -> Decisão Desfavorável -> Recurso -> Fim
        ```
        **Visualização:**
        """)
        dot_ramificado = '''
        digraph G {
            rankdir=LR;
            node [style=filled, fillcolor="#0F62FE", shape=box];
            "Início" -> "Análise" -> "Decisão Favorável" -> "Fim";
            "Análise" -> "Decisão Desfavorável" -> "Recurso" -> "Fim";
        }
        '''
        st.graphviz_chart(dot_ramificado, use_container_width=True)

        st.markdown("""
        ---
        ### 3) Fluxo com sub-sub-ramificações (níveis mais profundos)
        Você pode ter vários níveis de ramificações, escrevendo todas as possíveis rotas em linhas separadas.

        **Exemplo de texto:**
        ```
        Início -> Análise -> Decisão Favorável -> Arquivar Processo -> Fim
        Análise -> Decisão Desfavorável -> Recurso -> Julgamento do Recurso -> Fim
        ```
        **Visualização:**
        """)
        dot_subramificado = '''
        digraph G {
            rankdir=LR;
            node [style=filled, fillcolor="#0F62FE", shape=box];
            "Início" -> "Análise" -> "Decisão Favorável" -> "Arquivar Processo" -> "Fim";
            "Análise" -> "Decisão Desfavorável" -> "Recurso" -> "Julgamento do Recurso" -> "Fim";
        }
        '''
        st.graphviz_chart(dot_subramificado, use_container_width=True)

    st.header("Digite seus fluxos")

    fluxos_input = st.text_area(
        "Digite cada caminho do seu processo, um por linha, conectando os passos com '->'.\n\n"
        "Exemplo:\n"
        "Início -> Análise do Caso -> Decisão Favorável -> Arquivar Processo -> Fim\n"
        "Análise do Caso -> Decisão Desfavorável -> Recurso -> Julgamento do Recurso -> Fim",
        height=250,
        placeholder="Início -> Análise do Caso -> Decisão Favorável -> Arquivar Processo -> Fim\nAnálise do Caso -> Decisão Desfavorável -> Recurso -> Julgamento do Recurso -> Fim"
    )

    st.header("Personalize (opcional)")

    col1, col2 = st.columns(2)
    with col1:
        cor_nos = st.color_picker("Cor dos passos", "#0F62FE")
    with col2:
        cor_fundo = st.color_picker("Cor de fundo", "#FFFFFF")

    estilo = st.selectbox("Formato dos passos", ["Retângulo", "Elipse", "Losango"], index=0)
    map_forma = {
        "Retângulo": "box",
        "Elipse": "ellipse",
        "Losango": "diamond"
    }

    direcao = st.selectbox("Direção do fluxograma", ["Cima para Baixo", "Esquerda para Direita"], index=1)
    map_direcao = {
        "Cima para Baixo": "TB",
        "Esquerda para Direita": "LR"
    }

    st.header("Visualize")

    if st.button("Gerar Fluxograma"):
        if not fluxos_input.strip():
            st.warning("Por favor, escreva pelo menos um fluxo usando '->' para conectar os passos.")
        else:
            linhas = [linha.strip() for linha in fluxos_input.strip().split("\n") if linha.strip()]
            dot = f'digraph G {{\nrankdir={map_direcao[direcao]};\nnode [style=filled, fillcolor="{cor_nos}", shape={map_forma[estilo]}];\nbgcolor="{cor_fundo}";\n'
            for linha in linhas:
                passos = [p.strip() for p in linha.split("->") if p.strip()]
                for i in range(len(passos) - 1):
                    dot += f'"{passos[i]}" -> "{passos[i+1]}";\n'
            dot += "}"

            st.graphviz_chart(dot)
            st.success("Fluxograma gerado!")

# Nuvem de Palavras
elif opcao == "Nuvem de Palavras":
    st.header("Nuvem de Palavras")

    with st.expander(" Como funciona? (clique para ver)"):
        st.markdown("""
        ###  O que é uma Nuvem de Palavras?
        Uma nuvem de palavras mostra as palavras mais importantes ou frequentes de forma visual.

        ### 🪄 Como usar?
        1. **Adicione suas palavras** (manualmente ou cole um texto).
        2. **Ajuste as cores, formato e estilo** da nuvem.
        3. **Gere a visualização** com um clique.
        4. **Baixe a imagem** para usar onde quiser!

        ###  Como usar pesos (opcional)?
        - Palavras com maior peso ficam **maiores**.
        - Digite no formato: `palavra: peso`
          - Ex: `Justiça: 10`
          - Ex: `Recurso: 5`

        Se você colar um **texto normal**, o app conta automaticamente as palavras!
        """)

    st.header(" Escolha como quer adicionar palavras")

    modo = st.radio("Como deseja inserir as palavras?", ["Texto completo", "Lista com pesos"])

    texto_input = ""
    palavras_pesos = {}

    if modo == "Texto completo":
        texto_input = st.text_area("Cole aqui o texto completo (ex: sentença, petição, parecer etc):", height=200)
    else:
        st.markdown("Digite uma palavra por linha no formato `palavra: peso`. Exemplo:\n\n```\nJustiça: 10\nRecurso: 5\nApelação: 3\n```")
        texto_peso_input = st.text_area("Cole ou escreva sua lista de palavras com pesos:", height=200)
        linhas = texto_peso_input.strip().split("\n")
        for linha in linhas:
            if ":" in linha:
                palavra, peso = linha.split(":", 1)
                palavra = palavra.strip()
                try:
                    peso = int(peso.strip())
                    palavras_pesos[palavra] = peso
                except:
                    continue

    st.header("Personalize a aparência")

    col1, col2 = st.columns(2)

    with col1:
        cor_fundo = st.color_picker("Cor de fundo", "#FFFFFF")
        cor_max = st.color_picker("Cor das palavras", "#0F62FE")
        largura = st.slider("Largura da imagem", 300, 1200, 800)
    with col2:
        altura = st.slider("Altura da imagem", 200, 800, 400)
        fonte_max = st.slider("Tamanho máximo da fonte", 30, 200, 100)
        fonte_min = st.slider("Tamanho mínimo da fonte", 5, 50, 10)

    st.header("Gerar Nuvem de Palavras")

    if st.button("Criar Nuvem"):
        if modo == "Texto completo" and not texto_input.strip():
            st.warning("Por favor, cole algum texto.")
        elif modo == "Lista com pesos" and not palavras_pesos:
            st.warning("Por favor, insira pelo menos uma palavra com peso.")
        else:
            if modo == "Texto completo":
                wc = WordCloud(
                    width=largura,
                    height=altura,
                    background_color=cor_fundo,
                    colormap=None,
                    color_func=lambda *args, **kwargs: cor_max,
                    max_font_size=fonte_max,
                    min_font_size=fonte_min
                ).generate(texto_input)
            else:
                wc = WordCloud(
                    width=largura,
                    height=altura,
                    background_color=cor_fundo,
                    colormap=None,
                    color_func=lambda *args, **kwargs: cor_max,
                    max_font_size=fonte_max,
                    min_font_size=fonte_min
                ).generate_from_frequencies(frequencies=palavras_pesos)

            fig, ax = plt.subplots(figsize=(largura / 100, altura / 100))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight')
            st.download_button(
                label="Baixar Nuvem de Palavras",
                data=buf.getvalue(),
                file_name="nuvem_de_palavras.png",
                mime="image/png"
            )
