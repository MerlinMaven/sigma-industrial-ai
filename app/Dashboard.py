import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from tensorflow.keras.models import Model, load_model

# --- Configuration de la Page ---
st.set_page_config(page_title="Tableau de Bord Multi-Robots", page_icon="🏭", layout="wide")

# =============================================================================
# 1. CONFIGURATION CENTRALISÉE DES ROBOTS
# =============================================================================
ROBOT_CONFIG = {
    "Robot 1 (UR10e)": {
        "type": "robot",
        "csv_path": "data/UR10e_1_robot_data.csv",
        "encoder_path": "R_ts/R_ts/Robot_1/Signature/robot_1_LSTMAE_bottleneck8.h5",
        "processor_path": "R_ts/R_ts/Robot_1/M_double_tete/robot_1_dense_32_20250613_212536.h5"
    },
    "Robot 2 (UR10e)": {
        "type": "robot",
        "csv_path": "data/UR10e_2_robot_data.csv",
        "encoder_path": "R_ts/R_ts/Robot_2/Signature/robot_2_LSTMAE_bottleneck8.h5",
        "processor_path": "R_ts/R_ts/Robot_2/M_double_tete/robot_2_dense_32_20250613_154848.h5"
    },
    "Robot 3 (UR10e)": {
        "type": "robot",
        "csv_path": "data/UR10e_3_robot_data.csv",
        "encoder_path": "R_ts/R_ts/Robot_3/Signature/robot_3_LSTMAE_bottleneck8.h5",
        "processor_path": "R_ts/R_ts/Robot_3/M_double_tete/robot_3_dense_32_20250613_155011.h5"
    },
    "Linear Rail": {
        "type": "rail",
        "csv_path": "data/Linear_Rail_rail_data.csv",
        "encoder_path": "R_ts/R_ts/Rail_Linéaire/Signature/OPTIMIZED_LSTM_AE_bottleneck_8.h5",
        "processor_path": "R_ts/R_ts/Rail_Linéaire/M_double_tete/Best_DualHead_AE_CNN_AE.h5"
    },
    "Conveyor_Bottle": {
        "type": "conveyor",
        "csv_path": "data/Conveyor_Bottle_conveyor_data.csv",
        "model_path": "R_ts/R_ts/Convoyeru Bottle/BiLSTM_AE_complete.h5"
    },
    "Conveyor_Box": {
        "type": "conveyor",
        "csv_path": "data/Conveyor_Box_conveyor_data.csv",
        "model_path": "R_ts/R_ts/Convoyeur_Box/BiLSTM_AE_complete.h5"
    }
}

FEATURES_TO_PLOT = [
    'joint_1_pos', 'joint_2_pos', 'joint_3_pos', 'joint_4_pos', 'joint_5_pos', 'joint_6_pos',
    'joint_1_speed', 'joint_2_speed', 'joint_3_speed', 'joint_4_speed', 'joint_5_speed', 'joint_6_speed',
    'joint_1_acc', 'joint_2_acc', 'joint_3_acc', 'joint_4_acc', 'joint_5_acc', 'joint_6_acc'
]
FEATURES_FOR_SIGNATURE = [
    'joint_1_pos', 'joint_2_pos', 'joint_3_pos', 'joint_4_pos', 'joint_5_pos', 'joint_6_pos',
    'joint_1_speed', 'joint_2_speed', 'joint_3_speed', 'joint_4_speed', 'joint_5_speed', 'joint_6_speed',
    'acc_lisse_joint_1', 'acc_lisse_joint_2', 'acc_lisse_joint_3', 'acc_lisse_joint_4', 'acc_lisse_joint_5', 'acc_lisse_joint_6',
    'tcp_x', 'tcp_y', 'tcp_z', 'tcp_rx', 'tcp_ry', 'tcp_rz', 'cycle_time'
]
FEATURES_conv = ['conveyor_pos_x', 'conveyor_pos_y', 'conveyor_pos_z']
FEATURES_rail = ['rail_position', 'rail_speed', 'rail_acceleration']

TIME_COLUMN = 'timestamp'
TIME_STEPS = 20
SIMULATION_SPEED = 0.05
ALERT_THRESHOLD = 0.8

