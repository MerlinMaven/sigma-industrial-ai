# pages/3_🤖_Ask_Sigma_(Chatbot).py

import streamlit as st
import pandas as pd
import re
import time
import html
from datetime import datetime
from textwrap import dedent
from tensorflow.keras.models import Model, load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import numpy as np
from scipy.signal import savgol_filter

# =============================================================================
# 1. CONFIGURATION DE LA PAGE
# =============================================================================
st.set_page_config(page_title="Sigma Expert Assistant", page_icon="🤖", layout="wide")

# =============================================================================
# 2. CONFIGURATION DES COMPOSANTS ET FONCTIONS UTILES
# =============================================================================
COMPONENT_CONFIG = {
    "Robot 1 (UR10e)": {
        "csv_path": "data/UR10e_1_robot_data.csv",
        "encoder_path": "R_ts/R_ts/Robot_1/Signature/robot_1_LSTMAE_bottleneck8.h5",
        "processor_path": "R_ts/R_ts/Robot_1/M_double_tete/robot_1_dense_32_20250613_212536.h5",
    },
    "Robot 2 (UR10e)": {
        "csv_path": "data/UR10e_2_robot_data.csv",
        "encoder_path": "R_ts/R_ts/Robot_2/Signature/robot_2_LSTMAE_bottleneck8.h5",
        "processor_path": "R_ts/R_ts/Robot_2/M_double_tete/robot_2_dense_32_20250613_154848.h5",
    },
    "Robot 3 (UR10e)": {
        "csv_path": "data/UR10e_3_robot_data.csv",
        "encoder_path": "R_ts/R_ts/Robot_3/Signature/robot_3_LSTMAE_bottleneck8.h5",
        "processor_path": "R_ts/R_ts/Robot_3/M_double_tete/robot_3_dense_32_20250613_155011.h5",
    },
}

FEATURES_FOR_SIGNATURE = [
    'joint_1_pos', 'joint_2_pos', 'joint_3_pos', 'joint_4_pos', 'joint_5_pos', 'joint_6_pos',
    'joint_1_speed', 'joint_2_speed', 'joint_3_speed', 'joint_4_speed', 'joint_5_speed', 'joint_6_speed',
    'acc_lisse_joint_1', 'acc_lisse_joint_2', 'acc_lisse_joint_3', 'acc_lisse_joint_4', 'acc_lisse_joint_5', 'acc_lisse_joint_6',
    'tcp_x', 'tcp_y', 'tcp_z', 'tcp_rx', 'tcp_ry', 'tcp_rz', 'cycle_time'
]
TIME_COLUMN = 'timestamp'
TIME_STEPS = 20
ALERT_THRESHOLD = 0.8

# Fonctions utilitaires pour charger et analyser les données

def load_and_preprocess_data(path):
    try:
        df = pd.read_csv(path)
        df[TIME_COLUMN] = pd.to_datetime(df[TIME_COLUMN])
        for i in range(1, 7):
            input_col, output_col = f'joint_{i}_acc', f'acc_lisse_joint_{i}'
            if output_col not in df.columns and input_col in df.columns:
                df[output_col] = savgol_filter(df[input_col], window_length=51, polyorder=3)
        return df
    except FileNotFoundError:
        st.error(f"Fichier de données non trouvé : {path}. Veuillez vérifier le chemin.")
        return None
    except Exception as e:
        st.error(f"Erreur chargement {path}: {e}")
        return None

def setup_and_generate_all_analytics(_df_full, encoder_path, processor_path):
    try:
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(_df_full[FEATURES_FOR_SIGNATURE])
        sequences = np.array([data_scaled[i:i + TIME_STEPS] for i in range(len(data_scaled) - TIME_STEPS + 1)])
        autoencoder_full = load_model(encoder_path, compile=False)
        encoder_model = Model(inputs=autoencoder_full.input, outputs=autoencoder_full.get_layer('bottleneck').output)
        processor_model = load_model(processor_path, compile=False)
        all_signatures = encoder_model.predict(sequences, batch_size=256, verbose=0)
        pca_reducer = PCA(n_components=1)
        signatures_1d = pca_reducer.fit_transform(all_signatures.reshape(len(all_signatures), -1))
        reconstructed_sigs, predicted_sigs = processor_model.predict(all_signatures, batch_size=256, verbose=0)
        errors_recon = np.mean(np.square(all_signatures - reconstructed_sigs), axis=1)
        errors_pred = np.mean(np.square(all_signatures - predicted_sigs), axis=1)
        final_errors = np.minimum(errors_recon, errors_pred)
        anomaly_scores = np.clip(final_errors / 0.001, 0, 1.0)
        return {"signatures_1d": signatures_1d, "anomaly_scores": anomaly_scores}
    except FileNotFoundError:
        st.error(f"Fichier modèle non trouvé : {encoder_path} ou {processor_path}. Vérifiez les chemins.")
        return None
    except Exception as e:
        st.error(f"Erreur Analyse IA ({encoder_path.split('/')[-1]}): {e}")
        return None

