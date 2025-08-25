import streamlit as st
import time
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Sistema de Análise Preditiva - Football Studio", layout="wide")

# Inicialização do estado
if 'history' not in st.session_state:
    st.session_state.history = []
if 'analysis' not in st.session_state:
    st.session_state.analysis = {
        'patterns': [],
        'riskLevel': 'low',
        'manipulation': 'none',
        'prediction': None,
        'confidence': 0,
        'recommendation': 'watch',
        'strategy_suggestion': 'Aguardando dados...'
    }

# Mapeamento para emoji e nome
emoji_map = {'C': '🔴', 'V': '🔵', 'E': '🟡'}
name_map = {'C': 'Vermelho', 'V': 'Azul', 'E': 'Empate'}

# Função para adicionar resultado
def add_result(result):
    st.session_state.history.append({'result': result, 'timestamp': time.time()})
    analyze_data()

# Reset do histórico
def reset_history():
    st.session_state.history = []
    st.session_state.analysis = {
        'patterns': [],
        'riskLevel': 'low',
        'manipulation': 'none',
        'prediction': None,
        'confidence': 0,
        'recommendation': 'watch',
        'strategy_suggestion': 'Aguardando dados...'
    }

# --- Funções de Detecção de Padrões (Principais e Camuflados) ---

