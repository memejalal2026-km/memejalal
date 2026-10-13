/**
 * 화분 키우기: 링크 미리보기(OG) 처리
 *
 * 화분 공유 링크(/?from=닉네임&p=씨앗&s=단계)로 들어오면
 * 카톡·X 같은 SNS가 읽어 가는 미리보기 제목·그림을 그 화분에 맞게 바꿔 줘요.
 * 그 밖의 모든 요청은 원래 파일(index.html, 이미지 등)을 그대로 돌려줘요.
 *
 * 미리보기 그림: /og/p/{씨앗}-{0~5}.png (0 씨앗, 1 새싹, 2 자라는 중, 3 꽃봉오리·열매, 4 거의 다 큼, 5 완성)
 */
const SEEDS = {
  peony: "작약", hydra: "수국", rose: "장미", marigold: "메리골드", sun: "해바라기",
  clover: "네잎클로버", apple: "사과나무", grape: "포도나무", cherry: "앵두나무",
  persim: "감나무", pear: "배나무", avocado: "아보카도", blueberry: "블루베리", strawberry: "스트로베리",
  tulip: "튤립", cosmos: "코스모스", mugung: "무궁화", lavender: "라벤더",
  sakura: "벚나무", peach: "복숭아나무", tangerine: "귤나무", lemon: "레몬나무",
  forsythia: "개나리", azalea: "진달래", lily: "백합", carnation: "카네이션",
  chestnut: "밤나무", pomegranate: "석류나무", banana: "바나나나무", cactus: "선인장"
};

export const stateOf = s => (s <= 10 ? 0 : s <= 25 ? 1 : s <= 50 ? 2 : s <= 75 ? 3 : s <= 99 ? 4 : 5);
const josaIGA = w => { const c = w.charCodeAt(w.length - 1); return (c >= 0xac00 && c <= 0xd7a3 && (c - 0xac00) % 28) ? "이" : "가"; };

/** 링크 파라미터 → 미리보기 정보 (잘못된 값이면 null → 기본 미리보기 그대로) */
export function potMeta(url) {
  const p = url.searchParams.get("p");
  const s = parseInt(url.searchParams.get("s"), 10);
  const name = Object.prototype.hasOwnProperty.call(SEEDS, p) ? SEEDS[p] : null;
  if (!name || !(s >= 1 && s <= 100)) return null;
  const from = (url.searchParams.get("from") || "").trim().replace(/[\u0000-\u001f<>]/g, "").slice(0, 10);
  const who = from ? from + "님의 " : "";
  const title = s >= 100
    ? `${who}${name}${josaIGA(name)} 다 자랐어요! 🎉`
    : `${who}${name}${josaIGA(name)} ${s}단계까지 자랐어요! 🌱`;
  return {
    title,
    desc: "퀴즈 풀고 물 주기 💧 너도 키워볼래? · 화분 키우기",
    image: `${url.origin}/og/p/${p}-${stateOf(s)}.png`,
    url: url.href
  };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const isHome = url.pathname === "/" || url.pathname === "/index.html";
    const meta = isHome && request.method === "GET" ? potMeta(url) : null;
    if (!meta) return env.ASSETS.fetch(request);

    // 첫 화면 파일을 받아서 미리보기 태그만 바꿔 줌
    const res = await env.ASSETS.fetch(new Request(url.origin + "/", request));
    if (!(res.headers.get("content-type") || "").includes("text/html")) return res;
    const set = v => ({ element(el) { el.setAttribute("content", v); } });
    return new HTMLRewriter()
      .on('meta[property="og:title"]', set(meta.title))
      .on('meta[property="og:description"]', set(meta.desc))
      .on('meta[property="og:image"]', set(meta.image))
      .on('meta[property="og:url"]', set(meta.url))
      .on('meta[name="twitter:image"]', set(meta.image))
      .on('meta[name="twitter:title"]', set(meta.title))
      .on('meta[name="twitter:description"]', set(meta.desc))
      .transform(res);
  }
};
