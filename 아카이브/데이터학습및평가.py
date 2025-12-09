# -*- coding: utf-8 -*-
# === 5. 모델 학습 및 평가 (Phase 5) ===
# 설명: 최종 데이터셋을 사용하여 머신러닝 모델(Random Forest)을 학습시키고,
#       실제 아파트 매매가를 예측하여 성능을 평가합니다.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import platform
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

# ----------------------------------------------------------
# 1. 한글 폰트 설정 (Mac/Windows 호환)
# ----------------------------------------------------------
system_name = platform.system()
if system_name == 'Darwin': # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
elif system_name == 'Windows': # Windows
    plt.rcParams['font.family'] = 'Malgun Gothic'
else: # Linux (Colab 등)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False # 마이너스 부호 깨짐 방지

# ----------------------------------------------------------
# 2. 설정 및 데이터 로드
# ----------------------------------------------------------
INPUT_FILE = 'apartment_sales_final_features.csv'

def train_and_evaluate():
    print("--- 매매가 예측 모델 학습 시작 ---")

    # 파일 존재 여부 확인
    if not os.path.exists(INPUT_FILE):
        print(f"[오류] '{INPUT_FILE}' 파일이 없습니다.")
        print(">>> '데이터분석.py'를 먼저 실행해서 학습용 데이터를 준비해주세요!")
        return

    # 데이터 로드 (인코딩 처리)
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(INPUT_FILE, encoding='cp949')

    print(f"학습 데이터 로드 성공: {len(df)}건")

    # ----------------------------------------------------------
    # 3. 데이터 분할 (학습용 vs 테스트용)
    # ----------------------------------------------------------
    target_col = 'log_거래금액' # 타겟 변수 (로그 변환된 가격)

    # X: 타겟을 제외한 모든 특성, y: 타겟
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 80% 학습, 20% 테스트
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"데이터 분할 완료: 학습용 {len(X_train)}건, 테스트용 {len(X_test)}건")

    # ----------------------------------------------------------
    # 4. 모델 학습 (Random Forest)
    # ----------------------------------------------------------
    print("\n[AI 모델 학습 중...] 숲(Forest)을 키우는 중입니다... (잠시 대기)")
    
    # RandomForestRegressor: 여러 개의 결정 트리를 사용하여 예측하는 강력한 모델
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("모델 학습 완료!")

    # ----------------------------------------------------------
    # 5. 예측 및 평가
    # ----------------------------------------------------------
    # 테스트 데이터로 예측 수행 (결과는 로그 스케일)
    y_pred_log = model.predict(X_test)

    # 로그 스케일 -> 원래 가격(만원)으로 복원 (np.expm1)
    y_test_origin = np.expm1(y_test)
    y_pred_origin = np.expm1(y_pred_log)

    # 평가 지표 계산
    r2 = r2_score(y_test_origin, y_pred_origin)
    rmse = np.sqrt(mean_squared_error(y_test_origin, y_pred_origin))
    mae = mean_absolute_error(y_test_origin, y_pred_origin)

    print("\n" + "="*50)
    print(" 🏠 아파트 매매가 예측 AI 최종 성적표 🏠")
    print("="*50)
    print(f" 1. 예측 정확도 (R2 Score) : {r2:.4f} (1.0에 가까울수록 완벽)")
    print(f" 2. 평균 오차 (RMSE)       : {rmse:,.0f} 만원")
    print(f" 3. 평균 절대 오차 (MAE)   : {mae:,.0f} 만원")
    print("-" * 50)
    print(f" 해석: AI가 예측한 가격은 실제 거래가격과 평균적으로")
    print(f"       약 {mae/10000:.2f}억 원 ({mae:,.0f}만원) 정도 차이가 납니다.")
    print("="*50)

    # ----------------------------------------------------------
    # 6. 시각화 (결과 분석)
    # ----------------------------------------------------------
    
    # (1) 실제값 vs 예측값 산점도
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test_origin, y=y_pred_origin, alpha=0.6, color='#4c72b0')
    
    # 기준선 (완벽하게 맞춘 경우)
    min_val = min(y_test_origin.min(), y_pred_origin.min())
    max_val = max(y_test_origin.max(), y_pred_origin.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='완벽한 예측선')
    
    plt.title(f'아파트 실거래가 예측 결과 (R2: {r2:.2f})', fontsize=14)
    plt.xlabel('실제 거래가 (만원)', fontsize=12)
    plt.ylabel('AI 예측가 (만원)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # (2) 특성 중요도 (Feature Importance)
    # 어떤 변수가 집값 결정에 가장 큰 영향을 미쳤는지 확인
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance, palette='viridis')
    plt.title('아파트 집값 결정 중요 요인 (Feature Importance)', fontsize=14)
    plt.xlabel('중요도', fontsize=12)
    plt.ylabel('요인(Feature)', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train_and_evaluate()