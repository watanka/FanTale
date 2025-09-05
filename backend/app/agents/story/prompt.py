from app.agents.story.model import StoryPlan, StoryPlanFeedBack
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

plan_parser = PydanticOutputParser(pydantic_object=StoryPlan)
plan_feedback_parser = PydanticOutputParser(pydantic_object=StoryPlanFeedBack)
plan_feedback_edition_parser = PydanticOutputParser(pydantic_object=StoryPlan)


story_plan_generation_prompt = PromptTemplate(
    input_variables=["genre", "character_descriptions"],
    partial_variables={"format_instructions": plan_parser.get_format_instructions()},
    template="""
<role & general instruction>
- 너는 유명한 {genre} 소설 작가야. 연재 소설의 아웃라인을 JSON으로 작성해줘.
- 아웃라인은 title, characters, summary(전체 줄거리), num_chapters, plots로 구성해야 해.
- plots는 10~15개의 챕터로 구성되고, 각 항목은 chapter_number와 content(해당 챕터 줄거리 요약)로 작성해.
- num_chapters는 plots의 수와 일치해야 해.
</role & general instruction>

<detailed instruction>
- characters는 주어진 character_descriptions를 참고해서 생성해줘. 해당 character description으르 좋아하는 팬들이 읽는 거니까, 최대한 벤치마킹해서 캐릭터들과 그 캐릭터들의 설명을 생성해줘. 그리고 캐릭터들의 이름은 캐릭터의 특성과 스토리 배경에 어울릴만하게 지어줘. 예를 들어, 중세 시대인데 캐릭터 이름이 "돌쇠"라면 어색한 이름이야.
- summary는 characters와 genre를 참고해서 작성해줘. 전체적으로 큰 기승전결이 있고, 각 에피소드마다 또 작은 기승전결의 흐름이 있어야 해.
- summary를 기반으로 각 에피소드마다의 줄거리를 작성해줘. 이 줄거리들에는 이전 에피소드의 갈등이 해결되고, 새로운 갈등이 발생하는 기승전의 흐름이 있어야해. 이 흐름이 항상 드라마틱할 필요는 없어. 그리고 항상 고조된 갈등을 해결하는데 15%정도의 에피소드를 할애해. 독자들은 완전 오픈된 엔딩보다는 확실한 갈등 해결과 에필로그와 복선을 좋아해.
- title은 전체 줄거리와 plot이 완성된 후, 내용에 알맞게 작성해줘. 장르에 알맞는 제목이면서 신비하고 너무 느끼하지 않은 제목이면 좋겠어.
</detailed instruction>

<background>
<character_description>
{character_descriptions}
</character_description>
</background>

응답 형식 지침:
- 아래 스키마에 맞는 JSON만 반환해. 다른 설명/접두사/마크업 없이 JSON 한 덩어리만 출력해.
{format_instructions}
""",
)

story_plan_feedback_prompt = PromptTemplate(
    input_variables=["genre", "story_plan"],
    partial_variables={
        "format_instructions": plan_feedback_parser.get_format_instructions()
    },
    template="""
<role & general instruction>
- 너는 엄청 유명한 {genre} 소설의 비평가야. 네가 하는 비평들은 사람들의 공감을 얻어. 주어진 소설의 아웃라인을 읽고, 다방면으로 비판적인 피드백을 제공해줘.
- 피드백은 cliche_feedback, storyline_feedback, character_feedback 구성되어야 해. 각 피드백은 0-10점 사이의 점수(score)와 그 이유를 설명하는 reasoning으로 구성되어야 해.
</role & general instruction>

<detailed instruction>
- cliche_feedback은 스토리 라인이 너무 진부하거나 느끼한 내용일 경우 비판적으로 제공하면 돼. 만약 너무 예상 가능하거나, 흐름이 부자연스러운 부분에 대해 지적해.
- 독자들이 몰입해서 읽기 위해서는 스토리라인에 자연스러운 기승전결이 필요해. 무조건 기승전결일 필요는 없지만, 독자들이 애간장을 타고 몰입할 수 있는 스토리 플롯이 필요해. storyline_feedback에는 이런 관점에서 이 스토리라인이 부족한 점을 지적해줘.
- 독자들은 극단적인 캐릭터보다는 입체적인 캐릭터를 좋아해. 예를 들어 완전 나쁜 놈, 완전 착하기만한 놈보다는 각자의 사연이 있고, 작중 대립/갈등 상황에 놓이지만, 독자 입장에서는 각자의 입장이 이해되는 걸 좋아해. character_feedback은 이런 관점에서 이 스토리라인이 부족한 점을 지적해줘.
<detailed instruction>

<storyline>
{story_plan}
</storyline>

응답 형식 지침:
- 아래 스키마에 맞는 JSON만 반환해. 다른 설명/접두사/마크업 없이 JSON 한 덩어리만 출력해.
{format_instructions}
""",
)


story_plan_feedback_edition_prompt = PromptTemplate(
    input_variables=[
        "genre",
        "story_plan",
        "cliche_feedback",
        "storyline_feedback",
        "character_feedback",
    ],
    partial_variables={"format_instructions": plan_parser.get_format_instructions()},
    template="""
<role & general instruction>
- 너는 유명한 {genre} 소설 작가야. 작성한 story_plan을 아래 피드백을 보고 개선해서 작성해줘. 
- 이 비판적인 피드백을 적극 반영해서 스토리 플랜을 개선하고, 독자들이 몰입해서 재밌게 읽을 수 있는 스토리 플랜을 작성해줘.
- 새로운 story_plan에는 title, characters, summary(전체 줄거리), num_chapters, plots로 구성되어야 해.
- plots는 10~15개의 챕터로 구성되고, 각 항목은 chapter_number와 content(해당 챕터 줄거리 요약)로 작성해.

</role & general instruction>

<background>
<story_plan>
{story_plan}
</story_plan>
<cliche_feedback>
{cliche_feedback}
</cliche_feedback>
<storyline_feedback>
{storyline_feedback}
</storyline_feedback>
<character_feedback>
{character_feedback}
</character_feedback>
</background>

응답 형식 지침:
- 아래 스키마에 맞는 JSON만 반환해. 다른 설명/접두사/마크업 없이 JSON 한 덩어리만 출력해.
{format_instructions}
""",
)
