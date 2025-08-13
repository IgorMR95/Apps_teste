import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Calculadora Jurídica ", layout="wide")

st.title("Calculadora Jurídica com Memorial de Cálculo")

st.write("""
Calculadoras aprimoradas para cálculos comuns no dia a dia jurídico. Cada operação gera um pequeno memorial de cálculo detalhado para comprovar o raciocínio e facilitar a juntada em processos.
""")

tabs = st.tabs([
    "Correção Monetária",
    "Juros de Mora",
    "Parcelamento de Dívida",
    "Honorários",
    "Multa Contratual",
    "Indenização",
    "Custas Processuais",
    "Reajuste de Pensão",
    "Multa por Atraso de Aluguel",
    "Cláusula Penal Diária",
    "Conversão Percentual",
])

def gerar_excel(df, nome):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Memorial de Cálculo")
    output.seek(0)
    st.download_button(
        label="Baixar Memorial de Cálculo (.xlsx)",
        data=output,
        file_name=f"{nome}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# --------------------------
# Correção Monetária
# --------------------------
with tabs[0]:
    st.header("Correção Monetária")
    valor = st.number_input("Valor original", min_value=0.0, step=0.01, key="cm_valor")
    indice = st.number_input("Índice acumulado (%)", min_value=0.0, step=0.01, key="cm_indice")
    periodo = st.number_input("Período (meses)", min_value=1, step=1, key="cm_periodo")
    if st.button("Calcular", key="cm_btn"):
        valor_corrigido = valor * (1 + indice/100)**periodo
        st.success(f"Valor corrigido: R$ {valor_corrigido:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor Original",
                "Índice (%)",
                "Período (meses)",
                "Fórmula: V*(1+I/100)^P",
                "Valor Corrigido"
            ],
            "Valor": [
                valor,
                indice,
                periodo,
                f"{valor} * (1 + {indice}/100)^{periodo}",
                valor_corrigido
            ]
        })
        gerar_excel(df, "Memorial_Correcao_Monetaria")

# --------------------------
# Juros de Mora
# --------------------------
with tabs[1]:
    st.header("Juros de Mora")
    base = st.number_input("Valor base", min_value=0.0, step=0.01, key="jm_base")
    taxa = st.number_input("Taxa de juros (% ao mês)", min_value=0.0, step=0.01, key="jm_taxa")
    meses = st.number_input("Número de meses", min_value=1, step=1, key="jm_meses")
    if st.button("Calcular", key="jm_btn"):
        juros = base * (taxa/100) * meses
        total = base + juros
        st.success(f"Valor com juros: R$ {total:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Base",
                "Taxa de Juros (%)",
                "Meses",
                "Cálculo: Base * (Taxa/100) * Meses",
                "Juros",
                "Total"
            ],
            "Valor": [
                base,
                taxa,
                meses,
                f"{base} * ({taxa}/100) * {meses}",
                juros,
                total
            ]
        })
        gerar_excel(df, "Memorial_Juros_Mora")

# --------------------------
# Parcelamento de Dívida (com entrada)
# --------------------------
with tabs[2]:
    st.header("Parcelamento de Dívida")
    divida = st.number_input("Valor total da dívida", min_value=0.0, step=0.01, key="pd_divida")
    entrada = st.number_input("Valor de entrada (opcional)", min_value=0.0, step=0.01, key="pd_entrada")
    parcelas = st.number_input("Número de parcelas", min_value=1, step=1, key="pd_parcelas")
    taxa = st.number_input("Juros ao mês (%)", min_value=0.0, step=0.01, key="pd_taxa")
    if st.button("Calcular Parcelamento", key="pd_btn"):
        saldo = divida - entrada
        valor_parcela = (saldo * (1 + taxa/100)**parcelas) / parcelas
        st.success(f"Entrada: R$ {entrada:,.2f} | Valor de cada parcela: R$ {valor_parcela:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor da Dívida",
                "Entrada",
                "Saldo a Parcelar",
                "Taxa de Juros ao Mês (%)",
                "Parcelas",
                "Fórmula: Saldo * (1+Juros/100)^Parcelas / Parcelas",
                "Valor de Cada Parcela"
            ],
            "Valor": [
                divida,
                entrada,
                saldo,
                taxa,
                parcelas,
                f"{saldo} * (1+{taxa}/100)^{parcelas} / {parcelas}",
                valor_parcela
            ]
        })
        gerar_excel(df, "Memorial_Parcelamento")

