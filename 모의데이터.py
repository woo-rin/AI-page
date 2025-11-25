import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
import os

# === 설정값 ===
# 🚨 인증키: 이전에 확인된 유효한 키를 사용합니다.
SERVICE_KEY = "b24b18c2d2d6837e656f5ad4d6ee8de5dac06625be270c294842f3aeaafa94c6"

# 수집할 지역 및 기간 설정
LAWD_CD = '11680'  # 서울 강남구
DEAL_YMS = ['202401', '202402', '202403']  # 3개월치 데이터 수집

OUTPUT_FILE = 'apartment_rent_raw_data.csv' # 파이프라인 연결을 위해 이 이름 고정
API_URL = "https://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSDataLink/getAptRentRow"

def fetch_data(deal_ym):
    """특정 년월의 데이터를 API로 요청합니다."""
    params = {
        'serviceKey': SERVICE_KEY,
        'LAWD_CD': LAWD_CD,
        'DEAL_YMD': deal_ym
    }
    
    try:
        # 타임아웃 10초 설정
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        # XML 파싱
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        
        data_list = []
        for item in items:
            row = {}
            for child in item:
                # 태그 이름과 값을 딕셔너리에 저장
                row[child.tag] = child.text.strip() if child.text else None
            data_list.append(row)
            
        return data_list
        
    except Exception as e:
        print(f"[오류] {deal_ym} 데이터 수집 실패: {e}")
        return []

def main():
    print(f"--- 실제 데이터 수집 시작 (지역코드: {LAWD_CD}) ---")
    all_data = []

    for ym in DEAL_YMS:
        print(f" > {ym} 기간 데이터 요청 중...", end=" ")
        monthly_data = fetch_data(ym)
        print(f"성공 ({len(monthly_data)}건)")
        all_data.extend(monthly_data)
        time.sleep(1) # 서버 부하 방지용 대기

    if not all_data:
        print("[경고] 수집된 데이터가 없습니다. 네트워크 상태나 API 키를 확인해주세요.")
        return

    # 데이터프레임 생성
    df = pd.DataFrame(all_data)
    
    # 저장
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n[완료] 총 {len(df)}건의 실제 데이터를 '{OUTPUT_FILE}'로 저장했습니다.")
    print(f"저장 위치: {os.path.abspath(OUTPUT_FILE)}")
    
    # 데이터 미리보기
    print("\n--- 수집된 데이터 샘플 ---")
    print(df[['단지명', '보증금액', '월세금', '전용면적', '층']].head())

if __name__ == "__main__":
    main()