===========================
Methodology and Model Selection
===========================

The final architecture of Project Sigma is the result of a rigorous, multi-stage experimental process designed to identify the most effective components for each part of the pipeline. This section details our methodology.

Our evaluation process followed these key stages:

1. Exploratory Data Analysis (EDA) and Preprocessing
-------------------------------------------------------
The initial phase focused on understanding the raw data and preparing it for modeling.

- **1.1. Statistical Analysis & Visualization**: We began by analyzing the distribution, trends, and seasonality of each time-series feature to understand its baseline characteristics.
- **1.2. Signal Smoothing**: Noise is a common challenge in sensor data. We applied filtering techniques (e.g., moving averages) to smooth the more volatile signals, such as acceleration, to ensure our models learned the underlying patterns rather than the noise.
- **1.3. Dimensionality Estimation with PCA**: To inform the design of our autoencoder's bottleneck, a Principal Component Analysis (PCA) was conducted on the raw data. This helped us estimate the intrinsic dimensionality of the data and set a reasonable target for our signature size.

2. Comparative Study of Autoencoder Architectures
-------------------------------------------------
We benchmarked several autoencoder architectures to select the optimal models for both the initial **Encoder** and the final **Processor**.

- **2.1. Simple Autoencoders**: We evaluated a range of architectures, from simple dense autoencoders to more complex convolutional (CAE) and recurrent (LSTM, BiLSTM) models, to find the best feature extractor. The **LSTM Autoencoder** was selected for its superior ability to capture temporal dynamics in a compact signature.
- **2.2. Dual-Head Autoencoders (Reconstruction + Prediction)**: For the core processor, we implemented dual-output models. The goal was to find an architecture that excelled at both reconstructing the current signature and predicting the next. The **CNN-BiLSTM** model demonstrated the best overall performance on these dual tasks.

3. Validating the Signature-Based Approach
-------------------------------------------
A key hypothesis of this project is that anomaly detection is more effective in the learned signature space than on raw data. To validate this, we conducted a comparative analysis where we trained classical anomaly detection algorithms on both data types. The results confirmed a **significant performance uplift (+10-15%)** when using signatures, thereby validating our approach.

4. Hyperparameter Optimization with Optuna
------------------------------------------
To maximize the performance of our selected `CNN-BiLSTM` architecture, we conducted an extensive hyperparameter search using **Optuna**. We optimized key parameters such as the number of filters, LSTM units, dropout rates, and learning rate over 50 trials. This process led to the discovery of the optimal configuration used in our final model.

5. Final Evaluation and Benchmarking
------------------------------------
The performance of our final, optimized pipeline was rigorously evaluated. We visualized the input data, the reconstructed output, and the predicted output to qualitatively assess its accuracy. Furthermore, we compared its anomaly detection scores against industry-standard methods like **Isolation Forest** and **One-Class SVM** to provide a clear, quantitative benchmark of its superior performance.