from typing import Tuple
from dotenv import load_dotenv
from output_parsers import Summary, summary_parser
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.tweet import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

load_dotenv()


def ice_break_with(name: str) -> Tuple[Summary, str]:
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
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # langchain expression language
    # https://python.langchain.com/v0.1/docs/expression_language/get_started/
    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Ice Breaker")
    res = ice_break_with(name="Min Ju Woodstock LinkedIn")
    print(res)
