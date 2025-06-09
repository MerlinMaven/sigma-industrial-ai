=============================
Model Implementation Details
=============================

This section provides the detailed architectures for the final models used in the Sigma pipeline.

Final Signature Extractor (Encoder)
-----------------------------------
The following is the summary for the selected LSTM-based encoder.

.. code-block:: text

    Model: "base_encoder"
    _________________________________________________________________
     Layer (type)                Output Shape              Param #   
    =================================================================
     input_1 (InputLayer)        [(None, 20, 3)]           0         
                                                                     
     lstm (LSTM)                 (None, 20, 128)           67584     
                                                                     
     lstm_1 (LSTM)               (None, 8)                 4384      
                                                                     
    =================================================================
    Total params: 71,968
    Trainable params: 71,968
    Non-trainable params: 0
    _________________________________________________________________


Final Processor Model (CNN-BiLSTM Dual-Head)
--------------------------------------------
This is the summary for the final, Optuna-optimized processor model.

.. code-block:: text

    Model: "Final_Optimized_Model"
    __________________________________________________________________________________________________
     Layer (type)                   Output Shape         Param #     Connected to                     
    ==================================================================================================
     signature_input (InputLayer)   [(None, 8)]          0           []                               
                                                                                                        
     reshape (Reshape)              (None, 8, 1)         0           ['signature_input[0][0]']        
                                                                                                        
     conv1d (Conv1D)                (None, 8, 16)        64          ['reshape[0][0]']                
    ... (le reste de votre model.summary()) ...
    