===========================
Quick Start Guide: Reproducing the Final Analysis
===========================

This guide provides a step-by-step walkthrough to set up the environment, run the main analysis notebook, and reproduce the key results and visualizations of the Sigma project.

The goal is to execute the pre-trained models on the provided data, not to retrain them from scratch.

Prerequisites
-------------

*   **Git**: For cloning the project repository.
*   **Python 3.8+**
*   **Jupyter Notebook or JupyterLab**: For running the analysis notebook.
*   **Conda or venv**: Recommended for managing dependencies.

Step 1: Clone the Project Repository
------------------------------------
Open your terminal and clone the project from GitHub:

.. code-block:: bash

   git clone https://github.com/MerlinMaven/sigma-industrial-ai.git
   cd sigma-industrial-ai

Step 2: Set Up the Python Environment & Dependencies
----------------------------------------------------
Create a dedicated environment and install all required packages from the `requirements.txt` file.

**Using Conda:**

.. code-block:: bash

   conda create -n sigma_env python=3.9 -y
   conda activate sigma_env
   pip install -r requirements.txt

.. note::
   This step installs all necessary libraries, including `tensorflow`, `pandas`, `scikit-learn`, and `jupyterlab`.

Step 3: Launch Jupyter and Open the Analysis Notebook
------------------------------------------------------
Once the environment is set up, launch JupyterLab:

.. code-block:: bash

   jupyter lab

Navigate to the `notebooks/` directory and open the main analysis file. Let's assume it is named:
``Linear_Rail.ipynb``

Step 4: Run All Cells to Reproduce the Results
------------------------------------------------
The notebook is designed to be executed from top to bottom. It contains all the necessary steps, pre-configured with the correct file paths for the data and pre-trained models.

**To reproduce the analysis, simply click on the menu `Run -> Run All Cells`.**

This action will:

1.  Load the pre-generated time-series data.
2.  Load the pre-trained **Signature Extractor** (`LSTM_AE`) and the **Processor Model** (`CNN_BILSTM_AE`).
3.  Execute the full analysis pipeline, including the benchmark against classical methods.
4.  Generate and display all the final plots and quantitative reports directly within the notebook.

Expected Outcome
----------------

Upon successful execution of all cells, you will see the complete project report generated within the notebook. This includes:

*   The violin plot comparing anomaly scores ("Raw vs. Signatures").
*   The detailed performance metrics (RMSE/MAE).
*   The final conclusions.

This confirms that you have successfully reproduced the key findings of the project using the provided models and data.

Exploring Further
-----------------
With the notebook open, you are now in the project's "cockpit". You can:

*   Inspect the code in each cell to understand the implementation details.
*   Modify parameters and re-run individual cells to conduct your own experiments.
*   Explore the other notebooks in the directory, such as `data_collection.ipynb`, which contains the code used to generate the original data from RoboDK.