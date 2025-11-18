# === 2. 데이터 전처리 실행 스크립트 (Phase 2) ===
# 이 스크립트는 'apartment_rent_raw_data.csv' 파일을 읽어와 전처리를 수행합니다.
import pandas as pd
import numpy as np
import sys
import os 

# Input/Output 파일명 설정
INPUT_FILE = 'apartment_rent_raw_data.csv' # 모의 데이터 생성기로 만든 파일
OUTPUT_FILE = 'apartment_rent_processed.csv' # 최종 전처리 결과 파일

def preprocess_data(df):
    """
    원본 데이터프레임(CSV)을 전처리하여 모델 학습에 적합한 형태로 변환합니다.
    """
    print("--- 전처리 시작 ---")
    proc_df = df.copy()
    
    # ----------------------------------------------------
    # 단계 1: 데이터 클리닝 및 결측치 처리
    # ----------------------------------------------------
    print("\n[단계 1] 데이터 클리닝 및 결측치 처리 시작")
    print("  > 결측치 처리 전 상태:")
    print(proc_df.isnull().sum()) 
    
    # '보증금액' 및 '월세금'의 콤마(,)와 공백을 제거하고 숫자형으로 변환합니다.
    proc_df['보증금(만원)'] = proc_df['보증금액'].astype(str).str.replace(',', '').str.strip().astype(int)
    proc_df['월세(만원)'] = proc_df['월세금'].astype(str).str.replace(',', '').str.strip().astype(int)
    
    # '전용면적'을 float 타입으로 변환합니다.
    proc_df['전용면적(㎡)'] = proc_df['전용면적'].astype(float)
    
    # '건축년도' 결측치 처리: 중위값으로 채웁니다.
    median_build_year = proc_df['건축년도'].median()
    proc_df['건축년도'].fillna(median_build_year, inplace=True)
    print(f"  > '건축년도' 결측치를 중위값({median_build_year:.0f})으로 채웠습니다.")
    
    # '층' 결측치 처리: 중위값으로 채웁니다.
    median_floor = proc_df['층'].median()
    proc_df['층'].fillna(median_floor, inplace=True)
    print(f"  > '층' 결측치를 중위값({median_floor:.0f})으로 채웠습니다.")
    
    # ----------------------------------------------------
    # 단계 2: 파생 변수 생성
    # ----------------------------------------------------
    print("\n[단계 2] 파생변수 생성")
    
    # '전월세구분' 컬럼 생성: 월세가 0이면 '전세', 아니면 '월세'로 구분합니다.
    proc_df['전월세구분'] = np.where(proc_df['월세(만원)'] == 0, '전세', '월세')

    # '계약일자' 생성: 계약년, 월, 일을 합쳐 datetime 객체로 만듭니다.
    proc_df['계약일자'] = pd.to_datetime(proc_df['년'].astype(str) + '-' +
                                       proc_df['월'].astype(str) + '-' +
                                       proc_df['일'].astype(str))
    
    # '아파트연식' 파생변수 생성: 거래 시점의 년도에서 건축년도를 뺀 '연식'을 계산합니다.
    proc_df['아파트연식'] = proc_df['년'].astype(int) - proc_df['건축년도'].astype(int)
    
    print("  > '전월세구분', '계약일자', '아파트연식' 생성 완료")
    
    # ----------------------------------------------------
    # 단계 3: 최종 컬럼 정리 및 타입 변환
    # ----------------------------------------------------
    
    # 타입 변환 (정수형)
    proc_df['건축년도'] = proc_df['건축년도'].astype(int)
    proc_df['층'] = proc_df['층'].astype(int)
    
    # 불필요한 컬럼 제거: 파생변수를 만들거나 클리닝 과정에서 사용한 원본 컬럼을 제거합니다.
    columns_to_drop = ['년', '월', '일', '보증금액', '월세금', '해제여부', '해제사유발생일', '갱신청구권사용여부', '지번', '전용면적', '지역코드']
    proc_df = proc_df.drop(columns=[col for col in columns_to_drop if col in proc_df.columns], errors='ignore')

    # 최종 컬럼 순서 조정
    final_cols = ['아파트', '법정동', '전용면적(㎡)', '층', '건축년도', '아파트연식', '전월세구분', '보증금(만원)', '월세(만원)', '계약일자']
    proc_df = proc_df.reindex(columns=[col for col in final_cols if col in proc_df.columns])
    
    print("\n--- 전처리 완료 ---")
    return proc_df

if __name__ == "__main__":
    try:
        print(f"'{INPUT_FILE}' 파일이 있는지 확인 중...")
        
        if not os.path.exists(INPUT_FILE):
            raise FileNotFoundError(f"'{INPUT_FILE}'을 찾을 수 없습니다.")
            
        raw_df = pd.read_csv(INPUT_FILE)
        print(f"'{INPUT_FILE}' 로드 성공. (총 {len(raw_df)}건)")
        
        processed_df = preprocess_data(raw_df)

        if processed_df is not None:
            processed_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
            print(f"\n전처리 완료된 데이터가 '{OUTPUT_FILE}' 파일로 저장되었습니다.")
            
            print("\n--- 전처리 후 데이터 정보 요약 ---")
            processed_df.info()
            print("\n--- 전처리 후 데이터 샘플 (상위 5개) ---")
            print(processed_df.head())

    except FileNotFoundError:
        print(f"\n[오류] '{INPUT_FILE}'을 찾을 수 없습니다.")
        print(">>> 'generate_mock_data.py' 파일을 먼저 실행하여 원본 모의 데이터를 생성해주세요! <<<")
    except Exception as e:
        print(f"[오류] 파일 처리 중 문제 발생: {e}")