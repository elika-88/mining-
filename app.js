const translations = {
  en: {
    appTitle: "MineShift Safety Console", awaitingShift: "Awaiting shift data", filesReady: "{count} files ready",
    analyzing: "Analyzing shift...", shiftLoaded: "Analysis completed", shiftLoadedWarnings: "Analysis completed with warnings",
    workersLabel: "Active workers", equipmentLabel: "Active equipment", eventsLabel: "Shift events",
    importBtn: "Select CSV files", runBtn: "Run analysis", noDataTitle: "No shift data loaded",
    noDataDesc: "Select the shift CSV files, then run the analysis.", noRisksTitle: "No risks detected",
    noRisksDesc: "The backend returned no detected risks for this dataset.", recommendedProtocol: "Recommended action",
    actionDispatch: "Supervisor action", evidenceHeader: "Observed data", analysisReasoning: "Interpretation",
    qaTitle: "Shift inquiry", qaSubtitle: "Answers use the active analysis", q1: "Which risk requires immediate attention?",
    q2: "Which workers or vehicles are affected?", q3: "What changed during the last 30 minutes?",
    inputPlaceholder: "Ask about the current shift...", sendQuery: "Ask", matchVerified: "Grounded response",
    sourceRef: "Evidence references", filterPriority: "Priority", filterAll: "All", filterHigh: "High",
    filterMed: "Medium", filterLow: "Low", filterCritical: "Critical", operatingZone: "Operating zone",
    allSectors: "All zones", detectedSituations: "Detected risks", noRisksFeed: "No analysis results yet.",
    noRisksMatch: "No risks match the selected filters.", selectFilesError: "Select at least one supported CSV file.",
    unknownFileError: "Unsupported file name: {name}", requestError: "The backend request failed: {message}",
    questionNeedsAnalysis: "Run an analysis before asking a question.", insufficientEvidence: "No observed evidence was returned for this risk.",
    limitations: "Limitations", row: "row"
  },
  kk: {
    appTitle: "MineShift қауіпсіздік басқару панелі", awaitingShift: "Ауысым деректері күтілуде", filesReady: "{count} файл дайын",
    analyzing: "Ауысым талдануда...", shiftLoaded: "Талдау аяқталды", shiftLoadedWarnings: "Талдау ескертулермен аяқталды",
    workersLabel: "Белсенді жұмысшылар", equipmentLabel: "Белсенді техника", eventsLabel: "Ауысым оқиғалары",
    importBtn: "CSV файлдарын таңдау", runBtn: "Талдауды бастау", noDataTitle: "Ауысым деректері жүктелмеген",
    noDataDesc: "Ауысым CSV файлдарын таңдап, талдауды бастаңыз.", noRisksTitle: "Қауіптер анықталмады",
    noRisksDesc: "Сервер бұл деректер жиынтығында қауіп таппады.", recommendedProtocol: "Ұсынылатын әрекет",
    actionDispatch: "Жетекші әрекеті", evidenceHeader: "Бақыланған деректер", analysisReasoning: "Түсіндірме",
    qaTitle: "Ауысым бойынша сұрақ", qaSubtitle: "Жауап белсенді талдауға негізделеді", q1: "Қай қауіп дереу назар аударуды қажет етеді?",
    q2: "Қандай жұмысшылар немесе көліктер әсер алды?", q3: "Соңғы 30 минутта не өзгерді?",
    inputPlaceholder: "Ағымдағы ауысым туралы сұраңыз...", sendQuery: "Сұрау", matchVerified: "Деректерге негізделген жауап",
    sourceRef: "Дәлел сілтемелері", filterPriority: "Басымдық", filterAll: "Барлығы", filterHigh: "Жоғары",
    filterMed: "Орташа", filterLow: "Төмен", filterCritical: "Сындарлы", operatingZone: "Жұмыс аймағы",
    allSectors: "Барлық аймақтар", detectedSituations: "Анықталған қауіптер", noRisksFeed: "Талдау нәтижесі әлі жоқ.",
    noRisksMatch: "Таңдалған сүзгілерге сәйкес қауіп жоқ.", selectFilesError: "Кемінде бір қолдау көрсетілетін CSV файлын таңдаңыз.",
    unknownFileError: "Қолдау көрсетілмейтін файл атауы: {name}", requestError: "Сервер сұрауы орындалмады: {message}",
    questionNeedsAnalysis: "Сұрақ қоймас бұрын талдауды іске қосыңыз.", insufficientEvidence: "Бұл қауіп үшін бақылау дәлелі қайтарылмады.",
    limitations: "Шектеулер", row: "жол"
  },
  ru: {
    appTitle: "MineShift — консоль безопасности", awaitingShift: "Ожидание данных смены", filesReady: "Файлов готово: {count}",
    analyzing: "Анализ смены...", shiftLoaded: "Анализ завершён", shiftLoadedWarnings: "Анализ завершён с предупреждениями",
    workersLabel: "Активные рабочие", equipmentLabel: "Активная техника", eventsLabel: "События смены",
    importBtn: "Выбрать CSV", runBtn: "Запустить анализ", noDataTitle: "Данные смены не загружены",
    noDataDesc: "Выберите CSV-файлы смены и запустите анализ.", noRisksTitle: "Риски не обнаружены",
    noRisksDesc: "Сервер не обнаружил рисков в этом наборе данных.", recommendedProtocol: "Рекомендуемое действие",
    actionDispatch: "Действие руководителя", evidenceHeader: "Наблюдаемые данные", analysisReasoning: "Интерпретация",
    qaTitle: "Запрос по смене", qaSubtitle: "Ответы основаны на активном анализе", q1: "Какой риск требует немедленного внимания?",
    q2: "Какие рабочие или машины затронуты?", q3: "Что изменилось за последние 30 минут?",
    inputPlaceholder: "Задайте вопрос о текущей смене...", sendQuery: "Спросить", matchVerified: "Ответ на основе данных",
    sourceRef: "Ссылки на доказательства", filterPriority: "Приоритет", filterAll: "Все", filterHigh: "Высокий",
    filterMed: "Средний", filterLow: "Низкий", filterCritical: "Критический", operatingZone: "Рабочая зона",
    allSectors: "Все зоны", detectedSituations: "Обнаруженные риски", noRisksFeed: "Результатов анализа пока нет.",
    noRisksMatch: "Нет рисков по выбранным фильтрам.", selectFilesError: "Выберите хотя бы один поддерживаемый CSV-файл.",
    unknownFileError: "Неподдерживаемое имя файла: {name}", requestError: "Ошибка запроса к серверу: {message}",
    questionNeedsAnalysis: "Сначала запустите анализ.", insufficientEvidence: "Для этого риска не возвращены наблюдаемые данные.",
    limitations: "Ограничения", row: "строка"
  },
  zh: {
    appTitle: "MineShift 矿山安全调度控制台", awaitingShift: "等待导入班次数据", filesReady: "已选择 {count} 个文件",
    analyzing: "正在分析班次数据...", shiftLoaded: "分析已完成", shiftLoadedWarnings: "分析已完成，存在数据警告",
    workersLabel: "在岗人员", equipmentLabel: "运行设备", eventsLabel: "班次事件",
    importBtn: "选择 CSV 文件", runBtn: "执行分析", noDataTitle: "尚未接入班次数据",
    noDataDesc: "请选择本班次 CSV 文件，然后执行分析。", noRisksTitle: "未检测到风险",
    noRisksDesc: "后端未在当前数据集中返回任何风险。", recommendedProtocol: "建议处置行动",
    actionDispatch: "主管操作", evidenceHeader: "原始观测数据", analysisReasoning: "分析解释",
    qaTitle: "班次问答", qaSubtitle: "回答基于当前分析结果", q1: "哪个风险需要立即处理？",
    q2: "哪些人员或车辆受到影响？", q3: "过去 30 分钟发生了什么变化？",
    inputPlaceholder: "询问当前班次情况...", sendQuery: "提问", matchVerified: "基于数据的回答",
    sourceRef: "证据引用", filterPriority: "优先级", filterAll: "全部", filterHigh: "高危",
    filterMed: "中危", filterLow: "低危", filterCritical: "紧急", operatingZone: "作业区域",
    allSectors: "全部区域", detectedSituations: "检测到的风险", noRisksFeed: "尚无分析结果。",
    noRisksMatch: "当前筛选条件下没有风险。", selectFilesError: "请至少选择一个受支持的 CSV 文件。",
    unknownFileError: "不支持的文件名：{name}", requestError: "后端请求失败：{message}",
    questionNeedsAnalysis: "请先执行一次分析。", insufficientEvidence: "该风险没有返回原始观测证据。",
    limitations: "数据限制", row: "行"
  }
};

