import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")

credentials = Credentials(
    url="https://eu-gb.ml.cloud.ibm.com",
    api_key=api_key
)

model = Model(
    model_id="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    credentials=credentials,
    project_id=project_id
)

response = model.generate_text(
    prompt="Say hello to AI StudyMate in one sentence."
)

print(response)