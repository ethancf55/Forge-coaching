const GIST_ID = "5713db3869010e881bbf9ddde7f61aa1";

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.end(JSON.stringify(body));
}

module.exports = async function handler(req, res) {
  if (req.method === "OPTIONS") {
    return send(res, 204, {});
  }
  if (req.method !== "GET") {
    return send(res, 405, { error: "Method not allowed" });
  }

  try {
    const response = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
      headers: {
        Accept: "application/vnd.github+json",
        "User-Agent": "forge-desk-runtime",
      },
    });
    if (!response.ok) {
      return send(res, 502, { url: "", error: `gist ${response.status}` });
    }
    const gist = await response.json();
    const raw = gist.files?.["forge-desk-runtime.json"]?.content || gist.files?.["runtime.json"]?.content || "{}";
    let parsed = {};
    try {
      parsed = JSON.parse(raw);
    } catch {
      parsed = {};
    }
    return send(res, 200, {
      url: typeof parsed.url === "string" ? parsed.url : "",
      updatedAt: parsed.updatedAt || null,
    });
  } catch (error) {
    return send(res, 500, { url: "", error: String(error.message || error) });
  }
};
