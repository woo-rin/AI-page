# -*- coding: utf-8 -*-
# === 3 & 4. 데이터 분석 및 피처 엔지니어링 (Phase 3 & 4) ===
# 설명: 전처리된 매매 데이터를 불러와서 AI가 학습할 수 있는 형태로 변환합니다.
# (문자 -> 숫자 변환, 가격 로그 변환 등)

import pandas as pd
import numpy as np
import os
import sys
from sklearn.preprocessing import LabelEncoder

# 파일명 설정 (매매용)
INPUT_FILE = 'apartment_sales_processed.csv'       # 전처리 완료된 파일
OUTPUT_FILE = 'apartment_sales_final_features.csv' # AI 학습용 최종 파일

def analyze_and_transform(df):
    print("--- 데이터 분석 및 변환 시작 ---")
    final_df = df.copy()

    # 1. 안전장치: 컬럼명 확인 및 수정
    # 이전 단계에서 '단지명'이 '아파트'로 안 바뀌었을 경우를 대비합니다.
    if '단지명' in final_df.columns and '아파트' not in final_df.columns:
        final_df = final_df.rename(columns={'단지명': '아파트'})
        print("  > [수정] '단지명' 컬럼을 '아파트'로 변경했습니다.")

    # 2. 타겟 변수(가격) 로그 변환
    # 아파트 가격은 단위가 매우 크기 때문에(억 단위), 로그 변환을 해줘야 AI가 잘 배웁니다.
    # np.log1p는 0이 들어와도 에러가 안 나도록 안전하게 변환해줍니다.
    final_df['log_거래금액'] = np.log1p(final_df['거래금액(만원)'])
    print("  > 가격 데이터 로그 변환 완료 (정규 분포화)")

    # 3. 범주형 변수 인코딩 (문자 -> 숫자)
    # AI는 '대치동', '자이' 같은 글자를 모릅니다. 숫자로 번호를 매겨줍니다.
    le = LabelEncoder()
    
    # (1) 법정동 인코딩
    final_df['법정동_인코딩'] = le.fit_transform(final_df['법정동'])
    print(f"  > '법정동' 인코딩 완료 (예: 대치동 -> 1, 삼성동 -> 2)")
    
    # (2) 아파트 인코딩
    final_df['아파트_인코딩'] = le.fit_transform(final_df['아파트'])
    print(f"  > '아파트' 인코딩 완료 (예: 래미안 -> 10, 힐스테이트 -> 20)")
    
    # 4. 불필요한 컬럼 제거
    # AI 학습에 방해되거나, 이미 숫자로 변환된 원본 글자 컬럼을 지웁니다.
    columns_to_drop = ['아파트', '단지명', '법정동', '거래금액(만원)', '계약일자']
    final_df = final_df.drop(columns=[col for col in columns_to_drop if col in final_df.columns], errors='ignore')
    
    # 5. 컬럼 순서 정리
    # 학습 데이터의 순서를 보기 좋게 정렬합니다.
    final_cols = [
        '전용면적(㎡)', '층', '건축년도', '아파트연식',  # 수치형 정보
        '법정동_인코딩', '아파트_인코딩',              # 범주형 정보 (숫자 변환됨)
        'log_거래금액'                                # 타겟 (정답)
    ]
    
    # 존재하는 컬럼만 선택해서 재배치
    available_cols = [c for c in final_cols if c in final_df.columns]
    final_df = final_df[available_cols]
    
    print("--- 데이터 분석 및 변환 완료 ---")
    return final_df

if __name__ == "__main__":
    # 1. 파일 존재 여부 확인
    if not os.path.exists(INPUT_FILE):
        print(f"[오류] '{INPUT_FILE}' 파일이 없습니다.")
        print(">>> '데이터전처리.py'를 먼저 실행해서 매매 데이터를 준비해주세요!")
        sys.exit(1)

    # 2. 데이터 로드 (Mac 한글 깨짐 방지)
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(INPUT_FILE, encoding='cp949')
        
    print(f"전처리된 데이터 로드 성공: {len(df)}건")
    
    # 3. 분석 및 변환 수행
    final_features_df = analyze_and_transform(df)
    
    # 4. 결과 저장
    final_features_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n[성공] AI 학습용 데이터가 저장되었습니다: '{OUTPUT_FILE}'")
    
    # 5. 데이터 미리보기
    print("\n--- 최종 데이터 미리보기 ---")
    print(final_features_df.head())
    print("\n이제 '데이터학습및평가.py'를 실행하여 AI 모델을 학습시키세요!")