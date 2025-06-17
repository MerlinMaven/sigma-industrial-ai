============================================
Guide: Reproducing the Simulation Environment
============================================

This guide provides a step-by-step walkthrough to recreate the **Sigma Project's simulation environment** from scratch using RoboDK. Following these instructions will allow you to build the digital twin used for our data generation and experimental pipeline.

**Prerequisites:**

- A working installation of **RoboDK**.
- Basic familiarity with the RoboDK interface (e.g., navigating the tree, adding items).

Step 1: Assembling the Workcell Components
------------------------------------------

The first step is to populate the simulation station with all necessary components from RoboDK's online library.

1. **Open the Online Library**: Click the **"Open online library"** icon (🌐) in the main toolbar.

2. **Download Required Assets**:
   Search and download the following items (they will be added directly to your station):

   - **Robot**: ``Universal Robots UR10e``
   - **Linear Rail**: Search for a compatible rail such as ``SMC LEY`` or ``IGUS``
   - **Conveyors**: Add two instances of ``Conveyor Belt`` (can be resized later)
   - **Gripper Tool**: ``Robotiq 2F-85``
   - **Parts**: ``Box`` and ``Bottle``
   - **Workstation**: ``Table`` or ``Workbench``

Step 2: Structuring the Workcell
---------------------------------

Once all components are loaded, assemble them into a functional workcell:

1. **Mount the Robot on the Rail**:
   Drag the `UR10e` robot item and drop it onto the `Linear Rail` item. This links the robot to the rail, allowing synchronized motion.

2. **Attach the Tool to the Robot**:
   Drag the `Robotiq 2F-85` gripper onto the `UR10e` robot. RoboDK will automatically assign it to the flange.

3. **Position Key Components**:
   - Place the **table** at the center.
   - Position the **conveyors** on each side of the work area. Resize via: *double-click → More Options*.

4. **Define Reference Frames**:
   Create new frames using the **"Add a new Reference Frame"** icon:
   - ``Frame_Prise_Bouteille`` → near the bottle on the inbound conveyor
   - ``Frame_Depot_Boite`` → above the box on the outbound conveyor

5. **Initial Object Placement**:
   Place a `Bottle` object near `Frame_Prise_Bouteille`.

Step 3: Programming the Robotic Task
-------------------------------------

With the environment set up, the robot can now be programmed.

1. **Create Key Targets**:
   Move the robot manually to key positions and save each as a Target:

   - `Target_Home`: Safe neutral position
   - `Target_Approche_Bouteille` → above the bottle
   - `Target_Prise_Bouteille` → exact pick-up point
   - `Target_Approche_Boite` and `Target_Depot_Boite` → drop-off points

2. **Create the Main Program**:
   Click **"Add a new Program"** and name it `Main_Program`.

3. **Add Robot Instructions**:
   Use movement instructions to build the task logic:

   - `MoveJ`: For joint-space (fast) movements like `Target_Home`
   - `MoveL`: For precise, straight-line moves to approach/release points

4. **Simulate Gripper and Conveyor Actions**:
   Use **Program Calls** for interaction logic:

   - To pick up: `Attach(Bottle)` after `Target_Prise_Bouteille`
   - To drop off: `Detach(Conveyor_2)` after `Target_Depot_Boite`
   - To control conveyors: execute a script like `conveyor.setSpeed(50)`

Step 4: Orchestrating the Final Program
---------------------------------------

The `Main_Program` should represent a clean loop: from pick-up, to transfer, to drop-off — then back to home. This creates a continuous, realistic simulation of the industrial task.

---

By following this guide, any user can **faithfully reproduce** the simulation environment used in Project Sigma. This ensures reproducibility and provides a solid foundation for real-time data collection and algorithm validation.
