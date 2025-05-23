Introduction
============

Context and Scope
-----------------

The **Sigma** project addresses the challenge of industrial predictive maintenance through the real-time analysis of robotic systems.  
By capturing and learning from the **digital signatures** of robots, linear rails, and conveyors, Sigma anticipates mechanical degradation and helps reduce unplanned downtime.  
It targets engineers, technicians, and operators, providing a lightweight, AI-powered monitoring solution built on **computer vision**, **deep learning**, and **anomaly detection**.

Objectives
----------

Sigma is designed to:

1. Enable **real-time monitoring** of robotic components via digital signature analysis.  
2. Use **deep learning models** to learn and track normal operating behavior.  
3. Detect anomalies early and **predict potential failures** before they occur.  
4. Provide an **interactive dashboard** for visualization, diagnostics, and reporting.

Project Pipeline
----------------

The pipeline translates these objectives into five main phases:

#. **Data Ingestion**  
   - Acquire time series (positions, speeds, loads) via the **RoboDK API**  
   - Export and organize the data in CSV format  

#. **Preprocessing and Feature Engineering**  
   - Normalize signals, apply smoothing and windowing techniques  
   - Construct feature-rich temporal signatures  

#. **Modeling**  
   - Train **autoencoders** to reconstruct signatures and forecast short-term behavior  

#. **Anomaly Assessment**  
   - Detect abnormal patterns using reconstruction and prediction errors  
   - Apply **Isolation Forest** for robust anomaly scoring  

#. **Deployment and Interface**  
   - Integrate the full system into a **Streamlit dashboard** for real-time interaction, threshold tuning, and automatic report generation  

.. image:: documentation/build/html/_static/pipeline.svg
   :width: 100%
   :align: center
   :alt: Sigma Streamlit Pipeline

.. note::
   You can explore the full source code, simulation files, and trained models on GitHub:  
   🔗 `sigma-industrial-ai <https://github.com/MerlinMaven/sigma-industrial-ai.git>`_

Project Structure
-----------------

.. code-block:: text

   Sigma
   ├── files/
   │   ├── simulated_data/
   │   └── simulation.rdk
   └── notebooks/
       └── data_collection.ipynb
