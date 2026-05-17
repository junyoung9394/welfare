// js/config.example.js — API 키 설정 템플릿
// 이 파일을 복사하여 js/config.js 로 저장 후 키를 입력하세요.
// js/config.js 는 .gitignore 에 포함되어 git에 추적되지 않습니다.
//
// Vercel 배포 시에는 js/config.js 없이도 환경변수(BOKJIRO_API_KEY, WORK24_API_KEY)로 동작합니다.

window.WELFARE_CONFIG = {
  BOKJIRO_API_KEY: 'YOUR_BOKJIRO_API_KEY_HERE',  // 복지로 OpenAPI 키: https://www.bokjiro.go.kr
  WORK24_API_KEY:  'YOUR_WORK24_API_KEY_HERE',   // 고용24 API 키: https://www.work24.go.kr
};
