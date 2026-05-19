/**
 * 복지모아 API 연동 모듈
 *
 * [API 키 설정 방법]
 * - 로컬 개발: js/config.example.js 를 복사 → js/config.js 로 저장 후 키 입력
 *   (js/config.js 는 .gitignore 에 포함되어 git 에 올라가지 않습니다)
 * - Vercel 배포: 대시보드 > Settings > Environment Variables 에서 설정
 *     BOKJIRO_API_KEY — 복지로 OpenAPI 키 (https://www.bokjiro.go.kr)
 *     WORK24_API_KEY  — 고용24 API 키    (https://www.work24.go.kr)
 *   키가 Vercel 에 등록되면 /api/bokjiro, /api/work24 프록시가 자동으로 동작합니다.
 */

// ──────────────────────────────────────────
// 복지로 API
// ──────────────────────────────────────────
const BOKJIRO_PROXY_URL  = '/api/bokjiro';
const BOKJIRO_DIRECT_URL = 'https://www.bokjiro.go.kr/ssis-tbu/twatd/openapi/selectWlfInfo.do';

function _bokjiroKey() {
  return window.WELFARE_CONFIG?.BOKJIRO_API_KEY || null;
}

async function searchBokjiro(keyword, options = {}) {
  const key = _bokjiroKey();
  const params = new URLSearchParams({
    callTp: 'L',
    srchWrd: keyword,
    pageIndex: options.pageIndex || 1,
    pageSize:  options.pageSize  || 10,
    _type: 'json',
  });

  // 로컬 config.js 에 키가 있으면 직접 호출, 없으면 Vercel 프록시 사용
  let url;
  if (key) {
    params.set('serviceKey', key);
    url = `${BOKJIRO_DIRECT_URL}?${params}`;
  } else {
    url = `${BOKJIRO_PROXY_URL}?${params}`;
  }

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return _parseBokjiro(data);
  } catch (err) {
    console.error('복지로 API 오류:', err);
    return { items: [], totalCount: 0, error: err.message };
  }
}

function _parseBokjiro(data) {
  try {
    const body = data?.wlfInfoRsSVO?.wlfInfoDtlDTO || [];
    const totalCount = data?.wlfInfoRsSVO?.totalCount || 0;
    const items = (Array.isArray(body) ? body : [body]).map(function(item) {
      return {
        id:          item.servId,
        title:       item.servNm,
        summary:     item.servDgst,
        target:      item.tgtrDtlCn,
        supportType: item.srvPvsnNm,
        applyUrl:    item.aplyUrlAddr,
        department:  item.jurMnofNm,
        period:      item.lifeNmChk,
      };
    });
    return { items, totalCount };
  } catch {
    return { items: [], totalCount: 0 };
  }
}

async function getBokjiroDetail(servId) {
  const key = _bokjiroKey();
  const params = new URLSearchParams({ callTp: 'D', servId, _type: 'json' });

  let url;
  if (key) {
    params.set('serviceKey', key);
    url = `${BOKJIRO_DIRECT_URL}?${params}`;
  } else {
    url = `${BOKJIRO_PROXY_URL}?${params}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();
    return data?.wlfInfoRsSVO?.wlfInfoDtlDTO || null;
  } catch (err) {
    console.error('복지로 상세 API 오류:', err);
    return null;
  }
}

// ──────────────────────────────────────────
// 고용24 API
// ──────────────────────────────────────────
const WORK24_PROXY_URL  = '/api/work24';
const WORK24_DIRECT_URL = 'https://www.work24.go.kr/wk/a/b/1200/retrivePolicyMberList.do';

function _work24Key() {
  return window.WELFARE_CONFIG?.WORK24_API_KEY || null;
}

async function searchWork24(keyword, options = {}) {
  const key = _work24Key();
  const params = new URLSearchParams({
    returnType: 'JSON',
    startPage: options.pageIndex || 1,
    display:   options.pageSize  || 10,
    keyword,
  });

  let url;
  if (key) {
    params.set('authKey', key);
    url = `${WORK24_DIRECT_URL}?${params}`;
  } else {
    url = `${WORK24_PROXY_URL}?${params}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();
    return data?.workPolicyList || [];
  } catch (err) {
    console.error('고용24 API 오류:', err);
    return [];
  }
}

// 외부 노출
window.WelfareAPI = {
  searchBokjiro,
  getBokjiroDetail,
  searchWork24,
};
