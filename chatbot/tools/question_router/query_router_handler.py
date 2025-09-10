from redisvl.extensions.router import Route, SemanticRouter
from redisvl.utils.vectorize import OpenAITextVectorizer
import os

web = Route(
    name = "web_search",
    references = [
        "오늘 서울 날씨 어때?",
        "지금 코스피 지수 알려줘",
        "어젯밤 프리미어리그 경기 결과가 어떻게 됐어?",
        "현재 상영 중인 영화 순위 좀 알려줄래?",
        "가장 최근의 국제 뉴스 헤드라인은 뭐야?",
        "세종대왕의 업적에 대해 알려줘",
        "블록체인이란 무엇인가요?",
        "에펠탑의 높이는 몇 미터야?",
        "대한민국의 초대 대통령은 누구였지?",
        "라마단 기간에 대해 설명해줘",
        "김치찌개 맛있게 끓이는 법",
        "컴퓨터 화면 캡쳐하는 방법 알려줘",
        "타이어 교체는 어떻게 해?",
        "파이썬으로 웹 크롤러 만드는 법",
        "운동화 끈 안 풀리게 묶는 팁 있어?",
        "가성비 좋은 노트북 추천해줘",
        "강남역 근처 맛집 알려줄래?",
        "영화 '파묘'에 대한 사람들 평이 어때?",
        "서울에서 아이와 함께 가볼 만한 곳",
        "2024년 최신 스마트폰 비교 정보 좀 찾아줘",
        "양자역학의 불확정성 원리에 대해 설명해줘",
        "조선왕조실록에 기록된 특이한 사건들",
        "인공지능의 트랜스포머 모델은 어떻게 작동해?",
        "고대 로마의 수도 시설에 대해 알려줘",
        "지구 온난화가 해양 생태계에 미치는 영향",
    ],
    metadata = {"category" : "web_search"},
    distance_threshold = 0.6
)

class QueryRouterHandler:
    def __init__(self, redis_url : str):
        self.oai = OpenAITextVectorizer(
            model = "text-embedding-3-small",
            api_config = {"api_key" : os.getenv("OPENAI_API_KEY")}
        )
        self.router = SemanticRouter(
            name = "query_router",
            vectorizer = self.oai,
            routes = [web],
            redis_url = redis_url
        )

    def route(self, question : str):
        route_match = self.router(question)
        return route_match.name



