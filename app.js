const translations = {
  en: {
    appTitle: "MineShift Safety Console", awaitingShift: "Awaiting shift data", filesReady: "{count} files ready",
    analyzing: "Analyzing shift...", shiftLoaded: "Analysis completed", shiftLoadedWarnings: "Analysis completed with warnings",
    workersLabel: "Active workers", equipmentLabel: "Active equipment", eventsLabel: "Shift events", highRisksLabel: "High-priority risks",
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
    limitations: "Limitations", row: "row", datasetTitle: "Dataset readiness", shiftStart: "Shift start", shiftEnd: "Shift end",
    missingFiles: "Missing: {files}", allFilesReady: "All standard files selected", apiChecking: "Checking API", apiConnected: "API connected",
    apiUnavailable: "API unavailable", dataQuality: "Data quality", qualityWaiting: "Available after analysis", rejectedRecords: "{count} rejected",
    qualitySummary: "{valid} valid of {received} received · {rejected} rejected", exportReport: "Export report",
    languageNotice: "Interface labels are translated. Backend risk and answer text is shown in the language returned by the API.",
    score: "Score", clearEntityFilter: "Clear entity filter", filteringEntity: "Related to {entity}", evidenceUnavailable: "Evidence details unavailable",
    asking: "Asking...", selected: "Selected", scoreBreakdown: "Score breakdown",
    dropHint: "workers.csv, equipment.csv, environment.csv, events.csv — or click to browse", dropActive: "Release to add CSV files"
  },
  kk: {
    appTitle: "MineShift қауіпсіздік басқару панелі", awaitingShift: "Ауысым деректері күтілуде", filesReady: "{count} файл дайын",
    analyzing: "Ауысым талдануда...", shiftLoaded: "Талдау аяқталды", shiftLoadedWarnings: "Талдау ескертулермен аяқталды",
    workersLabel: "Белсенді жұмысшылар", equipmentLabel: "Белсенді техника", eventsLabel: "Ауысым оқиғалары", highRisksLabel: "Жоғары басымдықты қауіптер",
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
    limitations: "Шектеулер", row: "жол", datasetTitle: "Деректер жиынтығының дайындығы", shiftStart: "Ауысым басталуы", shiftEnd: "Ауысым аяқталуы",
    missingFiles: "Жетпейді: {files}", allFilesReady: "Барлық стандартты файл таңдалды", apiChecking: "API тексерілуде", apiConnected: "API қосылды",
    apiUnavailable: "API қолжетімсіз", dataQuality: "Деректер сапасы", qualityWaiting: "Талдаудан кейін қолжетімді", rejectedRecords: "{count} жазба қабылданбады",
    qualitySummary: "Қабылданғаны {received}, жарамдысы {valid}, қабылданбағаны {rejected}", exportReport: "Есепті экспорттау",
    languageNotice: "Интерфейс аударылады. Қауіп пен жауап мәтіні API қайтарған тілде көрсетіледі.",
    score: "Ұпай", clearEntityFilter: "Нысан сүзгісін тазалау", filteringEntity: "{entity} бойынша", evidenceUnavailable: "Дәлел деректері қолжетімсіз",
    asking: "Сұрау жіберілуде...", selected: "Таңдалды", scoreBreakdown: "Балл құрамы",
    dropHint: "workers.csv, equipment.csv, environment.csv, events.csv — немесе таңдау үшін басыңыз", dropActive: "CSV файлдарын қосу үшін жіберіңіз"
  },
  ru: {
    appTitle: "MineShift — консоль безопасности", awaitingShift: "Ожидание данных смены", filesReady: "Файлов готово: {count}",
    analyzing: "Анализ смены...", shiftLoaded: "Анализ завершён", shiftLoadedWarnings: "Анализ завершён с предупреждениями",
    workersLabel: "Активные рабочие", equipmentLabel: "Активная техника", eventsLabel: "События смены", highRisksLabel: "Риски высокого приоритета",
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
    limitations: "Ограничения", row: "строка", datasetTitle: "Готовность набора данных", shiftStart: "Начало смены", shiftEnd: "Конец смены",
    missingFiles: "Не хватает: {files}", allFilesReady: "Все стандартные файлы выбраны", apiChecking: "Проверка API", apiConnected: "API подключён",
    apiUnavailable: "API недоступен", dataQuality: "Качество данных", qualityWaiting: "Доступно после анализа", rejectedRecords: "Отклонено: {count}",
    qualitySummary: "Получено {received}, корректно {valid}, отклонено {rejected}", exportReport: "Экспортировать отчёт",
    languageNotice: "Интерфейс переведён. Тексты рисков и ответов показываются на языке, возвращённом API.",
    score: "Оценка", clearEntityFilter: "Сбросить фильтр объекта", filteringEntity: "Связано с {entity}", evidenceUnavailable: "Детали доказательства недоступны",
    asking: "Отправка вопроса...", selected: "Выбрано", scoreBreakdown: "Состав оценки",
    dropHint: "workers.csv, equipment.csv, environment.csv, events.csv — или нажмите для выбора", dropActive: "Отпустите, чтобы добавить CSV"
  },
  zh: {
    appTitle: "MineShift 矿山安全调度控制台", awaitingShift: "等待导入班次数据", filesReady: "已选择 {count} 个文件",
    analyzing: "正在分析班次数据...", shiftLoaded: "分析已完成", shiftLoadedWarnings: "分析已完成，存在数据警告",
    workersLabel: "在岗人员", equipmentLabel: "运行设备", eventsLabel: "班次事件", highRisksLabel: "高优先级风险",
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
    limitations: "数据限制", row: "行", datasetTitle: "数据集准备情况", shiftStart: "班次开始", shiftEnd: "班次结束",
    missingFiles: "缺少：{files}", allFilesReady: "四个标准文件已全部选择", apiChecking: "正在检查 API", apiConnected: "API 已连接",
    apiUnavailable: "API 不可用", dataQuality: "数据质量", qualityWaiting: "分析后显示", rejectedRecords: "拒绝 {count} 条记录",
    qualitySummary: "接收 {received} 条，有效 {valid} 条，拒绝 {rejected} 条", exportReport: "导出风险报告",
    languageNotice: "界面标签支持翻译；风险标题、解释和建议保持后端 API 返回的语言。",
    score: "评分", clearEntityFilter: "清除实体筛选", filteringEntity: "仅显示与 {entity} 相关", evidenceUnavailable: "无法获取证据详情",
    asking: "正在提问...", selected: "已选择", scoreBreakdown: "风险评分构成",
    dropHint: "workers.csv、equipment.csv、environment.csv、events.csv，也可以点击选择", dropActive: "松开即可添加 CSV 文件"
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
let entityFilter = null;
let apiConnected = null;

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

async function checkApiStatus() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 2500);
  try {
    const response = await fetch(apiUrl("/api/health"), { signal: controller.signal });
    apiConnected = response.ok;
  } catch {
    apiConnected = false;
  } finally {
    clearTimeout(timeout);
    updateApiStatus();
  }
}