# --------------------------
# Honorários (percentual ou fixo ou permuta)
# --------------------------
with tabs[3]:
    st.header("Honorários")
    tipo = st.selectbox("Tipo de Honorários", ["Percentual", "Valor Fixo", "Permuta"])
    if tipo == "Percentual":
        base = st.number_input("Valor base da causa/acordo", min_value=0.0, step=0.01, key="h_percentual_base")
        perc = st.number_input("Percentual (%)", min_value=0.0, step=0.01, key="h_percentual_perc")
        if st.button("Calcular Honorários Percentual", key="h_perc_btn"):
            honorarios = base * (perc/100)
            st.success(f"Honorários: R$ {honorarios:,.2f}")
            df = pd.DataFrame({
                "Descrição": ["Valor Base", "Percentual (%)", "Fórmula", "Honorários"],
                "Valor": [base, perc, f"{base} * {perc}/100", honorarios]
            })
            gerar_excel(df, "Memorial_Honorarios_Percentual")
    elif tipo == "Valor Fixo":
        fixo = st.number_input("Valor fixo combinado", min_value=0.0, step=0.01, key="h_fixo")
        if st.button("Calcular Honorários Fixos", key="h_fixo_btn"):
            st.success(f"Honorários fixos: R$ {fixo:,.2f}")
            df = pd.DataFrame({
                "Descrição": ["Honorários Fixos Combinados"],
                "Valor": [fixo]
            })
            gerar_excel(df, "Memorial_Honorarios_Fixos")
    else:
        bens = st.text_area("Descrição dos bens permutados")
        valor_estimado = st.number_input("Valor estimado dos bens", min_value=0.0, step=0.01, key="h_permuta")
        if st.button("Calcular Permuta", key="h_permuta_btn"):
            st.success(f"Bens permutados avaliados em: R$ {valor_estimado:,.2f}")
            df = pd.DataFrame({
                "Descrição": ["Descrição dos Bens", "Valor Estimado"],
                "Valor": [bens, valor_estimado]
            })
            gerar_excel(df, "Memorial_Honorarios_Permuta")

# --------------------------
# E assim por diante para as outras abas...

# --------------------------
# Multa Contratual
# --------------------------
with tabs[4]:
    st.header("Multa Contratual")
    valor_contrato = st.number_input("Valor do Contrato", min_value=0.0, step=0.01, key="mc_contrato")
    multa_percentual = st.number_input("Percentual de Multa (%)", min_value=0.0, step=0.01, key="mc_percentual")
    if st.button("Calcular Multa", key="mc_btn"):
        multa = valor_contrato * (multa_percentual/100)
        st.success(f"Valor da Multa Contratual: R$ {multa:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor do Contrato",
                "Percentual de Multa (%)",
                "Fórmula",
                "Valor da Multa"
            ],
            "Valor": [
                valor_contrato,
                multa_percentual,
                f"{valor_contrato} * ({multa_percentual}/100)",
                multa
            ]
        })
        gerar_excel(df, "Memorial_Multa_Contratual")

# --------------------------
# Indenização
# --------------------------
with tabs[5]:
    st.header("Indenização")
    dano_material = st.number_input("Dano Material (R$)", min_value=0.0, step=0.01, key="ind_material")
    dano_moral = st.number_input("Dano Moral (R$)", min_value=0.0, step=0.01, key="ind_moral")
    outras = st.number_input("Outras Indenizações (R$)", min_value=0.0, step=0.01, key="ind_outras")
    if st.button("Calcular Indenização Total", key="ind_btn"):
        total = dano_material + dano_moral + outras
        st.success(f"Indenização Total: R$ {total:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Dano Material",
                "Dano Moral",
                "Outras Indenizações",
                "Indenização Total"
            ],
            "Valor": [
                dano_material,
                dano_moral,
                outras,
                total
            ]
        })
        gerar_excel(df, "Memorial_Indenizacao")

# --------------------------
# Custas Processuais
# --------------------------
with tabs[6]:
    st.header("Custas Processuais")
    valor_causa = st.number_input("Valor da Causa", min_value=0.0, step=0.01, key="cp_causa")
    percentual_custas = st.number_input("Percentual de Custas (%)", min_value=0.0, step=0.01, key="cp_percentual")
    if st.button("Calcular Custas", key="cp_btn"):
        custas = valor_causa * (percentual_custas/100)
        st.success(f"Custas Processuais: R$ {custas:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor da Causa",
                "Percentual de Custas (%)",
                "Fórmula",
                "Valor das Custas"
            ],
            "Valor": [
                valor_causa,
                percentual_custas,
                f"{valor_causa} * ({percentual_custas}/100)",
                custas
            ]
        })
        gerar_excel(df, "Memorial_Custas")

