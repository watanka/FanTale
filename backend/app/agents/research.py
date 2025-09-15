"""
Idol Research Agent - Independent Graph Module
Provides character research functionality for story generation
"""

import os
import json
from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.checkpoint.memory import InMemorySaver

import logging

logger = logging.getLogger(__name__)

# Configuration
class ResearchConfig:
    MEMORY_FILE = "research_memory.json"
    LLM_MODEL = "gpt-4o-mini"
    LLM_TEMPERATURE = 0.3
    SEARCH_RESULTS_LIMIT = 3

# Initialize environment and tools
def initialize_research_tools():
    """Initialize research tools and model"""
    load_dotenv()
    
    for key in ["OPENAI_API_KEY", "TAVILY_API_KEY"]:
        if os.getenv(key):
            os.environ[key] = os.getenv(key)
    
    model = ChatOpenAI(
        model=ResearchConfig.LLM_MODEL, 
        temperature=ResearchConfig.LLM_TEMPERATURE
    )
    search_tool = TavilySearchResults(max_results=ResearchConfig.SEARCH_RESULTS_LIMIT)
    
    return model, search_tool, [search_tool]

# Data Models
class ResearchState(TypedDict):
    """Research agent state"""
    messages: Annotated[list, add_messages]
    idol_name: str
    search_phase: str  # "member_names" or "member_details"
    member_names: List[str]
    collected_info: str
    iteration: int

class CharacterProfile(BaseModel):
    """Character profile for story generation"""
    name: str = Field(description="캐릭터 이름")
    personality: str = Field(description="성격 특징")
    background: str = Field(description="배경 정보")
    relationships: str = Field(description="다른 캐릭터와의 관계", default="")

class ResearchResult(BaseModel):
    """Research result containing character profiles"""
    idol_group: str = Field(description="아이돌 그룹명")
    character_profiles: List[CharacterProfile] = Field(description="캐릭터 프로필 목록")
    summary: str = Field(description="전체 요약")

