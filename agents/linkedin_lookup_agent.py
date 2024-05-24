from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain_core.tools import Tool
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from agents.helper import get_profile_url_tavily
load_dotenv()


def lookup(name: str) -> str:
    # Initialize Language Model: The function first initializes an instance of ChatOpenAI with specific parameters (temperature=0 and model_name="gpt-3.5-turbo"),
    # which sets up a language model from OpenAI's GPT-3.5-turbo.
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # Define the Prompt Template: It defines a prompt template,
    # which instructs the language model to generate a response containing only the URL of the LinkedIn profile for the given name.
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                              Your answer should contain only a URL"""

    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    # Setup Tools for the Agent: The function prepares a tool that will be used by the agent to perform the actual search for the LinkedIn profile URL.
    # The tool is defined with a name, a function (get_profile_url_tavily), and a description of its purpose.
    tools_for_agent = [Tool(
        name="Call Tavily for Linkedin Profile Page",
        func=get_profile_url_tavily,
        description="useful for when you need get the Linkedin Page URL"
    )]

    # Pull React Prompt: It pulls a pre-defined REACT prompt from the Langchain hub.
    # https://smith.langchain.com/hub
    react_prompt = hub.pull("hwchase17/react")

    # Create Agent and Executor: The function creates an agent using the create_react_agent function, which incorporates the language model, tools, and prompt.
    # It then creates an executor (AgentExecutor) to handle the execution of the agent with the defined tools.
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    # Invoke the Agent: The agent executor is invoked with the formatted prompt containing the person's name.
    # The response from the agent is expected to include the LinkedIn profile URL.
    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    linkedin_profile_url = result["output"]
    return linkedin_profile_url
