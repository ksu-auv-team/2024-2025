/* ============================================
   KSU AUV Data Visualizer – Client Script
   ============================================ */

const BASE_API = "http://192.168.8.138:5000";  // Flask API
const CAM0 = "http://192.168.8.138:5001/video_0";
const CAM1 = "http://192.168.8.138:5001/video_1";

console.log("[AUV UI] index.js loaded");

/* ---------- Helpers ---------- */
function $(sel) { return document.querySelector(sel); }
function $all(sel) { return document.querySelectorAll(sel); }

function normalizeToArray(payload) {
  if (Array.isArray(payload)) return payload;
  if (!payload) return [];
  if (Array.isArray(payload.data)) return payload.data;
  if (Array.isArray(payload.items)) return payload.items;
  return [payload];
}

function fetchAndUpdateTable(url, tableId, rowBuilder) {
  fetch(url)
    .then(async (res) => {
      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        throw new Error(`GET ${url} -> ${res.status} ${res.statusText} ${txt}`);
      }
      return res.json();
    })
    .then((data) => {
      const tbody = document.querySelector(`#${tableId} tbody`);
      if (!tbody) return console.warn(`[Table] Missing tbody for #${tableId}`);
      const rows = normalizeToArray(data);
      rows.sort((a, b) => (b.id ?? 0) - (a.id ?? 0));  // sort by id desc
      tbody.innerHTML = rows.map(r => `<tr>${rowBuilder(r)}</tr>`).join("");
    })
    .catch((err) => {
      console.error(`[TableUpdate] ${tableId}:`, err);
    });
}

/* ---------- Camera refresh ---------- */
function updateCameraSrc(id, baseUrl) {
  const el = document.getElementById(id);
  if (!el) return;
  el.src = baseUrl + "?ts=" + Date.now();
}
// setInterval(() => updateCameraSrc("camera-feed-0", CAM0), 1000);
// setInterval(() => updateCameraSrc("camera-feed-1", CAM1), 333);

/* ---------- SPA navigation ---------- */
const pages = ["page-cameras", "page-data", "page-settings"];
const navLinks = $all(".nav-link");

function showPage(id) {
  pages.forEach((pid) => {
    const el = document.getElementById(pid);
    if (!el) return;
    el.classList.toggle("hidden", pid !== id);
  });
  navLinks.forEach((a) => a.classList.toggle("active", a.dataset.target === id));
}

// Initial route
window.addEventListener("load", () => {
  const hash = location.hash.replace("#", "");
  if (hash === "data") showPage("page-data");
  else if (hash === "settings") showPage("page-settings");
  else showPage("page-cameras");
});

// Click routing
navLinks.forEach((a) => {
  a.addEventListener("click", (e) => {
    e.preventDefault();
    const target = a.dataset.target;
    showPage(target);
    history.replaceState(null, "", "#" + a.getAttribute("href").replace("#", ""));
  });
});

/* ---------- Tabs (Data + Settings) ---------- */
function setupTabs(container) {
  const tabList = container.querySelector(".tab-list");
  if (!tabList) return;

  const tabs = tabList.querySelectorAll(".tab");
  const panels = container.querySelectorAll(".tab-panel");

  function activateTab(idx) {
    tabs.forEach((t, i) => t.setAttribute("aria-selected", String(i === idx)));
    panels.forEach((p, i) => p.classList.toggle("active", i === idx));
  }

  // normalize initial state (ensure exactly one active)
  let initial = Array.from(panels).findIndex(p => p.classList.contains("active"));
  if (initial < 0) initial = 0;
  activateTab(initial);

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activateTab(index));
    tab.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") activateTab((index + 1) % tabs.length);
      if (e.key === "ArrowLeft")  activateTab((index - 1 + tabs.length) % tabs.length);
    });
  });
}
setupTabs(document.getElementById("page-data"));
setupTabs(document.getElementById("page-settings"));

