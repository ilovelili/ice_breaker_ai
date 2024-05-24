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
    # find the LinkedIn profile URL for the given name.
    linkedin_username = linkedin_lookup_agent(name=name)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    # twitter_username = twitter_lookup_agent(name=name)
    # tweets = scrape_user_tweets(username=twitter_username, mock=True)  # tweet api costs money

    # This is a template for the prompt that will be used to generate a summary and two interesting facts about the person.
    # It instructs the language model to use information from LinkedIn.
    summary_template = """
    given the information about a person from linkedin {information},
    I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """

    # This creates a PromptTemplate using the defined summary_template. The input_variables are placeholders for the LinkedIn information,
    # and partial_variables are for format instructions obtained from summary_parser.get_format_instructions().
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    # This initializes an instance of ChatOpenAI with specific parameters for the language model.
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # langchain expression language
    # https://python.langchain.com/v0.1/docs/expression_language/get_started/
    # This creates a chain by combining the prompt template, language model, and summary parser using Langchain's expression language.
    # The chain is then invoked with the LinkedIn data to generate the summary.
    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Ice Breaker")
    res = ice_break_with(name="Elon Musk")
    print(res)
