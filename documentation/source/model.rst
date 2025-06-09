==================================
System Architecture
==================================

Project Sigma is built upon a sophisticated, two-stage architecture designed to first learn an efficient representation of system behavior and then use that representation for high-sensitivity anomaly detection.

Core Philosophy: From Raw Data to Behavioral Signatures
---------------------------------------------------------

The foundational premise of Sigma is that raw, high-dimensional sensor data can be distilled into a compact, information-rich **behavioral signature**. This signature captures the underlying dynamics and health of the system more effectively than any individual sensor reading. Our entire system is designed to leverage this powerful, compressed representation.

Architectural Components
------------------------

The system is composed of two primary, cascaded models, as illustrated in the diagram below.

.. figure:: /_static/model.svg
   :align: center
   :width: 800px
   :alt: Detailed model architecture of Sigma

**Stage 1: The Signature Extractor**

*   This first component is a pre-trained **LSTM Autoencoder** whose encoder part is used as a universal feature extractor.
*   Its sole purpose is to take a sequence of raw time-series data and transform it into a compact **8-dimensional signature vector (Z)**.
*   This model is trained once on a vast corpus of normal operational data to master the "language" of the system's dynamics, acting as a powerful tool for **Transfer Learning**.

**Stage 2: The Processor Model**

*   This is the core analysis engine, a **CNN-BiLSTM Autoencoder** optimized for performance. It takes the 8D signature from the Signature Extractor as input and performs two simultaneous tasks through its dual-head design:

    *   **Reconstruction Head**: Attempts to reconstruct the input signature. A high **Reconstruction Error** signals that the current system state is inconsistent or statistically unlikely.
    *   **Prediction Head**: Attempts to predict the signature of the *next* time step. A high **Prediction Error** indicates that the system's behavior is deviating from its expected dynamic trajectory.

.. note::
   The detailed layer-by-layer architecture of the final model is provided in the :doc:`Model Implementation Details Appendix <appendix/model_details>`.

**Final Anomaly Score**

The final anomaly score is a weighted combination of the Reconstruction Error and the Prediction Error. This creates a highly robust metric that is sensitive to both static anomalies (unusual states) and dynamic anomalies (unexpected behavior).

.. note::
   A detailed justification for the choice of each model architecture (LSTM, CNN-BiLSTM) and the hyperparameter optimization process is provided in the :doc:`Methodology and Models <methodology>` section.