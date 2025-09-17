## Introduction
<table>
  <tr>
    <td width="30%">
      <img src="assests/monitoring.gif" alt="Demo of my project">
    </td>
    <td width="70%" valign="top">
      <h3>Guardian</h3>
      <p>
         A prototype AI agent that automates personal productivity monitoring
         by analyzing web browsing activity and providing gentle notifications to
         help the user maintain focus.
      </p>
      <ul>
        <li><b>Author: </b>Dipanshu</li>
        <li><b>University: </b>IIT Mandi</li>
        <li><b>Department: </b>Computer science and engineering</li>
        <li><b>Date: </b>September 17, 2025</li>
        <li><b>Version: </b>1.0</li>
      </ul>
    </td>
  </tr>
</table>

## Output
Screenshots Taken during development process.
<table>
  <tr>
    <td width="50%">
      <img src="assests/1.png" alt="Demo of my project">
    </td>
    <td width="50%" valign="top">
      <img src="assests/2.png" alt="Demo of my project">
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="assests/3.png" alt="Demo of my project">
    </td>
    <td width="50%" valign="top">
      <img src="assests/4.png" alt="Demo of my project">
    </td>
  </tr>
</table>
Created UI [With streamlit]
<table>
  <tr>
    <td width="50%">
      <img src="assests/5.png" alt="Demo of my project">
    </td>
    <td width="50%" valign="top">
      <img src="assests/6.png" alt="Demo of my project">
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="assests/7.png" alt="Demo of my project">
    </td>
    <td width="50%" valign="top">
      <img src="assests/8.png" alt="Demo of my project">
    </td>
  </tr>
</table>

## System Architecture
<table>
  <tr>
    <td width="50%" valign="top">
      <img src="assests/diagram.svg" alt="Demo of my project">
    </td>
  </tr>
</table>


### Workflow
1. Data Collection: A Firefox Browser Extension acts as a sensor, collecting data about all open tabs every two minutes and sending it to a local server.

2. Data Ingestion & Persistence: A lightweight Flask server listens for this data and stores it in a local SQLite database, timestamping each entry.

3. Scheduled Trigger: A central scheduling process (run_agent.py) initiates the main reasoning cycle every five minutes.

4. Reasoning & Planning: The agent executes a single-path plan for each cycle.

5. Monitoring: A Streamlit UI provides a live, visual representation of the agent's workflow and internal state by reading from a structured log file. And allow to change wide range of parameters like changing models, notification timeout, scheduling time.

### Design Patterns
1. *Proactive Goal Creator:* The browser extension proactively captures the user's context to help achieve the implicit goal of productivity.

2. *Role-based Cooperation:* The system uses a multi-agent approach where two "brains" have distinct roles: an initial Analyst (Gemini) and a final Reviewer (DeepSeek).

3. *Cross-reflection:* The Second Brain (DeepSeek) reviews the output of the First Brain (Gemini), providing a layer of reflection and correction to improve reasoning certainty.

### Components 
1. **Firefox Extension (extension/):** A JavaScript-based extension that collects open tab information and sends it to the local data connector.

2. **Data Connector (connector/getData.py):** A Flask-based API endpoint that listens for incoming data from the extension and persists it to the database.

3. **Database (database/sqlite.py, runMemory.db):** The persistence layer using SQLite to store raw tab data and analysis results.

4. **Agent Core / Scheduler (run_agent.py):** The system's entry point. It runs the Flask server and schedules the brainCaller function.

5. **Reasoning Brains (brain/):**
    1. ***First Brain (Gemini 1.5 Flash):*** Performs a fast, initial analysis to form a hypothesis about distracting tabs.

    2. ***Second Brain (DeepSeek):*** Performs a final, more nuanced review and has the final say.

6. **Tools (tools/webSearch.py):** An external tool integration to perform a web search for gathering more context on a tab's content.

7. **Actions (actions/notification.py):** Executes the final decision by sending a cross-platform desktop notification to the user.

8. **Monitoring UI (UI/):** A Streamlit web dashboard that provides a live, visual monitor of the agent's execution plan.