# =============================================================================
# 2. FONCTIONS DE CALCUL (MISES EN CACHE)
# =============================================================================
# Note: Les fonctions prennent maintenant les chemins en arguments pour que le cache fonctionne par robot.
@st.cache_data
def load_and_preprocess_data(path):
    try:
        df = pd.read_csv(path)
        df[TIME_COLUMN] = pd.to_datetime(df[TIME_COLUMN])
        with st.spinner(f"Lissage des données d'accélération pour {path}..."):
            for i in range(1, 7):
                input_col, output_col = f'joint_{i}_acc', f'acc_lisse_joint_{i}'
                if output_col not in df.columns and input_col in df.columns:
                    df[output_col] = savgol_filter(df[input_col], window_length=51, polyorder=3)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement de {path}: {e}"); return None

@st.cache_data
def setup_and_generate_all_analytics(_df_full, config):
    try:
        with st.spinner(f"Analyse IA pour {config['csv_path']}..."):
            scaler = MinMaxScaler()

            if config["type"] == "robot":
                features = FEATURES_FOR_SIGNATURE
                encoder_path = config["encoder_path"]
                processor_path = config["processor_path"]

                data_scaled = scaler.fit_transform(_df_full[features])
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

            elif config["type"] == "rail":
                features = FEATURES_rail
                encoder_path = config["encoder_path"]
                processor_path = config["processor_path"]

                data_scaled = scaler.fit_transform(_df_full[features])
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

            elif config["type"] == "conveyor":
                features = FEATURES_conv
                model_path = config["model_path"]

                data_scaled = scaler.fit_transform(_df_full[features])
                sequences = np.array([data_scaled[i:i + TIME_STEPS] for i in range(len(data_scaled) - TIME_STEPS + 1)])

                model = load_model(model_path, compile=False)
                reconstructed = model.predict(sequences, batch_size=256, verbose=0)

                errors = np.mean(np.square(sequences - reconstructed), axis=(1, 2))
                pca_reducer = PCA(n_components=1)
                signatures_1d = pca_reducer.fit_transform(reconstructed.reshape(len(reconstructed), -1))

                anomaly_scores = np.clip(errors / 0.001, 0, 1.0)

                return {"signatures_1d": signatures_1d, "anomaly_scores": anomaly_scores}

    except Exception as e:
        st.error(f"Erreur dans l'analyse de {config['csv_path']}: {e}")
        return None



# =============================================================================
# 3. INTERFACE UTILISATEUR ET GESTION DE L'ÉTAT
# =============================================================================
st.title("🏭 Tableau de Bord de Supervision Multi-Robots")

# Sélecteur de robot dans la barre latérale
selected_robot_name = st.sidebar.selectbox(
    "Veuillez sélectionner un robot :",
    options=list(ROBOT_CONFIG.keys())
)

# Récupérer la configuration du robot choisi
config = ROBOT_CONFIG[selected_robot_name]

# Chargement des données et analyse pour le robot sélectionné
full_df = load_and_preprocess_data(config["csv_path"])
analytics_results = None
if full_df is not None:
    analytics_results = setup_and_generate_all_analytics(full_df, config)

# Fonction pour réinitialiser l'état de la simulation
def reset_simulation_state():
    st.session_state.stop = True
    st.session_state.row_index = 0
    st.session_state.df_history = pd.DataFrame(columns=[TIME_COLUMN] + FEATURES_TO_PLOT)
    st.session_state.df_signature_history = pd.DataFrame(columns=['time', 'signature_1d'])
    st.session_state.df_anomaly_history = pd.DataFrame(columns=['time', 'score'])

# Détecter si l'utilisateur a changé de robot et réinitialiser si c'est le cas
if 'current_robot' not in st.session_state or st.session_state.current_robot != selected_robot_name:
    st.session_state.current_robot = selected_robot_name
    reset_simulation_state()

# Boutons de contrôle dans la barre latérale
st.sidebar.title("Contrôles de la Simulation")
if st.sidebar.button('Démarrer', type="primary", disabled=(analytics_results is None)):
    st.session_state.stop = False
    st.session_state.row_index = 0 # On repart du début
    st.session_state.df_history = pd.DataFrame(columns=[TIME_COLUMN] + FEATURES_TO_PLOT)
    st.session_state.df_signature_history = pd.DataFrame(columns=['time', 'signature_1d'])
    st.session_state.df_anomaly_history = pd.DataFrame(columns=['time', 'score'])

