from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-2",
)

agent = Agent(model=model)

response = agent("Say hello and confirm you're working, in one short sentence.")
print(response)