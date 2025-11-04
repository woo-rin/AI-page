# 종속성 추가
import requests
from bs4 import BeautifulSoup
import pandas as pd
def Crawling_requests():
    url = "https://www.koreabaseball.com/record/player/hitterbasic/basic1.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    
    res.encoding = 'utf-8'
    
    soup = BeautifulSoup(res.text, "lxml")

    table = soup.find("table", {"summary": "선수 기본기록으로 경기,타석,타수,득점,안타,2루타, 3루타 등을 표시합니다"})
    
    df = pd.read_html(str(table), flavor='lxml')[0]

    # Pandas를 이용해 '롯데' 선수만 모은 Dataframe으로 치환
    # 우선은 롯데자이언츠만 크롤링
    df = df.loc[df['팀명']=='롯데']
    return df.to_dict(orient='records')
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Selenium을 이용해 웹에 접속 후 처리하는 함수 ( chrome drive 필수 )
def Crawling_selenium(team_code='LT'):
    # Chrome driver 호출
    driver = webdriver.Chrome()
    try:
        
        url = "https://www.koreabaseball.com/record/player/hitterbasic/basic1.aspx"
        driver.get(url)
        # 팀 선택 select 태그 로딩 대기
        select_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cphContents_cphContents_cphContents_ddlTeam_ddlTeam"))
        )

        select = Select(select_elem)
        select.select_by_value(team_code)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tData01"))
        )
        # 로드 후 렌더링 대기
        time.sleep(2)
        # 데이터 추출
        result = []
        # 결과 테이블 검색
        table = driver.find_element(By.CLASS_NAME, "tData01")
        # find_elements를 이용해 실제 결과 값 검색
        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        # 헤더 값 검색 ( 이유 : 후에 딕셔너리로 형변환 하기 위해 )
        header = table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr")
        # 딕셔너리로 변환
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            # 형변환 ( 근거 : selenium으로 크롤링 한 값은 모두 str로 반환 )
            def convert(val):
                val = val.strip()
                if val.replace('.', '', 1).isdigit():
                    return float(val) if '.' in val else int(val)
                return val
            # 딕셔너리화
            data = {header: convert(col.text) for header, col in zip(header.text.split(' '), cols)}
            result.append(data)
        return result
        # for문을 사용하는 이유?
        # 1. selenium으로 크롤링을 진행히면 헤더 ( 속성 이름 ) 없이 값만 있음
        # 2. 헤더 값을 불러와 각각 매칭해 딕셔너리로 저장
        # 3. 배열에 append해 기댓값으로 변환
        # 예시
        # 변환 전 :
        #       ['1', '박찬형', '롯데', '0.400', '15', '43', '40', '8', '16', '0', '1', '1', '21', '5', '0', '0']
        # 변환 후 :
        #       {'순위': 1, '선수명': '박찬형', '팀명': '롯데', 'AVG': 0.4, 'G': 15, 'PA': 43, ... }
    finally:
        # 드라이버 종료
        driver.quit()