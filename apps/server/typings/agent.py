from enum import Enum
from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel, Field

from typings.user import UserOutput


class AgentType(str, Enum):
    voice = "voice"
    text = "text"


class DataSourceFlow(str, Enum):
    PRE_RETRIEVAL = "pre_execution"
    SOURCE_DETECTION = "source_detection"


class InputModeType(List[str], Enum):
    text = ["Text"]
    voice = ["Voice"]
    text_voice = ["Text", "Voice"]


class AgentInput(BaseModel):
    name: str = Field(..., example="Agent Smith")
    description: Optional[str] = Field(None, example="Description of the agent")
    agent_type: Optional[AgentType] = Field(
        None,
        example=AgentType.voice,
        description="You have to choose between Text-based and Voice-based agents.",
    )
    workspace_id: Optional[UUID4] = Field(
        None, example="123e4567-e89b-12d3-a456-426614174000"
    )
    role: Optional[str] = Field(
        None, example="Speaker", description="A role can be anything of your choosing."
    )
    is_memory: Optional[bool] = Field(None, example=True)
    avatar: Optional[str] = Field(
        None,
        example="https://raw.githubusercontent.com/l3vels/L3AGI/77d65c9ad74d4da140ef7a30590f063768333bd9/apps/ui/src/assets/tools/openweather.svg",
    )
    is_template: bool = Field(None, example=True)


class ConfigInput(BaseModel):
    goals: List[str] = Field(
        ...,
        example=[
            "Provide a concise summary or highlight about the sourced articles.",
            "Efficiently locate relevant scientific articles from arxiv.org based on user queries.",
        ],
        description="A list of goals that the agent aims to achieve. These goals can include providing summaries, locating relevant articles, or any other specific objectives.",
    )
    constraints: List[str] = Field(
        ...,
        example=[
            "Does not replace professional advice or expert consultations in respective fields.",
            "Does not provide opinions or expert analysis. Presents only factual information based on sourced content.",
        ],
        description="A list of constraints or limitations that the agent adheres to. These constraints can include not replacing professional advice, not providing opinions or expert analysis, and presenting only factual information based on sourced content.",
    )
    tools: List[str] = Field(
        ...,
        example=[
            "59209d41-83cf-48c5-806a-ec87a55cdcc4",
            "ac34d174-6ca4-49cf-aef2-6e2cdf2e0028",
        ],
        description="You should pass an array of Toolkit IDs.",
    )
    datasources: List[str] = Field(
        ...,
        example=["0b9d648f-0fcb-4ced-8e08-502c5b8e0c06"],
        description="You should pass an array of Data Source IDs which you have created.",
    )
    model: Optional[str] = Field(
        None,
        example="8833a90e-86e4-4118-9e28-517de1a4def8",
        description="Expects Model ID",
    )
    temperature: float = Field(
        ...,
        gt=0,
        le=1.0,
        example=0.5,
        description="The temperature parameter for the agent. It should be a float value between 0 and 1, representing the level of randomness in the agent's responses. A higher value like 1.0 will result in more random responses, while a lower value like 0.5 will make the responses more focused and deterministic.",
    )
    instructions: List[str] = Field(
        ...,
        example=[
            "The more specific your inquiry, the more accurate Maven's assistance will be.",
            "Efficiently locate relevant scientific articles from arxiv.org based on user queries.",
        ],
        description="A list of instructions or guidance for interacting with the agent. These instructions can include tips on how to get more accurate assistance or specific guidelines for using certain features.",
    )
    suggestions: Optional[List[str]] = Field(
        None,
        example=[
            "What's the weather like today?",
            "Tell me a joke.",
            "How can I contact customer support?",
        ],
        description="An array of suggested dialogs or questions that users can choose from to interact with the system.",
    )
    greeting: Optional[str] = Field(
        None,
        example="Hello! I'm the ArXiv & Wikipedia Expert, your dedicated assistant for both academic research and general knowledge. How may I assist you today?",
        description="A greeting message displayed by the assistant to welcome users and provide an introduction to its capabilities.",
    )
    text: Optional[str] = Field(None, example="text")
    integrations: Optional[List[dict]] = Field(
        None, example=[{"integration1": "value1"}, {"integration2": "value2"}]
    )
    source_flow: Optional[str]
    synthesizer: Optional[str] = Field(
        None,
        example="b44769b1-1a20-44d3-b0f1-8b4c96e6a02a",
        description="only on `voice-based` agents! <br/> Expects Voice Tool ID",
    )
    default_voice: Optional[str] = Field(None, example="default_voice")
    voice_id: Optional[str] = Field(None, example="voice_id")
    transcriber: Optional[str] = Field(
        None,
        example="transcriber",
        description="only on `voice-based` agents! <br/> Expects Voice Tool ID",
    )
    response_mode: Optional[list[str]]
    input_mode: Optional[list[str]]
    runners: Optional[List[Dict]] = Field(
        None, example=[{"runner1": "value1"}, {"runner2": "value2"}]
    )
    sentiment_analyzer: Optional[Dict] = Field(
        None, example={"analyzer1": "value1", "analyzer2": "value2"}
    )


class AgentConfigInput(BaseModel):
    agent: AgentInput
    configs: ConfigInput


class CreateVoiceAgentInput(BaseModel):
    template_id: UUID4
    name: Optional[str] = ""
    description: Optional[str] = ""


class ConfigsOutput(BaseModel):
    goals: List[str]
    constraints: List[str]
    tools: List[str]
    datasources: List[str]
    model: Optional[str]
    temperature: float
    instructions: List[str]
    suggestions: Optional[List[str]]
    greeting: Optional[str]
    text: Optional[str]
    integrations: Optional[List[dict]]
    source_flow: Optional[str]
    synthesizer: Optional[str]
    default_voice: Optional[str]
    voice_id: Optional[str]
    transcriber: Optional[str]
    response_mode: Optional[List[str]]
    input_mode: Optional[List[str]]
    runners: Optional[List[Dict]]
    sentiment_analyzer: Optional[Dict]


class AgentOutput(BaseModel):
    id: UUID4
    name: str
    description: str
    agent_type: Optional[str]
    workspace_id: Optional[UUID4]
    parent_id: Optional[UUID4]
    role: str
    is_template: bool
    is_deleted: bool
    is_public: bool
    account_id: UUID4
    created_by: Optional[UUID4]
    creator: Optional[UserOutput]
    modified_by: Optional[UUID4]
    is_memory: Optional[bool]
    avatar: Optional[str]


class AgentWithConfigsOutput(BaseModel):
    agent: AgentOutput
    configs: Optional[ConfigsOutput]
    system_message: Optional[str]
