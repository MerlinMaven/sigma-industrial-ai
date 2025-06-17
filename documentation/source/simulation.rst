============================================
Data Generation & Simulation Environment
============================================

To develop and rigorously test our anomaly detection system, we required a source of data that was both **realistic and perfectly controlled**. Real-world factory data can be noisy, inconsistent, and often lacks the ground truth needed for robust model validation.

To overcome these challenges, we constructed a comprehensive simulation environment in **RoboDK**. This approach provides a high-fidelity **digital twin** of an industrial workcell, serving as a reliable and reproducible experimental testbed.

The use of a simulated environment offers three critical advantages:

1.  **Data Consistency**: It allows us to generate long, uninterrupted time-series data representing normal operations, free from the gaps, sensor failures, or contextual shifts common in real-world datasets.
2.  **Full Reproducibility**: Our simulation is a self-contained asset. Anyone with a copy of the ``.rdk`` file and our data collection script can regenerate the exact same baseline dataset, ensuring that our entire experimental pipeline is fully reproducible.
3.  **Foundation for Future Work**: This controlled environment is the perfect foundation for future research involving **synthetic anomaly injection**. We can programmatically simulate fault scenarios—such as a stuck joint, increased motor friction, or a sudden mechanical shock—to test the model's sensitivity and response to specific failure modes.


The Simulation Workcell
------------------------

Our simulation models a complete and dynamic industrial workcell designed to perform a cyclical pick-and-place task.

.. figure:: /_static/robodk_simulation_screenshot.png
   :align: center
   :width: 800px
   :alt: Screenshot of the RoboDK Simulation Environment

   *The Sigma Project's simulation environment, featuring a UR10e robot on a linear rail, conveyor systems, and part handling.*

The key components of the cell include:

-   **A UR10e Robotic Arm**: The primary actor, equipped with a gripper zweiten perform precise pick-and-place operations.
-   **A Linear Rail**: This provides the robot with a seventh axis of movement, enabling it to service a larger workspace and increasing the complexity of its motion dynamics.
-   **Two Conveyor Belts**: An inbound conveyor delivers parts (e.g., bottles) to the workcell, while an outbound conveyor removes the final products (e.g., boxes), simulating a realistic production flow.
-   **Programmed Logic**: The entire process is orchestrated through a main program within RoboDK, which calls subroutines for each action (e.g., `Pick`, `Place`, `MoveHome`). This creates a repetitive yet complex behavioral pattern, ideal for our anomaly detection task.


Data Collection Pipeline
------------------------

To interact with this environment, we developed a data collection pipeline in Python using the **RoboDK API**.

.. code-block:: python

   # Snippet from a data collection script
   from robodk import robolink

   RDK = robolink.Robolink()
   robot = RDK.Item('UR10e')
   
   # Loop to collect data at a high frequency
   while True:
       joints = robot.Joints().list()
       # ... calculate speed and acceleration ...
       # ... log data to a CSV file ...
       time.sleep(0.1)


This script automatically identifies all key components in the simulation and logs their full kinematic data—including joint positions, speeds, and accelerations—at a high frequency.

**To get started and reproduce our dataset:**

1.  **Open the Simulation File**: The ``simulation.rdk`` file is available in our GitHub repository. It contains the complete, pre-programmed workcell.
2.  **Run the Collection Script**: Executing our Python data collection script connects to the RoboDK API and automatically generates the same CSV data files used in our analysis.

This streamlined process ensures that our research is transparent, verifiable, and provides a solid foundation for any future work.