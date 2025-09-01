const API = "/api";
const chatWindow = document.getElementById("chatWindow");
const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("sendBtn");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

let history = [];

async function health() {
  try {
    const r = await fetch(`${API}/health`);
    const j = await r.json();
    document.getElementById("health").textContent =
      `OK | collection: ${j.collection} | embed: ${j.embedding_model} | llm: ${j.llm_model}`;
  } catch {
    document.getElementById("health").textContent = "backend недоступен";
  }
}

function addBubble(text, who = "user") {
  const div = document.createElement("div");
  div.className = `bubble ${who}`;
  div.innerHTML = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addSources(sources) {
  if (!sources || !sources.length) return;
  const wrap = document.createElement("div");
  wrap.className = "sources";
  sources.forEach((s) => {
    const el = document.createElement("details");
    const meta = s.metadata || {};
    el.innerHTML = `<summary>[${s.tag}] ${meta.source || ""}</summary><pre>${s.text}</pre>`;
    wrap.appendChild(el);
  });
  chatWindow.appendChild(wrap);
}

async function ask() {
  const q = questionInput.value.trim();
  if (!q) return;
  addBubble(q, "user");
  questionInput.value = "";
  addBubble("Думаю…", "bot");

  try {
    const r = await fetch(`${API}/chat`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ question: q, top_k: 5, history })
    });
    const j = await r.json();

    const last = chatWindow.querySelector(".bubble.bot:last-child");
    if (last) last.innerHTML = j.answer;

    addSources(j.sources);

    history.push([q, j.answer]);
  } catch (e) {
    const last = chatWindow.querySelector(".bubble.bot:last-child");
    if (last) last.innerHTML = "Ошибка: " + (e.message || "unknown");
  }
}

async function upload() {
  const file = document.getElementById("file").files[0];
  if (!file) return;
  uploadStatus.textContent = "Загрузка…";

  const fd = new FormData();
  fd.append("file", file);
  try {
    const r = await fetch(`${API}/upload`, { method: "POST", body: fd });
    const j = await r.json();
    if (!r.ok) throw new Error(j.detail || JSON.stringify(j));
    uploadStatus.textContent = `OK: ${j.file_name} → чанков: ${j.chunks_indexed}`;
  } catch (e) {
    uploadStatus.textContent = "Ошибка: " + e.message;
  }
}

sendBtn.addEventListener("click", ask);
questionInput.addEventListener("keydown", (e) => { if (e.key === "Enter") ask(); });
uploadBtn.addEventListener("click", upload);

health();
