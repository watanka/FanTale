from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
from app.agents.chapter.model import FeedBack


def _prettify(element: ET.Element) -> bytes:
    xml_bytes = ET.tostring(element, encoding="utf-8")
    dom = minidom.parseString(xml_bytes)
    return dom.toprettyxml(indent="  ", encoding="utf-8")


def parse_llm_output(xml_str: str) -> ET.Element:
    """llm에서 나온 xml 형태의 str 아웃풋을 필요한 정보들로 분리한다"""
    root = ET.fromstring(xml_str)
    title = root.find("title").text
    characters = "\n".join(
        ET.tostring(e, encoding="unicode") for e in root.find("characters").findall("p")
    )
    summary = root.find("summary").text
    plots = root.find("plots")
    episodes = plots.findall("episode")

    return title, characters, summary, episodes


def save_meta(title, characters, summary, save_name):

    meta_str = f"""<story>
    <title>{title}</title>
    <characters>
    {characters}
    </characters>
    <summary>
    {summary}
    </summary>
</story>
    """
    meta_root = ET.fromstring(meta_str)
    # save
    with open(save_name, "wb") as f:
        f.write(_prettify(meta_root))


def save_episode_summary(element: ET.Element, save_dir: Path):
    episode_number = element.findtext("episode_number")  # 태그 이름 확인 필요
    tree = ET.ElementTree(element)  # ElementTree로 감싸기
    save_path = f"{save_dir}/episode_{episode_number}.xml"
    tree.write(save_path, encoding="utf-8", xml_declaration=True)


def format_feedback(feedback: FeedBack):
    return f"score: {feedback.score}\nreasoning: {feedback.reasoning}"
