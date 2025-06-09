===========================
Quick Start Guide
===========================

This guide provides a step-by-step walkthrough to set up the environment, run the analysis pipeline, and reproduce the key results of the Sigma project on your local machine.

Prerequisites
-------------

Before you begin, ensure you have the following software installed:

*   **Git**: For cloning the project repository.
*   **Python 3.8+**: The core programming language.
*   **Conda or venv**: Recommended for creating an isolated Python environment.
*   **(Optional) RoboDK**: Only required if you wish to generate new data from the simulation files. The project already includes pre-generated data.

Step 1: Clone the Project Repository
------------------------------------
Open your terminal or command prompt and clone the project from GitHub:

.. code-block:: bash

   git clone https://github.com/MerlinMaven/sigma-industrial-ai.git
   cd sigma-industrial-ai

Step 2: Set Up the Python Environment
-------------------------------------
It is highly recommended to create a dedicated environment to avoid package conflicts.

**Using Conda:**

.. code-block:: bash

   conda create -n sigma_env python=3.9
   conda activate sigma_env

**Using venv:**

.. code-block:: bash
   
   python -m venv sigma_env
   source sigma_env/bin/activate  # On Windows, use: sigma_env\Scripts\activate

Step 3: Install Dependencies
----------------------------
All required Python libraries are listed in the `requirements.txt` file. Install them using pip:

.. code-block:: bash

   pip install -r requirements.txt

.. note::
   This installation includes `tensorflow`, `pandas`, `scikit-learn`, `seaborn`, and all other necessary packages. If you have a compatible NVIDIA GPU, the GPU-enabled version of TensorFlow will be used automatically.

Step 4: Verify Project Structure and Models
-------------------------------------------
Ensure that the pre-trained models are present in the repository. After cloning, you should have the following structure:

.. code-block:: text

   sigma-industrial-ai/
   ├── models/
   │   ├── saved_models/
   │   │   └── LSTM_AE_bottleneck_8.h5
   │   └── saved_dual_output_models/
   │       └── .../CNN_BILSTM_AE_complete.h5
   ├── data/
   │   └── .../Linear_Rail_rail_data.csv
   └── src/
       └── analysis_pipeline.py  (or your main script)

If the models are missing, you may need to download them from a release page or retrain them using the provided notebooks.

Step 5: Run the Main Analysis Pipeline
---------------------------------------
The core logic of the project is encapsulated in a single script. Execute it from the root of the project directory:

.. code-block:: bash

   python src/analysis_pipeline.py

This script will perform the entire end-to-end process:
1.  Load the pre-generated data.
2.  Load the pre-trained models.
3.  Run the anomaly detection benchmark ("Raw vs. Signatures").
4.  Generate and display the final analysis plots and metrics.
5.  Save a log file (`anomaly_detection_pipeline.log`) with the execution details.

Expected Outcome
----------------

Upon successful execution, you should see the final analysis plots (the violin plot comparing anomaly scores) displayed on your screen, and a quantitative report printed in your console. This will confirm that you have successfully reproduced the main results of the project.

Next Steps
----------
With the environment set up, you can now explore the project in more detail:

-   To understand the **project's goals and architecture**, please refer to the :doc:`Introduction` and :doc:`Architecture` sections.
-   To delve into the **experimental process and model selection**, see the :doc:`Methodology and Models` page.
-   To **generate new data using RoboDK**, open the `simulations/simulation.rdk` file and run the `notebooks/data_collection.ipynb` notebook.