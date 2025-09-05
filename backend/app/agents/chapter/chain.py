from app.agents.llm import chat_model
from app.agents.chapter.model import ChapterOutput, ChapterFeedBack
from app.agents.chapter.prompt import (
    chapter_generation_prompt,
    chapter_feedback_prompt,
    chapter_feedback_edition_prompt,
    chapter_parser,
    chapter_feedback_parser,
    chapter_feedback_edition_parser,
)
from app.agents.utils import format_feedback

chapter_chain = chapter_generation_prompt | chat_model | chapter_parser
chapter_feedback_chain = chapter_feedback_prompt | chat_model | chapter_feedback_parser
chapter_feedback_edition_chain = (
    chapter_feedback_edition_prompt | chat_model | chapter_feedback_edition_parser
)


def generate_chapter(
    genre: str,
    title: str,
    character_descriptions: str,
    previous_summary: str,
    chapter_plot: str,
    total_summary: str,
) -> ChapterOutput:
    """단일 챕터(ChapterOutput)를 생성한다."""
    chapter: ChapterOutput = chapter_chain.invoke(
        {
            "genre": genre,
            "title": title,
            "character_descriptions": character_descriptions,
            "previous_summary": previous_summary,
            "chapter_plot": chapter_plot,
            "total_summary": total_summary,
        }
    )
    return chapter


def generate_chapter_feedback(chapter_content: str) -> ChapterFeedBack:
    """피드백을 생성한다."""
    feedback: ChapterFeedBack = chapter_feedback_chain.invoke(
        {
            "chapter_content": chapter_content,
        }
    )
    return feedback


def edit_chapter(
    chapter_content: str,
    cliche_feedback: str,
    detail_feedback: str,
    novelist_feedback: str,
) -> ChapterOutput:
    """피드백을 통한 챕터 개선"""
    edited_chapter: ChapterOutput = chapter_feedback_edition_chain.invoke(
        {
            "chapter_content": format_feedback(chapter_content),
            "cliche_feedback": format_feedback(cliche_feedback),
            "detail_feedback": format_feedback(detail_feedback),
            "novelist_feedback": format_feedback(novelist_feedback),
        }
    )
    return edited_chapter
