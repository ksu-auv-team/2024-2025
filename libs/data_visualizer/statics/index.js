/* ==========
   Config
   ========== */
const BASE_API = "http://192.168.8.109:5000"; // Flask server
const CAM0 = "http://localhost:5001/video_0";
const CAM1 = "http://localhost:5001/video_1";

/* ==========
   Utils
   ========== */
function $(sel) { return document.querySelector(sel); }
function $all(sel) { return document.querySelectorAll(sel); }

function fetchJSON(url, options = {}) {
  return fetch(url, options).then(async (res) => {
    if (!res.ok) {
      let msg = "";
      try { msg = JSON.stringify(await res.json()); } catch (_e) {}
      throw new Error(`${res.status} ${res.statusText} ${msg}`);
    }
    return res.json();
  });
}

function fetchAndUpdateTable(url, tableId, rowBuilder) {
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.querySelector(`#${tableId} tbody`);
      if (!tbody) return;
      tbody.innerHTML = "";
      (Array.isArray(data) ? data : [data]).forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = rowBuilder(row);
        tbody.appendChild(tr);
      });
    })
    .catch(() => {});
}

/* ==========
   Camera refresh (cache-busting)
   ========== */
function updateCameraSrc(id, baseUrl) {
  const el = document.getElementById(id);
  if (!el) return;
  el.src = baseUrl + "?ts=" + Date.now();
}
setInterval(() => updateCameraSrc("camera-feed-0", CAM0), 1000);
setInterval(() => updateCameraSrc("camera-feed-1", CAM1), 333);

/* ==========
   SPA navigation
   ========== */
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

/* ==========
   Tabs (Data + Settings)
   ========== */
function setupTabs(container) {
  const tabList = container.querySelector(".tab-list");
  if (!tabList) return;

  const tabs = tabList.querySelectorAll(".tab");
  const panels = container.querySelectorAll(".tab-panel");

  function activateTab(idx) {
    tabs.forEach((t, i) => t.setAttribute("aria-selected", String(i === idx)));
    panels.forEach((p, i) => p.classList.toggle("active", i === idx));
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activateTab(index));
    tab.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") activateTab((index + 1) + 0 % tabs.length);
      if (e.key === "ArrowLeft") activateTab((index - 1 + tabs.length) % tabs.length);
    });
  });
}
setupTabs(document.getElementById("page-data"));
setupTabs(document.getElementById("page-settings"));

/* ==========
   Inputs form
   ========== */
(function initInputsForm() {
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

  // direction dropdown constraints
  const directions = ["forward","backward","left","right","up","down","yaw_right","yaw_left"];
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

  let stepIndex = 1; // simple increment
  const form = document.getElementById("inputs-form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const direction = dir1.value || dir2.value;
    if (!direction) {
      alert("Please select at least one direction.");
      return;
    }
    const force = Number(document.getElementById("force-input").value);

    const payload = {
      step_index: stepIndex++,
      direction: direction,
      force: force, // adjust scale if your API expects 0.0–1.0
      s1: 0.0,
      s2: 0.0,
      s3: 0.0,
      arm: false
    };

    fetch(`${BASE_API}/inputs/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then((res) => (res.ok ? alert("Inputs sent!") : res.json().then((j) => { throw new Error(JSON.stringify(j)); })))
      .catch((err) => alert("Error: " + err.message));
  });
})();

/* ==========
   Outputs form
   ========== */
(function initOutputsForm() {
  // slider <-> number sync for motors and s1
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
  armToggle.addEventListener("click", function () {
    armState = !armState;
    armToggle.textContent = armState ? "On" : "Off";
    armToggle.classList.toggle("primary", armState);
  });

  const s2Toggle = document.getElementById("s2-toggle");
  let s2State = false;
  s2Toggle.addEventListener("click", function () {
    s2State = !s2State;
    s2Toggle.textContent = s2State ? "Fired" : "Fire";
    s2Toggle.classList.toggle("primary", s2State);
  });

  const s3Toggle = document.getElementById("s3-toggle");
  let s3State = false;
  s3Toggle.addEventListener("click", function () {
    s3State = !s3State;
    s3Toggle.textContent = s3State ? "Fired" : "Fire";
    s3Toggle.classList.toggle("primary", s3State);
  });

  let stepIndex = 1;
  const form = document.getElementById("outputs-form");
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
      S2: s2State ? 1700 : 1300, // example mapping for toggles; adjust as needed
      S3: s3State ? 1700 : 1300,
      arm: armState
    };

    fetch(`${BASE_API}/outputs/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then((res) => (res.ok ? alert("Outputs sent!") : res.json().then((j) => { throw new Error(JSON.stringify(j)); })))
      .catch((err) => alert("Error: " + err.message));
  });
})();

/* ==========
   Table row builders (match your API fields)
   ========== */
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
    <td>${row.M1 ?? row.m1 ?? ""}</td>
    <td>${row.M2 ?? row.m2 ?? ""}</td>
    <td>${row.M3 ?? row.m3 ?? ""}</td>
    <td>${row.M4 ?? row.m4 ?? ""}</td>
    <td>${row.M5 ?? row.m5 ?? ""}</td>
    <td>${row.M6 ?? row.m6 ?? ""}</td>
    <td>${row.M7 ?? row.m7 ?? ""}</td>
    <td>${row.M8 ?? row.m8 ?? ""}</td>
    <td>${row.S1 ?? row.s1 ?? ""}</td>
    <td>${row.S2 ?? row.s2 ?? ""}</td>
    <td>${row.S3 ?? row.s3 ?? ""}</td>
    <td>${row.arm ?? ""}</td>`;
}

function batteriesRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.voltage ?? row.voltage1 ?? ""}</td>
    <td>${row.current ?? row.current1 ?? ""}</td>
    <td>${row.temp ?? row.temperature1 ?? ""}</td>
    <td>${row.timestamp ?? ""}</td>`;
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

function internalsRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.cpu_temp ?? row.temperature ?? ""}</td>
    <td>${row.ram ?? ""}</td>
    <td>${row.disk ?? ""}</td>
    <td>${row.timestamp ?? ""}</td>`;
}

function externalsRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.depth ?? ""}</td>
    <td>${row.temp ?? row.temperature ?? ""}</td>
    <td>${row.salinity ?? ""}</td>
    <td>${row.timestamp ?? ""}</td>`;
}

function sonarRow(row) {
  return `<td>${row.id ?? ""}</td>
    <td>${row.angle ?? ""}</td>
    <td>${row.range ?? row.distance ?? ""}</td>
    <td>${row.strength ?? ""}</td>
    <td>${row.timestamp ?? ""}</td>`;
}

/* ==========
   Polling
   ========== */
setInterval(() => {
  fetchAndUpdateTable(`${BASE_API}/inputs/`, "table-inputs", inputsRow);
  fetchAndUpdateTable(`${BASE_API}/outputs/`, "table-outputs", outputsRow);
  // fetchAndUpdateTable(`${BASE_API}/batteries/`, "table-batteries", batteriesRow);
  fetchAndUpdateTable(`${BASE_API}/imu/`, "table-imu", imuRow);
  // fetchAndUpdateTable(`${BASE_API}/internals/`, "table-internals", internalsRow);
  // fetchAndUpdateTable(`${BASE_API}/externals/`, "table-externals", externalsRow);
  // fetchAndUpdateTable(`${BASE_API}/sonar/`, "table-sonar", sonarRow);
}, 1000);
