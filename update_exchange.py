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
BASE_URL = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
# FORMAT = "json"  # 응답 형식
# LANG = "kr"      # 언어
# START_COUNT = 1
# END_COUNT = 100
# STAT_CODE = "731Y001"  # 환율(매매 기준율) 통계표 코드
# CYCLE = "D"            # 일별 데이터
TODAY = datetime.now().strftime("%Y%m%d")  # 오늘 날짜 "%Y-%m-%d  %H:%M:%S"
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
    params = {
        "authkey": API_KEY,
        "searchdate": TODAY,
        "data": "AP01"  # 환율 데이터 타입, API 문서 기준
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # API가 여러 환율을 한번에 반환하면 currency_code에 맞춰 필터링
        for item in data:
            # 여기서 item 필드명은 예시이므로 실제 응답에 맞게 변경 필요
            # 예를 들어 'cur_unit' 또는 'cur_cd' 같은 필드명일 수 있습니다.
            if item.get("cur_unit") == currency_name.split('(')[1][:-1]:  # ex) "USD"
                # 환율 정보 추출 (예: "deal_bas_r" 필드가 매매 기준율)
                value = item.get("deal_bas_r")
                if value:
                    return f"{currency_name}: {value} 원"
                else:
                    return f"{currency_name}: 환율 정보가 없습니다."
        return f"{currency_name}: 해당 통화 데이터가 없습니다."
    
    except requests.RequestException as e:
        return f"{currency_name}: 요청 실패 ({e})"
    except ValueError:
        return f"{currency_name}: 응답 JSON 파싱 실패"

def update_readme():
    """
    README.md 파일을 환율 정보로 업데이트
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    exchange_info = []
    for name, code in CURRENCY_CODES.items():
        info = get_exchange(name, code)
        exchange_info.append(info)
    
    exchange_text = "\n> ".join(exchange_info)

    readme_content = f"""
# Exchange Rate API Status

이 리포지토리는 한국은행 Open API를 사용하여 주요 국가(미국, 일본, 유럽)의 환율 정보를 자동으로 업데이트합니다.

## 📊 오늘의 환율 (매매 기준율)
> {exchange_text}

⏳ 업데이트 시간: {now} (KST)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()