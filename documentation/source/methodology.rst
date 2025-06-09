===========================
Methodology & Model Selection
===========================

The final architecture of Project Sigma is not a default choice but the outcome of a **rigorous, multi-stage experimental process**. This process was designed to scientifically validate our core hypotheses and identify the most effective components for each stage of the pipeline.

Our evaluation methodology followed these key phases:

1. Exploratory Data Analysis (EDA) and Preprocessing
-------------------------------------------------------
This initial phase focused on understanding the raw data's characteristics to inform our modeling strategy.

- **Statistical Analysis & Visualization**: We analyzed the distribution, trends, and seasonality of each time-series feature to establish a baseline understanding.
- **Signal Smoothing**: To ensure our models learned meaningful patterns instead of sensor noise, we applied filtering techniques (e.g., moving averages) to the more volatile signals, such as acceleration.
- **Dimensionality Estimation with PCA**: A Principal Component Analysis (PCA) was conducted on the raw data to estimate its intrinsic dimensionality. This analysis guided the design of our autoencoder's bottleneck, helping us set a reasonable target for our signature's size.

2. Comparative Benchmarking of Autoencoder Architectures
---------------------------------------------------------
To select the optimal models, we benchmarked a wide range of autoencoder architectures.

- **Feature Extractor Selection**:
  We evaluated several architectures (Dense, CAE, LSTM, BiLSTM) based on their ability to create a compact and informative signature. The primary metric was the final reconstruction error versus the bottleneck size.

  .. figure:: /_static/pareto_plot_bottleneck_selection.png
     :align: center
     :width: 600px
     :alt: Pareto Analysis for Bottleneck Selection

  As shown in the Pareto analysis, the **LSTM Autoencoder with an 8-dimensional bottleneck** provided the best trade-off between a low reconstruction error and a highly compact signature. It was therefore selected as our Signature Extractor.

- **Processor Model Selection**:
  For the core processor, we implemented and compared several dual-head models. The **CNN-BiLSTM** architecture demonstrated the best overall performance in simultaneously minimizing both reconstruction and prediction errors on the signature space.

3. Hyperparameter Optimization with Optuna
------------------------------------------
To maximize the performance of our selected `CNN-BiLSTM` processor, we conducted an extensive hyperparameter search using **Optuna**.

.. figure:: /_static/optuna_optimization_history.png
   :align: center
   :width: 500px
   :alt: Optuna Optimization History

The 50-trial optimization successfully converged towards a superior set of parameters, **reducing the final prediction loss by over 30%** compared to our initial baseline configuration. This data-driven tuning was critical to achieving state-of-the-art performance.

4. Final Validation & Benchmarking
------------------------------------
With our optimized model finalized, we conducted a final validation to prove two key points:
a) The superiority of operating on learned signatures over raw data.
b) The state-of-the-art performance of our final model compared to industry-standard algorithms.

To do this, we compared three types of models:
- Classical algorithms (Isolation Forest, One-Class SVM) on **raw, high-dimensional data**.
- The same classical algorithms on our **learned, low-dimensional signatures**.
- Our final, optimized **CNN-BiLSTM AE** on the signatures.

.. figure:: /_static/final_benchmark_violin_plot.png
   :align: center
   :width: 800px
   :alt: Anomaly Score Distribution Benchmark: Raw Data vs. Signatures vs. Final Model

The results are unequivocal. Firstly, models trained on signatures showed a **significant performance uplift of 10-15%** over those trained on raw data, validating our core hypothesis. Secondly, our final **CNN-BiLSTM AE** provides the sharpest and most reliable separation between normal and anomalous behavior, confirming its superior performance for this task.

.. note::

   The detailed, layer-by-layer architecture of the final, optimized models is provided in the :doc:`Model Implementation Details Appendix <appendix/model_details>`. 
   
   Furthermore, the full code for all experiments described above—from benchmarking to optimization—is available in our `Jupyter Notebooks on GitHub <lien_vers_notebook>`.

The complete quantitative and qualitative performance analysis of this final pipeline is presented in the next section, **Results Analysis**.