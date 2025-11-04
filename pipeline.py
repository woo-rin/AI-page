# pipeline.py
from crawling import Crawling_requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

# 1️⃣ 데이터 수집
def collect_data():
    print("📥 KBO 데이터 수집 중...")
    data = Crawling_requests()
    df = pd.DataFrame(data)
    print(f"✅ 수집 완료: {len(df)}명 선수")
    return df


# 2️⃣ 전처리
def preprocess_data(df):
    print("🧹 전처리 중...")
    # 숫자형만 추출
    numeric_df = df.select_dtypes(include=['number']).copy()

    # 결측치 처리
    numeric_df = numeric_df.fillna(0)

    # 스케일링
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(numeric_df)
    scaled_df = pd.DataFrame(scaled, columns=numeric_df.columns)

    print("✅ 전처리 완료")
    return scaled_df


# 3️⃣ 모델 학습
def train_model(data):
    print("🤖 모델 학습 중...")
    # 예시: 타율(AVG)로부터 WAR(대신 OBP 예측) 학습 시뮬레이션
    if 'AVG' not in data.columns or 'OBP' not in data.columns:
        print("⚠️ 데이터에 'AVG' 또는 'OBP'가 없어 예시용으로 대체 학습합니다.")
        data['AVG'] = data.iloc[:, 0]
        data['OBP'] = data.iloc[:, 1]

    X = data[['AVG']]
    y = data['OBP']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"✅ 모델 학습 완료 (정확도: {score:.2f})")
    return model


# 4️⃣ 예측
def predict_future(model, data):
    print("🔮 미래 성장 가능성 예측 중...")
    X = data[['AVG']]
    predictions = model.predict(X)
    data['Predicted_OBP'] = predictions
    print("✅ 예측 완료")
    return data


# 5️⃣ 전체 파이프라인 실행
def run_pipeline():
    df = collect_data()
    processed = preprocess_data(df)
    model = train_model(processed)
    result = predict_future(model, processed)
    result.to_csv("predicted_result.csv", index=False)
    print("💾 예측 결과 saved: predicted_result.csv")


if __name__ == "__main__":
    run_pipeline()
