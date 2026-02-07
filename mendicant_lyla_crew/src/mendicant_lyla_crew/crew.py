import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from dotenv import load_dotenv

# Load the enviroment variables from the .env file
load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# get api key from .env file

# Bypass the annoying openiai key requirement
# os.environ["OPENAI_API_KEY"] = "NA" # No es una key real, solo para bypass

# The api im using is Groq's
GROQ_API_KEY=os.getenv('GROQ_API_KEY')



@CrewBase
class MendicantLylaCrew():
    """MendicantLylaCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    


    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    
    # Agent's LLMs & API KEYS
    @property
    def creative_assistant_llm(self) -> LLM:
        return LLM(
        model=os.getenv('CREATIVE_MODEL'),
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
        
    @property
    def engineer_llm(self) -> LLM:
        return LLM(
        model=os.getenv('ENGINEER_MODEL'),
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
        
    @property
    def overseer_llm(self) -> LLM:
        return LLM(
        model=os.getenv('OVERSEER_MODEL'),
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
    
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

    @agent
    def creative_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_engineer'], # type: ignore[index]
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=300,  # 5-minute timeout
            max_retry_limit=3,  # More retries for complex code tasks
            reasoning=True,  # Enable reasoning and planning
            max_reasoning_attempts=3,  # Limit reasoning attempts
            
            max_rpm=20,  # Limit to 10 requests per minute to prevent rate limits
            
            
            
            # THIS BYPASSES THE PARSING BUG COMPLETELY:
            #base_url="https://api.groq.com/openai/v1"
            
            # API CALL & MODEL SELECTION 
            llm=self.engineer_llm
        
        )
        
        
    @agent
    def creative_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_assistant'], # type: ignore[index]
            verbose=True,
            
            # API CALL & MODEL SELECTION
            llm=self.creative_assistant_llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def define_ontology(self) -> Task:
        return Task(
            config=self.tasks_config['define_ontology'], # type: ignore[index]
            #expected_output=pass,
            #output_file='outputs/ontology.md' # Saves it cleanly in a folder crewai make the dir automatically if it doesn't exist
            expected_output='outputs/ontology.md'
        )

    @task
    def implement_math_logic(self) -> Task:
        return Task(
            config=self.tasks_config['implement_math_logic'], # type: ignore[index]
            expected_output='outputs/math_logic.py'
        )
        
    @task
    def design_ui_ux(self) -> Task:
        return Task(
            config=self.tasks_config['design_ui_ux'], # type: ignore[index]
            expected_output='outputs/ui_ux_design.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MendicantLylaCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=False,# Disable crew-level memory for a fresh context each run
            tracing=True,
            save_traces=True,
            embedder={
                "provider": "huggingface", # <--- Esto no requiere keys
                "config": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"
                }
            }
        )
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        