const apiBase = window.MINE_API_BASE || ((location.hostname === "localhost" || location.hostname === "127.0.0.1") ? "http://127.0.0.1:8000" : location.origin);
const supportedFiles = new Set(["workers.csv", "equipment.csv", "environment.csv", "events.csv"]);
let currentLanguage = "en";
let selectedFiles = new Map();
let currentAnalysis = null;
let selectedRiskId = null;
let priorityFilter = "all";
let zoneFilter = "all";

function text(key, values = {}) {
  let value = translations[currentLanguage][key] || translations.en[key] || key;
  Object.entries(values).forEach(([name, replacement]) => {
    value = value.replace(`{${name}}`, String(replacement));
  });
  return value;
}

function apiUrl(path) {
  return `${apiBase.replace(/\/$/, "")}${path}`;
}

function changeLanguage(language) {
  const scrollPosition = window.scrollY;
  currentLanguage = language;
  document.documentElement.lang = language;
  const languageSelect = document.getElementById("languageSelect");
  if (languageSelect.value !== language) languageSelect.value = language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = text(element.dataset.i18n);
  });
  document.getElementById("queryInput").placeholder = text("inputPlaceholder");
  updateShiftIndicator();
  renderAnalysis();
  requestAnimationFrame(() => window.scrollTo(0, scrollPosition));
}

