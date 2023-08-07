# swjungle-week-00
meditation center

- [figma link](https://www.figma.com/file/eS8ZOAd7RTTPHIzGj8Pw7V/WEEK00-7%EC%A1%B0?type=design&node-id=4%3A41&mode=design&t=SBkdoUYlEglZt8VT-1)

본 리포지토리는 openai API를 사용하여 사용자에게 가장 적합한 명상 세션을 도와주는 챗봇을 구현한 서비스입니다. 

챗봇은 로그한 유저에게 몇가지 질문을 던집니다. "당신의 현재 상태가 어떻게 됩니까?", "당신이 현재 이루고자 하는 목표가 있습니까?" 사용자는 그에 따른 응답을 제공할 수 있으며, 이를 기반으로 챗봇은 명상에 도움을 주는 음악과 명상법을 추천해줍니다.

대화내역은 데이터베이스에 기록되며, 유저는 과거의 대화를 다시 읽거나 응답 재생성이 가능합니다.

예시 화면 (figma)

<img width="449" alt="스크린샷 2023-08-07 오후 9 00 59" src="https://github.com/ChoiWheatley/swjungle-week-00/assets/18757823/e01b0743-cd56-42ad-92e1-8cb37a2841a0">

## 기술 스택

- Backend
  - flask: 웹 애플리케이션으로, 동적 웹 페이지 로딩과 사용자 인증, openai와의 상호작용을 담당합니다.
  - MongoDB: 챗봇과의 대화를 저장하고 추후에 다시 로드하거나 답변 regeneration을 통한 데이터 수정을 담당합니다.
- Frontend
  - Jinja2 Template: 동적으로 웹 페이지를 로드하는 데 사용되는 템플릿 파일입니다. 
  - Javascript: 챗봇과의 대화창을 컨트롤하기 위해 HTML Element를 다루어야 합니다. 이때 JS를 사용할 예정입니다.

## 협업툴

Github Issue & Github Pull Request

<img width="449" alt="github cat" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png">

> Why Github Issue?

깃허브 이슈를 활용하면 태그를 사용하여 버그, 기능추가, 할 일과 같은 다양한 관심사를 한 눈에 볼 수 있습니다. 커밋과 Pull Request를 자유롭게 링크하여 빠른 참조가 가능하며, 백링크 기능을 통해 해당 이슈를 언급한 다른 이슈나 PR, 커밋을 되짚어 올라갈 수도 있습니다.

> Why Github Pull Request?

PR은 여러명이 동시에 하나의 프로젝트를 수정하는 상황에서 발생할 수 있는 다양한 충돌을 main 브랜치가 아닌 개인 브랜치에서 해결하도록 강요하는 방법입니다. 따라서 main 브랜치는 항상 동작하는 코드만 올라올 수 있습니다. PR의 범위를 기능 하나로 축소하여 빠른 구현 이터레이션이 가능하며, 구현현황 체크가 용이해집니다.
