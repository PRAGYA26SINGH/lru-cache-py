import time
import requests
from flask import Flask, jsonify, render_template_string, request
from lru_cache import LRUCache

app = Flask(__name__)

# Initialize LRU Cache with capacity 4 so evictions can be seen quickly
cache = LRUCache(capacity=4)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Speed Booster | In-Memory LRU Cache</title>
  <style>
    * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background: #0f172a; color: #f8fafc; padding: 32px; max-width: 860px; margin: auto; }
    h1 { font-size: 1.8rem; margin-bottom: 6px; }
    p.sub { color: #94a3b8; margin-top: 0; font-size: 0.95rem; }
    .card { background: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; border: 1px solid #334155; }
    .input-group { display: flex; gap: 10px; margin-bottom: 12px; }
    input { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 1rem; }
    button { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; }
    button:hover { background: #2563eb; }
    .stats-bar { display: flex; gap: 16px; margin-top: 16px; }
    .stat-box { flex: 1; background: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155; }
    .stat-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: bold; }
    .stat-value { font-size: 1.4rem; font-weight: bold; margin-top: 6px; }
    .hit { color: #22c55e; }
    .miss { color: #f59e0b; }
    .memory-lane { display: flex; gap: 10px; margin-top: 12px; overflow-x: auto; padding-bottom: 4px; }
    .node-tile { background: #334155; border: 1px solid #64748b; padding: 10px 14px; border-radius: 8px; font-family: monospace; font-size: 0.9rem; }
    .node-mru { border-color: #3b82f6; background: #1e3a8a; }
    .node-lru { border-color: #ef4444; background: #451a1a; }
    .profile-card { display: flex; gap: 20px; align-items: center; margin-top: 16px; }
    .profile-card img { width: 80px; height: 80px; border-radius: 50%; border: 2px solid #3b82f6; }
  </style>
</head>
<body>

  <h1>⚡ In-Memory LRU Cache Accelerator</h1>
  <p class="sub">Eliminating slow upstream network requests with an O(1) in-memory cache layer.</p>

  <div class="card">
    <div class="input-group">
      <input type="text" id="username" placeholder="Enter GitHub username (e.g. torvalds, defunkt, octocat)..." value="torvalds" />
      <button onclick="fetchUser()">Fetch Profile</button>
    </div>
    <div style="font-size: 0.85rem; color: #94a3b8;">
      💡 Search once to fetch from upstream (Cold). Search again to witness an instant sub-2ms LRU Cache Hit (Hot).
    </div>

    <div class="stats-bar">
      <div class="stat-box">
        <div class="stat-label">Cache Status</div>
        <div class="stat-value" id="status">-</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">Response Latency</div>
        <div class="stat-value" id="latency">-</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">Efficiency Delta</div>
        <div class="stat-value" id="speedup">-</div>
      </div>
    </div>

    <div id="result"></div>
  </div>

  <div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin: 0; font-size: 1.1rem;">Live In-Memory Cache Visualizer</h3>
      <span style="font-size: 0.85rem; color: #94a3b8;">Capacity: 4 items</span>
    </div>
    <p class="sub" style="margin-top: 4px;">Left: Most Recently Used (MRU) ⟶ Right: Least Recently Used (LRU)</p>
    <div class="memory-lane" id="memoryLane">
      <span style="color: #64748b; font-size: 0.9rem;">Cache is empty</span>
    </div>
  </div>

  <script>
    async function fetchUser() {
      const username = document.getElementById("username").value.trim();
      if (!username) return;

      const res = await fetch(`/api/user?username=${encodeURIComponent(username)}`);
      const data = await res.json();

      if (data.error) {
        alert(data.error);
        return;
      }

      const statusElem = document.getElementById("status");
      statusElem.innerText = data.source;
      statusElem.className = "stat-value " + (data.source.includes("HIT") ? "hit" : "miss");

      document.getElementById("latency").innerText = `${data.latency_ms} ms`;
      document.getElementById("speedup").innerText = data.speedup;

      // Render profile
      document.getElementById("result").innerHTML = `
        <div class="profile-card">
          <img src="${data.profile.avatar_url}" />
          <div>
            <h3 style="margin: 0;">${data.profile.name || data.profile.login}</h3>
            <div style="color: #94a3b8; font-size: 0.9rem;">@${data.profile.login}</div>
            <p style="margin: 6px 0 0; font-size: 0.9rem;">${data.profile.bio || "No bio provided"}</p>
            <div style="margin-top: 6px; font-size: 0.85rem; color: #38bdf8;">
              Public Repos: ${data.profile.public_repos} | Followers: ${data.profile.followers}
            </div>
          </div>
        </div>
      `;

      // Render memory lane
      const lane = document.getElementById("memoryLane");
      if (data.cache_keys.length === 0) {
        lane.innerHTML = '<span style="color: #64748b;">Cache is empty</span>';
      } else {
        lane.innerHTML = data.cache_keys.map((k, idx) => {
          let badge = idx === 0 ? " (MRU)" : (idx === data.cache_keys.length - 1 && data.cache_keys.length === 4 ? " (LRU)" : "");
          let cls = idx === 0 ? "node-tile node-mru" : (idx === data.cache_keys.length - 1 && data.cache_keys.length === 4 ? "node-tile node-lru" : "node-tile");
          return `<div class="${cls}">[${k}]${badge}</div>`;
        }).join(" ⟶ ");
      }
    }

    // Run on Enter key
    document.getElementById("username").addEventListener("keypress", (e) => {
      if (e.key === "Enter") fetchUser();
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/user")
def get_user():
    username = request.args.get("username", "").strip().lower()
    if not username:
        return jsonify({"error": "Username required"}), 400

    start_time = time.perf_counter()

    # 1. Attempt LRU Cache lookup
    cached_data = cache.get(username)

    if cached_data is not None:
        elapsed = (time.perf_counter() - start_time) * 1000
        return jsonify({
            "source": "CACHE HIT (O(1))",
            "latency_ms": round(elapsed, 2),
            "speedup": "~99% faster",
            "profile": cached_data,
            "cache_keys": cache.get_ordered_keys()
        })

    # 2. Cache MISS: Fetch from external GitHub REST API
    headers = {"User-Agent": "LRU-Cache-Demo-App"}
    api_url = f"https://api.github.com/users/{username}"
    resp = requests.get(api_url, headers=headers)

    if resp.status_code != 200:
        return jsonify({"error": f"GitHub user '{username}' not found"}), 404

    profile_data = resp.json()
    cache.put(username, profile_data)

    elapsed = (time.perf_counter() - start_time) * 1000
    return jsonify({
        "source": "API FETCH (Cold)",
        "latency_ms": round(elapsed, 2),
        "speedup": "Baseline (0%)",
        "profile": profile_data,
        "cache_keys": cache.get_ordered_keys()
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)