/* ---------- Inputs form + Arm button (no immediate POST) ---------- */
(function initInputs() {
  // slider <-> number sync
  const pairs = [["force-input", "force-input-num"]];
  pairs.forEach(([sliderId, inputId]) => {
    const slider = document.getElementById(sliderId);
    const input = document.getElementById(inputId);
    if (slider && input) {
      slider.addEventListener("input", () => (input.value = slider.value));
      input.addEventListener("input", () => (slider.value = input.value));
    }
  });

  // direction constraints
  const opposites = {forward:"backward", backward:"forward", left:"right", right:"left", up:"down", down:"up", yaw_right:"yaw_left", yaw_left:"yaw_right"};
  const dir1 = document.getElementById("direction1");
  const dir2 = document.getElementById("direction2");

  function updateDirectionOptions() {
    const selected1 = dir1.value;
    const selected2 = dir2.value;
    Array.from(dir1.options).forEach((opt) => (opt.disabled = false));
    Array.from(dir2.options).forEach((opt) => (opt.disabled = false));
    if (selected1) {
      Array.from(dir2.options).forEach((opt) => {
        if (opt.value === selected1 || opt.value === opposites[selected1]) opt.disabled = true;
      });
    }
    if (selected2) {
      Array.from(dir1.options).forEach((opt) => {
        if (opt.value === selected2 || opt.value === opposites[selected2]) opt.disabled = true;
      });
    }
  }
  dir1.addEventListener("change", updateDirectionOptions);
  dir2.addEventListener("change", updateDirectionOptions);

  // Arm toggle (affects next submit only)
  const armBtn = document.getElementById("inputs-arm-toggle");
  let inputsArmState = false; // default: disarmed
  let stepIndex = 1;

  if (armBtn) {
    armBtn.addEventListener("click", () => {
      inputsArmState = !inputsArmState;
      armBtn.textContent = inputsArmState ? "Disarm" : "Arm";
      armBtn.classList.toggle("primary", inputsArmState);
    });
  }

  // Main Inputs form submit
  const form = document.getElementById("inputs-form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const directionChosen = dir1.value || dir2.value;
    if (!directionChosen) {
      alert("Please select at least one direction.");
      return;
    }
    const force = Number(document.getElementById("force-input").value);

    const payload = {
      step_index: stepIndex++,
      direction: directionChosen,
      force: force,
      s1: 0.0,
      s2: 0.0,
      s3: 0.0,
      arm: inputsArmState   // <-- set by the Arm button; no POST on toggle
    };

    fetch(`${BASE_API}/inputs/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then((res) => {
        if (!res.ok) return res.json().then(j => { throw new Error(JSON.stringify(j)); });
        alert("Inputs sent!");
        fetchAndUpdateTable(`${BASE_API}/inputs/`, "table-inputs", inputsRow);
      })
      .catch((err) => alert("Error: " + err.message));
  });
})();

/* ---------- Outputs form ---------- */
(function initOutputs() {
  // slider <-> number sync for motors + s1
  ["m1","m2","m3","m4","m5","m6","m7","m8","s1"].forEach((id) => {
    const slider = document.getElementById(id);
    const input = document.getElementById(`${id}-input`);
    if (slider && input) {
      slider.addEventListener("input", () => (input.value = slider.value));
      input.addEventListener("input", () => (slider.value = input.value));
    }
  });

  // toggles
  const armToggle = document.getElementById("arm-toggle");
  let armState = false;
  if (armToggle) {
    armToggle.addEventListener("click", function () {
      armState = !armState;
      armToggle.textContent = armState ? "On" : "Off";
      armToggle.classList.toggle("primary", armState);
    });
  }

  const s2Toggle = document.getElementById("s2-toggle");
  let s2State = false;
  if (s2Toggle) {
    s2Toggle.addEventListener("click", function () {
      s2State = !s2State;
      s2Toggle.textContent = s2State ? "Fired" : "Fire";
      s2Toggle.classList.toggle("primary", s2State);
    });
  }

  const s3Toggle = document.getElementById("s3-toggle");
  let s3State = false;
  if (s3Toggle) {
    s3Toggle.addEventListener("click", function () {
      s3State = !s3State;
      s3Toggle.textContent = s3State ? "Fired" : "Fire";
      s3Toggle.classList.toggle("primary", s3State);
    });
  }

  let stepIndex = 1;
  const form = document.getElementById("outputs-form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const payload = {
      step_index: stepIndex++,
      direction: document.getElementById("out-direction").value || "hold",
      force: Number(document.getElementById("out-force").value || 0),
      M1: Number(document.getElementById("m1").value),
      M2: Number(document.getElementById("m2").value),
      M3: Number(document.getElementById("m3").value),
      M4: Number(document.getElementById("m4").value),
      M5: Number(document.getElementById("m5").value),
      M6: Number(document.getElementById("m6").value),
      M7: Number(document.getElementById("m7").value),
      M8: Number(document.getElementById("m8").value),
      S1: Number(document.getElementById("s1").value),
      S2: s2State ? 0 : 255,
      S3: s3State ? 0 : 255,
      arm: armState
    };

    fetch(`${BASE_API}/outputs/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then((res) => {
        if (!res.ok) return res.json().then(j => { throw new Error(JSON.stringify(j)); });
        alert("Outputs sent!");
        fetchAndUpdateTable(`${BASE_API}/outputs/`, "table-outputs", outputsRow);
      })
      .catch((err) => alert("Error: " + err.message));
  });
})();

