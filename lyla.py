import streamlit as st
from crewai import Agent, Task


from dotenv import load_dotenv

# Load the enviroment variables from the .env file
load_dotenv()

# API KEY
GROQ_API_KEY=os.getenv('GROQ_API_KEY')

# Interaction agent for Streamlit app

@agent
def lyla(self) -> Agent:
    return Agent(
        config=self.agents_config['lyla'], # type: ignore[index]
        verbose=True,
        reasoning=True,  # Enable reasoning and planning
        max_reasoning_attempts=3,  # Limit reasoning attempts
        max_iter=5,  # Allow more iterations for complex planning
        allow_delegation=True,  # Allow delegation to other agents
            
        # API CALL & MODEL SELECTION
        llm=self.overseer_llm,
 
             
        )


my_agents = {
    "Lyla": lyla()
}

selected_agent_name = st.sidebar.selectbox("Select Agent", list(my_agents.keys()))
selected_agent = my_agents[selected_agent_name]

if prompt := st.chat_input(f"Talk to {selected_agent_name}"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Execute only the selected agent's logic
    # Note: We create a temporary task for this specific interaction
    from crewai import Task
    response = selected_agent.execute_task(
        Task(description=prompt, expected_output="Start a chat to discuss the subjects", agent=selected_agent)
    )
    
    with st.chat_message("assistant"):
        st.markdown(response)