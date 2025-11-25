import pandas as pd
import numpy as np
import random
import os

# --- 설정값 ---
NUM_ROWS = 200000
OUTPUT_FILENAME = 'apartment_sales_raw_data.csv' # 매매 데이터용 파일명

def create_realistic_sales_data(num_rows=200000):
    """
    아파트 '매매' 실거래가를 모방한 데이터 생성
    (강남구 실제 시세 및 프리미엄 로직 반영)
    """
    # 1. 지역 및 입지 가중치 (강남구 주요 동네)
    districts = {
        '압구정동': 2.5, # 재건축 대장주 (가장 비쌈)
        '반포동': 2.3,   # 한강변 신축
        '대치동': 2.0,   # 학군 프리미엄
        '삼성동': 1.8,   # 개발 호재
        '도곡동': 1.6,   # 전통 부촌
        '역삼동': 1.3,   # 업무 지구
        '개포동': 1.4    # 신축 대단지
    }
    
    # 아파트 브랜드
    apt_brands = ['현대', '래미안', '자이', '힐스테이트', '아이파크', '푸르지오', '더샵', 'e편한세상', '아크로', '롯데캐슬']
    
    data = []
    
    for _ in range(num_rows):
        # 기본 정보 생성
        dong = random.choice(list(districts.keys()))
        brand = random.choice(apt_brands)
        apt_name = f"{dong} {brand}"
        
        # 층수 (1~45층)
        floor = random.randint(1, 45)
        
        # 전용면적 (평형대 모사: 25평, 34평, 40평, 50평)
        # 59.9(25평), 84.9(34평), 114.5(40평대), 135.8(50평대)
        area = random.choice([59.9, 84.9, 114.5, 135.8]) + round(random.uniform(-1, 1), 2)
        
        # 건축년도 (1980 ~ 2024)
        build_year = random.randint(1980, 2024)
        age = 2024 - build_year
        
        # --- 매매가 결정 로직 (단위: 만원) ---
        
        # 1. 기본 평당가 설정 (강남구 기준: 평당 6,000 ~ 1.2억 가정)
        # 3.3m^2 당 가격을 랜덤하게 설정하되, 동네(districts) 가중치를 곱함
        base_price_per_pyeong = random.randint(5000, 8000) 
        pyeong = area / 3.3
        
        # 기본 가격 = 평수 * 평당가 * 동네 가중치
        base_price = pyeong * base_price_per_pyeong * districts[dong]
        
        # 2. 연식에 따른 프리미엄 (U자형 곡선)
        if age <= 5:
            base_price *= 1.25 # 신축 프리미엄 (+25%)
        elif age >= 30:
            base_price *= 1.35 # 재건축 기대감 프리미엄 (+35%)
        elif age >= 15:
            base_price *= 0.9  # 애매한 구축 감가 (-10%)
            
        # 3. 층수 프리미엄 (고층일수록 비쌈)
        if floor >= 20:
            base_price += (floor * 300) # 고층 프리미엄
        elif floor <= 3:
            base_price -= 5000 # 저층 감가
        
        # 4. 랜덤 변동성 추가 (+- 1~2억원 차이)
        final_price = base_price + random.randint(-15000, 15000)
        
        # 최소 가격 방어 (10억 미만은 거의 없다고 가정)
        if final_price < 100000: final_price = 100000
        
        # 100만원 단위 절삭
        final_price = int(final_price / 100) * 100
        
        # 데이터 적재
        row = {
            '아파트': apt_name,
            '법정동': dong,
            '거래금액': f'{final_price:,}', # 콤마가 포함된 문자열 (API 원본 형태)
            '건축년도': build_year,
            '전용면적': round(area, 2),
            '층': floor,
            '년': 2024,
            '월': random.randint(1, 12),
            '일': random.randint(1, 28)
        }
        data.append(row)
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    # 데이터 생성
    df = create_realistic_sales_data(NUM_ROWS)
    
    # CSV 저장
    df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
    
    print(f"--- [매매] 가상 데이터 생성 완료 ---")
    print(f"생성된 데이터 수: {len(df)}건")
    print(f"저장 파일명: {OUTPUT_FILENAME}")
    print("\n[데이터 미리보기]")
    print(df.head())