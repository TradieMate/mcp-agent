from mcp import ListToolsResult
import streamlit as st
import asyncio
import os
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from dataclasses import dataclass
from typing import Optional, Type, TypeVar

T = TypeVar("T", bound=OpenAIAugmentedLLM)


@dataclass
class AgentState:
    """Container for agent and its associated LLM"""

    agent: Agent
    llm: Optional[OpenAIAugmentedLLM] = None


async def get_agent_state(
    key: str,
    agent_class: Type[Agent],
    llm_class: Optional[Type[T]] = None,
    **agent_kwargs,
) -> AgentState:
    """
    Get or create agent state, reinitializing connections if retrieved from session.

    Args:
        key: Session state key
        agent_class: Agent class to instantiate
        llm_class: Optional LLM class to attach
        **agent_kwargs: Arguments for agent instantiation
    """
    if key not in st.session_state:
        # Create new agent
        agent = agent_class(
            connection_persistence=False,
            **agent_kwargs,
        )
        await agent.initialize()

        # Attach LLM if specified
        llm = None
        if llm_class:
            llm = await agent.attach_llm(llm_class)

        state: AgentState = AgentState(agent=agent, llm=llm)
        st.session_state[key] = state
    else:
        state = st.session_state[key]

    return state


def format_list_tools_result(list_tools_result: ListToolsResult):
    res = ""
    for tool in list_tools_result.tools:
        res += f"- **{tool.name}**: {tool.description}\n\n"
    return res


async def main():
    await app.initialize()

    # Use the state management pattern
    state = await get_agent_state(
        key="finder_agent",
        agent_class=Agent,
        llm_class=OpenAIAugmentedLLM,
        name="finder",
        instruction="""You are an AI assistant with access to web search and SEO analysis capabilities.
        You can search the web using Tavily and perform SEO analysis using DataForSEO.
        Help users by searching for information, analyzing websites, and providing insights.""",
        server_names=["tavily", "dataforseo"],  # Web search and SEO analysis servers
    )

    tools = await state.agent.list_tools()
    tools_str = format_list_tools_result(tools)

    st.title("🤖 MCP Agent Chatbot")
    st.caption("🚀 A Streamlit chatbot powered by mcp-agent framework")
    
    # Add some info about the deployment
    st.sidebar.title("About")
    st.sidebar.info("""
    This is an MCP (Model Context Protocol) agent deployed on Render.
    
    The agent has access to web fetching capabilities and can help you with:
    - Fetching content from URLs
    - Answering questions
    - General assistance
    """)

    with st.expander("View Available Tools"):
        st.markdown(tools_str)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hello! I'm your MCP agent assistant. I can help you fetch information from the web and answer your questions. How can I help you today?"}
        ]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})

        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            response = ""
            with st.spinner("Thinking..."):
                # Pass the conversation history to the LLM
                conversation_history = st.session_state["messages"][
                    1:
                ]  # Skip the initial greeting

                response = await state.llm.generate_str(
                    message=prompt,
                    request_params=RequestParams(
                        use_history=True,
                        history=conversation_history,  # Pass the conversation history
                    ),
                )
            st.markdown(response)

        st.session_state["messages"].append({"role": "assistant", "content": response})


if __name__ == "__main__":
    # Configure Streamlit for deployment
    st.set_page_config(
        page_title="MCP Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    app = MCPApp(name="mcp_basic_agent")
    asyncio.run(main())