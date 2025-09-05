from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from app.agents.chapter.model import ChapterOutput, ChapterFeedBack

chapter_parser = PydanticOutputParser(pydantic_object=ChapterOutput)
chapter_feedback_parser = PydanticOutputParser(pydantic_object=ChapterFeedBack)
chapter_feedback_edition_parser = PydanticOutputParser(pydantic_object=ChapterOutput)

chapter_generation_prompt = PromptTemplate(
    input_variables=[
        "genre",
        "title",
        "character_descriptions",
        "previous_summary",
        "chapter_plot",
        "total_summary",
    ],
    partial_variables={"format_instructions": chapter_parser.get_format_instructions()},
    template="""
- 너는 유명한 {genre} 소설 작가야. 독자들이 열광하는 연재 소설의 한 챕터를 작성하고, previous_summary를 업데이트할꺼야. 소설 제목은 {title}이야.
- 챕터는 1500-2000자 정도의 텍스트로 구성할꺼야. 이번 챕터는 이전 갈등을 해소하거나 다음 갈등을 고조시키고, 마지막은 다음 챕터가 궁금해지도록 클리프행어로 마무리해줘.
- previous_summary에는 반드시 이전 챕터에서 서술된 갈등/단서가 포함되어야 해. 만약 비어있다면 첫 챕터이므로 chapter_plot과 total_summary만 참고하면 돼.
- 아래의 character_descriptions, previous_summary, chapter_plot(이번 회차 줄거리), total_summary(전체 줄거리)를 참고해서 챕터(content)를 작성하고, previous_summary를 업데이트해줘. 그리고 챕터 줄거리에 맞게 chapter_name을 작명해줘.
<background>
<character descriptions>
{character_descriptions}
</character descriptions>
<previous_summary>
{previous_summary}
</previous_summary>
<chapter_plot>
{chapter_plot}
</chapter_plot>
<total_summary>
{total_summary}
</total_summary>
</background>

응답 형식 지침:
- 아래 스키마에 맞는 JSON만 반환해. 다른 설명/접두사/마크업 없이 JSON 한 덩어리만 출력해.
{format_instructions}
    """,
)


chapter_feedback_prompt = PromptTemplate(
    input_variables=["chapter_content"],
    partial_variables={
        "format_instructions": chapter_feedback_parser.get_format_instructions()
    },
    template="""
<role & general instruction>
너는 소설 비평가야. 독자의 입장에서 chapter를 읽고 아주 신랄하게 피드백을 해줘. 글에 이미 있는 내용은 적지 말고, 어떻게 하면 글의 퀄리티를 개선할 수 있을지 피드백을 줘.
</role & general instruction>

<detail instruction>
- 피드백은 3가지로 구성되어야해. cliche_feedback, detail_feedback, novelist_feedback. 각 피드백은 0-10점 사이의 점수(score)와 그 이유를 설명하는 reasoning으로 구성되어야 해.
- cliche_feedback은 챕터에 사용된 캐릭터나 상황이 너무 일반적이거나 오그라드는 내용에 대한 피드백이야. 
- detail_feedback은 챕터에 담긴 내용 중 독자들이 좋아할만한 부분을 얘기해.
- novelist_feedback은 다른 소설가가 이 소설을 읽고 남긴 피드백을 얘기해
</detail instruction>

<chapter>
{chapter_content}
</chapter>

응답 형식 지침:
- 아래 스키마에 맞는 JSON만 반환해. 다른 설명/접두사/마크업 없이 JSON 한 덩어리만 출력해.
{format_instructions}
""",
)

chapter_feedback_edition_prompt = PromptTemplate(
    input_variables=[
        "chapter_content",
        "cliche_feedback",
        "detail_feedback",
        "novelist_feedback",
    ],
    partial_variables={
        "format_instructions": chapter_feedback_edition_parser.get_format_instructions()
    },
    template="""
<role & general instruction>
너는 세계 탑클래스 소설 작가야. chapter 내용과 아래 피드백을 기반으로 에피소드를 재작성해주고, 지금까지의 내용을 포함한 previous_summary를 업데이트해줘. 그리고 내용에 맞게 chapter_name도 작성해줘.
</role & general instruction>

<detail_instruction>
- cliche_feedback은 챕터에 사용된 캐릭터나 상황이 너무 일반적이거나 오그라드는 내용에 대한 피드백이야. 좀 더 부드럽고 자연스럽게 대화체를 다듬고 상황을 표현해줘.
- detail_feedback은 챕터에 담긴 내용 중 독자들이 좋아할만한 부분을 얘기해. 이 부분에 대해 더 상세하고 구체적으로 표현하면 소설의 퀄리티가 높아질꺼야.
- novelist_feedback은 다른 소설가가 이 소설을 읽고 남긴 피드백을 얘기해. 독자의 흥미를 이끌어낼 수 있도록 스토리의 기승전결에 더 집중해서 고치면 퀄리티를 개선할 수 있어.
- 이 피드백을 적극 반영해서 chapter 내용을 고쳐줘.
</detail_instruction>

<chapter>
{chapter_content}
</chapter>

<cliche_feedback>
{cliche_feedback}
</cliche_feedback>

<detail_feedback>
{detail_feedback}
</detail_feedback>

<novelist_feedback>
{novelist_feedback}
</novelist_feedback>

응답 형식 지침:
- 아래 스키마에 맞는 JSON만 반환해. 다른 설명/접두사/마크업 없이 JSON 한 덩어리만 출력해.
{format_instructions}
""",
)
