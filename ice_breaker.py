from third_parties.linkedin import scrape_linkedin_profile
from agents import linkedin_lookup_agent
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent.lookup(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    given the Linkedin information {information} about the person that I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    res = chain.invoke(input={"information": linkedin_data})
    return res


if __name__ == "__main__":
    print("Ice Breaker")
    res = ice_break_with(name="Min Ju Woodstock LinkedIn")
    print(res)