function updateApiStatus() {
  const status = document.getElementById("apiStatus");
  if (apiConnected === null) {
    status.textContent = text("apiChecking");
    status.className = "min-w-[112px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-neutral-100 text-subtext border border-line";
    return;
  }
  status.textContent = apiConnected ? text("apiConnected") : text("apiUnavailable");
  status.className = apiConnected
    ? "min-w-[112px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-100"
    : "min-w-[112px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-100";
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
  updateApiStatus();
  renderFileStatus();
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
  const evidenceList = document.getElementById("answerEvidenceList");
  evidenceList.replaceChildren();
  if (sources) renderAnswerEvidenceEmpty(evidenceList, sources);
  document.getElementById("answerBox").classList.remove("hidden");
}

function handleFilesUpload(event) {
  selectFiles(event.target.files, true);
  event.target.value = "";
}

function selectFiles(files, replace = false) {
  const nextFiles = replace ? new Map() : new Map(selectedFiles);
  for (const file of files) {
    const normalizedName = file.name.toLowerCase();
    if (!supportedFiles.has(normalizedName)) {
      showMessage(text("unknownFileError", { name: file.name }));
      continue;
    }
    nextFiles.set(normalizedName.replace(".csv", ""), file);
  }
  selectedFiles = nextFiles;
  updateShiftIndicator();
  renderFileStatus();
}

