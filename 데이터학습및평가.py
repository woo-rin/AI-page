# -*- coding: utf-8 -*-
# === 5. 모델 학습 및 평가 (Phase 5 - Mac 호환 버전) ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor 

# 🌟 [중요] Mac 한글 폰트 깨짐 방지 설정 🌟
# Mac에서는 'AppleGothic'을 사용해야 그래프 한글이 깨지지 않습니다.
plt.rcParams['font.family'] = 'AppleGothic' 
plt.rcParams['axes.unicode_minus'] = False  # 마이너스(-) 기호 깨짐 방지

INPUT_FILE = 'apartment_rent_final_features.csv'

def train_and_evaluate():
    print("--- 모델 학습 및 평가 시작 ---")
    
    # 1. 데이터 로드
    if not os.path.exists(INPUT_FILE):
        print(f"[오류] '{INPUT_FILE}'을 찾을 수 없습니다. Phase 4(데이터분서.py)를 먼저 실행하세요.")
        return

    # 🌟 [중요] CSV 한글 깨짐 방지: encoding='utf-8-sig' 사용
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    except UnicodeDecodeError:
        # 혹시 utf-8-sig로 안 열리면 cp949로 시도 (비상용)
        df = pd.read_csv(INPUT_FILE, encoding='cp949')
        
    print(f"데이터 로드 성공: {len(df)}건")

    # 2. 학습 데이터(X)와 타겟(y) 분리
    target_col = 'log_보증금'
    drop_cols = ['log_보증금', '전세환산가(만원)'] 
    
    # 데이터에 존재하는 컬럼만 삭제 (안전장치)
    available_drop_cols = [col for col in drop_cols if col in df.columns]
    X = df.drop(columns=available_drop_cols)
    y = df[target_col]
    
    print(f"\n학습에 사용할 특성(Features): {list(X.columns)}")

    # 3. 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"데이터 분할 완료: 학습용 {len(X_train)}건, 테스트용 {len(X_test)}건")

    # 4. 모델 학습 (Random Forest)
    print("\n[모델 학습 중...] Random Forest 알고리즘이 패턴을 학습하고 있습니다.")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("모델 학습 완료!")

    # 5. 예측 수행
    y_pred_log = model.predict(X_test)

    # 6. 결과 역변환 (로그 스케일 -> 원래 가격 단위)
    y_test_origin = np.expm1(y_test)
    y_pred_origin = np.expm1(y_pred_log)

    # 7. 성능 평가
    r2 = r2_score(y_test_origin, y_pred_origin)
    rmse = np.sqrt(mean_squared_error(y_test_origin, y_pred_origin))
    mae = mean_absolute_error(y_test_origin, y_pred_origin)

    print("\n" + "="*40)
    print(" 📊 모델 성능 평가 결과")
    print("="*40)
    print(f" 1. 결정 계수 (R2 Score): {r2:.4f}")
    print(f" 2. 평균 오차 (RMSE): {rmse:,.0f} 만원")
    print(f" 3. 평균 절대 오차 (MAE): {mae:,.0f} 만원")
    print("-" * 40)
    print(f" 해석: 이 모델은 실제 가격과 평균적으로 약 {mae:,.0f}만원 정도의 차이를 보입니다.")
    print("="*40)

    # 8. 시각화
    # (1) 실제값 vs 예측값 산점도
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test_origin, y=y_pred_origin, alpha=0.6, color='blue')
    plt.plot([y_test_origin.min(), y_test_origin.max()], 
             [y_test_origin.min(), y_test_origin.max()], 
             'r--', lw=2)
    plt.title('실제 가격 vs 예측 가격 (Actual vs Predicted)') # 한글 제목
    plt.xlabel('실제 가격 (원)')
    plt.ylabel('예측 가격 (원)')
    plt.grid(True)
    plt.show()

    # (2) 특성 중요도 (Feature Importance)
    plt.figure(figsize=(10, 6))
    sorted_idx = model.feature_importances_.argsort()
    plt.barh(X.columns[sorted_idx], model.feature_importances_[sorted_idx], color='green')
    plt.title('변수 중요도 (Feature Importance)') # 한글 제목
    plt.xlabel('중요도')
    plt.grid(axis='x')
    plt.show()

if __name__ == "__main__":
    train_and_evaluate()