# Initialisation des données et des scores d'anomalie dans le session_state
if "components" not in st.session_state:
    st.session_state.components = list(COMPONENT_CONFIG.keys())
    st.session_state.streams = {}
    st.session_state.alert_threshold = ALERT_THRESHOLD
    for name, config in COMPONENT_CONFIG.items():
        df = load_and_preprocess_data(config["csv_path"])
        if df is not None:
            analytics = setup_and_generate_all_analytics(df, config["encoder_path"], config["processor_path"])
            if analytics is not None:
                history = pd.DataFrame({
                    "timestamp": df[TIME_COLUMN][TIME_STEPS-1:].values,
                    "anomaly_score": analytics["anomaly_scores"].flatten()
                })
                st.session_state.streams[name] = {"history": history}

# =============================================================================
# 3. STYLES CSS
# =============================================================================
def load_css():
    st.markdown("""
    <style>
        body { color: #e6e6e6; }
        .stApp { background-color: #181c24; }
        .expert-header { background: linear-gradient(90deg, #232946, #1a1f2b); color: #e6e6e6; padding: 20px 25px; border-radius: 16px; margin-bottom: 20px; display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); border: 1px solid #232946; }
        .expert-avatar { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(45deg, #3a86ff, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 32px; flex-shrink: 0; box-shadow: 0 4px 12px rgba(58,134,255,0.2); }
        .expert-info h3 { margin: 0; font-size: 22px; font-weight: 700; }
        .expert-info p { margin: 0; font-size: 14px; opacity: 0.8; color: #bfc9d1; }
        .bubble-row { display: flex; margin: 12px 0; max-width: 95%; }
        .bubble-user { justify-content: flex-end; margin-left: auto; }
        .bubble-assistant { justify-content: flex-start; }
        .message-bubble { padding: 15px 20px; border-radius: 22px; word-wrap: break-word; box-shadow: 0 3px 12px rgba(0,0,0,0.15); font-size: 16px; line-height: 1.6; }
        .user-message { background: linear-gradient(135deg, #3a86ff, #00b4d8); color: #ffffff; border-bottom-right-radius: 8px; }
        .assistant-message { background: #232946; color: #e6e6e6; border: 1px solid #2d3454; border-bottom-left-radius: 8px; }
        .chat-message-time { font-size: 11px; opacity: 0.6; margin-top: 8px; text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px; }
        .priority-badge { padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }
        .priority-high { background: #e63946; color: #fff; }
        .priority-medium { background: #f9c74f; color: #232946; }
        .priority-low { background: #43aa8b; color: #fff; }
        .stButton>button { background: #232946; color: #e6e6e6; border: 1px solid #3a86ff; border-radius: 12px; font-weight: 600; padding: 12px 0; transition: all 0.3s ease; }
        .stButton>button:hover { background: #3a86ff; color: #fff; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(58,134,255,0.2); }
        .stChatInput>div>div { background-color: #232946; }
        hr { border-color: #232946; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 4. MOTEUR D'EXPERTISE (CLASSE LOGIQUE)
# =============================================================================
class SigmaExpert:
    def __init__(self):
        self.conversation_count = 0
        self.response_time_avg = 0.0
        self.INTENT_DATA = {
            "status_check": {"keywords": ["statut", "état", "status", "fonctionne", "marche"], "patterns": [r'(statut|état|status) (?:du |de |d\'|)(.+)', r'comment va (.+)']},
            "maintenance": {"keywords": ["maintenance", "réparer", "réparation", "panne", "défaut"], "patterns": [r'quand.*(maintenance|réparer)']},
            "diagnostic": {"keywords": ["diagnostic", "erreur", "anomalie", "problème", "bug"], "patterns": []},
            "optimization": {"keywords": ["optimiser", "améliorer", "performance", "efficacité", "vitesse"], "patterns": []},
            "report": {"keywords": ["rapport", "report", "résumé", "analyse", "statistiques"], "patterns": []},
            "greeting": {"keywords": ["bonjour", "salut", "hello", "bonsoir", "coucou"], "patterns": []},
            "help": {"keywords": ["aide", "help", "comment faire", "que peux-tu"], "patterns": []}
        }
        self.intent_handlers = {
            "status_check": self._handle_status_check, "maintenance": self._handle_maintenance,
            "diagnostic": self._handle_diagnostic, "optimization": self._handle_optimization,
            "report": self._handle_report, "greeting": self._handle_greeting, "help": self._handle_help,
        }
    def _calculate_score(self, query: str, keywords: list, patterns: list) -> int:
        score = sum(2 for keyword in keywords if keyword in query)
        score += sum(5 for pattern in patterns if re.search(pattern, query))
        return score
    def analyze_query(self, user_query: str) -> dict:
        query = user_query.lower().strip()
        if not query: return {"intent": "empty", "confidence": 0}
        intentions = {intent: self._calculate_score(query, data["keywords"], data["patterns"]) for intent, data in self.INTENT_DATA.items()}
        primary_intent = max(intentions, key=intentions.get)
        return {"intent": primary_intent, "confidence": intentions[primary_intent], "query": user_query}
    def generate_response(self, analysis: dict) -> dict:
        start_time = time.time()
        handler = self._generate_clarification_response if analysis["confidence"] < 2 else self.intent_handlers.get(analysis["intent"], self._generate_fallback_response)
        response = handler(analysis["query"])
        response_time = time.time() - start_time
        if self.conversation_count > 0: self.response_time_avg = (self.response_time_avg * (self.conversation_count - 1) + response_time) / self.conversation_count
        else: self.response_time_avg = response_time
        return response
    def _handle_status_check(self, query: str) -> dict:
        match = re.search(r'(statut|état|status) (?:du |de |d\'|)(.+)', query.lower())
        component_name = match.group(2).strip() if match else None
        available_components = st.session_state.get('components', [])
        if not component_name:
            return {"content": dedent(f"🔍 **Vérification de Statut**\n\nDe quel composant souhaitez-vous connaître le statut ?\n\n**Composants disponibles :** `{'`, `'.join(available_components) or 'Aucun'}`"), "priority": "low"}
        found_comp = next((c for c in available_components if component_name in c.lower()), None)
        if not found_comp:
            return {"content": dedent(f"❓ **Composant non trouvé :** `{component_name}`\n\n**Composants disponibles :** `{'`, `'.join(available_components) or 'Aucun'}`"), "priority": "low"}
        stream_state = st.session_state.get('streams', {}).get(found_comp)
        if stream_state is not None and not stream_state['history'].empty:
            history = stream_state['history']
            last_score = history['anomaly_score'].iloc[-1]
            threshold = st.session_state.get('alert_threshold', 0.8)
            status, priority = ("🚨 ALERTE", "high") if last_score > threshold else ("✅ NORMAL", "low")
            return {"content": dedent(f"**📊 Analyse de Statut - {found_comp}**\n\n- **État Actuel :** {status}\n- **Score d'Anomalie :** `{last_score:.4f}`\n- **Seuil d'Alerte :** `{threshold}`\n\n**💡 Recommandation :** {'Intervention immédiate requise.' if priority == 'high' else 'Surveillance continue.'}"), "priority": priority}
        else:
            return {"content": dedent(f"⚠️ **Aucune donnée disponible** pour **{found_comp}**.\n\nVeuillez démarrer le monitoring."), "priority": "medium"}
    def _handle_maintenance(self, query: str) -> dict:
        return {"content": dedent("**🔧 Planification de Maintenance**\n\nJe peux vous aider à optimiser votre maintenance en me basant sur les données en temps réel pour :\n- **Prévoir** les pannes (Maintenance Prédictive).\n- **Planifier** les interventions au moment optimal.\n\n**Voulez-vous que je génère un plan de maintenance pour les composants à risque ?**"), "priority": "medium"}
    def _handle_diagnostic(self, query: str) -> dict:
        return {"content": dedent("**🔍 Lancement d'un Diagnostic**\n\nJe peux lancer un diagnostic complet pour :\n- **Identifier** les causes profondes des anomalies.\n- **Analyser** les logs d'erreurs et les corréler avec les données.\n\n**Souhaitez-vous lancer un diagnostic complet maintenant ?**"), "priority": "medium"}
    def _handle_optimization(self, query: str) -> dict:
        return {"content": dedent("**⚡ Optimisation des Performances**\n\nJe peux analyser les données historiques pour suggérer des améliorations sur :\n- **Les paramètres de fonctionnement** pour améliorer l'efficacité.\n- **Les seuils d'alerte** pour réduire les faux positifs.\n\n**Sur quel aspect souhaitez-vous vous concentrer ?**"), "priority": "medium"}
    def _handle_report(self, query: str) -> dict:
        return {"content": dedent("**📊 Génération de Rapports**\n\nTypes disponibles :\n- **Rapport d'activité** (24h).\n- **Analyse de tendance** (hebdo/mensuel).\n- **Rapport d'incident** (focus sur une anomalie).\n\n**Quel rapport souhaitez-vous et pour quelle période ?**"), "priority": "low"}
    def _handle_greeting(self, query: str) -> dict:
        return {"content": dedent("👋 **Bonjour ! Je suis Sigma, votre expert en monitoring.**\n\nJe suis là pour vous aider à surveiller, diagnostiquer et optimiser vos systèmes.\n\n**Comment puis-je vous assister aujourd'hui ?**"), "priority": "low"}
    def _handle_help(self, query: str) -> dict:
        return {"content": dedent("**❓ Centre d'Aide - Sigma Expert**\n\nExemples de questions :\n- `Quel est le statut du robot principal ?`\n- `Y a-t-il des besoins de maintenance ?`\n- `Génère un rapport pour la semaine dernière.`\n\nUtilisez les boutons ou posez votre question."), "priority": "low"}
    def _generate_clarification_response(self, query: str) -> dict:
        return {"content": dedent(f"🤔 **Je ne suis pas certain de comprendre.** Votre demande : *\"{query}\"*\n\nPourriez-vous reformuler avec des mots comme `statut`, `maintenance`, `diagnostic` ?"), "priority": "low"}
    def _generate_fallback_response(self, query: str) -> dict:
        return {"content": dedent("❓ **Désolé, cela dépasse mes compétences actuelles.**\n\nJe suis spécialisé dans le monitoring, la maintenance et le diagnostic."), "priority": "low"}

# =============================================================================
# 5. FONCTIONS DE L'INTERFACE UTILISATEUR (UI)
# =============================================================================
def render_header():
    st.markdown("""<div class="expert-header"><div class="expert-avatar">🤖</div><div class="expert-info"><h3>Sigma Expert Assistant</h3><p>Votre partenaire pour le monitoring et la maintenance prédictive.</p></div></div>""", unsafe_allow_html=True)

def display_chat_history():
    for message in st.session_state.chat_history:
        role = message["role"]
        timestamp = message.get('timestamp', datetime.now()).strftime('%H:%M')
        if role == "user":
            escaped_content = html.escape(message["content"])
            st.markdown(f"""
            <div class="bubble-row bubble-user">
                <div class="message-bubble user-message">
                    {escaped_content}
                    <div class="chat-message-time">{timestamp}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            content = message["content"].strip()
            priority = message.get("priority", "low")
            priority_html = f'<span class="priority-badge priority-{priority}">{priority}</span>'
            st.markdown(f"""
            <div class="bubble-row bubble-assistant">
                <div class="message-bubble assistant-message">
                    {content}
                    <div class="chat-message-time">
                        <span>{timestamp}</span>
                        {priority_html}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

def handle_user_input(prompt: str):
    st.session_state.chat_history.append({"role": "user", "content": prompt, "timestamp": datetime.now()})
    with st.spinner("🤖 Sigma analyse..."):
        time.sleep(0.5)
        expert = st.session_state.sigma_expert
        analysis = expert.analyze_query(prompt)
        response = expert.generate_response(analysis)
        expert.conversation_count += 1
    st.session_state.chat_history.append({"role": "assistant", "content": response["content"], "priority": response.get("priority", "low"), "timestamp": datetime.now()})
    st.rerun()

# =============================================================================
# 6. INTERFACE PRINCIPALE DE L'APPLICATION
# =============================================================================
load_css()

if "sigma_expert" not in st.session_state:
    st.session_state.sigma_expert = SigmaExpert()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    initial_response = st.session_state.sigma_expert._handle_greeting("")
    st.session_state.chat_history.append({"role": "assistant", **initial_response, "timestamp": datetime.now()})

render_header()
display_chat_history()

st.write("---")
st.subheader("Actions rapides")

cols = st.columns(3)
quick_actions = {
    "📊 Vérifier Statut": "Quel est le statut des composants ?",
    "🔧 Planifier Maintenance": "Comment planifier la maintenance ?",
    "🔍 Lancer Diagnostic": "Lancer un diagnostic système.",
    "⚡ Optimiser Performances": "Comment optimiser les performances ?",
    "📈 Générer Rapport": "Générer un rapport d'activité.",
    "❓ Aide": "J'ai besoin d'aide."
}

action_items = list(quick_actions.items())
for i, col in enumerate(cols):
    for j in range(2):
        action_index = i * 2 + j
        if action_index < len(action_items):
            label, prompt = action_items[action_index]
            if col.button(label, use_container_width=True):
                handle_user_input(prompt)

if prompt := st.chat_input("💬 Posez votre question à Sigma..."):
    handle_user_input(prompt)
