# === 2. 데이터 전처리 실행 스크립트 (수정본) ===
import pandas as pd
import numpy as np
import sys
import os 

# Input/Output 파일명 설정
INPUT_FILE = 'apartment_rent_raw_data.csv' 
OUTPUT_FILE = 'apartment_rent_processed.csv'

def preprocess_data(df):
    print("--- 전처리 시작 ---")
    proc_df = df.copy()
    
    # 1. 컬럼명 변경 ('단지명' -> '아파트'로 미리 변경)
    if '단지명' in proc_df.columns:
        proc_df = proc_df.rename(columns={'단지명': '아파트'})
    
    # 2. 금액 데이터 숫자 변환 (콤마 제거)
    proc_df['보증금(만원)'] = proc_df['보증금액'].astype(str).str.replace(',', '').str.strip().astype(int)
    proc_df['월세(만원)'] = proc_df['월세금'].astype(str).str.replace(',', '').str.strip().astype(int)
    
    # 3. 면적 데이터 변환
    # 원본 '전용면적'을 '전용면적(㎡)'라는 이름으로 새로 만듭니다.
    proc_df['전용면적(㎡)'] = proc_df['전용면적'].astype(float)
    
    # 4. 결측치 처리
    median_build_year = proc_df['건축년도'].median()
    proc_df['건축년도'] = proc_df['건축년도'].fillna(median_build_year)
    
    median_floor = proc_df['층'].median()
    proc_df['층'] = proc_df['층'].fillna(median_floor)
    
    # 5. 파생변수 생성
    proc_df['전월세구분'] = np.where(proc_df['월세(만원)'] == 0, '전세', '월세')
    
    # 날짜 처리
    proc_df['계약일자'] = pd.to_datetime(proc_df['년'].astype(str) + '-' +
                                       proc_df['월'].astype(str) + '-' +
                                       proc_df['일'].astype(str))
    
    proc_df['아파트연식'] = proc_df['년'].astype(int) - proc_df['건축년도'].astype(int)
    
    # 6. 타입 변환
    proc_df['건축년도'] = proc_df['건축년도'].astype(int)
    proc_df['층'] = proc_df['층'].astype(int)

    # 7. 최종 컬럼 선택 (오타 수정됨)
    # 여기에 있는 컬럼만 남기고 나머지는 버립니다.
    final_cols = [
        '아파트', '법정동', '전용면적(㎡)', '층', '건축년도', 
        '아파트연식', '전월세구분', '보증금(만원)', '월세(만원)', '계약일자'
    ]
    
    # 안전장치: 실제 존재하는 컬럼만 선택
    available_cols = [c for c in final_cols if c in proc_df.columns]
    proc_df = proc_df[available_cols]
    
    print("\n--- 전처리 완료 ---")
    return proc_df

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"[오류] '{INPUT_FILE}'이 없습니다. '모의데이터.py'를 먼저 실행하세요.")
        sys.exit(1)
        
    raw_df = pd.read_csv(INPUT_FILE)
    print(f"로드 성공: {len(raw_df)}건")
    
    processed_df = preprocess_data(raw_df)

    # 저장
    processed_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"저장 완료: '{OUTPUT_FILE}'")
    
    print("\n--- 결과 데이터 요약 ---")
    processed_df.info() # 여기가 비어있지 않아야 성공입니다!
    print(processed_df.head())