function updateShiftIndicator() {
  const indicator = document.getElementById("shiftIndicator");
  if (currentAnalysis) {
    indicator.textContent = currentAnalysis.overview.status === "completed_with_warnings" ? text("shiftLoadedWarnings") : text("shiftLoaded");
  } else if (selectedFiles.size) {
    indicator.textContent = text("filesReady", { count: selectedFiles.size });
  } else {
    indicator.textContent = text("awaitingShift");
  }
}

function showMessage(message, sources = "") {
  document.getElementById("answerQuestion").textContent = text("appTitle");
  document.getElementById("answerContent").textContent = message;
  document.getElementById("answerSources").textContent = sources || "—";
  document.getElementById("answerBox").classList.remove("hidden");
}

function handleFilesUpload(event) {
  const nextFiles = new Map();
  for (const file of event.target.files) {
    const normalizedName = file.name.toLowerCase();
    if (!supportedFiles.has(normalizedName)) {
      showMessage(text("unknownFileError", { name: file.name }));
      continue;
    }
    nextFiles.set(normalizedName.replace(".csv", ""), file);
  }
  selectedFiles = nextFiles;
  updateShiftIndicator();
}

async function triggerAnalyze() {
  if (!selectedFiles.size) {
    showMessage(text("selectFilesError"));
    return;
  }
  const buttonText = document.getElementById("rerunText");
  const button = document.getElementById("rerunBtn");
  button.disabled = true;
  button.classList.add("opacity-60", "cursor-wait");
  buttonText.textContent = text("analyzing");
  const formData = new FormData();
  selectedFiles.forEach((file, field) => formData.append(field, file, file.name));
  try {
    const response = await fetch(apiUrl("/api/analyses"), { method: "POST", body: formData });
    const payload = await response.json().catch(() => null);
    if (!response.ok) throw new Error(payload?.detail || `${response.status} ${response.statusText}`);
    currentAnalysis = payload;
    selectedRiskId = payload.risks[0]?.risk_id || null;
    priorityFilter = "all";
    zoneFilter = "all";
    document.getElementById("answerBox").classList.add("hidden");
    renderAnalysis();
  } catch (error) {
    showMessage(text("requestError", { message: error.message }));
  } finally {
    button.disabled = false;
    button.classList.remove("opacity-60", "cursor-wait");
    buttonText.textContent = text("runBtn");
    updateShiftIndicator();
  }
}

function renderAnalysis() {
  const overview = currentAnalysis?.overview;
  document.getElementById("statWorkers").textContent = overview?.active_workers ?? "--";
  document.getElementById("statEquipment").textContent = overview?.active_equipment ?? "--";
  document.getElementById("statEvents").textContent = overview?.shift_events ?? "--";
  renderPriorityCounts();
  renderZoneFilters();
  renderRiskCards();
  renderSelectedRisk();
}

function renderPriorityCounts() {
  const risks = currentAnalysis?.risks || [];
  document.getElementById("count-pri-all").textContent = risks.length;
  document.getElementById("count-pri-high").textContent = risks.filter((risk) => ["HIGH", "CRITICAL"].includes(risk.priority)).length;
  document.getElementById("count-pri-medium").textContent = risks.filter((risk) => risk.priority === "MEDIUM").length;
  document.getElementById("count-pri-low").textContent = risks.filter((risk) => risk.priority === "LOW").length;
}

