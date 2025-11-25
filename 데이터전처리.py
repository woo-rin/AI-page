import pandas as pd
import numpy as np
import sys
import os 

# 파일명 설정 (매매 데이터용)
INPUT_FILE = 'apartment_sales_raw_data.csv' 
OUTPUT_FILE = 'apartment_sales_processed.csv'

def preprocess_data(df):
    print("--- 매매 데이터 전처리 시작 ---")
    proc_df = df.copy()
    
    # 1. 컬럼명 변경 (안전장치)
    # 모의데이터 생성기에 따라 '단지명'으로 생성될 수도 있으므로 '아파트'로 통일합니다.
    if '단지명' in proc_df.columns:
        proc_df = proc_df.rename(columns={'단지명': '아파트'})
    
    # 2. 금액 데이터 숫자 변환 ('거래금액' 콤마 제거)
    # 문자열 "1,000,000" -> 정수 1000000 변환
    if '거래금액' in proc_df.columns:
        proc_df['거래금액(만원)'] = proc_df['거래금액'].astype(str).str.replace(',', '').str.strip().astype(int)
    
    # 3. 면적 데이터 변환
    proc_df['전용면적(㎡)'] = proc_df['전용면적'].astype(float)
    
    # 4. 결측치 처리 (중위값으로 대체)
    if '건축년도' in proc_df.columns:
        median_build_year = proc_df['건축년도'].median()
        proc_df['건축년도'] = proc_df['건축년도'].fillna(median_build_year)
    
    if '층' in proc_df.columns:
        median_floor = proc_df['층'].median()
        proc_df['층'] = proc_df['층'].fillna(median_floor)
    
    # 5. 파생변수 생성
    # 날짜 합치기 (년-월-일 -> 계약일자)
    proc_df['계약일자'] = pd.to_datetime(proc_df['년'].astype(str) + '-' +
                                       proc_df['월'].astype(str) + '-' +
                                       proc_df['일'].astype(str))
    
    # 아파트 연식 계산 (거래년도 - 건축년도)
    proc_df['아파트연식'] = proc_df['년'].astype(int) - proc_df['건축년도'].astype(int)
    
    # 6. 최종 컬럼 선택
    # 분석 및 학습에 필요한 핵심 컬럼만 남깁니다.
    final_cols = [
        '아파트', '법정동', '전용면적(㎡)', '층', '건축년도', 
        '아파트연식', '거래금액(만원)', '계약일자'
    ]
    
    # 실제 존재하는 컬럼만 선택 (오류 방지)
    available_cols = [c for c in final_cols if c in proc_df.columns]
    proc_df = proc_df[available_cols]
    
    print("\n--- 전처리 완료 ---")
    return proc_df

if __name__ == "__main__":
    # 파일 존재 여부 확인
    if not os.path.exists(INPUT_FILE):
        print(f"[오류] '{INPUT_FILE}' 파일이 없습니다.")
        print(" 먼저 '모의데이터.py'를 실행하여 매매 데이터를 생성해주세요.")
        sys.exit(1)
        
    # 데이터 로드
    raw_df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    print(f"원본 데이터 로드 성공: {len(raw_df)}건")
    
    # 전처리 수행
    processed_df = preprocess_data(raw_df)

    # 결과 저장
    processed_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"전처리 데이터 저장 완료: '{OUTPUT_FILE}'")
    
    print("\n--- 결과 데이터 요약 ---")
    processed_df.info()
    print("\n--- 데이터 샘플 ---")
    print(processed_df.head())