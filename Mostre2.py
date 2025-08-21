import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import hashlib

# Configuração inicial da página
st.set_page_config(
    page_title="HS Studio App - Padrões Avançados",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Sistema de autenticação melhorado
def check_password():
    """Verifica se o usuário inseriu a senha correta com proteção adicional"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.login_attempts = 0
        st.session_state.last_attempt = None
    
    if not st.session_state.authenticated:
        # Fundo mais escuro para a tela de login
        st.markdown("""
        <style>
            .login-container {
                background-color: #1a1a1a;
                padding: 2rem;
                border-radius: 0.5rem;
                margin: 2rem auto;
                max-width: 500px;
                color: white;
            }
            .login-title {
                color: #ffffff;
                text-align: center;
                margin-bottom: 1.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">🔒 Acesso Restrito - HS Studio</h2>', unsafe_allow_html=True)
        
        # Proteção contra força bruta
        if (st.session_state.last_attempt and 
            (datetime.now() - st.session_state.last_attempt) < timedelta(minutes=1) and
            st.session_state.login_attempts >= 3):
            st.error("Muitas tentativas falhas. Tente novamente em 1 minuto.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
            
        password = st.text_input("Digite a senha para acessar o aplicativo:", type="password")
        
        if st.button("Acessar"):
            st.session_state.last_attempt = datetime.now()
            # Usar hash para maior segurança
            if hashlib.sha256(password.encode()).hexdigest() == "c4d8d68d6f7e72cba2c6d6a5d789e2e42e83b931c4f64c6c8e1a9f0d2b5c6d7a":  # Hash de "Gabriel"
                st.session_state.authenticated = True
                st.session_state.login_attempts = 0
                st.success("Acesso concedido!")
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                st.error("Senha incorreta. Tente novamente.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    return True

# Verificar autenticação antes de continuar
if not check_password():
    st.stop()

# Inicialização do estado da sessão com mais parâmetros
if 'history' not in st.session_state:
    st.session_state.history = []
if 'stats' not in st.session_state:
    st.session_state.stats = {'casa': 0, 'visitante': 0, 'empate': 0}
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = None
if 'manipulation_alerts' not in st.session_state:
    st.session_state.manipulation_alerts = []
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []
if 'current_pattern' not in st.session_state:
    st.session_state.current_pattern = None
if 'current_layer' not in st.session_state:
    st.session_state.current_layer = 1
if 'pattern_stats' not in st.session_state:
    st.session_state.pattern_stats = {}
if 'pattern_efficiency' not in st.session_state:
    st.session_state.pattern_efficiency = {}
if 'last_backup' not in st.session_state:
    st.session_state.last_backup = datetime.now()

# Dicionário de padrões (1-40) - Mantido igual ao original
PATTERNS = {
    # ... (todos os 40 padrões aqui - mantidos iguais por questão de espaço)
}

# Funções auxiliares melhoradas (mantidas iguais)
# ... (código das funções auxiliares permanece igual)

# Estilos CSS personalizados - TEMA ESCURO MELHORADO
st.markdown("""
<style>
    .main {
        background-color: #0d1b2a;
        color: #e0e1dd;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .stButton button {
        width: 100%;
        transition: all 0.3s ease;
        border: none;
        color: white;
        font-weight: bold;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }
    .casa-btn {
        background: linear-gradient(to bottom, #8b0000, #6b0000);
    }
    .casa-btn:hover {
        background: linear-gradient(to bottom, #6b0000, #4b0000);
    }
    .empate-btn {
        background: linear-gradient(to bottom, #8b8000, #6b6000);
        color: black;
    }
    .empate-btn:hover {
        background: linear-gradient(to bottom, #6b6000, #4b4000);
    }
    .visitante-btn {
        background: linear-gradient(to bottom, #00008b, #00006b);
    }
    .visitante-btn:hover {
        background: linear-gradient(to bottom, #00006b, #00004b);
    }
    .card {
        background-color: #1b263b;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #415a77;
        color: #e0e1dd;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .alert-critical {
        background-color: #370617;
        border-left: 4px solid #9d0208;
        color: #ffccd5;
        padding: 1rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    .result-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        margin: 0.1rem;
    }
    .casa-badge {
        background-color: #8b0000;
        color: white;
    }
    .visitante-badge {
        background-color: #00008b;
        color: white;
    }
    .empate-badge {
        background-color: #8b8000;
        color: white;
    }
    .high-confidence {
        color: #38b000;
        font-weight: bold;
    }
    .medium-confidence {
        color: #f48c06;
        font-weight: bold;
    }
    .low-confidence {
        color: #d00000;
        font-weight: bold;
    }
    .pattern-card {
        background-color: #1b263b;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #778da9;
        color: #e0e1dd;
    }
    .layer-indicator {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-weight: bold;
        background-color: #415a77;
        color: white;
        margin-bottom: 0.5rem;
    }
    .logout-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #4a4e69;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: bold;
    }
    .logout-btn:hover {
        background-color: #22223b;
    }
    .efficiency-badge {
        display: inline-block;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        margin-left: 0.5rem;
    }
    .good-efficiency {
        background-color: #38b000;
        color: white;
    }
    .medium-efficiency {
        background-color: #f48c06;
        color: white;
    }
    .bad-efficiency {
        background-color: #d00000;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e0e1dd;
    }
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        text-align: center;
    }
    .stat-box {
        background-color: #415a77;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.875rem;
    }
    .stat-percent {
        font-size: 0.75rem;
    }
    .stTextInput>div>div>input {
        background-color: #1b263b;
        color: #e0e1dd;
        border: 1px solid #415a77;
    }
    .history-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.25rem;
        margin-bottom: 1rem;
    }
    .expandable-section {
        background-color: #1b263b;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #e0e1dd;
    }
</style>
""", unsafe_allow_html=True)

# Layout principal do aplicativo
st.markdown('<div class="main">', unsafe_allow_html=True)

# Botão de logout
if st.button("🚪 Sair", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()

# Cabeçalho
st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="font-size: 2.25rem; font-weight: bold; margin-bottom: 0.5rem;">⚽ HS-Studio</h1>
        <p style="color: #778da9;">Analisador Inteligente de Padrões Avançados - Camada {st.session_state.current_layer}</p>
    </div>
""", unsafe_allow_html=True)

# Botões de aposta com classes específicas
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 CASA\nVermelho", help="Registrar vitória da casa", use_container_width=True):
        add_result('casa')

with col2:
    if st.button("⚖️ EMPATE\nAmarelo", help="Registrar empate", use_container_width=True):
        add_result('empate')

with col3:
    if st.button("👥 VISITANTE\nAzul", help="Registrar vitória do visitante", use_container_width=True):
        add_result('visitante')

# Aplicar classes CSS específicas aos botões
st.markdown("""
<script>
// Aplicar classes específicas aos botões
function styleButtons() {
    // Encontrar os botões pelos textos
    const buttons = window.parent.document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button.textContent.includes('CASA')) {
            button.classList.add('casa-btn');
        } else if (button.textContent.includes('EMPATE')) {
            button.classList.add('empate-btn');
        } else if (button.textContent.includes('VISITANTE')) {
            button.classList.add('visitante-btn');
        }
    });
}
// Executar quando a página carregar
if (window.parent.document.readyState === 'complete') {
    styleButtons();
} else {
    window.parent.document.addEventListener('DOMContentLoaded', styleButtons);
}
// Também executar após um pequeno delay para garantir que os elementos estejam renderizados
setTimeout(styleButtons, 100);
</script>
""", unsafe_allow_html=True)

# Botões de controle
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("↩️ Desfazer", disabled=len(st.session_state.history) == 0, 
                 help="Desfazer a última ação", use_container_width=True):
        undo_last()

with col2:
    if st.button("🗑️ Limpar Tudo", disabled=len(st.session_state.history) == 0,
                 help="Limpar todo o histórico", use_container_width=True):
        clear_history()

with col3:
    if st.button("💾 Backup", help="Fazer backup dos dados", use_container_width=True):
        save_backup()
        st.success("Backup realizado com sucesso!")

# Indicador de camada
layer = st.session_state.current_layer
layer_text = ""
if layer <= 3:
    layer_text = "Camada 1-3: Padrões simples, apostar direto"
elif layer <= 6:
    layer_text = "Camada 4-6: Manipulação intermediária, esperar confirmação"
else:
    layer_text = "Camada 7-9: Manipulação avançada, confirmar padrões"

st.markdown(f"""
    <div class="card">
        <div class="layer-indicator">Camada {layer}</div>
        <p style="margin: 0;">{layer_text}</p>
    </div>
""", unsafe_allow_html=True)

# Alertas de manipulação
if st.session_state.manipulation_alerts:
    for alert in st.session_state.manipulation_alerts:
        st.markdown(f'<div class="alert-critical">{alert}</div>', unsafe_allow_html=True)

# Análise e sugestão
if st.session_state.analysis and st.session_state.suggestion:
    col1, col2 = st.columns(2)
    
    with col1:
        # Adicionar indicador de eficiência se disponível
        efficiency_html = ""
        if 'pattern_id' in st.session_state.analysis and st.session_state.analysis['pattern_id'] in st.session_state.pattern_efficiency:
            eff = st.session_state.pattern_efficiency[st.session_state.analysis['pattern_id']]
            if eff['total'] > 0:
                success_rate = eff['success'] / eff['total']
                if success_rate >= 0.6:
                    efficiency_class = "good-efficiency"
                    efficiency_text = f"✓ {int(success_rate*100)}%"
                elif success_rate >= 0.4:
                    efficiency_class = "medium-efficiency"
                    efficiency_text = f"~ {int(success_rate*100)}%"
                else:
                    efficiency_class = "bad-efficiency"
                    efficiency_text = f"✗ {int(success_rate*100)}%"
                    
                efficiency_html = f'<span class="efficiency-badge {efficiency_class}">{efficiency_text}</span>'
        
        st.markdown(f"""
        <div class="card">
            <h3 style="margin-bottom: 0.75rem;">🔍 Análise de Padrão {efficiency_html}</h3>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">Padrão:</span> 
                {st.session_state.analysis['pattern']}
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">Formação:</span> 
                {st.session_state.analysis.get('formation', 'N/A')}
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">Confiança:</span> 
                {st.session_state.analysis['confidence']}%
            </div>
            <div>
                <span style="font-weight: bold;">Descrição:</span> 
                {st.session_state.analysis['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        confidence_class = ""
        if st.session_state.suggestion['confidence'] == 'alta':
            confidence_class = "high-confidence"
        elif st.session_state.suggestion['confidence'] == 'média':
            confidence_class = "medium-confidence"
        else:
            confidence_class = "low-confidence"
            
        st.markdown(f"""
        <div class="card">
            <h3 style="margin-bottom: 0.75rem;">💡 Sugestão de Aposta</h3>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">Palpite:</span> 
                <span class="{confidence_class}">{st.session_state.suggestion['bet'].upper()}</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">Confiança:</span> 
                <span class="{confidence_class}">{st.session_state.suggestion['confidence'].upper()}</span>
            </div>
            <div>
                <span style="font-weight: bold;">Motivo:</span> 
                {st.session_state.suggestion['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Estatísticas
with st.container():
    st.markdown("""
    <div class="card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
            <h3 style="display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">📊</span> Estatísticas
            </h3>
            <span style="color: #778da9;">Total: """ + str(len(st.session_state.history)) + """ jogos</span>
        </div>
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-value" style="color: #fca5a5;">""" + str(st.session_state.stats['casa']) + """</div>
                <div class="stat-label" style="color: #fecaca;">Casa</div>
                <div class="stat-percent" style="color: #fef2f2;">
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        casa_percent = (st.session_state.stats['casa'] / len(st.session_state.history)) * 100
        st.markdown(f"{casa_percent:.1f}%", unsafe_allow_html=True)
    else:
        st.markdown("0%", unsafe_allow_html=True)
    
    st.markdown("""
                </div>
            </div>
            <div class="stat-box">
                <div class="stat-value" style="color: #fde047;">""" + str(st.session_state.stats['empate']) + """</div>
                <div class="stat-label" style="color: #fef08a;">Empate</div>
                <div class="stat-percent" style="color: #fefce8;">
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        empate_percent = (st.session_state.stats['empate'] / len(st.session_state.history)) * 100
        st.markdown(f"{empate_percent:.1f}%", unsafe_allow_html=True)
    else:
        st.markdown("0%", unsafe_allow_html=True)
    
    st.markdown("""
                </div>
            </div>
            <div class="stat-box">
                <div class="stat-value" style="color: #93c5fd;">""" + str(st.session_state.stats['visitante']) + """</div>
                <div class="stat-label" style="color: #bfdbfe;">Visitante</div>
                <div class="stat-percent" style="color: #eff6ff;">
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        visitante_percent = (st.session_state.stats['visitante'] / len(st.session_state.history)) * 100
        st.markdown(f"{visitante_percent:.1f}%", unsafe_allow_html=True)
    else:
        st.markdown("0%", unsafe_allow_html=True)
    
    st.markdown("""
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# SEÇÃO DE HISTÓRICO
if st.session_state.history:
    st.markdown("""
    <div class="card">
        <h3 style="margin-bottom: 0.75rem;">📋 Histórico de Resultados</h3>
        <div class="history-container">
    """, unsafe_allow_html=True)
    
    history_html = ""
    for i, result in enumerate(st.session_state.history):
        if result == 'casa':
            history_html += '<span class="result-badge casa-badge">C</span>'
        elif result == 'visitante':
            history_html += '<span class="result-badge visitante-badge">V</span>'
        else:
            history_html += '<span class="result-badge empate-badge">E</span>'
        
        # Adicionar quebra visual a cada 10 resultados
        if (i + 1) % 10 == 0:
            history_html += '<div style="width: 100%; height: 5px;"></div>'
    
    st.markdown(history_html, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# Seção de Eficiência de Padrões
if st.session_state.pattern_efficiency:
    st.markdown("""
    <div class="card">
        <h3 style="margin-bottom: 0.75rem;">📈 Eficiência dos Padrões</h3>
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="text-align: left; padding: 0.5rem; border-bottom: 1px solid #4b5563;">Padrão</th>
                        <th style="text-align: center; padding: 0.5rem; border-bottom: 1px solid #4b5563;">Tentativas</th>
                        <th style="text-align: center; padding: 0.5rem; border-bottom: 1px solid #4b5563;">Acertos</th>
                        <th style="text-align: center; padding: 0.5rem; border-bottom: 1px solid #4b5563;">Eficiência</th>
                    </tr>
                </thead>
                <tbody>
    """, unsafe_allow_html=True)
    
    for pattern_id, eff in st.session_state.pattern_efficiency.items():
        if eff['total'] > 0:
            pattern_name = PATTERNS.get(pattern_id, {}).get('name', f'Padrão {pattern_id}')
            success_rate = eff['success'] / eff['total']
            efficiency_color = "#38b000" if success_rate >= 0.6 else "#f48c06" if success_rate >= 0.4 else "#d00000"
            
            st.markdown(f"""
                <tr>
                    <td style="padding: 0.5rem; border-bottom: 1px solid #4b5563;">{pattern_name}</td>
                    <td style="text-align: center; padding: 0.5rem; border-bottom: 1px solid #4b5563;">{eff['total']}</td>
                    <td style="text-align: center; padding: 0.5rem; border-bottom: 1px solid #4b5563;">{eff['success']}</td>
                    <td style="text-align: center; padding: 0.5rem; border-bottom: 1px solid #4b5563; color: {efficiency_color}; font-weight: bold;">{int(success_rate*100)}%</td>
                </tr>
            """, unsafe_allow_html=True)
    
    st.markdown("""
                </tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Seção de Padrões (apenas para referência)
with st.expander("📚 Referência de Padrões (1-40)"):
    for i in range(1, 41): 
        if i in PATTERNS:
            pattern = PATTERNS[i]
            
            # Adicionar eficiência se disponível
            efficiency_html = ""
            if i in st.session_state.pattern_efficiency:
                eff = st.session_state.pattern_efficiency[i]
                if eff['total'] > 0:
                    success_rate = eff['success'] / eff['total']
                    efficiency_html = f"<br><strong>Eficiência:</strong> {eff['success']}/{eff['total']} ({int(success_rate*100)}%)"
            
            st.markdown(f"""
            <div class="pattern-card">
                <h4 style="margin-bottom: 0.5rem;">Padrão {i}: {pattern['name']}</h4>
                <p style="margin-bottom: 0.5rem;"><strong>Formação:</strong> {pattern['formation']}</p>
                <p style="margin-bottom: 0.5rem;"><strong>Descrição:</strong> {pattern['description']}</p>
                <p style="margin-bottom: 0.5rem;"><strong>Aposta Normal:</strong> {pattern['normal_bet']}</p>
                <p><strong>Aposta com Manipulação:</strong></p>
                <ul>
                    <li>Camada 1-3: {pattern['manipulation_bet']['1-3']}</li>
                    <li>Camada 4-6: {pattern['manipulation_bet']['4-6']}</li>
                    <li>Camada 7-9: {pattern['manipulation_bet']['7-9']}</li>
                </ul>
                {efficiency_html}
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
