시나리오: 사용자 요청이 들어오면, 한 스토리당 챕터를 15개 정도 생성해야한다. 이걸 전부 처리하기에는 비용이 많이 든다. 이걸 배치 처리로 구성해 비용을 절약한다.

사용자 요청 -> Story 생성 -> List[ChapterBatchRequest] 생성 
ChapterBatchRequest:
    story_id: str
    chapter_number: int
    previous_summary: str
    chapter_plot: str
    total_summary: str
    genre: str
    requested_deadline: datetime

scheduler -> List[ChapterBatchRequest]의 requested_deadline을 확인하여 batch 요청할 file에 추가. (file을 어떻게 구성할지는 추가 계획 필요) file에 추가한 후에는 file 추가되었음을 DB에 상태 업데이트
scheduler -> file 생성 후 일정 시간이 지나거나 file의 batch가 꽉 차게 되면 batch api 호출
scheduler -> batch api 결과는 바로 나오지 않으므로, polling하고 결과가 나온 값에 대해 db update
