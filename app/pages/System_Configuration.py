# pages/4_⚙️_System_Configuration.py
import streamlit as st

st.set_page_config(page_title="Configuration", page_icon="⚙️", layout="centered")

st.title("⚙️ System Configuration")
st.markdown("Ajustez les paramètres de détection pour le système de monitoring.")
st.info("⚠️ **Attention :** Modifier ces seuils affectera la sensibilité de la détection d'anomalies pour tous les robots.")

# Initialiser les seuils si non présents
if 'threshold_attention' not in st.session_state:
    st.session_state.threshold_attention = 0.6
if 'threshold_alerte' not in st.session_state:
    st.session_state.threshold_alerte = 0.85

# Sliders pour ajuster les seuils
new_attention_threshold = st.slider(
    "Seuil d'ATTENTION",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.threshold_attention,
    step=0.05,
    help="Score au-delà duquel un robot passe en état 'Attention' (jaune)."
)

new_alert_threshold = st.slider(
    "Seuil d'ALERTE",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.threshold_alerte,
    step=0.05,
    help="Score au-delà duquel une alerte est déclenchée (rouge)."
)

if new_attention_threshold >= new_alert_threshold:
    st.error("Le seuil d'attention doit être inférieur au seuil d'alerte.")
else:
    st.session_state.threshold_attention = new_attention_threshold
    st.session_state.threshold_alerte = new_alert_threshold
    st.success("Seuils mis à jour avec succès !")

st.markdown("---")
st.write("### Paramètres Actuels")
col1, col2 = st.columns(2)
col1.metric("Seuil Attention", f"{st.session_state.threshold_attention:.2f}")
col2.metric("Seuil Alerte", f"{st.session_state.threshold_alerte:.2f}")