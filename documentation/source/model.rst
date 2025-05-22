Model
==========================================================================================

Sigma is based on the premise that industrial systems exhibit characteristic normal behavioral patterns, referred to as "signatures." By learning these signatures, the model can detect deviations indicative of anomalies or degradation, enabling accurate estimation of the Remaining Useful Life (RUL).

Given that the system operates in an environment where only normal (non-anomalous) data is available, we utilize unsupervised learning techniques. This is because the model is designed to learn the normal operating conditions without the need for labeled anomaly data. By learning the "signature" of normal behavior, the model can effectively identify any deviation from these learned patterns, which signals an anomaly or potential failure.

System Architecture
-------------------

The Sigma-RUL system comprises the following components:

1. **First Encoder**: Encodes raw sensor signals into compressed latent representations termed "signatures."
2. **Isolation Forest**: Applied to the bottleneck representations of the first autoencoder to detect anomalies in real-time.
3. **Second Dual-Head Autoencoder**:

   - **Decoder 1 – Reconstructed Series**: Reconstructs the learned signatures to verify data integrity.
   - **Decoder 2 – Forecasted Series**: Predicts the future behavior of the signatures for early degradation detection.

.. note::
    
    Sigma combines Autoencoders and Isolation Forest for multi-perspective anomaly detection. The Autoencoders detect gradual changes in temporal patterns, while Isolation Forest identifies abrupt outliers in the latent space. This hybrid approach enhances RUL estimation by reducing false positives/negatives and capturing anomalies across different degradation stages.



.. figure:: /_static/model.png
   :align: center
   :width: 800px
   :alt: Robot Joint Position Over Time



Model Selection
---------------

The following LSTM-based autoencoder architectures are implemented and available for use within the Sigma-RUL framework:

+------------------+-------------------------------------------------------------+
| Model            | Description                                                 |
+==================+=============================================================+
| Linear-AE        | Autoencoder with linear layers only                         | 
+------------------+-------------------------------------------------------------+ 
| LSTM-AE          | Autoencoder based on unidirectional LSTM cells              | 
+------------------+-------------------------------------------------------------+
| BiLSTM-AE        | Bidirectional LSTM to capture temporal dependencies         |
+------------------+-------------------------------------------------------------+
| CAE              | Convolutional Autoencoder for extracting local features     |
+------------------+-------------------------------------------------------------+
| ConvBiLSTM-AE    | Combination of CNN and BiLSTM for robust temporal modeling  | 
+------------------+-------------------------------------------------------------+

Benchmarking Methodology
------------------------

Evaluation Procedure
~~~~~~~~~~~~~~~~~~~~

For each architecture:

1. Implemented as the first autoencoder for signature generation.
2. Implemented as the second dual-head autoencoder.
3. Performance evaluated in terms of:

   - Quality of signature reconstruction.
   - Accuracy of future behavior prediction.

Evaluation Metrics
~~~~~~~~~~~~~~~~~~

+-------------------+-------------------------------------------------------------+--------------------------------+
| Metric            | Description                                                 | Application                    |
+===================+=============================================================+================================+
| MSE               | Mean Squared Error                                          | Signature reconstruction       |
+-------------------+-------------------------------------------------------------+--------------------------------+
| MAE               | Mean Absolute Error                                         | Signature reconstruction       |
+-------------------+-------------------------------------------------------------+--------------------------------+
| RMSE              | Root Mean Squared Error                                     | Future behavior prediction     |
+-------------------+-------------------------------------------------------------+--------------------------------+
| MAPE              | Mean Absolute Percentage Error                              | RUL estimation                 |
+-------------------+-------------------------------------------------------------+--------------------------------+
| Inference Time    | Duration of model inference                                 | Real-time applicability        |
+-------------------+-------------------------------------------------------------+--------------------------------+

Experimental Protocol
---------------------

Data Preprocessing
~~~~~~~~~~~~~~~~~~

1. **Normalization**: Apply z-score or min-max normalization based on data distribution.
2. **Segmentation**: Divide time series into fixed-size windows.
3. **Data Augmentation**: Apply identical augmentation techniques across all models.

Hyperparameters
~~~~~~~~~~~~~~~

Optimize the following hyperparameters for each architecture:

- Bottleneck size (latent dimension)
- Number of layers
- Units per layer
- Learning rate
- Activation function

Optimization is performed via cross-validation using grid search or Bayesian optimization.

Results and Analysis
--------------------

Global Comparative Table
~~~~~~~~~~~~~~~~~~~~~~~~

+------------------+--------------------+-----------------+-----------+--------------------+----------------------------+
| Model            | MSE Reconstruction | RMSE Prediction | MAPE RUL  | Training Time      | Inference Time             |
+==================+====================+=================+===========+====================+============================+
| Linear-AE        | [To be completed]  | [To be completed] | [To be completed] | [To be completed] | [To be completed] |
+------------------+--------------------+-----------------+-----------+--------------------+----------------------------+
| LSTM-AE          | [To be completed]  | [To be completed] | [To be completed] | [To be completed] | [To be completed] |
+------------------+--------------------+-----------------+-----------+--------------------+----------------------------+
| BiLSTM-AE        | [To be completed]  | [To be completed] | [To be completed] | [To be completed] | [To be completed] |
+------------------+--------------------+-----------------+-----------+--------------------+----------------------------+
| CAE              | [To be completed]  | [To be completed] | [To be completed] | [To be completed] | [To be completed] |
+------------------+--------------------+-----------------+-----------+--------------------+----------------------------+
| ConvBiLSTM-AE    | [To be completed]  | [To be completed] | [To be completed] | [To be completed] | [To be completed] |
+------------------+--------------------+-----------------+-----------+--------------------+----------------------------+

Detailed Analysis by Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Linear-AE**: [To be completed]
- **LSTM-AE**: [To be completed]
- **BiLSTM-AE**: [To be completed]
- **CAE**: [To be completed]
- **ConvBiLSTM-AE**: [To be completed]


Discussion
----------

Recommendations
---------------

Based on the benchmarking results, we recommend:

1. For signature generation autoencoder: [To be completed]
2. For dual-head autoencoder: [To be completed]
3. Optimal hyperparameter configurations: [To be completed]

Implementation Code
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Example code for implementing the different architectures
   # Will be provided after the experimentation phase