/* ---------- Row builders ---------- */
function inputsRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.step_index ?? ""}</td>
    <td>${row.direction ?? ""}</td>
    <td>${row.force ?? ""}</td>
    <td>${row.s1 ?? ""}</td>
    <td>${row.s2 ?? ""}</td>
    <td>${row.s3 ?? ""}</td>
    <td>${row.arm ?? ""}</td>
    <td>${row.timestamp ?? ""}</td>`;
}

function outputsRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.step_index ?? ""}</td>
    <td>${row.direction ?? ""}</td>
    <td>${row.force ?? ""}</td>
    <td>${row.M1 ?? ""}</td><td>${row.M2 ?? ""}</td><td>${row.M3 ?? ""}</td><td>${row.M4 ?? ""}</td>
    <td>${row.M5 ?? ""}</td><td>${row.M6 ?? ""}</td><td>${row.M7 ?? ""}</td><td>${row.M8 ?? ""}</td>
    <td>${row.S1 ?? ""}</td><td>${row.S2 ?? ""}</td><td>${row.S3 ?? ""}</td>
    <td>${row.arm ?? ""}</td>`;
}

function imuRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.X ?? ""}</td>
    <td>${row.Y ?? ""}</td>
    <td>${row.Z ?? ""}</td>
    <td>${row.roll ?? ""}</td>
    <td>${row.pitch ?? ""}</td>
    <td>${row.yaw ?? ""}</td>
    <td>${row.timestamp ?? ""}</td>`;
}

/* ---------- Initial fetch + Polling ---------- */
window.addEventListener("load", () => {
  fetchAndUpdateTable(`${BASE_API}/inputs/`,  "table-inputs",  inputsRow);
  fetchAndUpdateTable(`${BASE_API}/outputs/`, "table-outputs", outputsRow);
  fetchAndUpdateTable(`${BASE_API}/imu/`,     "table-imu",     imuRow);
});

setInterval(() => {
  fetchAndUpdateTable(`${BASE_API}/inputs/`,  "table-inputs",  inputsRow);
  fetchAndUpdateTable(`${BASE_API}/outputs/`, "table-outputs", outputsRow);
  fetchAndUpdateTable(`${BASE_API}/imu/`,     "table-imu",     imuRow);
}, 1000);
