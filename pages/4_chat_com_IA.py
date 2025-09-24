# ================================================
# chat_juristas_api.py
# ================================================
# Chatbot didático com Gemini para juristas
# - Interface em Streamlit
# - Opções de ajuste do comportamento da IA
# - Usuário pode inserir a chave da API pela interface
# ================================================

# Instalação (no Colab):
# !pip install streamlit google-generativeai cloudflared

import streamlit as st
import google.generativeai as genai

# =============================================
# INTERFACE DO APP
# =============================================
st.set_page_config(page_title="Chat IA para Juristas", layout="wide")
st.title("⚖️ Chat IA - Demonstração")

st.markdown("Converse com a IA e veja como ajustes simples podem mudar o estilo da resposta.")

# =============================================
# MENU LATERAL: CONFIGURAÇÕES
# =============================================
st.sidebar.header("⚙️ Configurações do Chat")

# Entrada da chave da API
api_key = st.sidebar.text_input(
    "🔑 Chave da API Google Gemini",
    type="password",
    help="Insira sua chave obtida no Google AI Studio (https://aistudio.google.com/)."
)

# Só configura a API se a chave for inserida
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
else:
    st.sidebar.warning("⚠️ Insira sua chave API para ativar o chatbot.")
    model = None

# Instrução inicial (define o papel da IA)
system_prompt = st.sidebar.text_area(
    "📝 Instrução inicial",
    value="Você é um advogado especialista em direito civil. Responda sempre de forma clara e fundamentada.",
    help="Exemplo: 'Você é um professor de direito explicando para iniciantes'."
)

# =============================================
# PARÂMETROS DE GERAÇÃO (com explicações simples)
# =============================================
st.sidebar.subheader("🎛️ Ajustes de Resposta")

temperature = st.sidebar.slider(
    "Temperatura", 0.0, 2.0, 1.0, 0.1,
    help="Baixa = respostas objetivas. Alta = respostas criativas."
)

top_p = st.sidebar.slider(
    "Top-p", 0.0, 1.0, 0.9, 0.05,
    help="Baixa = vocabulário restrito. Alta = mais variedade."
)

top_k = st.sidebar.slider(
    "Top-k", 1, 100, 40, 1,
    help="Quantas opções de palavras a IA avalia. Baixo = seguro. Alto = diverso."
)

max_tokens = st.sidebar.slider(
    "Máx. tokens", 50, 1024, 300, 50,
    help="Define o tamanho máximo da resposta."
)

# Texto explicativo no menu lateral
st.sidebar.markdown("""
---
📌 **Explicações rápidas:**
- **Temperatura** → controla criatividade  
- **Top-p** → restringe ou amplia vocabulário  
- **Top-k** → quantas opções a IA analisa  
- **Máx. tokens** → limite do tamanho da resposta  
- **Instrução inicial** → papel da IA (advogado, professor, consultor)  
""")

# =============================================
# ÁREA DE CHAT
# =============================================
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Mostrar histórico de mensagens
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
query = st.chat_input("Digite sua pergunta:")

if query and model:
    # Guardar pergunta
    st.session_state.mensagens.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Montar prompt final
    prompt = f"{system_prompt}\n\nPergunta: {query}"

    # Gerar resposta
    resposta = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_tokens,
        )
    ).text.strip()

    # Mostrar resposta
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)

elif query and not model:
    st.warning("⚠️ Insira sua chave API primeiro para obter respostas.")

