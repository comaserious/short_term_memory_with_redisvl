# RedisVL을 활용한 단기 기억 챗봇

## 📝 프로젝트 소개
이 프로젝트는 RedisVL과 OpenAI 임베딩 모델을 활용하여 여러 대화 스레드를 독립적으로 관리할 수 있는 단기 기억 챗봇 메모리 시스템을 구현한 예제입니다.

Jupyter Notebook (`redisvl_test.ipynb`)에 전체 구현 과정과 실행 예제가 포함되어 있습니다.

## ✨ 주요 기능
- **대화 기록 저장**: Redis JSON을 사용하여 각 대화의 메타데이터(발화자, 시간 등)와 내용을 저장합니다.
- **벡터 유사도 검색**: OpenAI 임베딩 모델(`text-embedding-3-small`)을 사용하여 대화 내용을 벡터로 변환하고, Redis의 벡터 검색 기능을 통해 유사한 대화 내용을 찾습니다.
- **멀티스레드 대화 관리**: `thread_id`를 기준으로 각 대화 세션을 분리하여 관리하므로, 여러 사용자의 대화를 동시에 처리할 수 있습니다.

## ⚙️ 사전 준비
- Python 3.8 이상
- Docker
- OpenAI API 키

## 🚀 실행 방법

### 1. Redis Stack 실행
이 프로젝트는 Redis Search 기능을 사용하므로 Redis Stack 서버가 필요합니다. Docker를 사용하여 간편하게 실행할 수 있습니다.

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 -p 30000:30000 redis/redis-stack:latest
```
> **Note**: Jupyter Notebook의 Redis 접속 포트가 `30000`으로 설정되어 있어, `-p 30000:30000` 옵션을 추가했습니다.

### 2. 프로젝트 설정
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
# Windows
# venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

# 필요 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정
OpenAI API 키를 설정해야 합니다. 프로젝트 루트에 `.env` 파일을 생성하고, 내부에 자신의 API 키를 입력하세요.

**`.env` 파일 예시:**
```
OPENAI_API_KEY="sk-..."
```

### 4. Jupyter Notebook 실행
Jupyter Notebook을 실행하여 `redisvl_test.ipynb` 파일을 열고, 각 셀을 순서대로 실행하며 작동 방식을 확인할 수 있습니다.

```bash
jupyter notebook
```

## 📜 코드 핵심 설명

### Redis 인덱스 스키마 (`schema`)
Redis Search 인덱스의 구조를 정의합니다. 대화 기록을 저장하기 위해 다음과 같은 필드를 포함합니다.
- `thread_id`: 대화를 구분하는 ID (Tag)
- `role`: 메시지 발화자 - 'user' 또는 'bot' (Tag)
- `content`: 실제 대화 내용 (Text)
- `timestamp`: 대화 순서 정렬을 위한 시간 (Numeric)
- `embedding`: `content`를 벡터로 변환한 값 (Vector)

### `ConversationMemory` 클래스
대화 기록을 관리하는 핵심 클래스입니다.
- `__init__(self, thread_id, redis_url)`: `thread_id`를 기반으로 대화 세션을 초기화하고 Redis에 연결합니다. 인덱스가 없으면 스키마에 따라 새로 생성합니다.
- `add_message(self, role, content)`: 사용자와 봇의 메시지를 받아 임베딩을 생성하고 Redis에 저장합니다.
- `search_similar_messages(self, query, top_k)`: 주어진 질문(query)과 가장 유사한 대화 기록을 `top_k` 개수만큼 찾아 반환합니다. `thread_id`로 필터링하여 현재 대화 내에서만 검색합니다.
