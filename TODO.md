- [ ] 에피소드 퀄리티 개선
    - [ ] 에이전트 구성
- [ ] 에피소드 생성 파라미터 정의
    - 에피소드 당 글자 수: 토큰 수
    - 

1. 사용자 인풋(genre, idols)으로 `generate_plot`
2. meta, episode_summaries 생성
3. meta, episode_summaries/episode_{num}.xml 기반으로 다음 episode 생성

- UI 개선. 다크모드
- 스토리 생성 진행 상태에 대한 정의 필요
- llm batch api 사용해서 비용 절약하기
    - story_plan 생성 -> story_plan 피드백 -> story_plan 수정
    - story_plan 기반으로 chapter 생성 -> chapter 피드백 -> chapter 수정, 다음 챕터에 previous_summary 제공

    - 첫 3화는 바로 생성. 나머지는 batch로 생성
    - 스토리 생성 요청 -> 큐에 삽입 -> 일정량 모이면 batch_api 호출
    - 병렬로 처리할 수 있는 부분: 서로 다른 스토리일 경우
    - 
- 결말이 흐지부지되는 경우
- 줄거리에 모든 내용이 다 담기면 안됨. 예고편 같은 느낌으로 나와야함