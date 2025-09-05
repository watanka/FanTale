from app.agents.story.chain import generate_story_plan
from app.db.repository import story_repository, summary_repository
import os
import pytest
from app.db.repository.story_repository import StoryRepository
from app.db.repository.chapter_plot_repository import ChapterPlotRepository

from app.services.mappers import story_item_to_model, chapterplot_item_to_model


def test_아이돌_정보를_검색한다():
    """
    스토리 플롯을 생성하기 위해 사용자가 선택한 아이돌 정보를 검색하고 요약한다.
    """
    keyword = "BTS"
    print(f"{keyword}에 대한 검색 결과\n")
    # print(search(keyword))


def test_스토리_플롯을_작성한다():
    story_repository = StoryRepository()
    chapter_plot_repository = ChapterPlotRepository()

    character_descriptions = """
Jin Personality: ugh he is beautiful inside and out, absolutely hilarious, works the hardest without complaining or bringing attention to it. I love how he maintains a cool head and doesn’t get worked up and also love how he never talks about himself. Physical: From forehead down to waist, perfection

Edit: Also today I came across a lot of Jin's puns from last night's muster and I've realised I never gave him credit for how witty & smart he is. Those puns are really good and he regularly comes up with them on the fly and its a travesty we don't get 90% of them until later!!

Namjoon Personality: How he can’t contain his excitement and always encouraging his members. Physical: hands and calves.

Yoongi Personality: haha how he talks a lot but people think he is quiet lol, also just being matter of fact about things. Physical: gummy smile

Hoseok Personality: his pride in his team. Have you noticed he never cringes at anything they create no matter how ridiculous. Physical: his swagger? And little dimple things around his lips and really happy smile. It’s so pure.

Jimin Personality: the way he cuddles and appreciates everyone and also shows concern openly like when people fall on stage, etc. Physical: Thighs

Taehyung Personality: how he never really clowns anyone? I mean my bias is Jin who is king of clowning and I love it but I don’t know it just makes V so pure. Also once Jin was asked what’s the cutest thing about every member and for Tae he said “how when he sees a member is down he quietly follows them around”. It just stuck with me and I love it. Physical - Nose and eye combination

Jungkook Personality:he is such a millennial meme kid and I love it. Physical: how his eyes sparkle and his pure bunny smile.
    """
    genre = "로맨스"
    plan = generate_story_plan(genre, character_descriptions)

    # plan의 Story 부분을 story에 저장
    # plan plots 부분을 ChapterPlot에 저장
    story_model = story_item_to_model(plan, user_id=1)
    story_id = story_repository.save(story_model)

    for item in plan.plots:
        chapter_plot_model = chapterplot_item_to_model(story_id, item)
        chapter_plot_repository.save(chapter_plot_model)

    story = story_repository.get(story_id)
    print(story.title, story.genre, story.characters, story.summary, story.num_chapters)
    chapter_plots = chapter_plot_repository.list_by_story(story_id)
    for chapter_plot in chapter_plots:
        print(chapter_plot.chapter_number, chapter_plot.content)
