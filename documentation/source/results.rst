===========================
Results and Performance Analysis
===========================

This section presents the performance of our final, optimized pipeline. To provide a clear and detailed analysis, we focus on a specific case study: the **Vertical Linear Rail**.

The methodology described in the previous section was applied systematically to each component of the industrial cell. The case of the linear rail serves as a representative example of the system's high-fidelity performance.

Case Study: Performance on the Vertical Linear Rail
------------------------------------------------------
.. note::
   This analysis uses the final pipeline: the **LSTM-based Signature Extractor** followed by the **Optuna-optimized CNN-BiLSTM Processor Model**.

**Qualitative Analysis: Reconstruction & Prediction**

The following plots compare the original time-series signal with the outputs of our model's two tasks: reconstructing the current state and predicting the state one step into the future.

*(Insérez ici votre graphique principal de comparaison avec le zoom)*

The model demonstrates high fidelity in both tasks. The reconstructed signal (in red) almost perfectly overlays the original signal. The predicted signal (in blue), while slightly less precise as expected, successfully captures the dynamic trends, proving the model's deep understanding of the system's behavior.

**Quantitative Analysis: Performance Metrics**

To quantify this performance, we calculated the Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE) for both tasks on the denormalized test dataset.

.. rst-class:: table-center

   ::

      =============================================================================
      📊 PERFORMANCE REPORT: VERTICAL LINEAR RAIL (Dénormalisé)
      =============================================================================
      Feature              | Tâche              | MAE (Erreur Moyenne) | RMSE
      -----------------------------------------------------------------------------
      rail_position        | Reconstruction     | 10.0771              | 15.5968
                           | Prédiction (t+1)   | 13.7775              | 25.2882
      -----------------------------------------------------------------------------
      rail_speed           | Reconstruction     | 73.3913              | 132.0795
                           | Prédiction (t+1)   | 87.5624              | 164.0219
      -----------------------------------------------------------------------------
      rail_acceleration    | Reconstruction     | 745.5022             | 1271.2927
                           | Prédiction (t+1)   | 814.0240             | 1365.6223
    
Summary of Models for the Entire Industrial Cell
--------------------------------------------------
Following the same rigorous methodology, a specialized model was derived for each component. The table below summarizes the final selected architectures.

.. list-table::
   :widths: 30 35 35
   :header-rows: 1

   * - Industrial Component
     - Selected Signature Extractor
     - Selected Processor Model
    * - **Vertical Linear Rail**
     - LSTM AE (Bottleneck: 8)
     - CNN AE (Optimized)
   * - **Robot 1 (Depalletizer)**
     - LSTM AE (Bottleneck: 8)
     - Dense AE 
   * - **Robot 2 (Filler)**
     - LSTM AE (Bottleneck: 8)
     - Dense AE 
   * - **Robot 3 (Palletizer Rail)**
     - LSTM AE (Bottleneck: 8)
     - Dense AE 
   * - **Conveyor_Box**
     - 
     - CNN-BiLSTM AE (Optimized)
   * - **Conveyor_Bottle**
     - 
     - CNN-BiLSTM AE (Optimized)

This modular, custom-tailored approach ensures maximum performance for each component while leveraging a consistent and scalable end-to-end pipeline.