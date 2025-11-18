import pandas as pd
import numpy as np
import random
import os

# --- 설정값 ---
NUM_ROWS = 2000 # 생성할 데이터 행의 수
OUTPUT_FILENAME = 'apartment_rent_raw_data.csv'

def create_mock_data(num_rows=1000):
    """
    아파트 전월세 실거래가 데이터를 모방한 가상 데이터를 생성합니다.
    실제 국토교통부 API의 컬럼 구조를 따릅니다.
    """
    
    # 지역 및 아파트 목록 설정
    lawd_cd = '11680' # 강남구 법정동 코드
    districts = ['역삼동', '대치동', '삼성동', '청담동', '압구정동']
    apartments = [f'강남_{i}차_아파트' for i in range(1, 10)] + ['타워팰리스', '아이파크', '래미안']
    
    data = []
    
    for _ in range(num_rows):
        # 기본 정보
        district = random.choice(districts)
        apt_name = random.choice(apartments)
        
        # 계약일자
        year = 2024
        month = random.randint(1, 3)
        day = random.randint(1, 28)
        
        # 건물 정보
        build_year = random.randint(1980, 2024)
        floor = random.randint(1, 45)
        area = round(random.uniform(50.0, 150.0), 2)
        
        # 거래 금액 (단위: 만원)
        is_jeonse = random.random() < 0.7 # 70%는 전세
        
        if is_jeonse:
            deposit = random.randint(30000, 150000)
            monthly_rent = 0
            # 전세는 갱신청구권 사용 여부 빈도 높임
            renewal_used = random.choice(['O', 'X', None])
        else:
            deposit = random.randint(1000, 5000)
            monthly_rent = random.randint(50, 300)
            renewal_used = random.choice(['O', 'X', None, None]) # 월세는 None 빈도 높임

        # 해제 여부 (5% 확률로 해제 발생)
        is_canceled = random.random() < 0.05
        cancel_date = f'{year}{month:02d}{day:02d}' if is_canceled else None

        row = {
            '갱신청구권사용여부': renewal_used,
            '단지명': apt_name,
            '법정동': district,
            '보증금액': f'{deposit:,}', # API 형식 모방 (콤마 포함)
            '건축년도': build_year,
            '월세금': f'{monthly_rent:,}', # API 형식 모방 (콤마 포함)
            '전용면적': area,
            '지번': f'{random.randint(100, 999)}',
            '지역코드': lawd_cd,
            '층': floor,
            '해제여부': 'O' if is_canceled else None,
            '해제사유발생일': cancel_date,
            '년': year,
            '월': month,
            '일': day
        }
        data.append(row)
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    # 1. 모의 데이터 생성
    raw_data_df = create_mock_data(num_rows=NUM_ROWS)
    
    # 2. CSV 파일로 저장 (Phase 1의 산출물)
    raw_data_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
    
    # 3. 결과 확인
    print(f"--- 모의 데이터 생성 완료 ---")
    print(f"총 {len(raw_data_df)}건의 데이터가 '{OUTPUT_FILENAME}' 파일로 저장되었습니다.")
    print(f"저장 위치: {os.path.abspath(OUTPUT_FILENAME)}")
    
    print("\n--- 데이터 샘플 (상위 5개) ---")
    print(raw_data_df.head())
    
    print("\n--- 데이터 정보 요약 ---")
    raw_data_df.info()