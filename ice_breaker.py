from typing import Tuple
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from agents.linkedin_lookup_agent import linkedin_lookup_agent
import json
from third_parties.linkedin import scrape_linkedin_profile
from output_parsers import PersonIntel, person_intel_parser

load_dotenv()


def ice_break(name="") -> Tuple[PersonIntel, str]:
    SUMMARY_TEMPLATE = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. a short summary
        2. 5 interesting facts about them
        3. a topic that may interest them
        4. 2 creative ice breakers to open a converstaion with them
        
        {format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=SUMMARY_TEMPLATE,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Switch between ProxyCurl and JSON data
    linkedin_data = json.load(open("./linkedin_response.json"))
    # linkedin_profile_url = linkedin_lookup_agent(name)
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url)

    result = chain.run(information=linkedin_data)

    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print(ice_break())
