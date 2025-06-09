=======================================================
Introduction to Project Sigma: Intelligent Monitoring of Robotic Systems
=======================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   architecture
   methodology
   results
   deployment

Sigma is an advanced predictive maintenance system designed to ensure the reliability of automated industrial processes. Leveraging cutting-edge artificial intelligence techniques, Sigma learns the normal behavior of robotic systems in order to detect faults and degradation well before they become critical.

Context and Vision
==================

In the Industry 4.0 era, even brief production downtimes can result in significant costs. Traditional predictive maintenance often relies on static rules or sensor thresholds—methods that fail to capture complex system dynamics or early signs of failure.

Project Sigma proposes a paradigm shift. Instead of monitoring isolated sensor values, it builds and analyzes a behavioral digital signature for each machine. This signature is a compact, information-rich representation of a system’s normal operation, capturing subtle interactions between its components.

Our solution is tailored for maintenance engineers, production managers, and data scientists, offering them a smart, lightweight, and interpretable tool for industrial asset health monitoring.

Technical and Strategic Objectives
==================================

Sigma is designed to meet the following key goals:

- **Deep Representation Learning**: Design and train deep learning models (LSTM autoencoders, CNNs) to extract meaningful behavioral signatures from raw time-series data.

- **Multi-Faceted Anomaly Detection**: Build a robust detection system based on both reconstruction error (current state consistency) and prediction error (future state anticipation) for earlier failure detection.

- **Systematic Benchmarking**: Evaluate the performance of our signature-based approach against traditional anomaly detection algorithms (e.g., Isolation Forest, One-Class SVM) to quantify its added value.

- **Intuitive Human-Machine Interface**: Deploy the solution via an interactive Streamlit dashboard for real-time monitoring, assisted diagnostics, and automated reporting.

Pipeline Architecture
=====================

Our pipeline transforms raw data into actionable insights through the following structured stages:

.. image:: _static/pipeline.svg
   :width: 100%
   :align: center
   :alt: Sigma Pipeline Architecture

**1. Data Ingestion and Simulation**:

- Time-series data (positions, speeds, accelerations) is generated and collected through RoboDK simulation to ensure realistic and controlled datasets.

**2. Preprocessing and Windowing**:

- Signals are normalized and smoothed to remove irrelevant noise. A sliding window technique is applied to create temporal sequences.

**3. Signature Extraction (Transfer Learning)**:

- A pre-trained LSTM encoder is used as a feature extractor. It compresses each high-dimensional sequence into a compact 8D signature that captures its temporal dynamics — the core of our transfer learning strategy.

**4. Modeling and Anomaly Analysis**:

- A dual-head CNN+BiLSTM processor is trained on these signatures to simultaneously reconstruct and predict the system behavior one step ahead.

- An anomaly score is computed by combining the reconstruction and prediction errors, providing a robust health metric.

**5. Deployment and Visualization**:

- The entire system is integrated into a Streamlit dashboard, providing a user-friendly interface for real-time monitoring, alert analysis, and threshold tuning.

.. note::

   The entire project — including source code, RoboDK simulations, pre-trained models, and experimentation notebooks — is available on our GitHub repository.

🔗 Check out the project on GitHub: `sigma-industrial-ai <https://github.com/MerlinMaven/sigma-industrial-ai.git>`_

Project Structure
=================

The following tree illustrates the structure of the Sigma project repository. It includes multiple simulation files, trained models, and time series data files.

.. code-block:: text

   sigma-industrial-ai/
   ├── data/
   │   ├── simulated_data/
   │   │   ├── Linear_Rail_rail_data.csv
   │   │   └── ... (additional simulated CSV files)
   │   └── simulations/
   │       ├── simulation.rdk
   │       └── ... (additional RoboDK simulation files)
   ├── models/
   │   ├── saved_models/
   │   │   ├── LSTM_AE_bottleneck_8.h5
   │   │   └── ... (other single-output models)
   │   └── saved_dual_output_models/
   │       ├── CNN_BILSTM_AE_v1.h5
   │       └── ... (other dual-output architectures)
   ├── notebooks/
   │   ├── data_collection.ipynb
   │   ├── Linear_Rail.ipynb
   │   └── ... (additional experiments and evaluation notebooks)
   ├── src/
   │   ├── pipeline.py
   │   └── dashboard.py
   ├── requirements.txt
   └── README.md
