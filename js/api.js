/**
 * 복지로 OpenAPI 연동 모듈
 * API 키 발급: https://www.bokjiro.go.kr/ssis-tbu/twatd/openapi/openApiManage.do
 *
 * 사용법:
 *   1. 아래 BOKJIRO_API_KEY 에 발급받은 키를 입력
 *   2. search.html 에서 <script src="js/api.js"></script> 추가
 *   3. searchBokjiro('청년 월세') 형태로 호출
 */

const BOKJIRO_API_KEY = 'sUl0xfEp9wcBrWjayiTv5+ixiC9mwyYp7+47Ezx/Ux6W3cfOL2f1PdOaKwvDcSK2QuSrs8A9QPf90w/vpI9r/w==';

const BOKJIRO_BASE_URL = 'https://www.bokjiro.go.kr/ssis-tbu/twatd/openapi/selectWlfInfo.do';

/**
 * 복지로 API 검색
 * @param {string} keyword - 검색 키워드
 * @param {Object} options - 추가 필터 옵션
 * @param {number} options.pageIndex - 페이지 번호 (기본 1)
 * @param {number} options.pageSize - 페이지당 결과 수 (기본 10)
 */
async function searchBokjiro(keyword, options = {}) {
  const params = new URLSearchParams({
    serviceKey: BOKJIRO_API_KEY,
    callTp: 'L',           // L: 목록조회
    srchWrd: keyword,
    pageIndex: options.pageIndex || 1,
    pageSize: options.pageSize || 10,
    _type: 'json',
  });

  // CORS 이슈 때문에 프록시를 거쳐야 할 수 있음
  // Vercel Edge Function 또는 serverless function 사용 권장
  const url = `${BOKJIRO_BASE_URL}?${params.toString()}`;

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return parseBokjiroResponse(data);
  } catch (err) {
    console.error('복지로 API 오류:', err);
    return { items: [], totalCount: 0, error: err.message };
  }
}

function parseBokjiroResponse(data) {
  try {
    const body = data?.wlfInfoRsSVO?.wlfInfoDtlDTO || [];
    const totalCount = data?.wlfInfoRsSVO?.totalCount || 0;
    const items = (Array.isArray(body) ? body : [body]).map(function(item) {
      return {
        id: item.servId,
        title: item.servNm,
        summary: item.servDgst,
        target: item.tgtrDtlCn,
        supportType: item.srvPvsnNm,
        applyUrl: item.aplyUrlAddr,
        department: item.jurMnofNm,
        period: item.lifeNmChk,
      };
    });
    return { items, totalCount };
  } catch {
    return { items: [], totalCount: 0 };
  }
}

/**
 * 복지로 API — 상세 조회
 * @param {string} servId - 서비스 ID
 */
async function getBokjiroDetail(servId) {
  const params = new URLSearchParams({
    serviceKey: BOKJIRO_API_KEY,
    callTp: 'D',
    servId,
    _type: 'json',
  });
  try {
    const res = await fetch(`${BOKJIRO_BASE_URL}?${params.toString()}`);
    const data = await res.json();
    return data?.wlfInfoRsSVO?.wlfInfoDtlDTO || null;
  } catch (err) {
    console.error('복지로 상세 API 오류:', err);
    return null;
  }
}

/**
 * 고용24 API — 청년 취업 지원 프로그램 검색
 * API 키 발급: https://www.work24.go.kr/cm/c/f/apiApplList.do
 */
const WORK24_API_KEY = 'YOUR_WORK24_API_KEY_HERE'; // ← 고용24 API 키
const WORK24_BASE_URL = 'https://www.work24.go.kr/wk/a/b/1200/retrivePolicyMberList.do';

async function searchWork24(keyword, options = {}) {
  const params = new URLSearchParams({
    authKey: WORK24_API_KEY,
    returnType: 'JSON',
    startPage: options.pageIndex || 1,
    display: options.pageSize || 10,
    keyword,
  });
  try {
    const res = await fetch(`${WORK24_BASE_URL}?${params.toString()}`);
    const data = await res.json();
    return data?.workPolicyList || [];
  } catch (err) {
    console.error('고용24 API 오류:', err);
    return [];
  }
}

// 외부에서 사용할 수 있도록 전역 노출
window.WelfareAPI = {
  searchBokjiro,
  getBokjiroDetail,
  searchWork24,
};