# --------------------------
# Reajuste de Pensão
# --------------------------
with tabs[7]:
    st.header("Reajuste de Pensão Alimentícia")
    pensao_atual = st.number_input("Valor Atual da Pensão", min_value=0.0, step=0.01, key="rp_atual")
    indice_reajuste = st.number_input("Índice de Reajuste (%)", min_value=0.0, step=0.01, key="rp_indice")
    meses = st.number_input("Meses desde o último reajuste", min_value=1, step=1, key="rp_meses")
    if st.button("Calcular Reajuste", key="rp_btn"):
        nova_pensao = pensao_atual * (1 + indice_reajuste/100)**(meses/12)
        st.success(f"Novo valor da pensão: R$ {nova_pensao:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor Atual",
                "Índice de Reajuste (%) ao ano",
                "Meses desde o último reajuste",
                "Fórmula",
                "Novo Valor da Pensão"
            ],
            "Valor": [
                pensao_atual,
                indice_reajuste,
                meses,
                f"{pensao_atual} * (1 + {indice_reajuste}/100)^({meses}/12)",
                nova_pensao
            ]
        })
        gerar_excel(df, "Memorial_Reajuste_Pensao")

# --------------------------
# Multa por Atraso de Aluguel
# --------------------------
with tabs[8]:
    st.header("Multa por Atraso de Aluguel")
    aluguel = st.number_input("Valor do Aluguel", min_value=0.0, step=0.01, key="ma_aluguel")
    multa_aluguel = st.number_input("Percentual de Multa por Atraso (%)", min_value=0.0, step=0.01, key="ma_percentual")
    dias_atraso = st.number_input("Dias de Atraso", min_value=0, step=1, key="ma_dias")
    if st.button("Calcular Multa por Atraso", key="ma_btn"):
        multa_total = aluguel * (multa_aluguel/100) * (dias_atraso/30)
        st.success(f"Multa por atraso: R$ {multa_total:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor do Aluguel",
                "Percentual de Multa por Atraso (%)",
                "Dias de Atraso",
                "Fórmula",
                "Multa Total"
            ],
            "Valor": [
                aluguel,
                multa_aluguel,
                dias_atraso,
                f"{aluguel} * ({multa_aluguel}/100) * ({dias_atraso}/30)",
                multa_total
            ]
        })
        gerar_excel(df, "Memorial_Multa_Atraso_Aluguel")

# --------------------------
# Cláusula Penal Diária
# --------------------------
with tabs[9]:
    st.header("⏱Cláusula Penal Diária")
    valor_diaria = st.number_input("Valor Diário da Multa", min_value=0.0, step=0.01, key="cpd_valor")
    dias_descumprimento = st.number_input("Dias de Descumprimento", min_value=0, step=1, key="cpd_dias")
    if st.button("Calcular Cláusula Penal", key="cpd_btn"):
        penal_total = valor_diaria * dias_descumprimento
        st.success(f"Valor da Cláusula Penal: R$ {penal_total:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor Diário da Multa",
                "Dias de Descumprimento",
                "Fórmula",
                "Valor Total da Cláusula Penal"
            ],
            "Valor": [
                valor_diaria,
                dias_descumprimento,
                f"{valor_diaria} * {dias_descumprimento}",
                penal_total
            ]
        })
        gerar_excel(df, "Memorial_Clausula_Penal")

# --------------------------
# Conversão Percentual
# --------------------------
with tabs[10]:
    st.header("Conversão Percentual")
    valor_base = st.number_input("Valor Base", min_value=0.0, step=0.01, key="cp_base")
    percentual = st.number_input("Percentual (%)", min_value=0.0, step=0.01, key="cp_percentual2")
    if st.button("Converter", key="cp_btn2"):
        resultado = valor_base * (percentual/100)
        st.success(f"Resultado: R$ {resultado:,.2f}")
        df = pd.DataFrame({
            "Descrição": [
                "Valor Base",
                "Percentual (%)",
                "Fórmula",
                "Resultado"
            ],
            "Valor": [
                valor_base,
                percentual,
                f"{valor_base} * ({percentual}/100)",
                resultado
            ]
        })
        gerar_excel(df, "Memorial_Conversao_Percentual")
