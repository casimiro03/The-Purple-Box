import os
import streamlit as st
from crewai import Agent, Task
from dotenv import load_dotenv

import streamlit as st

#st.write("Hello, I am testing the UI")


# 1. Setup Environment
load_dotenv()

# Assuming your class is named 'MyProjectCrew'
# We'll instantiate it to access the decorated agents
from mendicant_lyla_crew.crew import MendicantLylaCrew

crew_instance = MendicantLylaCrew()

# 2. Sidebar for Agent Selection
# This makes the "house" feel organized
st.sidebar.title("Agent Directory")
my_agents = {
    "Lyla": crew_instance.lyla(),
    # "Analyst": crew_instance.analyst_agent(), # You can add more easily here
}

selected_agent_name = st.sidebar.selectbox("Who do you want to talk to?", list(my_agents.keys()))
selected_agent = my_agents[selected_agent_name]

# 3. Chat Interface
st.title(f"Interacting with {selected_agent_name}")

# Initialize chat history so the conversation doesn't disappear on refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Talk to {selected_agent_name}..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 4. Agent Execution
    with st.chat_message("assistant"):
        with st.spinner(f"{selected_agent_name} is thinking..."):
            # We create a task on the fly
            interaction_task = Task(
                description=prompt, 
                expected_output="A conversational and helpful response based on the project context.", 
                agent=selected_agent
            )
            
            # Use execute_task for direct agent response without the whole crew
            response = selected_agent.execute_task(interaction_task)
            st.markdown(response)
            
    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": response})
