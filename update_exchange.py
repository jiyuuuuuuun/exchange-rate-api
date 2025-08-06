# update_exchange.py
# 필요한 패키지 설치: pip install python-dotenv requests
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()

# 한국은행 Open API 설정
API_KEY = os.getenv("EXCHANGE_RATE")
BASE_URL = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"

CURRENCY_CODES = {
    "미국 달러(USD)": "0000001",
    "일본 엔(JPY)": "0000002",
    "유로(EUR)": "0000003"
}

README_PATH = "README.md"

def get_exchange(currency_name, currency_code, date_str):
    """
    지정된 날짜(date_str)와 통화에 대해 한국은행 Open API에서 환율 정보를 가져옴
    date_str: "YYYYMMDD" 형식 문자열
    """
    params = {
        "authkey": API_KEY,
        "searchdate": date_str,
        "data": "AP01"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data:
            # 응답 JSON 구조에 맞게 필드명 확인 필요
            if item.get("cur_unit") == currency_name.split('(')[1][:-1]:  # 예: "USD"
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
    README.md 파일을 오늘과 어제 환율 정보로 업데이트
    """
    today_dt = datetime.now()
    yesterday_dt = today_dt - timedelta(days=1)

    today_str = today_dt.strftime("%Y%m%d")
    yesterday_str = yesterday_dt.strftime("%Y%m%d")

    exchange_info_today = []
    exchange_info_yesterday = []

    for name, code in CURRENCY_CODES.items():
        exchange_info_today.append(get_exchange(name, code, today_str))
        exchange_info_yesterday.append(get_exchange(name, code, yesterday_str))

    readme_content = f"""
# Exchange Rate API Status

이 리포지토리는 한국은행 Open API를 사용하여 주요 국가(미국, 일본, 유럽)의 환율 정보를 자동으로 업데이트합니다.

## 📅 오늘 환율 ({today_dt.strftime("%Y-%m-%d")})
> {'\n> '.join(exchange_info_today)}

## 📅 어제 환율 ({yesterday_dt.strftime("%Y-%m-%d")})
> {'\n> '.join(exchange_info_yesterday)}

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