function renderFileStatus() {
  const list = document.getElementById("selectedFileList");
  const missing = [...supportedFiles].filter((fileName) => !selectedFiles.has(fileName.replace(".csv", "")));
  list.replaceChildren();
  [...supportedFiles].forEach((fileName) => {
    const selected = selectedFiles.get(fileName.replace(".csv", ""));
    const item = document.createElement("span");
    item.className = selected
      ? "rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1 text-emerald-700 font-medium"
      : "rounded-full border border-line bg-subtle px-3 py-1 text-subtext";
    item.textContent = selected ? selected.name : fileName;
    item.title = selected ? `${selected.name} · ${formatBytes(selected.size)}` : fileName;
    list.appendChild(item);
  });
  const missingText = document.getElementById("missingFileList");
  const badge = document.getElementById("missingFilesBadge");
  if (missing.length) {
    missingText.textContent = text("missingFiles", { files: missing.join(", ") });
    badge.textContent = String(missing.length);
    badge.classList.remove("hidden");
  } else {
    missingText.textContent = text("allFilesReady");
    badge.classList.add("hidden");
  }
}

async function triggerAnalyze() {
  if (!selectedFiles.size) {
    showMessage(text("selectFilesError"));
    return;
  }
  const buttonText = document.getElementById("rerunText");
  const button = document.getElementById("rerunBtn");
  const spinner = document.getElementById("analysisSpinner");
  button.disabled = true;
  button.classList.add("opacity-60", "cursor-wait");
  spinner.classList.remove("hidden");
  buttonText.textContent = text("analyzing");
  document.getElementById("workspace").setAttribute("aria-busy", "true");
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
    entityFilter = null;
    apiConnected = true;
    updateApiStatus();
    document.getElementById("answerBox").classList.add("hidden");
    renderAnalysis();
  } catch (error) {
    apiConnected = false;
    updateApiStatus();
    showMessage(text("requestError", { message: error.message }));
  } finally {
    button.disabled = false;
    button.classList.remove("opacity-60", "cursor-wait");
    spinner.classList.add("hidden");
    buttonText.textContent = text("runBtn");
    document.getElementById("workspace").setAttribute("aria-busy", "false");
    updateShiftIndicator();
  }
}

