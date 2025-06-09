**============================================**
Data Source: Industrial Process Simulation
**============================================**

.. sidebar:: **Source & Reproducibility**
   
   .. raw:: html
   
      <div style="text-align: justify; text-justify: inter-word; hyphens: auto;">
   
   The core of this project relies on a **controlled and reproducible simulation** of an industrial process, modeled in the professional robotics environment, **RoboDK**.
   
   The original simulation project is publicly available and can be explored here:
   
   🔗 **Official RoboDK Project**: `Mixed Applications with UR10e <https://robodk.com/example/Mixed-Applications-with-UR10e>`_
   
   .. raw:: html
   
      </div>

Overview
--------

.. raw:: html

   <div style="text-align: justify; text-justify: inter-word; hyphens: auto; line-height: 1.6;">

The entire dataset for this project is generated from a **digital twin** of a real-world packaging and palletizing cell. Using a simulation ensures access to high-fidelity, perfectly labeled "normal" operation data, free from the noise and inconsistencies often found in real-world sensor feeds. This provides an ideal baseline for training robust anomaly detection models.

RoboDK allows for the creation of complex robotic cells and the extraction of precise operational data—such as positions, velocities, and accelerations—which are essential for developing predictive maintenance and system health monitoring solutions.

.. raw:: html

   </div>

Simulation Environment
----------------------

The simulated process automates a **depalletizing, bottle filling, and palletizing** workflow.

1.  **Depalletizing**: A UR10e robot arm picks empty boxes and places them onto a conveyor belt.
2.  **Filling**: A second UR10e fills each box with bottles delivered by another conveyor.
3.  **Palletizing**: A third UR10e, mounted on a linear rail, stacks the filled boxes onto a new pallet.

**Simulation Video:**

.. raw:: html

   <div style="text-align: center;">
   <video controls width="100%" style="max-width: 700px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
       <source src="_static/simulation_video.mp4" type="video/mp4">
       Your browser does not support the video tag.
   </video>
   </div>

Key Components
--------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Component
     - Description
   * - **UR10e Robots (x3)**
     - 6-axis collaborative arms handling depalletizing, filling, and palletizing tasks. Known for their precision and flexibility in packaging applications.
   * - **Conveyors (x2)**
     - Transport boxes and bottles, ensuring a continuous material flow throughout the cell.
   * - **Vertical Linear Rail**
     - Provides the palletizing robot with extended vertical reach, enabling the stacking of multiple pallet layers.

Data Collection & Characteristics
---------------------------------

Real-time operational data is recorded for each component and saved in **CSV format**. This dataset exclusively captures **normal operating behavior**, establishing a clean baseline for our anomaly detection models. The primary collected features include:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Data Point
     - Description
   * - **Cartesian Positions**
     - X, Y, Z coordinates for all moving parts.
   * - **Joint Velocities & Accelerations**
     - Kinematic data for each of the 6 robot axes.
   * - **Linear Speeds & Accelerations**
     - Movement data for conveyors and the linear rail.
   * - **Timestamps**
     - High-resolution timestamps to ensure temporal consistency.

**Example Time‑Series Plots:**

.. figure:: /_static/rail_data.png
   :align: center
   :width: 600px
   
   Time-series from the **vertical rail** showing its core operational metrics.

.. figure:: /_static/belt_data.png
   :align: center
   :width: 600px

   Time-series of **conveyor speed** as boxes are transported.

Getting Started: Reproducing the Data
-------------------------------------

This section provides a step-by-step guide to run the simulation and generate the dataset yourself.

**Prerequisites:**

*   ✅ **RoboDK**: [Download here](https://robodk.com/download)
*   ✅ **Python 3.8+** with the libraries listed in `requirements.txt`.

**Local Workflow:**

1.  **Clone the Repository:**
    
    .. code-block:: bash

       git clone https://github.com/MerlinMaven/sigma-industrial-ai.git
       cd sigma-industrial-ai

2.  **Install Dependencies:**

    .. code-block:: bash

       pip install -r requirements.txt

3.  **Run the Simulation:**
    Open the simulation file ``simulations/simulation.rdk`` in the RoboDK application.

4.  **Execute the Collection Notebook:**
    Launch Jupyter and run all cells in ``notebooks/data_collection.ipynb`` to connect to the RoboDK API and generate the CSV data files.

.. tip:: **A Note on Colab and Local Runtimes**

   Google Colab runs in the cloud and **cannot directly connect** to a RoboDK instance running on your local machine. To generate data, you must run the Jupyter Notebook **on the same computer where RoboDK is installed**. This allows the notebook to communicate with the RoboDK API via its local server.

.. raw:: html

   <br>
   <a href="https://colab.research.google.com/github/MerlinMaven/sigma-industrial-ai/blob/main/notebooks/data_collection.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
   <br>