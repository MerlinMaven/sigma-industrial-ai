============================================
Guide: Reproducing the Simulation Environment
============================================

This guide provides a detailed, step-by-step walkthrough for recreating the **Sigma Project's simulation environment** from scratch in RoboDK. Following these instructions will allow you to build the digital twin used for our data generation and experiments.

**Prerequisites:**

*   A working installation of **RoboDK**.
*   Basic familiarity with the RoboDK interface (navigating the tree, adding items, etc.).

Step 1: Assembling the Workcell Components
---------------------------------------------

The first step is to populate the simulation (known as a "station") with all the necessary components from RoboDK's extensive online library.

1.  **Open the Online Library**: In RoboDK, click the **"Open online library"** icon (a globe 🌐 in the main toolbar).

2.  **Download Assets**: Use the search bar in the library to find and download the following items. Each will be automatically added to your station.
    
    -   **Robot**: ``Universal Robots UR10e``
    -   **Linear Rail**: Search for a compatible rail. Generic options like ``SMC LEY`` or models from ``IGUS`` are excellent choices.
    -   **Conveyors**: Search for ``conveyor`` and select two instances of a model like ``Conveyor Belt``. Their dimensions can be adjusted later.
    -   **Gripper Tool**: Search for ``Robotiq 2F-85``, a common gripper for UR robots.
    -   **Parts**: Search for and download a simple ``Box`` and ``Bottle``.
    -   **Workstation**: Search for a ``Table`` or ``Workbench`` to serve as the base.

Step 2: Staging the Simulation Environment
-------------------------------------------

Once all components are loaded, they must be assembled into a functional workcell. This is done by structuring the items in RoboDK's project tree.

1.  **Mount Robot on Rail**:
    In the project tree on the left, **drag the `UR10e` robot item and drop it directly onto the `Linear Rail` item**. RoboDK will automatically link them, making the robot move with the rail.

2.  **Attach Tool to Robot**:
    Similarly, **drag the `Robotiq 2F-85` gripper and drop it onto the `UR10e` robot**. The tool will snap to the robot's flange, and a default Tool Center Point (TCP) will be created.

3.  **Position Key Components**:
    - Place the **table** at the center of your station.
    - Position the two **conveyors** on opposite sides of the work area. You can resize them by double-clicking the item and selecting "More options...".

4.  **Define Reference Frames (Expert Practice)**:
    Using reference frames is critical for robust programming. Create new frames using the **"Add a new Reference Frame"** icon.
    -   Create and position a frame named ``Frame_Prise_Bouteille`` at the pick-up location on the inbound conveyor.
    -   Create and position another frame named ``Frame_Depot_Boite`` at the drop-off location on the outbound conveyor.

5.  **Initial Part Placement**:
    Place a ``Bottle`` object on the inbound conveyor, near the ``Frame_Prise_Bouteille``.


Step 3: Programming the Robotic Task
-------------------------------------

With the cell assembled, the next step is to program the robot's movements and actions.

1.  **Create Key Targets**:
    A "Target" is a saved robot position. Manually move the robot to each key location and create a new target by clicking the **"Add a new Target"** icon.
    
    -   ``Target_Home``: A safe, neutral position.
    -   ``Target_Approche_Bouteille``: A point directly above the bottle.
    -   ``Target_Prise_Bouteille``: The exact position for gripping the bottle.
    -   Create corresponding targets for the box drop-off location (`Target_Approche_Boite`, `Target_Depot_Boite`).

2.  **Build the Main Program**:
    Click **"Add a new Program"** and name it `Main_Program`. This will contain the main logic loop.

3.  **Add Movement Instructions**:
    From the toolbar, add movement instructions to your program.
    -   **Joint Move**: Use for fast, non-linear movements (e.g., returning to `Target_Home`).
    -   **Linear Move**: Use for precise approaches and retreats where a straight-line path is required.

4.  **Simulate Gripper and Conveyor Actions**:
    Use the **"Program call"** instruction to trigger events.
    -   **To pick up an object**: After moving to the grip target, add a program call with the instruction ``Attach(Bottle)``.
    -   **To release an object**: After moving to the release target, add a program call with ``Detach(Conveyor_2)``. The object will attach to the nearest surface below.
    -   **To control conveyors**: A program call can execute a small Python script to set the conveyor's speed, for example: `convoyeur.setSpeed(50)`.

Step 4: Orchestrating the Final Program
----------------------------------------

Your final `Main_Program` in the RoboDK tree should represent a logical, looping sequence of these instructions, creating a continuous and realistic simulation of the industrial task.

.. figure:: /_static/robodk_program_tree.png
   :align: center
   :width: 400px
   :alt: Example of a program structure in the RoboDK tree.

   *An example of how the main program loop can be structured in the RoboDK project tree.*

By following this guide, you can precisely replicate the simulation environment used for this project, ensuring a consistent foundation for data generation and analysis.