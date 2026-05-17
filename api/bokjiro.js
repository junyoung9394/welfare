// Vercel Serverless Function — 복지로 OpenAPI CORS 프록시
// BOKJIRO_API_KEY 환경변수를 Vercel 프로젝트 설정에서 등록하세요.

const BOKJIRO_BASE_URL = 'https://www.bokjiro.go.kr/ssis-tbu/twatd/openapi/selectWlfInfo.do';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const apiKey = process.env.BOKJIRO_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'BOKJIRO_API_KEY 환경변수가 설정되지 않았습니다.' });
  }

  const { callTp = 'L', srchWrd = '', servId = '', pageIndex = 1, pageSize = 10 } = req.query;

  const params = new URLSearchParams({
    serviceKey: apiKey,
    callTp,
    srchWrd,
    servId,
    pageIndex,
    pageSize,
    _type: 'json',
  });

  try {
    const upstream = await fetch(`${BOKJIRO_BASE_URL}?${params}`);
    if (!upstream.ok) throw new Error(`Upstream HTTP ${upstream.status}`);
    const data = await upstream.json();
    return res.status(200).json(data);
  } catch (err) {
    return res.status(502).json({ error: err.message });
  }
}
