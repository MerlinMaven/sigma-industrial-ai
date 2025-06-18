============================================
Deployment & Interactive Interface
============================================

The final stage of the Sigma pipeline is to **deploy the system** into an accessible, interactive application for end-users such as engineers, operators, and maintenance technicians. This crucial step transforms our complex AI models into a practical tool for data-driven decision-making.

We chose **Streamlit** as our deployment framework for its unique ability to rapidly transform Python scripts into beautiful, interactive web applications.

The "Sigma Control Center" Dashboard
--------------------------------------

Our Streamlit application, the "Sigma Control Center," provides a comprehensive, at-a-glance overview of the entire robotic workcell. It is designed around principles of clarity and actionable intelligence.

**Core Interface Components:**

-   **Multi-Component View**: A grid layout displays the health status of each monitored component (robots, conveyors, rails) simultaneously, allowing for easy comparison.
-   **Real-Time Visualization**: Each component has a dedicated chart plotting its primary operational signal alongside its calculated **anomaly score**.
-   **Dynamic Thresholds**: Users can interactively adjust alert thresholds directly on the graphs to fine-tune sensitivity.
-   **Health Status KPIs**: A clear, color-coded status indicator (🟢 **Normal**, 🟡 **Warning**, 🔴 **Alert**) provides an immediate assessment of each machine's health.

.. figure:: /_static/interface.png
   :align: center
   :width: 100%
   :alt: The main dashboard of the Sigma Control Center.

   *The primary monitoring dashboard, providing a real-time overview of all industrial assets.*

A Conversational AI for Enhanced Usability: The "Ask Sigma" Chatbot
---------------------------------------------------------------------

To maximize accessibility and efficiency, we moved beyond a purely visual dashboard by integrating a **conversational AI assistant**, named "Ask Sigma." The goal is to allow any user, regardless of their technical expertise, to query the system and perform complex actions using intuitive, guided interactions.

Our design philosophy for the chatbot is a **"Dual Menu" approach**, which combines a proactive, button-driven main menu with guided question-and-answer dialogues.

.. figure:: /_static/chat.png
   :align: center
   :width: 700px
   :alt: The Dual Menu concept for the Ask Sigma chatbot.

   *The "Dual Menu" strategy: A proactive main menu guides the user, while subsequent dialogues gather specific information step-by-step.*


**1. The Main Menu: Proactive Guidance**

Instead of presenting a blank prompt, the chatbot initiates the conversation by offering the main functionalities as clear, clickable buttons. This immediately orients the user and eliminates any ambiguity about the system's capabilities.

*Initial Interaction Example:*
   | **Sigma Assistant:** Welcome, Engineer. How can I assist you today?
   |
   | `[ Check Robot Status ]` `[ Generate Performance Report ]` `[ Adjust Settings ]`

**2. Guided Dialogues: Precision Through Interaction**

Once the user selects a primary action, the chatbot engages in a **structured, step-by-step dialogue** to gather all necessary details, often presenting further options as buttons.

*Example Scenario: Generating a Custom Report*

1.  **User Clicks:** `[ Generate Performance Report ]`
2.  **Chatbot Asks:** "Understood. What type of report would you like?"
    `[ Daily Summary ]` `[ Weekly Trend Report ]` `[ Custom Period ]`
3.  **User Clicks:** `[ Custom Period ]`
4.  **Chatbot Prompts:** "Please provide the start date (e.g., YYYY-MM-DD)."
5.  ...and so on, until all required parameters are collected and the action is executed.

This guided approach minimizes user error and streamlines complex tasks. It allows operators to perform actions like **generating diagnostic reports, exporting data slices, or even triggering model fine-tuning cycles** through a simple, fool-proof conversation.

By integrating this conversational layer, we transform a passive monitoring tool into an **active, intelligent assistant**, significantly lowering the barrier to entry and maximizing the operational value of our AI pipeline.

Deployment Considerations
-------------------------

.. important::
   **Local Execution Required**: The system is designed to process real-time data from a **locally running RoboDK instance**. For full functionality, the Streamlit application must be run on the same machine or network as the RoboDK simulation to allow for API communication.

.. note::
   **Public Demo Version**: For presentation and demonstration purposes, a public version of the application is available online. It operates in **"replay mode"**, using pre-recorded data to illustrate the system's full analysis and visualization capabilities without requiring a live RoboDK connection.

   👉 **Link to the demo version**: `https://sigma-rul-demo.streamlit.app <https://sigma-rul-demo.streamlit.app>`_

Access to the Source Code
--------------------------

The complete application code, including the Streamlit dashboard (`dashboard.py`), all trained models, and the necessary configuration files for local deployment, is available on our GitHub repository.

👉 **Link to the GitHub repository**: `https://github.com/MerlinMaven/sigma-industrial-ai.git <https://github.com/MerlinMaven/sigma-industrial-ai.git>`_