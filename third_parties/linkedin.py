import os
import requests


def scrape_linkedin_profile(profile_url: str):
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    api_key = os.environ.get("PROXYCURL_API_KEY")
    header_dic = {"Authorization": "Bearer " + api_key}
    params = {
        "url": profile_url,
        "fallback_to_cache": "on-error",
        "use_cache": "if-present",
        "skills": "include",
        "inferred_salary": "include",
        "personal_email": "include",
        "personal_contact_number": "include",
        "twitter_profile_id": "include",
        "facebook_profile_id": "include",
        "github_profile_id": "include",
        "extra": "include",
    }
    response = requests.get(api_endpoint, params=params, headers=header_dic)

    linkedin_data = {
        k: v
        for k, v in response.json().items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if linkedin_data.get("groups"):
        for group_dict in linkedin_data.get("groups"):
            group_dict.pop()

    return linkedin_data
