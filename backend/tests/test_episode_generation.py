from app.agents.story.chain import generate_chapter
from app.services.mappers import chapter_state_to_model
from app.db.repository.story_repository import StoryRepository
from app.db.repository.chapter_plot_repository import ChapterPlotRepository
from app.db.repository.chapter_repository import ChapterRepository
from datetime import datetime


def test_챕터를_작성하고_DB에_저장한다():
    story_id = 1
    story_repository = StoryRepository()
    chapter_repository = ChapterRepository()
    chapter_plot_repository = ChapterPlotRepository()

    story = story_repository.get(story_id)
    chapter_plots = chapter_plot_repository.list_by_story(story_id)

    genre = story.genre
    title = story.title
    character_descriptions = story.characters
    total_summary = story.summary

    previous_summary = ""
    for plot in chapter_plots:
        chapter_plot = plot.content

        ch = generate_chapter(
            genre=genre,
            title=title,
            character_descriptions=character_descriptions,
            previous_summary=previous_summary,
            chapter_plot=chapter_plot,
            total_summary=total_summary,
        )
        # 다음 챕터의 previous_summary 업데이트
        chapter_plot_repository.update(
            plot.id + 1, previous_summary=ch.previous_summary
        )
        previous_summary = ch.previous_summary
        # available_from 계산 로직
        available_from = datetime.now()
        chapter_model = chapter_state_to_model(
            story_id, plot.chapter_number, ch, available_from
        )
        chapter_id = chapter_repository.save(chapter_model)

        chapter = chapter_repository.get(chapter_id)

        print(f"{chapter.chapter_name}==============")
        print(chapter.content)
        print("==============")
