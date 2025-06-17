=============================
Model Implementation Details
=============================

This section provides the detailed architectures for the final models used in the Sigma pipeline.

Final Signature Extractor (Encoder)
-----------------------------------
The following is the summary for the selected LSTM-based encoder.

.. code-block:: text

     Model: "Encoder : LSTM_AE_8"
    _____________________________________________________________________________
     Layer (type)                             Output Shape              Param #   
    =============================================================================
     input_layer (InputLayer)              [(None, 20, 3)]                  0         
                                                                     
     lstm (LSTM)                           (None, 20,64)                17,408      
                                                                     
     bottleneck (LSTM)                     (None, 8)                     2,336       

     repeat_vector (RepeatVector)          (None, 20, 8)                     0                                             

     lstm_1 (LSTM)                         (None, 20, 64)               18,688  

     time_distributed (TimeDistributed)    (None, 20, 3)                   195 
    =============================================================================
    Total params: 38,627
    Trainable params: 38,627
    Non-trainable params: 0
    _________________________________________________________________

Final Processor Model (CNN Dual-Head)
--------------------------------------------
This is the summary for the final, Optuna-optimized processor model.

.. code-block:: text

    Model: "Final_Model"
    __________________________________________________________________________________________________
     Layer (type)                   Output Shape         Param #     Connected to                     
    ==================================================================================================
     signature_input (InputLayer)   [(None, 8)]          0           []                               
                                                                                                        
     reshape (Reshape)              (None, 8, 1)         0           ['signature_input[0][0]']        
                                                                                                        
     conv1d (Conv1D)                (None, 8, 16)        64          ['reshape[0][0]']                
                                                                                                    
     conv1d_12 (Conv1D)             (None, 8, 8)         32          ['reshape_9[0][0]']              
                                                                                                  
     max_pooling1d_4 (MaxPooling1D)  (None, 4, 8)        0           ['conv1d_12[0][0]']              
                                                                                                  
     bottleneck (Flatten)           (None, 32)           0           ['max_pooling1d_4[0][0]']        
                                                                                                  
     dense_7 (Dense)                (None, 32)           1056        ['bottleneck[0][0]']             
                                                                                                  
     reshape_10 (Reshape)           (None, 4, 8)         0           ['dense_7[0][0]']                
                                                                                                  
     up_sampling1d_4 (UpSampling1D)  (None, 8, 8)        0           ['reshape_10[0][0]']             
                                                                                                  
     conv1d_13 (Conv1D)             (None, 8, 1)         25          ['up_sampling1d_4[0][0]']        
                                                                                                  
     pred_head_1 (Dense)            (None, 64)           2112        ['bottleneck[0][0]']             
                                                                                                  
     reconstruction_output (Flatten  (None, 8)           0           ['conv1d_13[0][0]']              
 )                                                                                                                                                                                            
     prediction_output (Dense)      (None, 8)            520         ['pred_head_1[0][0]']            
    ==================================================================================================
    Total params: 3,745
    Trainable params: 3,745
    Non-trainable params: 0     