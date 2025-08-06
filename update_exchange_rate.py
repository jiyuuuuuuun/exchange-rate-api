# update_exchange.py
# 필요한 패키지 설치: pip install python-dotenv requests
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()

# 한국은행 Open API 설정
API_KEY = os.getenv("EXCHANGE_RATE")
BASE_URL = "https://ecos.bok.or.kr/api/StatisticSearch"
FORMAT = "json"  # 응답 형식
LANG = "kr"      # 언어
START_COUNT = 1
END_COUNT = 100
STAT_CODE = "731Y001"  # 환율(매매 기준율) 통계표 코드
CYCLE = "D"            # 일별 데이터
TODAY = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")  # 오늘 날짜
CURRENCY_CODES = {
    "미국 달러(USD)": "0000001",
    "일본 엔(JPY)": "0000002",
    "유로(EUR)": "0000003"
}

# README 파일 경로
README_PATH = "README.md"

def get_exchange(currency_name, currency_code):
    """
    한국은행 Open API를 호출하여 지정된 통화의 환율 정보를 가져오는 함수
    """
    url = f"{BASE_URL}/{API_KEY}/{FORMAT}/{LANG}/{START_COUNT}/{END_COUNT}/{STAT_CODE}/{CYCLE}/{TODAY}/{TODAY}/{currency_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            value = data['StatisticSearch']['row'][0]['DATA_VALUE']
            return f"{currency_name}: {value} 원"
        except (KeyError, IndexError):
            return f"{currency_name}: 데이터를 찾을 수 없습니다."
    else:
        return f"{currency_name}: 요청 실패 (status {response.status_code})"

def update_readme():
    """
    README.md 파일을 환율 정보로 업데이트
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 통화별 환율 정보 수집
    exchange_info = []
    for name, code in CURRENCY_CODES.items():
        info = get_exchange(name, code)
        exchange_info.append(info)
    
    exchange_text = "\n> ".join(exchange_info)

    # README.md 내용 구성
    readme_content = f"""
# Exchange Rate API Status

이 리포지토리는 한국은행 Open API를 사용하여 주요 국가(미국, 일본, 유럽)의 환율 정보를 자동으로 업데이트합니다.

## 📊 오늘의 환율 (매매 기준율)
> {exchange_text}

⏳ 업데이트 시간: {now} (KST)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    # README.md 파일 쓰기
    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
