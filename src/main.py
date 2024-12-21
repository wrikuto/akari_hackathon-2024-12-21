from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from typing import Literal
from langchain_core.tools import tool
from langgraph.graph import END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from textwrap import dedent
import pandas as pd
import uuid
import asyncio  # 必要に応じて asyncio をインポートします
from analyze_lifelog import analy_food, analy_step, analy_nutrition, food_df, nutriton_df, step_df
from dataclasses import dataclass
from pydantic import BaseModel, Field
from enum import Enum
from googlemap_searcher import search_places
import heapq
from datetime import datetime

from utils import TasksQueue, AgentState, TaskType, AnalyzedUserData
from agent_supervisor import SupserVisorAgent
from agent_interview import interviewAgent
from agent_analyzer import UserDataAnalyzer
from agent_db_searcher import DataBaseSearchAgent
from agent_suggest import SuggestMenuAgent
from agent_general import GeneralAgent

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "finc"






class AgentState(TypedDict):
	messages: Annotated[list, add_messages]

