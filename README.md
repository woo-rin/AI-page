# KBO-Crawling
## 명세서
### /
```json
redirect '/docs' # Swagger UI로 리다이렉트
```
dlqk
### /request_list
succes
```json
{
  "status": "success",
  "data": [
    {
      "순위": "number",
      "선수명": "string",
      "팀명": "string",
      "AVG": "number",
      "G": "number",
      "PA": "number",
      "AB": "number",
      "R": "number",
      "H": "number",
      "2B": "number",
      "3B": "number",
      "HR": "number",
      "TB": "number",
      "RBI": "number",
      "SAC": "number",
      "SF": "number"
    }
  ]
}
```
error
```json
{
   "status": "error",
   "message": "string"
}
```
### /selenium_list
succes
```json
{
  "status": "success",
  "data": [
    {
      "순위": "number",
      "선수명": "string",
      "팀명": "string",
      "AVG": "number",
      "G": "number",
      "PA": "number",
      "AB": "number",
      "R": "number",
      "H": "number",
      "2B": "number",
      "3B": "number",
      "HR": "number",
      "TB": "number",
      "RBI": "number",
      "SAC": "number",
      "SF": "number"
    }
  ]
}
```
error
```json
{
   "status": "error",
   "message": "string"
}
```
---
## References
- [KBO 공식 기록실](https://www.koreabaseball.com/record/player/hitterbasic/basic1.aspx)
- [Selenium 공식 문서](https://www.selenium.dev/documentation/)
- [Window | Linux ChromeDriver 설치 가이드](https://pointer81.tistory.com/entry/Selenium-%EC%8B%A4%ED%96%89%EC%9D%84-%EC%9C%84%ED%95%9C-ChromeDriver-%EC%84%A4%EC%B9%98-%EA%B0%80%EC%9D%B4%EB%93%9C)
- [mac(AppleSilicone) ChromeDriver 설치 가이드](https://ddingmin00.tistory.com/entry/mac-m1-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-Selenium-Chromedriver-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0)