function renderZoneFilters() {
  const container = document.getElementById("zoneFiltersContainer");
  container.replaceChildren();
  const zones = [...new Set((currentAnalysis?.risks || []).map((risk) => risk.zone_id).filter(Boolean))];
  [["all", text("allSectors")], ...zones.map((zone) => [zone, zone])].forEach(([value, label]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.zone = value;
    button.textContent = label;
    button.className = value === zoneFilter
      ? "filter-zone-btn px-3.5 py-1.5 rounded-full text-xs font-medium transition-all bg-heavy text-white"
      : "filter-zone-btn px-3.5 py-1.5 rounded-full text-xs font-medium transition-all bg-subtle text-subtext hover:text-heavy";
    button.addEventListener("click", () => setFilterZone(value));
    container.appendChild(button);
  });
}

function matchesPriority(risk) {
  if (priorityFilter === "all") return true;
  if (priorityFilter === "high") return risk.priority === "HIGH" || risk.priority === "CRITICAL";
  return risk.priority.toLowerCase() === priorityFilter;
}

function priorityPresentation(priority) {
  if (priority === "CRITICAL") return { label: text("filterCritical"), classes: "bg-red-50 text-red-700 border-red-100" };
  if (priority === "HIGH") return { label: text("filterHigh"), classes: "bg-rose-50 text-rose-700 border-rose-100" };
  if (priority === "MEDIUM") return { label: text("filterMed"), classes: "bg-amber-50 text-amber-800 border-amber-100" };
  return { label: text("filterLow"), classes: "bg-neutral-100 text-subtext border-neutral-200" };
}

function renderRiskCards() {
  const container = document.getElementById("riskCardsContainer");
  container.replaceChildren();
  const risks = currentAnalysis?.risks || [];
  if (!currentAnalysis) {
    renderRiskEmpty(container, text("noRisksFeed"));
    document.getElementById("riskCountLabel").textContent = "0";
    return;
  }
  const filtered = risks.filter((risk) => matchesPriority(risk) && (zoneFilter === "all" || risk.zone_id === zoneFilter));
  document.getElementById("riskCountLabel").textContent = `${filtered.length} / ${risks.length}`;
  if (!filtered.length) {
    renderRiskEmpty(container, risks.length ? text("noRisksMatch") : text("noRisksDesc"));
    return;
  }
  filtered.forEach((risk) => {
    const presentation = priorityPresentation(risk.priority);
    const card = document.createElement("button");
    card.type = "button";
    card.className = risk.risk_id === selectedRiskId
      ? "w-full text-left p-4 rounded-2xl border bg-subtle/80 border-heavy shadow-sm transition-all"
      : "w-full text-left p-4 rounded-2xl border bg-surface border-line soft-shadow-hover hover:border-neutral-300 transition-all";
    const entities = risk.affected_entities.map((entity) => entity.id).join(", ") || "—";
    card.innerHTML = `<div class="flex items-center justify-between mb-2 gap-3"><div class="flex items-center gap-2 min-w-0"><span class="${presentation.classes} border rounded-full px-2.5 py-0.5 text-[11px] font-semibold">${presentation.label}</span><span class="text-xs font-medium text-subtext truncate">${escapeHtml(risk.zone_id || "—")}</span></div><span class="text-[11px] font-mono text-subtext">${formatDateTime(risk.detected_at)}</span></div><h4 class="text-sm font-semibold text-heavy leading-snug mb-1">${escapeHtml(risk.title)}</h4><p class="text-[11px] text-subtext font-mono truncate">${escapeHtml(entities)}</p>`;
    card.addEventListener("click", () => {
      selectedRiskId = risk.risk_id;
      renderRiskCards();
      renderSelectedRisk();
    });
    container.appendChild(card);
  });
}

function renderRiskEmpty(container, message) {
  const empty = document.createElement("div");
  empty.className = "p-8 text-center text-xs text-subtext bg-subtle/50 rounded-2xl border border-dashed border-line";
  empty.textContent = message;
  container.appendChild(empty);
}

function renderSelectedRisk() {
  const empty = document.getElementById("emptyInspector");
  const content = document.getElementById("activeInspectorContent");
  const risk = (currentAnalysis?.risks || []).find((item) => item.risk_id === selectedRiskId);
  if (!risk) {
    content.classList.add("hidden");
    empty.classList.remove("hidden");
    empty.querySelector("h3").textContent = currentAnalysis ? text("noRisksTitle") : text("noDataTitle");
    empty.querySelector("p").textContent = currentAnalysis ? text("noRisksDesc") : text("noDataDesc");
    return;
  }
  empty.classList.add("hidden");
  content.classList.remove("hidden");
  const presentation = priorityPresentation(risk.priority);
  const badge = document.getElementById("detailPriorityBadge");
  badge.className = `${presentation.classes} border rounded-full px-3 py-1 text-xs font-semibold`;
  badge.textContent = presentation.label;
  document.getElementById("detailZone").textContent = risk.zone_id || "—";
  document.getElementById("detailTime").textContent = formatDateTime(risk.detected_at);
  document.getElementById("detailTitle").textContent = risk.title;
  document.getElementById("detailEntities").textContent = risk.affected_entities.map((entity) => `${entity.type}: ${entity.id}`).join(" · ") || "—";
  document.getElementById("detailAction").textContent = risk.recommended_action;
  document.getElementById("detailReasoning").textContent = risk.interpretation;
  renderEvidence(risk);
}

