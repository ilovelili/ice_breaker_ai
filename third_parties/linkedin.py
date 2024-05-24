import os
import requests
from dotenv import load_dotenv

load_dotenv()

# https://nubela.co/proxycurl/docs#people-api


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape from linkedin profiles,
    manually scrape from linkedin profiles
    """

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        #  uses the Proxycurl API to fetch LinkedIn profile data
        # https://nubela.co/proxycurl/docs#people-api-person-profile-endpoint
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        response = requests.get(api_endpoint, params={"url": linkedin_profile_url}, headers={
            "Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}, timeout=10)

        data = response.json()
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
            and k not in ["people_also_viewed", "certifications"]
        }

        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

        return data
