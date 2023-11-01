from typing import List

from models.agent import AgentModel
from typings.agent import AgentOutput, AgentWithConfigsOutput, ConfigsOutput
from utils.system_message import SystemMessageBuilder
from utils.type import convert_value_to_type
from utils.user import \
    convert_model_to_response as user_convert_model_to_response


def convert_model_to_response(
    agent_model: AgentModel, is_system_message: bool = False
) -> AgentWithConfigsOutput:
    agent_data = {}

    # Extract attributes from AgentModel using annotations of Agent
    for key in AgentOutput.__annotations__.keys():
        if hasattr(agent_model, key):
            target_type = AgentOutput.__annotations__.get(key)
            agent_data[key] = convert_value_to_type(
                value=getattr(agent_model, key), target_type=target_type
            )

    # Convert AgentConfigModel instances to Config
    configs = {}
    if hasattr(agent_model, "configs"):
        for config_model in agent_model.configs:
            key = getattr(config_model, "key")
            value = getattr(config_model, "value")

            # Convert value to the type specified in ConfigsOutput
            target_type = ConfigsOutput.__annotations__.get(key)

            if target_type:
                value = convert_value_to_type(value, target_type)

            configs[key] = value

    if hasattr(agent_model, "creator") and agent_model.creator:
        agent_data["creator"] = user_convert_model_to_response(agent_model.creator)

    agent_with_config = AgentWithConfigsOutput(
        agent=AgentOutput(**agent_data),
        configs=ConfigsOutput(**configs) if configs else None,
    )
    if is_system_message:
        system_message = SystemMessageBuilder(agent_with_config).build()
        agent_with_config.system_message = system_message

    return agent_with_config


def convert_agents_to_agent_list(
    agents: List[AgentModel],
) -> List[AgentWithConfigsOutput]:
    return [convert_model_to_response(agent_model) for agent_model in agents]
