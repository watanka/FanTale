from app.agents.story.prompt import (
    story_plan_generation_prompt,
    story_plan_feedback_edition_prompt,
    story_plan_feedback_prompt,
    plan_feedback_edition_parser,
    plan_feedback_parser,
    plan_parser,
)
from app.agents.utils import format_feedback
from app.agents.story.model import StoryPlan, StoryPlanFeedBack
from app.agents.llm import chat_model

story_plan_chain = story_plan_generation_prompt | chat_model | plan_parser
story_plan_feedback_chain = (
    story_plan_feedback_prompt | chat_model | plan_feedback_parser
)
story_plan_feedback_edition_chain = (
    story_plan_feedback_edition_prompt | chat_model | plan_feedback_edition_parser
)


def generate_story_plan(genre: str, character_descriptions: str) -> StoryPlan:
    """스토리 전체 계획(StoryPlan)을 생성한다."""
    plan: StoryPlan = story_plan_chain.invoke(
        {
            "genre": genre,
            "character_descriptions": character_descriptions,
        }
    )
    return plan


def generate_story_plan_feedback(genre: str, story_plan: StoryPlan):
    feedback: StoryPlanFeedBack = story_plan_feedback_chain.invoke(
        {
            "genre": genre,
            "story_plan": story_plan.to_str(),
        }
    )
    return feedback


def edit_story_plan(
    genre: str, story_plan: StoryPlan, feedback: StoryPlanFeedBack
) -> StoryPlan:

    edited_plan: StoryPlan = story_plan_feedback_edition_chain.invoke(
        {
            "genre": genre,
            "story_plan": story_plan.to_str(),
            "cliche_feedback": format_feedback(feedback.cliche_feedback),
            "storyline_feedback": format_feedback(feedback.storyline_feedback),
            "character_feedback": format_feedback(feedback.character_feedback),
        }
    )
    return edited_plan