function renderEvidence(risk) {
  const list = document.getElementById("evidenceList");
  list.replaceChildren();
  document.getElementById("evidenceCount").textContent = `${risk.observed_data.length}`;
  if (!risk.observed_data.length) {
    renderRiskEmpty(list, text("insufficientEvidence"));
    return;
  }
  risk.observed_data.forEach((evidence) => {
    const row = document.createElement("div");
    row.className = "p-3.5 bg-subtle/70 rounded-xl text-xs";
    const facts = Object.entries(evidence.facts).map(([key, value]) => `${key}: ${value ?? "—"}`).join(" · ");
    row.innerHTML = `<div class="flex items-start justify-between gap-4"><div class="min-w-0"><div class="font-medium text-heavy break-words">${escapeHtml(facts)}</div><div class="font-mono text-[11px] text-subtext mt-1">${formatDateTime(evidence.timestamp)} · ${escapeHtml(evidence.zone_id || "—")} · ${text("row")} ${evidence.source_row}</div></div><span class="shrink-0 font-mono text-[11px] text-subtext bg-surface px-2.5 py-0.5 rounded-md border border-line">${escapeHtml(evidence.source_file)}</span></div>`;
    list.appendChild(row);
  });
  if (risk.limitations.length) {
    const limitations = document.createElement("div");
    limitations.className = "p-3.5 border border-dashed border-line rounded-xl text-xs text-subtext";
    limitations.textContent = `${text("limitations")}: ${risk.limitations.join(" · ")}`;
    list.appendChild(limitations);
  }
}

function setFilterPriority(priority) {
  priorityFilter = priority;
  document.querySelectorAll(".filter-pri-btn").forEach((button) => {
    button.className = button.id === `btn-pri-${priority}`
      ? "filter-pri-btn flex-1 py-1.5 text-xs font-medium rounded-lg transition-all bg-surface text-heavy shadow-sm"
      : "filter-pri-btn flex-1 py-1.5 text-xs font-medium rounded-lg transition-all text-subtext hover:text-heavy";
  });
  renderRiskCards();
}

function setFilterZone(zone) {
  zoneFilter = zone;
  renderZoneFilters();
  renderRiskCards();
}

function askQuestion(question) {
  document.getElementById("queryInput").value = question;
  submitCustomQuery();
}

async function submitCustomQuery() {
  const question = document.getElementById("queryInput").value.trim();
  if (!question) return;
  if (!currentAnalysis?.analysis_id) {
    showMessage(text("questionNeedsAnalysis"));
    return;
  }
  const answerBox = document.getElementById("answerBox");
  const answerContent = document.getElementById("answerContent");
  document.getElementById("answerQuestion").textContent = question;
  answerContent.textContent = text("analyzing");
  document.getElementById("answerSources").textContent = "—";
  answerBox.classList.remove("hidden");
  try {
    const requestPayload = { question };
    const selectedRiskReference = /this (?:alert|risk)|selected (?:alert|risk)|这个(?:告警|风险)|该(?:告警|风险)|этот риск|это предупреждение|осы қауіп/i;
    if (selectedRiskId && selectedRiskReference.test(question)) {
      requestPayload.risk_id = selectedRiskId;
    }
    const response = await fetch(apiUrl(`/api/analyses/${encodeURIComponent(currentAnalysis.analysis_id)}/questions`), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestPayload)
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) throw new Error(payload?.detail || `${response.status} ${response.statusText}`);
    const sections = [payload.answer, payload.interpretation, payload.recommended_action].filter(Boolean);
    if (payload.limitations?.length) sections.push(`${text("limitations")}: ${payload.limitations.join(" · ")}`);
    answerContent.textContent = sections.join("\n\n");
    const evidenceIds = [...new Set((payload.observed_facts || []).flatMap((fact) => fact.evidence_ids || []))];
    document.getElementById("answerSources").textContent = evidenceIds.join(", ") || "—";
  } catch (error) {
    answerContent.textContent = text("requestError", { message: error.message });
  }
}

function formatDateTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat(currentLanguage === "kk" ? "kk-KZ" : currentLanguage, {
    month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit"
  }).format(date);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

changeLanguage("en");