function renderAnalysis() {
  const overview = currentAnalysis?.overview;
  document.getElementById("statWorkers").textContent = overview?.active_workers ?? "--";
  document.getElementById("statEquipment").textContent = overview?.active_equipment ?? "--";
  document.getElementById("statEvents").textContent = overview?.shift_events ?? "--";
  document.getElementById("statHighRisks").textContent = overview?.high_priority_risks ?? "--";
  document.getElementById("shiftStartValue").textContent = formatDateTime(overview?.shift_started_at);
  document.getElementById("shiftEndValue").textContent = formatDateTime(overview?.shift_ended_at);
  renderPriorityCounts();
  updatePriorityFilterState();
  renderDataQuality();
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

function renderDataQuality() {
  const overview = currentAnalysis?.overview;
  const panel = document.getElementById("dataQualityPanel");
  const summary = document.getElementById("qualitySummary");
  const details = document.getElementById("qualityDetails");
  const badge = document.getElementById("rejectedBadge");
  details.replaceChildren();
  if (!overview) {
    summary.textContent = text("qualityWaiting");
    badge.classList.add("hidden");
    panel.open = false;
    return;
  }
  const processing = overview?.processing_summary;
  summary.textContent = text("qualitySummary", {
    received: processing.received_records,
    valid: processing.valid_records,
    rejected: processing.rejected_records
  });
  if (processing.rejected_records > 0) {
    badge.textContent = text("rejectedRecords", { count: processing.rejected_records });
    badge.classList.remove("hidden");
    panel.open = true;
  } else {
    badge.classList.add("hidden");
  }
  overview.files.forEach((file) => {
    const item = document.createElement("div");
    item.className = "grid grid-cols-[minmax(0,1fr)_auto] gap-3 rounded-xl bg-subtle/60 px-3.5 py-3 text-xs";
    item.innerHTML = `<div class="min-w-0"><div class="font-medium text-heavy truncate">${escapeHtml(file.source_file || file.file_type)}</div><div class="text-subtext mt-1">${escapeHtml(file.warnings.join(" · ") || "—")}</div></div><div class="font-mono text-right text-subtext">${file.valid_records}/${file.received_records}<br><span class="${file.rejected_records ? "text-rose-700" : ""}">-${file.rejected_records}</span></div>`;
    details.appendChild(item);
  });
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
    button.setAttribute("aria-pressed", String(value === zoneFilter));
    button.className = value === zoneFilter
      ? "focus-ring filter-zone-btn px-3.5 py-1.5 rounded-full text-xs font-medium transition-all bg-heavy text-white"
      : "focus-ring filter-zone-btn px-3.5 py-1.5 rounded-full text-xs font-medium transition-all bg-subtle text-subtext hover:text-heavy";
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
  renderActiveEntityFilter();
  const risks = currentAnalysis?.risks || [];
  if (!currentAnalysis) {
    renderRiskEmpty(container, text("noRisksFeed"));
    document.getElementById("riskCountLabel").textContent = "0";
    return;
  }
  const filtered = risks.filter((risk) => matchesPriority(risk)
    && (zoneFilter === "all" || risk.zone_id === zoneFilter)
    && (!entityFilter || risk.affected_entities.some((entity) => entity.id === entityFilter)))
    .sort((first, second) => second.score - first.score);
  document.getElementById("riskCountLabel").textContent = `${filtered.length} / ${risks.length}`;
  if (!filtered.length) {
    renderRiskEmpty(container, risks.length ? text("noRisksMatch") : text("noRisksDesc"));
    return;
  }
  filtered.forEach((risk) => {
    const presentation = priorityPresentation(risk.priority);
    const card = document.createElement("button");
    card.type = "button";
    card.setAttribute("aria-pressed", String(risk.risk_id === selectedRiskId));
    card.className = risk.risk_id === selectedRiskId
      ? "focus-ring w-full text-left p-4 rounded-2xl border bg-subtle/80 border-heavy shadow-sm transition-all"
      : "focus-ring w-full text-left p-4 rounded-2xl border bg-surface border-line soft-shadow-hover hover:border-neutral-300 transition-all";
    const entities = risk.affected_entities.map((entity) => entity.id).join(", ") || "—";
    card.innerHTML = `<div class="flex items-center justify-between mb-2 gap-3"><div class="flex items-center gap-2 min-w-0"><span class="${presentation.classes} border rounded-full px-2.5 py-0.5 text-[11px] font-semibold">${presentation.label}</span><span class="text-xs font-medium text-subtext truncate">${escapeHtml(risk.zone_id || "—")}</span></div><div class="flex items-center gap-2 shrink-0"><span class="rounded-full bg-heavy text-white px-2.5 py-0.5 text-[11px] font-semibold font-mono">${risk.score}/100</span><span class="text-[11px] font-mono text-subtext">${formatDateTime(risk.detected_at)}</span></div></div><h4 class="text-sm font-semibold text-heavy leading-snug mb-1">${escapeHtml(risk.title)}</h4><p class="text-[11px] text-subtext font-mono truncate">${escapeHtml(entities)}</p>`;
    card.addEventListener("click", () => {
      selectedRiskId = risk.risk_id;
      renderRiskCards();
      renderSelectedRisk();
    });
    container.appendChild(card);
  });
}

function renderActiveEntityFilter() {
  const container = document.getElementById("activeEntityFilter");
  if (!entityFilter) {
    container.classList.add("hidden");
    container.replaceChildren();
    return;
  }
  container.classList.remove("hidden");
  container.innerHTML = `<button type="button" class="focus-ring w-full flex items-center justify-between rounded-xl border border-line bg-subtle px-3 py-2 text-xs text-heavy"><span>${escapeHtml(text("filteringEntity", { entity: entityFilter }))}</span><span class="text-subtext">${escapeHtml(text("clearEntityFilter"))}</span></button>`;
  container.querySelector("button").addEventListener("click", () => {
    entityFilter = null;
    renderRiskCards();
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
    document.getElementById("detailEntities").replaceChildren();
    document.getElementById("exportButton").classList.add("hidden");
    return;
  }
  empty.classList.add("hidden");
  content.classList.remove("hidden");
  const presentation = priorityPresentation(risk.priority);
  const badge = document.getElementById("detailPriorityBadge");
  badge.className = `${presentation.classes} border rounded-full px-3 py-1 text-xs font-semibold`;
  badge.textContent = presentation.label;
  document.getElementById("detailZone").textContent = risk.zone_id || "—";
  document.getElementById("detailScore").textContent = `${risk.score}/100`;
  document.getElementById("detailTime").textContent = formatDateTime(risk.detected_at);
  document.getElementById("detailTitle").textContent = risk.title;
  const entities = document.getElementById("detailEntities");
  entities.replaceChildren();
  risk.affected_entities.forEach((entity) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "focus-ring rounded-full border border-line bg-subtle px-3 py-1 text-[11px] font-medium text-heavy hover:border-neutral-300";
    button.textContent = `${entity.type}: ${entity.id}`;
    button.addEventListener("click", () => {
      entityFilter = entity.id;
      renderRiskCards();
    });
    entities.appendChild(button);
  });
  document.getElementById("detailAction").textContent = risk.recommended_action;
  document.getElementById("detailReasoning").textContent = risk.interpretation;
  const exportButton = document.getElementById("exportButton");
  exportButton.classList.remove("hidden");
  exportButton.onclick = () => exportRiskReport(risk);
  renderScoreBreakdown(risk.score_breakdown);
  renderEvidence(risk);
}

function renderScoreBreakdown(breakdown) {
  const container = document.getElementById("scoreBreakdown");
  container.replaceChildren();
  Object.entries(breakdown || {}).forEach(([label, value]) => {
    const item = document.createElement("div");
    item.className = "score-item";
    item.innerHTML = `<span class="score-value">${escapeHtml(value)}</span><span class="score-label">${escapeHtml(label.replaceAll("_", " "))}</span>`;
    container.appendChild(item);
  });
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
  updatePriorityFilterState();
  renderRiskCards();
}

function updatePriorityFilterState() {
  document.querySelectorAll(".filter-pri-btn").forEach((button) => {
    const selected = button.id === `btn-pri-${priorityFilter}`;
    button.setAttribute("aria-pressed", String(selected));
    button.className = selected
      ? "focus-ring filter-pri-btn flex-1 py-1.5 text-xs font-medium rounded-lg transition-all bg-surface text-heavy shadow-sm"
      : "focus-ring filter-pri-btn flex-1 py-1.5 text-xs font-medium rounded-lg transition-all text-subtext hover:text-heavy";
  });
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

function askPresetQuestion(key) {
  askQuestion(text(key));
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
  const answerEvidenceList = document.getElementById("answerEvidenceList");
  const queryButton = document.getElementById("queryButton");
  const querySpinner = document.getElementById("querySpinner");
  const queryButtonText = document.getElementById("queryButtonText");
  document.getElementById("answerQuestion").textContent = question;
  answerContent.textContent = text("asking");
  answerEvidenceList.replaceChildren();
  answerBox.classList.remove("hidden");
  queryButton.disabled = true;
  querySpinner.classList.remove("hidden");
  queryButtonText.classList.add("hidden");
  document.getElementById("queryInput").disabled = true;
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
    apiConnected = true;
    updateApiStatus();
    const sections = [payload.answer, payload.interpretation, payload.recommended_action].filter(Boolean);
    if (payload.limitations?.length) sections.push(`${text("limitations")}: ${payload.limitations.join(" · ")}`);
    answerContent.textContent = sections.join("\n\n");
    await renderQuestionEvidence(payload.observed_facts || []);
  } catch (error) {
    answerContent.textContent = text("requestError", { message: error.message });
    renderAnswerEvidenceEmpty(answerEvidenceList, text("evidenceUnavailable"));
  } finally {
    queryButton.disabled = false;
    querySpinner.classList.add("hidden");
    queryButtonText.classList.remove("hidden");
    document.getElementById("queryInput").disabled = false;
  }
}

async function renderQuestionEvidence(facts) {
  const container = document.getElementById("answerEvidenceList");
  container.replaceChildren();
  if (!facts.length) {
    renderAnswerEvidenceEmpty(container, text("evidenceUnavailable"));
    return;
  }
  for (const fact of facts) {
    const details = document.createElement("details");
    details.className = "rounded-xl border border-line bg-surface px-3.5 py-3";
    const summary = document.createElement("summary");
    summary.className = "focus-ring cursor-pointer text-xs font-medium text-heavy";
    summary.textContent = fact.statement;
    details.appendChild(summary);
    const evidenceContainer = document.createElement("div");
    evidenceContainer.className = "grid gap-2 mt-3";
    details.appendChild(evidenceContainer);
    container.appendChild(details);
    for (const evidenceId of fact.evidence_ids || []) {
      const evidence = await resolveEvidence(evidenceId);
      evidenceContainer.appendChild(createEvidenceDetail(evidenceId, evidence));
    }
  }
}

async function resolveEvidence(evidenceId) {
  const localEvidence = (currentAnalysis?.risks || [])
    .flatMap((risk) => risk.observed_data || [])
    .find((evidence) => evidence.evidence_id === evidenceId);
  if (localEvidence) return localEvidence;
  try {
    const response = await fetch(apiUrl(`/api/analyses/${encodeURIComponent(currentAnalysis.analysis_id)}/evidence/${encodeURIComponent(evidenceId)}`));
    if (!response.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}

function createEvidenceDetail(evidenceId, evidence) {
  const item = document.createElement("div");
  item.className = "rounded-lg bg-subtle/70 px-3 py-2.5 text-[11px] text-subtext";
  if (!evidence) {
    item.textContent = `${evidenceId} · ${text("evidenceUnavailable")}`;
    return item;
  }
  const facts = Object.entries(evidence.facts).map(([key, value]) => `${key}: ${value ?? "—"}`).join(" · ");
  item.innerHTML = `<div class="font-mono text-heavy">${escapeHtml(evidenceId)}</div><div class="mt-1">${formatDateTime(evidence.timestamp)} · ${escapeHtml(evidence.zone_id || "—")} · ${escapeHtml(evidence.source_file)} · ${text("row")} ${evidence.source_row}</div><div class="mt-1 text-heavy">${escapeHtml(facts)}</div>`;
  return item;
}

function renderAnswerEvidenceEmpty(container, message) {
  const empty = document.createElement("div");
  empty.className = "rounded-lg border border-dashed border-line px-3 py-2 text-[11px] text-subtext";
  empty.textContent = message;
  container.appendChild(empty);
}

function exportRiskReport(risk) {
  const overview = currentAnalysis.overview;
  const lines = [
    risk.title,
    `${text("score")}: ${risk.score}/100`,
    `${text("filterPriority")}: ${risk.priority}`,
    `${text("operatingZone")}: ${risk.zone_id || "—"}`,
    `${text("shiftStart")}: ${formatDateTime(overview.shift_started_at)}`,
    `${text("shiftEnd")}: ${formatDateTime(overview.shift_ended_at)}`,
    "",
    `${text("recommendedProtocol")}:`,
    risk.recommended_action,
    "",
    `${text("analysisReasoning")}:`,
    risk.interpretation,
    "",
    `${text("evidenceHeader")}:`,
    ...risk.observed_data.map((evidence) => {
      const facts = Object.entries(evidence.facts).map(([key, value]) => `${key}: ${value ?? "—"}`).join(" · ");
      return `${formatDateTime(evidence.timestamp)} | ${evidence.zone_id || "—"} | ${evidence.source_file}:${evidence.source_row} | ${facts}`;
    }),
    "",
    `${text("limitations")}:`,
    ...(risk.limitations.length ? risk.limitations : ["—"])
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${risk.risk_id}-report.txt`;
  link.hidden = true;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function formatDateTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  if (date.getFullYear() === 2000 && date.getMonth() === 0 && date.getDate() === 1) {
    return new Intl.DateTimeFormat(currentLanguage === "kk" ? "kk-KZ" : currentLanguage, {
      hour: "2-digit", minute: "2-digit"
    }).format(date);
  }
  return new Intl.DateTimeFormat(currentLanguage === "kk" ? "kk-KZ" : currentLanguage, {
    month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit"
  }).format(date);
}

function formatBytes(value) {
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KB`;
  return `${(value / (1024 * 1024)).toFixed(1)} MB`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

renderFileStatus();
changeLanguage("en");
checkApiStatus();

const dropZone = document.getElementById("dropZone");
dropZone.addEventListener("click", (event) => {
  if (event.target.closest("button")) return;
  document.getElementById("csvFileInput").click();
});
dropZone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    document.getElementById("csvFileInput").click();
  }
});
["dragenter", "dragover"].forEach((eventName) => dropZone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropZone.classList.add("drop-active");
}));
["dragleave", "drop"].forEach((eventName) => dropZone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropZone.classList.remove("drop-active");
}));
dropZone.addEventListener("drop", (event) => selectFiles(event.dataTransfer.files));
