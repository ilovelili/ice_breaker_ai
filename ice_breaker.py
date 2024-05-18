from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.tweet import scrape_user_tweets
from agents import linkedin_lookup_agent, twitter_lookup_agent

from dotenv import load_dotenv
load_dotenv()


def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)  # tweet api costs money

    summary_template = """
    given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    print(res)


if __name__ == "__main__":
    print("Ice Breaker")
    res = ice_break_with(name="Min Ju Woodstock LinkedIn")
    print(res)