def detect_all_patterns(results):
    detected = []
    
    # 1. Alternância simples (🔴🔵🔴🔵)
    if len(results) >= 4 and results[-1] != results[-2] and results[-2] != results[-3] and results[-3] != results[-4]:
        detected.append({'type': 'Alternância simples', 'description': 'Padrão alternado (🔴🔵) detectado', 'action': 'Esperar quebra para jogar.', 'certainty': 80})

    # 2. Dupla 2x2 (🔴🔴🔵🔵)
    if len(results) >= 4 and results[-4] == results[-3] and results[-2] == results[-1] and results[-4] != results[-2]:
        detected.append({'type': 'Dupla 2x2', 'description': 'Padrão 2x2 (🔴🔴🔵🔵) detectado', 'action': 'Vigiar empate (🟡) ou alternância na próxima jogada.', 'certainty': 90})

    # 3. Trinca (🔴🔴🔴)
    if len(results) >= 3 and results[-3] == results[-2] == results[-1]:
        detected.append({'type': 'Trinca', 'description': f"Sequência de 3x {name_map[results[-1]]}", 'action': 'Entrar contra (apostar na cor oposta) no 4º. Forte quebra.', 'certainty': 85})

    # 4. Espelho curto (🔴🔵🔵🔴)
    if len(results) >= 4 and results[-4] == results[-1] and results[-3] == results[-2] and results[-4] != results[-3]:
        detected.append({'type': 'Espelho curto', 'description': 'Padrão Espelho Curto (🔴🔵🔵🔴) detectado', 'action': 'Cuidado, isca de empate (🟡).', 'certainty': 70})

    # 5. Quebra camuflada (🔴🔴🔵🔴)
    if len(results) >= 4 and results[-4] == results[-3] and results[-2] != results[-1] and results[-3] != results[-2]:
        if results[-1] == results[-2] :
             detected.append({'type': 'Quebra camuflada', 'description': 'Parecia sequência, mas quebrou no meio (🔴🔴🔵🔴)', 'action': 'Seguir o lado que quebrou (🔵).', 'certainty': 65})
        else:
            if len(results) >= 5 and results[-5] == results[-4] and results[-3] == results[-2] and results[-2] != results[-1] and results[-5] != results[-3] and results[-1] == results[-3]:
                detected.append({'type': 'Quebra camuflada', 'description': 'Padrão Quebra Camuflada (🔴🔴🔵🔴) detectado', 'action': 'Seguir o lado que quebrou (🔵).', 'certainty': 75})

    # 6. Escadinha irregular (🔴🔵🔴🔴)
    if len(results) >= 4 and results[-4] != results[-3] and results[-3] != results[-2] and results[-2] == results[-1]:
        detected.append({'type': 'Escadinha irregular', 'description': 'Alternância que virou repetição (🔴🔵🔴🔴)', 'action': 'Seguir o lado que se repetiu.', 'certainty': 70})

    # 7. Duplas consecutivas (🔴🔴🔵🔵🔴🔴)
    if len(results) >= 6 and results[-6] == results[-5] and results[-4] == results[-3] and results[-2] == results[-1] and results[-6] != results[-4]:
        detected.append({'type': 'Duplas consecutivas', 'description': 'Duplas consecutivas (🔴🔴🔵🔵🔴🔴) detectado', 'action': 'Vigiar por empate.', 'certainty': 85})

    # 8. Virada brusca (🔴🔵🔵🔵)
    if len(results) >= 4 and results[-4] != results[-3] and results[-3] == results[-2] == results[-1]:
        detected.append({'type': 'Virada brusca', 'description': 'Alternava, mas virou sequência longa (🔴🔵🔵🔵)', 'action': 'Seguir a sequência.', 'certainty': 90})

    # 9. Empate âncora (🔴🟡🔵)
    if len(results) >= 3 and results[-2] == 'E' and results[-3] != results[-1]:
        detected.append({'type': 'Empate âncora', 'description': 'Empate entre cores diferentes (🔴🟡🔵)', 'action': 'Observar o padrão anterior ao empate.', 'certainty': 80})

    # 10. Alternância longa (🔴🔵🔴🔵🔴🔵)
    if len(results) >= 5:
        is_long_alternating = True
        for i in range(1, 6):
            if results[-i] == results[-(i+1)]:
                is_long_alternating = False
                break
        if is_long_alternating:
            detected.append({'type': 'Alternância longa', 'description': 'Alternância acima de 5x', 'action': 'Entrar com cautela, a quebra está próxima.', 'certainty': 95})

    # --- Padrões Camuflados ---

    # Camuflagem do 2x2 → 3x2 ou 2x3 (🔴🔴🔴🔵🔵 ou 🔴🔴🔵🔵🔵)
    if len(results) >= 5:
        if (results[-5]==results[-4]==results[-3] and results[-2]==results[-1] and results[-3]!=results[-1]) or (results[-5]==results[-4] and results[-3]==results[-2]==results[-1] and results[-4]!=results[-1]):
            detected.append({'type': 'Camuflagem do 2x2', 'description': 'Variação do 2x2 (3x2 ou 2x3)', 'action': 'Vigiar empate ou alternância.', 'certainty': 70})

    # Trinca esticada → 4x ou 5x (🔴🔴🔴🔴)
    if len(results) >= 4 and results[-4]==results[-3]==results[-2]==results[-1]:
        detected.append({'type': 'Trinca esticada', 'description': 'Sequência prolongada (4x ou 5x)', 'action': 'Quebra é iminente, entrar contra com cautela.', 'certainty': 95})

    # Empate como repetidor (🔴🟡🔴)
    if len(results) >= 3 and results[-2] == 'E' and results[-3] == results[-1]:
        detected.append({'type': 'Empate como repetidor', 'description': 'Empate repetiu a cor anterior (🔴🟡🔴)', 'action': 'Seguir o lado repetido.', 'certainty': 85})

    # Empate como quebra oculta (🔴🔴🟡🔵🔵)
    if len(results) >= 5 and results[-5]==results[-4] and results[-3]=='E' and results[-2]==results[-1] and results[-4]!=results[-1]:
        detected.append({'type': 'Empate como quebra oculta', 'description': 'Empate escondeu uma quebra de lado', 'action': 'O padrão mudou, observe a nova sequência.', 'certainty': 80})
    
    # Adicione os outros padrões camuflados aqui seguindo a mesma lógica...

    return detected

