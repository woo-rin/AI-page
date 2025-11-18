# 이 스크립트는 전처리된 데이터를 기반으로 모델 학습에 필요한 최종 특성을 생성합니다.
import pandas as pd
import numpy as np
import os
import sys
from sklearn.preprocessing import LabelEncoder

# 파일명 설정 (인코딩 문제 방지를 위해 'utf-8-sig' 사용)
INPUT_FILE = 'apartment_rent_processed.csv'
OUTPUT_FILE = 'apartment_rent_final_features.csv'

def feature_engineering(df):
    """
    모델 학습을 위해 파생 변수 생성, 타겟 변수 변환, 인코딩을 수행합니다.
    """
    print("--- 피처 엔지니어링 시작 ---")
    final_df = df.copy()

    # --- [수정] '아파트' 컬럼명 처리 (이전 단계 버그 대응) ---
    # '아파트' 컬럼이 비어있는(NaN) 경우, 인코딩 시 오류가 발생할 수 있습니다.
    # 또한 '단지명'이 '아파트'로 제대로 변경되었는지 다시 한번 확인합니다.
    if '아파트' not in final_df.columns and '단지명' in final_df.columns:
         final_df = final_df.rename(columns={'단지명': '아파트'})
         print("  > [수정] '단지명' -> '아파트'로 컬럼명 변경")
    
    # '아파트' 컬럼에 결측치가 있는지 확인 (이전 버그로 인해 발생 가능)
    if '아파트' in final_df.columns and final_df['아파트'].isnull().any():
        print("  > [경고] '아파트' 컬럼에 결측치가 있습니다. '기타'로 대체합니다.")
        final_df['아파트'] = final_df['아파트'].fillna('기타')
    # ---------------------------------------------------

    # ----------------------------------------------------
    # 단계 1: 타겟 변수 로그 변환 (왜도 해소)
    # ----------------------------------------------------
    print("\n[단계 1] 타겟 변수 로그 변환 및 전세 환산가 계산")
    
    # EDA(1-B)에서 확인했듯이, 보증금에 로그(log1p) 변환을 적용합니다.
    final_df['log_보증금'] = np.log1p(final_df['보증금(만원)'])
    print("  > '보증금(만원)'에 로그 변환 완료: 'log_보증금' 생성")

    # ----------------------------------------------------
    # 단계 2: 전세 환산가 계산 (전월세 스케일 통일)
    # ----------------------------------------------------
    # 월세는 보증금 + (월세 * 12개월 / 전월세 전환율)로 전세가와 유사한 스케일로 변환합니다.
    # 전월세 전환율 (임의로 5% 가정, 실제로는 지역/시점별로 다름)
    CONVERSION_RATE = 0.05 
    
    # 전세 환산가(만원) 계산
    final_df['전세환산가(만원)'] = np.where(
        final_df['전월세구분'] == '월세',
        final_df['보증금(만원)'] + (final_df['월세(만원)'] * 12 / CONVERSION_RATE),
        final_df['보증금(만원)'] # 전세는 그대로 보증금을 사용
    )
    print("  > '전세환산가(만원)' 생성 완료 (전월세 통합 가격)")

    # ----------------------------------------------------
    # 단계 3: 범주형 변수 인코딩
    # ----------------------------------------------------
    print("\n[단계 3] 범주형 변수 인코딩 (Label Encoding)")
    
    # '아파트'와 '법정동'은 모델이 학습할 수 있도록 숫자로 변환합니다.
    le = LabelEncoder()
    
    # '법정동' 인코딩
    final_df['법정동_인코딩'] = le.fit_transform(final_df['법정동'])
    print(f"  > '법정동' 인코딩 완료. 총 {len(le.classes_)}개의 고유 법정동")
    
    # '아파트' 인코딩
    final_df['아파트_인코딩'] = le.fit_transform(final_df['아파트'])
    print(f"  > '아파트' 인코딩 완료. 총 {len(le.classes_)}개의 고유 아파트 단지")
    
    # ----------------------------------------------------
    # 단계 4: 불필요한 원본 컬럼 제거
    # ----------------------------------------------------
    print("\n[단계 4] 불필요한 원본 컬럼 제거")
    
    columns_to_drop = [
        '아파트', '법정동', '전월세구분', '보증금(만원)', '월세(만원)', '계약일자', 
    ]
    
    final_df = final_df.drop(columns=[col for col in columns_to_drop if col in final_df.columns], errors='ignore')
    
    # 최종 컬럼 순서 조정 (보기 쉽게)
    final_cols = ['전용면적(㎡)', '층', '건축년도', '아파트연식', '법정동_인코딩', '아파트_인코딩', '전세환산가(만원)', 'log_보증금']
    final_df = final_df.reindex(columns=[col for col in final_cols if col in final_df.columns])
    
    print("\n--- 피처 엔지니어링 완료 ---")
    return final_df

if __name__ == "__main__":
    try:
        if not os.path.exists(INPUT_FILE):
            raise FileNotFoundError(f"'{INPUT_FILE}'을 찾을 수 없습니다.")
            
        # 🌟 한글 깨짐 방지를 위해 명시적으로 인코딩 지정 🌟
        processed_df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
        print(f"'{INPUT_FILE}' 로드 성공. (총 {len(processed_df)}건)")
        
        final_df = feature_engineering(processed_df)

        if final_df is not None:
            # 🌟 한글 깨짐 방지를 위해 명시적으로 인코딩 지정 🌟
            final_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
            print(f"\n피처 엔지니어링 완료된 데이터가 '{OUTPUT_FILE}' 파일로 저장되었습니다.")
            
            print("\n--- 최종 데이터 정보 요약 ---")
            final_df.info()
            print("\n--- 최종 데이터 샘플 (상위 5개) ---")
            print(final_df.head())

    except FileNotFoundError:
        print(f"\n[오류] '{INPUT_FILE}'을 찾을 수 없습니다.")
        print(">>> 'preprocessing.py' 파일을 먼저 실행하여 전처리된 데이터를 생성해주세요! <<<")
    except Exception as e:
        print(f"[오류] 피처 엔지니어링 중 문제 발생: {e}")
        sys.exit(1)