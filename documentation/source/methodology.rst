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
We benchmarked a wide range of autoencoder architectures to select the optimal model for both the initial **Signature Extractor** and the final **Processor Model**.

- **Feature Extractor Selection**: We evaluated architectures ranging from simple dense autoencoders to more complex convolutional (CAE) and recurrent (LSTM, BiLSTM) models. The **LSTM Autoencoder** was ultimately selected for its superior ability to capture temporal dynamics within a compact, expressive signature.
- **Processor Model Selection**: For the core analysis engine, we implemented and compared several dual-output models. The goal was to find an architecture that excelled at both reconstructing the current signature and predicting the next. The **CNN-BiLSTM** model demonstrated the best overall performance on these dual tasks.

3. Validating the Signature-Based Approach
-------------------------------------------
A key hypothesis of this project is that anomaly detection is more effective in a learned latent space. To validate this, we trained classical algorithms (Isolation Forest, One-Class SVM) on both raw data and on our learned signatures. The results confirmed a **significant performance uplift (+10-15%)** when using signatures, thereby proving the value of our representation learning strategy.

4. Hyperparameter Optimization with Optuna
------------------------------------------
To maximize the performance of our selected `CNN-BiLSTM` architecture, we conducted an extensive hyperparameter search using **Optuna**. We optimized key parameters such as the number of filters, LSTM units, dropout rates, and learning rate over 50 trials. This data-driven process led to the discovery of the optimal configuration used in our final model.

*A detailed analysis of the optimization process, including importance plots, can be found in our experimentation notebooks.*

5. Final Pipeline Evaluation
----------------------------
The performance of our final, optimized pipeline was rigorously benchmarked. This included qualitative analysis through the visualization of reconstructed and predicted outputs, as well as quantitative comparison against industry-standard methods. The complete findings are presented in the **Results Analysis** section.