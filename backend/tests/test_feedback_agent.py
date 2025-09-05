from app.agents.graph import graph
from app.db.repository.story_repository import StoryRepository
from app.db.repository.chapter_repository import ChapterRepository
from app.db.repository.chapter_plot_repository import ChapterPlotRepository


def test_피드백_agent를_통해_결과가_향상되는지_확인한다():
    story_id = 1
    chapter_id = 1

    story_repository = StoryRepository()
    chapter_repository = ChapterRepository()
    chapter_plot_repository = ChapterPlotRepository()

    story = story_repository.get(story_id)
    chapter = chapter_repository.get(chapter_id)
    chapter_plot = chapter_plot_repository.get(chapter_id)

    previous_summary = chapter_plot.previous_summary if chapter_plot else ""
    print("original chapter content: ")
    print(chapter.content)

    edited_chapter = graph.invoke(
        {
            "genre": story.genre,
            "title": story.title,
            "character_descriptions": story.characters,
            "previous_summary": previous_summary,
            "chapter_plot": chapter_plot,
            "total_summary": story.summary,
            "content": chapter.content,
            "cliche_feedback": "",
            "detail_feedback": "",
            "novelist_feedback": "",
        }
    )