if st.sidebar.button('Arrêter'):
    st.session_state.stop = True
    st.info("La simulation a été arrêtée.")

# Placeholder pour l'affichage dynamique
placeholder = st.empty()

# =============================================================================
# 4. BOUCLE DE SIMULATION ET AFFICHAGE
# =============================================================================
if analytics_results is not None:
    while not st.session_state.get('stop', True):
        current_index = st.session_state.row_index
        if current_index >= len(full_df):
            st.session_state.stop = True
            st.warning("Fin du fichier de données atteinte. Simulation terminée.")
            break

        st.session_state.df_history = pd.concat([st.session_state.df_history, full_df.iloc[[current_index]]], ignore_index=True)
        if current_index >= TIME_STEPS - 1:
            signature_index = current_index - (TIME_STEPS - 1)
            if signature_index < len(analytics_results["signatures_1d"]):
                timestamp = full_df.iloc[current_index][TIME_COLUMN]
                # Signature
                sig_val = analytics_results["signatures_1d"][signature_index][0]
                st.session_state.df_signature_history = pd.concat([st.session_state.df_signature_history, pd.DataFrame({'time': [timestamp], 'signature_1d': [sig_val]})], ignore_index=True)
                # Score d'anomalie
                score_val = analytics_results["anomaly_scores"][signature_index]
                st.session_state.df_anomaly_history = pd.concat([st.session_state.df_anomaly_history, pd.DataFrame({'time': [timestamp], 'score': [score_val]})], ignore_index=True)

        with placeholder.container():
            st.header(f"Analyse en direct pour : {selected_robot_name}")
            
            col_sig, col_score = st.columns(2)
            
            with col_sig:
                st.subheader("Signature Comportementale 1D")
                if not st.session_state.df_signature_history.empty:
                    chart_sig = alt.Chart(st.session_state.df_signature_history).mark_line().encode(x=alt.X('time:T', title='Temps'), y=alt.Y('signature_1d:Q', title='Valeur'), color=alt.value("#1f77b4"))
                    st.altair_chart(chart_sig, use_container_width=True)
            
            with col_score:
                st.subheader("Score d'Anomalie")
                if not st.session_state.df_anomaly_history.empty:
                    score_line = alt.Chart(st.session_state.df_anomaly_history).mark_line(color='crimson').encode(x=alt.X('time:T', title='Temps'), y=alt.Y('score:Q', title="Score", scale=alt.Scale(domain=[0, 1.05])))
                    threshold_rule = alt.Chart(pd.DataFrame({'y': [ALERT_THRESHOLD]})).mark_rule(color='orange', strokeDash=[5,5]).encode(y='y')
                    st.altair_chart(score_line + threshold_rule, use_container_width=True)
            
            st.markdown("---")
            
            with st.expander(f"Cliquer pour voir les détails des capteurs de {selected_robot_name}", expanded=False):
                st.markdown("##### Données Brutes des Capteurs")
                cols = st.columns(3)
                if config["type"] == "robot":
                    features_to_plot = FEATURES_TO_PLOT 
                elif config["type"] == "rail":
                    features_to_plot = FEATURES_rail
                elif config["type"] == "conveyor":
                    features_to_plot = FEATURES_conv
                else:
                    features_to_plot = FEATURES_TO_PLOT   # fallback

                for i, feature in enumerate(features_to_plot):
                    with cols[i % 3]:
                        st.markdown(f"**{feature.replace('_', ' ').title()}**")
                        df_to_plot = st.session_state.df_history[[TIME_COLUMN, feature]].dropna()
                        if not df_to_plot.empty:
                            st.line_chart(df_to_plot.set_index(TIME_COLUMN), height=150)
                        else:
                            st.write("Pas encore de données disponibles")

        st.session_state.row_index += 1
        time.sleep(SIMULATION_SPEED)

else:
    st.error("Impossible de démarrer. Vérifiez les chemins des fichiers et les logs d'erreurs affichés ci-dessus lors du chargement.")

if st.session_state.get('stop', True):
    st.info(f"Prêt à démarrer la simulation pour {selected_robot_name}. Utilisez les contrôles dans la barre latérale.")