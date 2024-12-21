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
import pandas as pd
import uuid
from googlemap_search import search_places, get_traffic_info
from langchain_community.tools.tavily_search import TavilySearchResults


load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "akari_hackathon_2024-12-21"


class AgentState(TypedDict):
	messages: Annotated[list, add_messages]



class Agent:
	def __init__(self, llm: ChatOpenAI, tools):
		self.llm = llm
		self._llm_with_tools = llm.bind_tools(tools)
		self.general_prompt = ChatPromptTemplate.from_messages(
			[
				MessagesPlaceholder(variable_name="messages"),
				(
					"system",
					"""
					あなたは地図検索の担当です。ユーザーのリクエストに応じて、地図検索を行います。
					ユーザーが明確に位置から目的の場所を聞いているときは`search_places`のみを、ユーザーが何かの場所を探しているときは`tavily_search`を使ってください。
					"""
				),
				("user", "{messages}"),
			]
		)

	def run(self, state: AgentState) -> dict:
		messages = state["messages"]

		chain = self.general_prompt | self._llm_with_tools
		response = chain.invoke({"messages": messages})


		return {"messages": [response]}




class ChatBot():
	def __init__(self, llm: ChatOpenAI):
		self._llm = llm
		self._memory = MemorySaver()
		self._tools = [search_places, TavilySearchResults(max_results=3)]
		self._tool_node = ToolNode(self._tools)
		self._agent = Agent(self._llm, self._tools)


	def _create_graph(self):
		graph = StateGraph(AgentState)

		graph.add_node("agent", self._agent.run)
		graph.add_node("tool_node", self._tool_node)

		graph.add_edge(START, "agent")
		graph.add_conditional_edges(
			"agent",
			self._should_continue,
			{
				"continue": "tool_node",
				"end": END,
			},
		)
		graph.add_edge("tool_node", "agent")

		graph = graph.compile(checkpointer=self._memory)
		return graph
	


	def _should_continue(self, state):
		return "continue" if state["messages"][-1].tool_calls else "end"


	def create_image(self, graph):
		png_data = graph.get_graph(xray=True).draw_mermaid_png()

		# バイナリデータをカレントディレクトリに保存
		with open("image.png", "wb") as f:
			f.write(png_data)




def main():
	llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
	agent = ChatBot(llm)
	graph = agent._create_graph()
	agent.create_image(graph)

	config = {"configurable": {"thread_id": str(uuid.uuid4())}}
	while True:
		try:
			user = input("---\nUser (q/Q to quit): ")
		except:
			raise Exception("Error in input")
		if user in {"q", "Q"}:
			print("AI: さようなら!")
			break
		output = None
		for output in graph.stream({"messages": [HumanMessage(content=user)]}, config=config, stream_mode="updates"):
			# last_message = next(iter(output.values()))["messages"][-1]
			last_message = next(iter(output.values()))

			if isinstance(last_message["messages"][0], AIMessage):
				print("AI: ", last_message["messages"][0].content)






if __name__ == "__main__":
	main()