# --- Funções de Análise e Sugestão ---
def analyze_data():
    data = st.session_state.history
    if len(data) < 10:
        st.session_state.analysis['strategy_suggestion'] = 'Aguardando mais dados para análise...'
        return

    results = [d['result'] for d in data]
    patterns = detect_all_patterns(results)
    
    # Lógica de Previsão e Sugestão
    prediction_data = {'color': None, 'confidence': 0}
    strategy_text = "Aguardando um padrão claro para sugerir estratégia."
    recommendation_text = 'watch'
    
    if patterns:
        best_pattern = max(patterns, key=lambda p: p['certainty'])
        
        strategy_text = f"**Padrão detectado:** {best_pattern['description']}. **Sua jogada:** {best_pattern['action']}"
        recommendation_text = 'bet'
        
        # Lógica de previsão baseada no melhor padrão
        if best_pattern['type'] == 'Trinca':
            prediction_data['color'] = 'V' if results[-1] == 'C' else 'C'
            prediction_data['confidence'] = best_pattern['certainty']
        elif best_pattern['type'] == 'Virada brusca':
            prediction_data['color'] = results[-1]
            prediction_data['confidence'] = best_pattern['certainty']
        elif best_pattern['type'] == 'Dupla 2x2':
            prediction_data['color'] = results[-1]
            prediction_data['confidence'] = best_pattern['certainty']
        else: # Padrões de alternância e espelho
            prediction_data['color'] = 'V' if results[-1] == 'C' else 'C'
            prediction_data['confidence'] = best_pattern['certainty']
    
    st.session_state.analysis = {
        'patterns': patterns,
        'riskLevel': 'high' if len(results) > 20 and results.count('E')/len(results) > 0.15 else 'low', # Simples para este exemplo
        'manipulation': 'high' if results.count('E')/len(results) > 0.25 else 'low',
        'prediction': prediction_data['color'],
        'confidence': prediction_data['confidence'],
        'recommendation': recommendation_text,
        'strategy_suggestion': strategy_text
    }


# --- Layout Streamlit ---
st.title("🎰 Sistema de Análise Preditiva - Football Studio")
st.markdown("⚠️ **Disclaimer:** Este sistema é para fins de entretenimento e demonstração. Jogos de azar são aleatórios e não podem ser previstos. Aposte com responsabilidade.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Inserir Resultados")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("🔴 Vermelho (C)", on_click=add_result, args=('C',))
    with c2:
        st.button("🔵 Azul (V)", on_click=add_result, args=('V',))
    with c3:
        st.button("🟡 Empate (E)", on_click=add_result, args=('E',))

    st.button("🔄 Resetar Histórico", on_click=reset_history)

    st.subheader("📊 Histórico (Mais recente à esquerda)")
    if st.session_state.history:
        recent_history = st.session_state.history[::-1]
        lines = []
        for i in range(0, len(recent_history), 9):
            row = recent_history[i:i+9]
            emojis = [emoji_map[r['result']] for r in row]
            lines.append(" ".join(emojis))
        for line in lines:
            st.markdown(f"**{line}**")
    else:
        st.info("Nenhum resultado inserido ainda.")

with col2:
    st.subheader("📈 Análise")
    analysis = st.session_state.analysis
    
    st.markdown(f"**Nível de Risco:** <span style='color:{'red' if analysis['riskLevel'] == 'high' else 'green'}; font-weight:bold;'>{analysis['riskLevel'].upper()}</span>", unsafe_allow_html=True)
    st.markdown(f"**Possível Manipulação:** <span style='color:{'red' if analysis['manipulation'] == 'high' else 'green'}; font-weight:bold;'>{analysis['manipulation'].upper()}</span>", unsafe_allow_html=True)

    st.markdown(f"**Previsão:** {emoji_map.get(analysis['prediction'], 'Aguardando...')}")
    st.markdown(f"**Confiança:** {analysis['confidence']}%")
    
    recommendation_color = 'green' if analysis['recommendation'] == 'bet' else 'orange' if analysis['recommendation'] == 'watch' else 'red'
    st.markdown(f"**Recomendação:** <span style='color:{recommendation_color}; font-weight:bold;'>{analysis['recommendation'].upper()}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧠 Sugestão de Estratégia")
    st.info(analysis['strategy_suggestion'])
    
    if analysis['patterns']:
        st.markdown("### Padrões Detectados:")
        for p in sorted(analysis['patterns'], key=lambda x: x['certainty'], reverse=True):
            st.markdown(f"- **{p['type']}**: {p['description']}")
            st.markdown(f"  - _Ação Sugerida:_ {p['action']}")
            st.markdown(f"  - _Nível de Certeza:_ {p['certainty']}%")