# Memory Manager
class ResearchMemoryManager:
    """Research memory management"""
    
    def __init__(self):
        self.memory_file = ResearchConfig.MEMORY_FILE
        self.data = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load research memory: {e}")
        return {}
    
    def save_research_result(self, idol_name: str, result: ResearchResult):
        """Save research result to memory"""
        self.data[idol_name] = {
            "result": result.dict(),
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save research memory: {e}")
    
    def get_research_result(self, idol_name: str) -> ResearchResult:
        """Get cached research result if available"""
        if idol_name in self.data:
            try:
                result_data = self.data[idol_name]["result"]
                return ResearchResult(**result_data)
            except Exception as e:
                logger.error(f"Failed to load cached result: {e}")
        return None

# Graph Nodes
class ResearchNodes:
    """Research graph node implementations"""
    
    def __init__(self, model: ChatOpenAI, tools: List):
        self.model = model
        self.tools = tools
        self.memory_manager = ResearchMemoryManager()
    
    def research_coordinator(self, state: ResearchState) -> ResearchState:
        """Research coordinator - generates search queries"""
        logger.info(f"Research Coordinator - Phase: {state['search_phase']}, Iteration: {state['iteration']}")
        
        if state['search_phase'] == "member_names":
            # First phase: find member names
            search_query = f"{state['idol_name']} members names list"
            
        else:
            # Second phase: search individual members
            if state['iteration'] <= len(state['member_names']):
                current_member = state['member_names'][state['iteration'] - 1]
                search_query = f"{state['idol_name']} {current_member} personality profile characteristics"
            else:
                # All members searched, end
                return state
        
        # Create tool call
        tool_call = {
            "name": "tavily_search_results_json",
            "args": {"query": search_query},
            "id": f"search_{state['iteration']}"
        }
        
        ai_message = AIMessage(
            content=f"검색 실행: {search_query}",
            tool_calls=[tool_call]
        )
        
        state['messages'].append(ai_message)
        return state
    
    def summary_node(self, state: ResearchState) -> ResearchState:
        """Summarize search results and update state"""
        logger.info("Processing search results")
        
        # Extract search results from last tool message
        search_results = []
        for msg in reversed(state['messages']):
            if isinstance(msg, ToolMessage):
                try:
                    results = json.loads(msg.content)
                    if isinstance(results, list):
                        search_results = results
                        break
                except:
                    continue
        
        if not search_results:
            return state
        
        # Process results based on phase
        if state['search_phase'] == "member_names":
            # Extract member names using LLM
            results_text = "\n".join([
                f"- {r.get('title', '')}: {r.get('content', '')[:200]}" 
                for r in search_results
            ])
            
            prompt = f"""
다음 검색 결과에서 {state['idol_name']} 그룹의 멤버 이름들을 추출해주세요.
각 멤버의 이름만 콤마로 구분해서 나열해주세요.

검색 결과:
{results_text}

멤버 이름들:
"""
            
            response = self.model.invoke([HumanMessage(content=prompt)])
            member_names_text = response.content.strip()
            
            # Parse member names
            member_names = [name.strip() for name in member_names_text.split(',') if name.strip()]
            state['member_names'] = member_names
            state['search_phase'] = "member_details"
            state['iteration'] = 1
            
            logger.info(f"Found members: {member_names}")
            
        else:
            # Summarize member details
            results_text = "\n".join([
                f"{r.get('title', '')}: {r.get('content', '')}" 
                for r in search_results
            ])
            
            current_member = state['member_names'][state['iteration'] - 1] if state['iteration'] <= len(state['member_names']) else "Unknown"
            
            prompt = f"""
다음은 {current_member}에 대한 검색 결과입니다. 
팬픽션 캐릭터로 활용할 수 있도록 다음 형식으로 요약해주세요:

성격: (주요 성격 특징 3-4가지)
배경: (출생, 경력, 특기 등)
매력포인트: (팬들이 좋아하는 특징)

검색 결과:
{results_text}

요약:
"""
            
            response = self.model.invoke([HumanMessage(content=prompt)])
            summary = response.content.strip()
            
            # Add to collected info
            state['collected_info'] += f"\n\n[{current_member}]\n{summary}"
            
            logger.info(f"Summarized {current_member}")
            
            # Move to next member
            state['iteration'] += 1
        
        return state
    
    def should_continue(self, state: ResearchState) -> str:
        """Decide next action"""
        if state['search_phase'] == "member_names":
            if state['member_names']:
                return "coordinator"  # Start member details phase
            else:
                return END
        
        elif state['search_phase'] == "member_details":
            if state['iteration'] <= len(state['member_names']):
                return "coordinator"  # Continue with next member
            else:
                return END  # All members processed
        
        return END

# Graph Builder
class ResearchGraphBuilder:
    """Research graph builder"""
    
    def __init__(self):
        self.model, self.search_tool, self.tools = initialize_research_tools()
        self.nodes = ResearchNodes(self.model, self.tools)
    
    def create_graph(self):
        """Create research graph"""
        graph_builder = StateGraph(ResearchState)
        
        # Add nodes
        tool_node = ToolNode(tools=self.tools)
        graph_builder.add_node("coordinator", self.nodes.research_coordinator)
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_node("summary", self.nodes.summary_node)
        
        # Add edges
        graph_builder.add_edge(START, "coordinator")
        graph_builder.add_edge("coordinator", "tools")
        graph_builder.add_edge("tools", "summary")
        graph_builder.add_conditional_edges(
            "summary",
            self.nodes.should_continue,
            {"coordinator": "coordinator", END: END}
        )
        
        return graph_builder.compile(checkpointer=InMemorySaver())

# Graph Creation Function
def create_research_graph():
    """
    Create and return the research graph
    
    Returns:
        Compiled research graph
    """
    graph_builder = ResearchGraphBuilder()
    return graph_builder.create_graph()

# Helper function to create initial state
def create_research_initial_state(idol_name: str) -> ResearchState:
    """
    Create initial state for research graph
    
    Args:
        idol_name: Name of the idol group to research
        
    Returns:
        Initial research state
    """
    return ResearchState(
        messages=[HumanMessage(content=f"Research {idol_name}")],
        idol_name=idol_name,
        search_phase="member_names",
        member_names=[],
        collected_info="",
        iteration=1
    )

# Helper function to format final result
def format_research_result(final_state: ResearchState) -> str:
    """
    Format final research state into character descriptions
    
    Args:
        final_state: Final state from research graph
        
    Returns:
        Formatted character descriptions
    """
    try:
        # Create research result
        character_profiles = _parse_character_profiles(
            final_state['member_names'], 
            final_state['collected_info']
        )
        
        research_result = ResearchResult(
            idol_group=final_state['idol_name'],
            character_profiles=character_profiles,
            summary=f"{final_state['idol_name']} 그룹 {len(character_profiles)}명의 캐릭터 프로필"
        )
        
        # Save to memory
        memory_manager = ResearchMemoryManager()
        memory_manager.save_research_result(final_state['idol_name'], research_result)
        
        return _format_character_descriptions(research_result)
        
    except Exception as e:
        logger.error(f"Failed to format research result: {e}")
        return f"연구 실패: {final_state['idol_name']}에 대한 정보를 수집할 수 없습니다."

def _parse_character_profiles(member_names: List[str], collected_info: str) -> List[CharacterProfile]:
    """Parse collected info into character profiles"""
    profiles = []
    
    # Split by member sections
    sections = collected_info.split('\n\n[')
    
    for i, member_name in enumerate(member_names):
        # Find corresponding section
        member_info = ""
        for section in sections:
            if section.startswith(member_name) or section.startswith(f"[{member_name}"):
                member_info = section.replace(f"[{member_name}]", "").strip()
                break
        
        if not member_info and i < len(sections) - 1:
            member_info = sections[i + 1].strip()
        
        # Extract personality and background
        personality = ""
        background = ""
        
        lines = member_info.split('\n')
        for line in lines:
            if line.startswith('성격:'):
                personality = line.replace('성격:', '').strip()
            elif line.startswith('배경:'):
                background = line.replace('배경:', '').strip()
        
        if not personality:
            personality = member_info[:100] + "..." if len(member_info) > 100 else member_info
        
        profiles.append(CharacterProfile(
            name=member_name,
            personality=personality or f"{member_name}의 독특한 매력과 개성",
            background=background or f"{member_name}의 배경 정보"
        ))
    
    return profiles

def _format_character_descriptions(research_result: ResearchResult) -> str:
    """Format research result for story generation"""
    descriptions = []
    
    for profile in research_result.character_profiles:
        description = f"""
{profile.name}:
- 성격: {profile.personality}
- 배경: {profile.background}
"""
        descriptions.append(description.strip())
    
    return f"{research_result.idol_group} 멤버들:\n\n" + "\n\n".join(descriptions)

# Test function
if __name__ == "__main__":
    # Test the graph directly
    graph = create_research_graph()
    initial_state = create_research_initial_state("에스파")
    
    config = {"configurable": {"thread_id": "research_에스파"}}
    final_state = graph.invoke(initial_state, config)
    
    result = format_research_result(final_state)
    print(result)
