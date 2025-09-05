from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from app.agents.chapter.chain import (
    generate_chapter,
    generate_chapter_feedback,
    edit_chapter,
)
from app.agents.chapter.model import ChapterOutput, ChapterFeedBack
from app.agents.story.chain import (
    generate_story_plan,
    generate_story_plan_feedback,
    edit_story_plan,
)
from app.agents.story.model import StoryPlan, StoryPlanFeedBack
from app.agents.chapter.model import FeedBack

import logging

logger = logging.getLogger(__name__)

MINIMUM_CHAPTER_SCORE = 7
MINIMUM_STORYPLAN_SCORE = 7

MAX_NUM_CHAPTER_EDIT = 2
MAX_NUM_STORYPLAN_EDIT = 4


class StoryPlanState(TypedDict):
    genre: str
    character_descriptions: str
    story_plan: StoryPlan
    cliche_feedback: FeedBack
    storyline_feedback: FeedBack
    character_feedback: FeedBack
    num_edits: int


class ChapterState(TypedDict):
    genre: str
    title: str
    character_descriptions: str
    previous_summary: str
    chapter_plot: str
    total_summary: str
    content: str
    cliche_feedback: FeedBack
    detail_feedback: FeedBack
    novelist_feedback: FeedBack
    num_edits: int


def chapter_node(state: ChapterState):
    chapter_output: ChapterOutput = generate_chapter(
        genre=state["genre"],
        title=state["title"],
        character_descriptions=state["character_descriptions"],
        previous_summary=state["previous_summary"],
        chapter_plot=state["chapter_plot"],
        total_summary=state["total_summary"],
    )
    logger.debug("original contents: %s", chapter_output.content)
    state["content"] = chapter_output.content
    return state


def chapter_feedback_node(state: ChapterState):
    logger.info("chapter feedback")

    feedback: ChapterFeedBack = generate_chapter_feedback(state["content"])
    state["cliche_feedback"] = feedback.cliche_feedback
    state["detail_feedback"] = feedback.detail_feedback
    state["novelist_feedback"] = feedback.novelist_feedback
    logger.debug("cliche feedback: %s", state["cliche_feedback"].reasoning)
    logger.debug("detail feedback: %s", state["detail_feedback"].reasoning)
    logger.debug("novelist feedback: %s", state["novelist_feedback"].reasoning)

    return state


def edit_chapter_node(state: ChapterState):
    chapter_output: ChapterOutput = edit_chapter(
        chapter_content=state["content"],
        cliche_feedback=state["cliche_feedback"],
        detail_feedback=state["detail_feedback"],
        novelist_feedback=state["novelist_feedback"],
    )
    logger.info("edited chapter content:")
    logger.debug("%s", chapter_output.chapter_name)
    logger.debug("----")
    logger.debug("%s", chapter_output.previous_summary)
    logger.debug("----")
    logger.debug("%s", chapter_output.content)
    logger.debug("----")

    state["content"] = chapter_output.content
    state["num_edits"] += 1
    return state


def storyplan_node(state: StoryPlanState):
    storyplan: StoryPlan = generate_story_plan(
        genre=state["genre"],
        character_descriptions=state["character_descriptions"],
    )
    logger.info("storyplan: %s", storyplan.summary)
    state["story_plan"] = storyplan
    return state


def storyplan_feedback_node(state: StoryPlanState):

    feedback: StoryPlanFeedBack = generate_story_plan_feedback(
        genre=state["genre"],
        story_plan=state["story_plan"],
    )

    logger.debug("cliche feedback: %s", feedback.cliche_feedback)
    logger.debug("storyline feedback: %s", feedback.storyline_feedback)
    logger.debug("character feedback: %s", feedback.character_feedback)
    state["cliche_feedback"] = feedback.cliche_feedback
    state["storyline_feedback"] = feedback.storyline_feedback
    state["character_feedback"] = feedback.character_feedback
    return state


def edit_storyplan_node(state: StoryPlanState):
    try:
        storyplan: StoryPlan = edit_story_plan(
            genre=state["genre"],
            story_plan=state["story_plan"],
            feedback=StoryPlanFeedBack(
                cliche_feedback=state["cliche_feedback"],
                storyline_feedback=state["storyline_feedback"],
                character_feedback=state["character_feedback"],
            ),
        )
        state["story_plan"] = storyplan
        state["num_edits"] += 1
        logger.info("storyplan edited: %s", storyplan.summary)
    except Exception as e:
        # Fallback: keep previous plan to avoid crashing the server
        logger.exception("edit_story_plan failed, using previous plan.")
    return state


def _evaluate_chapter_scores(
    cliche_feedback: FeedBack, detail_feedback: FeedBack, novelist_feedback: FeedBack
):
    return (cliche_feedback.score + detail_feedback.score + novelist_feedback.score) / 3


def should_continue_chapter_edit(state: ChapterState):
    score = _evaluate_chapter_scores(
        state["cliche_feedback"],
        state["detail_feedback"],
        state["novelist_feedback"],
    )
    if score < MINIMUM_CHAPTER_SCORE and state["num_edits"] < MAX_NUM_CHAPTER_EDIT:
        return "edit_chapter"
    else:
        return "__end__"


def _evaluate_storyplan_scores(
    cliche_feedback: FeedBack,
    storyline_feedback: FeedBack,
    character_feedback: FeedBack,
):
    return (
        cliche_feedback.score + storyline_feedback.score + character_feedback.score
    ) / 3


def should_continue_storyplan_edit(state: StoryPlanState):
    score = _evaluate_storyplan_scores(
        state["cliche_feedback"],
        state["storyline_feedback"],
        state["character_feedback"],
    )
    if score < MINIMUM_STORYPLAN_SCORE and state["num_edits"] < MAX_NUM_STORYPLAN_EDIT:
        return "edit_story_plan"
    else:
        return "__end__"


storyplan_workflow = StateGraph(StoryPlanState)
storyplan_workflow.add_node("generate_story_plan", storyplan_node)
storyplan_workflow.add_node("story_feedback", storyplan_feedback_node)
storyplan_workflow.add_node("edit_story_plan", edit_storyplan_node)

storyplan_workflow.add_edge(START, "generate_story_plan")
storyplan_workflow.add_edge("generate_story_plan", "story_feedback")
storyplan_workflow.add_conditional_edges(
    "story_feedback",
    should_continue_storyplan_edit,
    {"edit_story_plan": "edit_story_plan", "__end__": END},
)
storyplan_workflow.add_edge("edit_story_plan", "story_feedback")

storyplan_graph = storyplan_workflow.compile()

chapter_workflow = StateGraph(ChapterState)
chapter_workflow.add_node("generate_chapter", chapter_node)
chapter_workflow.add_node("chapter_feedback", chapter_feedback_node)
chapter_workflow.add_node("edit_chapter", edit_chapter_node)

chapter_workflow.add_edge(START, "generate_chapter")
chapter_workflow.add_edge("generate_chapter", "chapter_feedback")
chapter_workflow.add_conditional_edges(
    "chapter_feedback",
    should_continue_chapter_edit,
    {"edit_chapter": "edit_chapter", "__end__": END},
)
chapter_workflow.add_edge("edit_chapter", "chapter_feedback")

chapter_graph = chapter_workflow.compile()


if __name__ == "__main__":
    # visualize and save langgraph
    g = storyplan_graph.get_graph(xray=True)
    g.draw_png("storyplan.png")

    g = chapter_graph.get_graph(xray=True)
    g.draw_png("chapter.png")
