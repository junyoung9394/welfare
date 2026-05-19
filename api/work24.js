// Vercel Serverless Function — 고용24 API CORS 프록시
// WORK24_API_KEY 환경변수를 Vercel 프로젝트 설정에서 등록하세요.

const WORK24_BASE_URL = 'https://www.work24.go.kr/wk/a/b/1200/retrivePolicyMberList.do';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const apiKey = process.env.WORK24_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'WORK24_API_KEY 환경변수가 설정되지 않았습니다.' });
  }

  const { keyword = '', startPage = 1, display = 10 } = req.query;

  const params = new URLSearchParams({
    authKey: apiKey,
    returnType: 'JSON',
    startPage,
    display,
    keyword,
  });

  try {
    const upstream = await fetch(`${WORK24_BASE_URL}?${params}`);
    if (!upstream.ok) throw new Error(`Upstream HTTP ${upstream.status}`);
    const data = await upstream.json();
    return res.status(200).json(data);
  } catch (err) {
    return res.status(502).json({ error: err.message });
  }
}
