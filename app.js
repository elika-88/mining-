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
    dropHint: "workers.csv, equipment.csv, environment.csv, events.csv — or click to browse", dropActive: "Release to add CSV files",
    clearFiles: "Clear all", removeFile: "Remove", replaceFile: "Replace", fileSelected: "Selected", fileMissing: "Missing",
    fileReplaced: "{name} replaced", incompleteCoverage: "Data coverage is incomplete; analysis may be limited.", fileTooLarge: "{name} exceeds the 10 MB limit.",
    nonCsvFile: "{name} is not a CSV file.", emptyFile: "Empty file", apiDisconnectedHelp: "Backend unavailable — start run.ps1 and retry.",
    backendTimeout: "Backend request timed out — retry or inspect the backend console.", noValidRecords: "No valid records — inspect rejected rows in Data Quality.",
    noRiskCaution: "No detected risks — this does not prove the shift is safe.", aiChecking: "Checking AI", aiConfigured: "AI configured", aiConnected: "AI routed", aiFallback: "AI fallback",
    aiModel: "Model", aiRouted: "AI-routed", deterministicFallback: "Deterministic fallback", insufficientData: "Insufficient data",
    aiFallbackNotice: "AI provider unavailable; grounded fallback used.", printReport: "Print / Save PDF", exportJson: "Export JSON",
    timelineTitle: "Evidence timeline", timelineNotice: "Shows only observed records returned by the analysis; no movement path is inferred.", recentThirty: "Last 30 minutes",
    noTimeline: "No observed records are available for the current filters.", qualityContractNote: "The current API exposes file-level warnings; rejected row details are not available to the frontend."
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
    dropHint: "workers.csv, equipment.csv, environment.csv, events.csv — немесе таңдау үшін басыңыз", dropActive: "CSV файлдарын қосу үшін жіберіңіз",
    clearFiles: "Барлығын тазалау", removeFile: "Жою", replaceFile: "Ауыстыру", fileSelected: "Таңдалды", fileMissing: "Жоқ",
    fileReplaced: "{name} ауыстырылды", incompleteCoverage: "Деректер толық емес; талдау шектеулі болуы мүмкін.", fileTooLarge: "{name} 10 МБ шегінен асады.",
    nonCsvFile: "{name} CSV файлы емес.", emptyFile: "Бос файл", apiDisconnectedHelp: "Сервер қолжетімсіз — run.ps1 іске қосып, қайталаңыз.",
    backendTimeout: "Сервер сұрауының уақыты аяқталды — қайта көріңіз.", noValidRecords: "Жарамды жазба жоқ — Data Quality бөлімін тексеріңіз.",
    noRiskCaution: "Қауіп анықталмады — бұл ауысым толық қауіпсіз екенін дәлелдемейді.", aiChecking: "AI тексерілуде", aiConfigured: "AI бапталған", aiConnected: "AI бағыттады", aiFallback: "AI резервтік режимде",
    aiModel: "Модель", aiRouted: "AI бағыттады", deterministicFallback: "Детерминирленген резерв", insufficientData: "Дерек жеткіліксіз",
    aiFallbackNotice: "AI провайдері қолжетімсіз; деректерге негізделген резерв қолданылды.", printReport: "Басып шығару / PDF", exportJson: "JSON экспорттау",
    timelineTitle: "Дәлелдер уақыт сызығы", timelineNotice: "Тек талдаудан қайтарылған нақты жазбалар көрсетіледі; қозғалыс жолы болжанбайды.", recentThirty: "Соңғы 30 минут",
    noTimeline: "Ағымдағы сүзгілер үшін бақылау жазбалары жоқ.", qualityContractNote: "API файл деңгейіндегі ескертулерді ғана береді; қабылданбаған жол деректері фронтендке берілмейді."
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
    dropHint: "workers.csv, equipment.csv, environment.csv, events.csv — или нажмите для выбора", dropActive: "Отпустите, чтобы добавить CSV",
    clearFiles: "Очистить всё", removeFile: "Удалить", replaceFile: "Заменить", fileSelected: "Выбран", fileMissing: "Отсутствует",
    fileReplaced: "{name} заменён", incompleteCoverage: "Покрытие данных неполное; анализ может быть ограничен.", fileTooLarge: "{name} превышает лимит 10 МБ.",
    nonCsvFile: "{name} не является CSV-файлом.", emptyFile: "Пустой файл", apiDisconnectedHelp: "Backend недоступен — запустите run.ps1 и повторите.",
    backendTimeout: "Истекло время ожидания backend — повторите запрос.", noValidRecords: "Нет корректных записей — проверьте Data Quality.",
    noRiskCaution: "Риски не обнаружены — это не доказывает безопасность смены.", aiChecking: "Проверка AI", aiConfigured: "AI настроен", aiConnected: "AI маршрутизировал", aiFallback: "AI fallback",
    aiModel: "Модель", aiRouted: "AI-routed", deterministicFallback: "Детерминированный fallback", insufficientData: "Недостаточно данных",
    aiFallbackNotice: "AI provider недоступен; использован grounded fallback.", printReport: "Печать / Сохранить PDF", exportJson: "Экспорт JSON",
    timelineTitle: "Хронология доказательств", timelineNotice: "Показаны только фактические записи анализа; траектория движения не моделируется.", recentThirty: "Последние 30 минут",
    noTimeline: "Для текущих фильтров нет наблюдаемых записей.", qualityContractNote: "API передаёт предупреждения на уровне файлов; детали отклонённых строк недоступны фронтенду."
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
    dropHint: "workers.csv、equipment.csv、environment.csv、events.csv，也可以点击选择", dropActive: "松开即可添加 CSV 文件",
    clearFiles: "清空全部", removeFile: "删除", replaceFile: "替换", fileSelected: "已选择", fileMissing: "缺失",
    fileReplaced: "已替换 {name}", incompleteCoverage: "数据覆盖不完整，分析结果可能有限。", fileTooLarge: "{name} 超过 10 MB 限制。",
    nonCsvFile: "{name} 不是 CSV 文件。", emptyFile: "空文件", apiDisconnectedHelp: "后端不可用——请启动 run.ps1 后重试。",
    backendTimeout: "后端请求超时——请重试或检查后端控制台。", noValidRecords: "没有有效记录——请在数据质量面板检查被拒绝的行。",
    noRiskCaution: "未检测到风险——这并不能证明当前班次绝对安全。", aiChecking: "正在检查 AI", aiConfigured: "AI 已配置", aiConnected: "AI 已路由", aiFallback: "AI 降级模式",
    aiModel: "模型", aiRouted: "AI 路由", deterministicFallback: "确定性降级", insufficientData: "数据不足",
    aiFallbackNotice: "AI 提供商不可用，已使用基于数据的降级回答。", printReport: "打印 / 保存为 PDF", exportJson: "导出 JSON",
    timelineTitle: "证据时间线", timelineNotice: "仅显示分析返回的真实观测记录，不推测人员或设备移动轨迹。", recentThirty: "最近 30 分钟",
    noTimeline: "当前筛选条件下没有观测记录。", qualityContractNote: "当前 API 仅提供文件级警告；前端无法获得被拒绝行的结构化详情。"
  }
};

const apiBase = window.MINE_API_BASE || ((location.hostname === "localhost" || location.hostname === "127.0.0.1") ? "http://127.0.0.1:8000" : location.origin);
const supportedFiles = new Set(["workers.csv", "equipment.csv", "environment.csv", "events.csv"]);
const maxFileBytes = 10 * 1024 * 1024;
const preferenceKey = "mine-safety-ui-preferences";
const storedPreferences = loadPreferences();
let currentLanguage = ["en", "kk", "ru", "zh"].includes(storedPreferences.language) ? storedPreferences.language : "en";
let selectedFiles = new Map();
let currentAnalysis = null;
let selectedRiskId = null;
let priorityFilter = ["all", "high", "medium", "low"].includes(storedPreferences.priorityFilter) ? storedPreferences.priorityFilter : "all";
let zoneFilter = storedPreferences.zoneFilter || "all";
let entityFilter = null;
let apiConnected = null;
let aiConfig = null;
let lastAnswerMode = null;
let lastFallbackReason = null;
let riskThresholds = null;
let replaceTarget = null;
let isAnalyzing = false;

function text(key, values = {}) {
  let value = translations[currentLanguage][key] || translations.en[key] || key;
  Object.entries(values).forEach(([name, replacement]) => {
    value = value.replace(`{${name}}`, String(replacement));
  });
  return value;
}

function loadPreferences() {
  try {
    return JSON.parse(localStorage.getItem(preferenceKey) || "{}");
  } catch {
    return {};
  }
}

function savePreferences() {
  localStorage.setItem(preferenceKey, JSON.stringify({
    language: currentLanguage,
    priorityFilter,
    zoneFilter,
    qualityOpen: document.getElementById("dataQualityPanel")?.open || false
  }));
}

function apiUrl(path) {
  return `${apiBase.replace(/\/$/, "")}${path}`;
}

async function checkApiStatus() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 2500);
  try {
    const [healthResponse, aiResponse, thresholdsResponse] = await Promise.all([
      fetch(apiUrl("/api/health"), { signal: controller.signal }),
      fetch(apiUrl("/api/config/ai"), { signal: controller.signal }),
      fetch(apiUrl("/api/config/risk-thresholds"), { signal: controller.signal })
    ]);
    apiConnected = healthResponse.ok;
    aiConfig = aiResponse.ok ? await aiResponse.json() : null;
    riskThresholds = thresholdsResponse.ok ? await thresholdsResponse.json() : null;
  } catch {
    apiConnected = false;
    aiConfig = null;
    riskThresholds = null;
  } finally {
    clearTimeout(timeout);
    updateApiStatus();
    updateAiStatus();
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

function updateAiStatus() {
  const status = document.getElementById("aiStatus");
  if (apiConnected === null) {
    status.textContent = text("aiChecking");
    status.className = "min-w-[148px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-neutral-100 text-subtext border border-line";
    return;
  }
  const configured = Boolean(apiConnected && aiConfig?.configured);
  const routed = configured && lastAnswerMode === "llm_routed";
  const fallback = !configured || lastFallbackReason === "ai_route_unavailable";
  const model = aiConfig?.model ? ` · ${aiConfig.model}` : "";
  status.textContent = routed
    ? `${text("aiConnected")}${model}`
    : fallback
      ? `${text("aiFallback")}${model}`
      : `${text("aiConfigured")}${model}`;
  status.title = aiConfig?.model ? `${text("aiModel")}: ${aiConfig.model}` : text("aiFallbackNotice");
  status.className = routed
    ? "ai-connected min-w-[148px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium"
    : fallback
      ? "min-w-[148px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-800 border border-amber-100"
      : "min-w-[148px] flex items-center justify-center px-3 py-1 rounded-full text-xs font-medium bg-sky-50 text-sky-800 border border-sky-100";
}

async function changeLanguage(language) {
  const scrollPosition = window.scrollY;
  if (!translations[language]) return;
  const previousLanguage = currentLanguage;
  const languageSelect = document.getElementById("languageSelect");
  if (currentAnalysis && (currentAnalysis.language || "en") !== language) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);
    languageSelect.disabled = true;
    try {
      const response = await fetch(apiUrl(`/api/analyses/${encodeURIComponent(currentAnalysis.analysis_id)}/localize`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language }),
        signal: controller.signal
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(payload?.detail || `${response.status} ${response.statusText}`);
      currentAnalysis = payload;
      if (!(payload.risks || []).some((risk) => risk.risk_id === selectedRiskId)) {
        selectedRiskId = payload.risks?.[0]?.risk_id || null;
      }
      document.getElementById("answerBox").classList.add("hidden");
      apiConnected = true;
    } catch (error) {
      languageSelect.value = previousLanguage;
      showMessage(classifyRequestError(error));
      return;
    } finally {
      clearTimeout(timeout);
      languageSelect.disabled = false;
    }
  }
  currentLanguage = language;
  document.documentElement.lang = language;
  if (languageSelect.value !== language) languageSelect.value = language;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = text(element.dataset.i18n);
  });
  document.getElementById("queryInput").placeholder = text("inputPlaceholder");
  updateShiftIndicator();
  updateApiStatus();
  updateAiStatus();
  renderFileStatus();
  renderAnalysis();
  savePreferences();
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
  const answerMode = document.getElementById("answerMode");
  answerMode.textContent = text("insufficientData");
  answerMode.className = "rounded-full border border-amber-100 bg-amber-50 px-2.5 py-1 text-[11px] text-amber-800 font-medium";
  const evidenceList = document.getElementById("answerEvidenceList");
  evidenceList.replaceChildren();
  if (sources) renderAnswerEvidenceEmpty(evidenceList, sources);
  document.getElementById("answerBox").classList.remove("hidden");
}

function handleFilesUpload(event) {
  selectFiles(event.target.files);
  event.target.value = "";
}

function selectFiles(files, replace = false) {
  const nextFiles = replace ? new Map() : new Map(selectedFiles);
  const feedback = [];
  for (const file of files) {
    const normalizedName = file.name.toLowerCase();
    if (!normalizedName.endsWith(".csv") || (file.type && !["text/csv", "application/vnd.ms-excel"].includes(file.type))) {
      feedback.push(text("nonCsvFile", { name: file.name }));
      continue;
    }
    if (!supportedFiles.has(normalizedName)) {
      feedback.push(text("unknownFileError", { name: file.name }));
      continue;
    }
    if (file.size > maxFileBytes) {
      feedback.push(text("fileTooLarge", { name: file.name }));
      continue;
    }
    const field = normalizedName.replace(".csv", "");
    if (nextFiles.has(field)) feedback.push(text("fileReplaced", { name: file.name }));
    nextFiles.set(field, file);
  }
  selectedFiles = nextFiles;
  updateShiftIndicator();
  renderFileStatus();
  if (feedback.length) showFileFeedback(feedback.join(" · "), true);
}

function renderFileStatus() {
  const list = document.getElementById("selectedFileList");
  const missing = [...supportedFiles].filter((fileName) => !selectedFiles.has(fileName.replace(".csv", "")));
  list.replaceChildren();
  [...supportedFiles].forEach((fileName) => {
    const field = fileName.replace(".csv", "");
    const selected = selectedFiles.get(field);
    const item = document.createElement("article");
    item.className = selected
      ? "rounded-xl border border-emerald-100 bg-emerald-50 p-3 text-emerald-800"
      : "rounded-xl border border-line bg-subtle/70 p-3 text-subtext";
    const heading = document.createElement("div");
    heading.className = "font-medium text-heavy truncate";
    heading.textContent = selected ? selected.name : fileName;
    heading.title = heading.textContent;
    const meta = document.createElement("div");
    meta.className = "mt-1 text-[11px]";
    meta.textContent = selected
      ? `${field} · ${formatBytes(selected.size)} · ${selected.size ? text("fileSelected") : text("emptyFile")}`
      : `${field} · ${text("fileMissing")}`;
    item.append(heading, meta);
    if (selected) {
      const actions = document.createElement("div");
      actions.className = "mt-3 flex gap-2";
      actions.append(
        createFileAction(text("replaceFile"), () => beginReplaceFile(field)),
        createFileAction(text("removeFile"), () => removeFile(field), true)
      );
      item.appendChild(actions);
    }
    list.appendChild(item);
  });
  const missingText = document.getElementById("missingFileList");
  const badge = document.getElementById("missingFilesBadge");
  if (missing.length) {
    missingText.textContent = text("missingFiles", { files: missing.join(", ") });
    badge.textContent = String(missing.length);
    badge.classList.remove("hidden");
    showFileFeedback(text("incompleteCoverage"));
  } else {
    missingText.textContent = text("allFilesReady");
    badge.classList.add("hidden");
    showFileFeedback("");
  }
  document.getElementById("clearFilesButton").classList.toggle("hidden", selectedFiles.size === 0);
  document.getElementById("rerunBtn").disabled = selectedFiles.size === 0 || isAnalyzing;
}

function createFileAction(label, handler, destructive = false) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `focus-ring rounded-lg border px-2.5 py-1 text-[11px] font-medium ${destructive ? "border-rose-100 bg-white text-rose-700" : "border-line bg-white text-heavy"}`;
  button.textContent = label;
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    handler();
  });
  return button;
}

function removeFile(field) {
  selectedFiles.delete(field);
  renderFileStatus();
  updateShiftIndicator();
}

function beginReplaceFile(field) {
  replaceTarget = field;
  document.getElementById("replaceFileInput").click();
}

function clearFiles() {
  selectedFiles.clear();
  currentAnalysis = null;
  selectedRiskId = null;
  renderFileStatus();
  renderAnalysis();
  updateShiftIndicator();
}

function showFileFeedback(message, isError = false) {
  const notice = document.getElementById("fileCoverageNotice");
  notice.textContent = message;
  notice.classList.toggle("hidden", !message);
  notice.className = `${message ? "mt-2 rounded-lg px-3 py-2 text-xs" : "hidden"} ${isError ? "bg-rose-50 text-rose-700" : "bg-amber-50 text-amber-800"}`;
}

async function triggerAnalyze() {
  if (!selectedFiles.size || isAnalyzing) {
    showMessage(text("selectFilesError"));
    return;
  }
  const buttonText = document.getElementById("rerunText");
  const button = document.getElementById("rerunBtn");
  const spinner = document.getElementById("analysisSpinner");
  isAnalyzing = true;
  button.disabled = true;
  button.classList.add("opacity-60", "cursor-wait");
  spinner.classList.remove("hidden");
  buttonText.textContent = text("analyzing");
  document.getElementById("workspace").setAttribute("aria-busy", "true");
  const formData = new FormData();
  selectedFiles.forEach((file, field) => formData.append(field, file, file.name));
  formData.append("language", currentLanguage);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);
  try {
    const response = await fetch(apiUrl("/api/analyses"), { method: "POST", body: formData, signal: controller.signal });
    const payload = await response.json().catch(() => null);
    if (!response.ok) throw new Error(payload?.detail || `${response.status} ${response.statusText}`);
    currentAnalysis = payload;
    selectedRiskId = payload.risks[0]?.risk_id || null;
    priorityFilter = "all";
    zoneFilter = "all";
    entityFilter = null;
    apiConnected = true;
    lastAnswerMode = payload.answer_mode;
    lastFallbackReason = payload.fallback_reason;
    updateApiStatus();
    updateAiStatus();
    document.getElementById("answerBox").classList.add("hidden");
    renderAnalysis();
  } catch (error) {
    apiConnected = false;
    updateApiStatus();
    showMessage(classifyRequestError(error));
  } finally {
    clearTimeout(timeout);
    isAnalyzing = false;
    button.disabled = selectedFiles.size === 0;
    button.classList.remove("opacity-60", "cursor-wait");
    spinner.classList.add("hidden");
    buttonText.textContent = text("runBtn");
    document.getElementById("workspace").setAttribute("aria-busy", "false");
    updateShiftIndicator();
  }
}

function classifyRequestError(error) {
  if (error?.name === "AbortError") return text("backendTimeout");
  if (error instanceof TypeError || /failed to fetch|network/i.test(error?.message || "")) return text("apiDisconnectedHelp");
  return text("requestError", { message: error?.message || "Unknown error" });
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
  renderTimeline();
  if (overview && overview.processing_summary.valid_records === 0) {
    showMessage(text("noValidRecords"));
  }
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
    panel.open = Boolean(storedPreferences.qualityOpen);
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
    panel.open = Boolean(storedPreferences.qualityOpen);
  }
  const tableWrap = document.createElement("div");
  tableWrap.className = "overflow-x-auto rounded-xl border border-line";
  const table = document.createElement("table");
  table.className = "w-full text-left text-xs";
  table.innerHTML = "<thead class=\"bg-subtle text-subtext\"><tr><th class=\"px-3 py-2 font-medium\">File</th><th class=\"px-3 py-2 font-medium\">Received</th><th class=\"px-3 py-2 font-medium\">Valid</th><th class=\"px-3 py-2 font-medium\">Rejected</th><th class=\"px-3 py-2 font-medium\">Status</th></tr></thead>";
  const body = document.createElement("tbody");
  overview.files.forEach((file) => {
    const row = document.createElement("tr");
    row.className = "border-t border-line text-heavy";
    const status = file.rejected_records || file.warnings.length ? "Warning" : "Valid";
    row.innerHTML = `<td class="px-3 py-2 font-medium">${escapeHtml(file.source_file || file.file_type)}</td><td class="px-3 py-2 font-mono">${file.received_records}</td><td class="px-3 py-2 font-mono">${file.valid_records}</td><td class="px-3 py-2 font-mono ${file.rejected_records ? "text-rose-700" : ""}">${file.rejected_records}</td><td class="px-3 py-2"><span class="rounded-full px-2 py-0.5 ${status === "Warning" ? "bg-amber-50 text-amber-800" : "bg-emerald-50 text-emerald-700"}">${status}</span></td>`;
    body.appendChild(row);
    if (file.warnings.length) {
      const warningRow = document.createElement("tr");
      warningRow.className = "border-t border-line";
      warningRow.innerHTML = `<td colspan="5" class="px-3 py-2"><details><summary class="focus-ring cursor-pointer text-xs font-medium text-amber-800">${file.warnings.length} warning(s)</summary><div class="mt-2 grid gap-1 text-xs text-subtext">${file.warnings.map((warning) => `<div>${escapeHtml(warning)}</div>`).join("")}</div></details></td>`;
      body.appendChild(warningRow);
    }
  });
  table.appendChild(body);
  tableWrap.appendChild(table);
  details.appendChild(tableWrap);
  const contractNote = document.createElement("p");
  contractNote.className = "text-[11px] text-subtext";
  contractNote.textContent = text("qualityContractNote");
  details.appendChild(contractNote);
}

function renderZoneFilters() {
  const container = document.getElementById("zoneFiltersContainer");
  container.replaceChildren();
  const zones = [...new Set((currentAnalysis?.risks || []).map((risk) => risk.zone_id).filter(Boolean))];
  if (currentAnalysis && zoneFilter !== "all" && !zones.includes(zoneFilter)) zoneFilter = "all";
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
    renderTimeline();
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
    empty.querySelector("p").textContent = currentAnalysis ? text("noRiskCaution") : text("noDataDesc");
    document.getElementById("detailEntities").replaceChildren();
    document.getElementById("reportActions").classList.add("hidden");
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
      renderTimeline();
    });
    entities.appendChild(button);
  });
  document.getElementById("detailAction").textContent = risk.recommended_action;
  document.getElementById("detailReasoning").textContent = risk.interpretation;
  const limitations = document.getElementById("detailLimitations");
  limitations.replaceChildren();
  (risk.limitations.length ? risk.limitations : [text("insufficientEvidence")]).forEach((limitation) => {
    const item = document.createElement("div");
    item.textContent = limitation;
    limitations.appendChild(item);
  });
  const reportActions = document.getElementById("reportActions");
  reportActions.classList.remove("hidden");
  document.getElementById("printButton").onclick = () => printRiskReport(risk);
  document.getElementById("jsonExportButton").onclick = () => exportRiskJson(risk);
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
    const issues = evidence.validation_issues?.length
      ? `<div class="mt-2 rounded-lg bg-amber-50 px-2.5 py-2 text-amber-800">${escapeHtml(evidence.validation_issues.join(" · "))}</div>`
      : "";
    row.innerHTML = `<div class="flex items-start justify-between gap-4"><div class="min-w-0"><div class="font-medium text-heavy break-words">${escapeHtml(facts)}</div><div class="font-mono text-[11px] text-subtext mt-1">${formatDateTime(evidence.timestamp)} · ${escapeHtml(evidence.zone_id || "—")} · ${text("row")} ${evidence.source_row}</div>${issues}</div><span class="shrink-0 font-mono text-[11px] text-subtext bg-surface px-2.5 py-0.5 rounded-md border border-line">${escapeHtml(evidence.source_file)}</span></div>`;
    list.appendChild(row);
  });
}

function setFilterPriority(priority) {
  priorityFilter = priority;
  savePreferences();
  updatePriorityFilterState();
  renderRiskCards();
  renderTimeline();
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
  savePreferences();
  renderZoneFilters();
  renderRiskCards();
  renderTimeline();
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
  const answerMode = document.getElementById("answerMode");
  document.getElementById("answerQuestion").textContent = question;
  answerContent.textContent = text("asking");
  answerMode.textContent = text("asking");
  answerEvidenceList.replaceChildren();
  answerBox.classList.remove("hidden");
  queryButton.disabled = true;
  querySpinner.classList.remove("hidden");
  queryButtonText.classList.add("hidden");
  document.getElementById("queryInput").disabled = true;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 45000);
  try {
    const requestPayload = { question, language: currentLanguage };
    const selectedRiskReference = /this (?:alert|risk)|selected (?:alert|risk)|这个(?:告警|风险)|该(?:告警|风险)|этот риск|это предупреждение|осы қауіп/i;
    if (selectedRiskId && selectedRiskReference.test(question)) {
      requestPayload.risk_id = selectedRiskId;
    }
    const response = await fetch(apiUrl(`/api/analyses/${encodeURIComponent(currentAnalysis.analysis_id)}/questions`), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestPayload),
      signal: controller.signal
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) throw new Error(payload?.detail || `${response.status} ${response.statusText}`);
    apiConnected = true;
    updateApiStatus();
    const sections = [payload.answer, payload.interpretation, payload.recommended_action].filter(Boolean);
    const mode = answerModePresentation(payload);
    answerMode.textContent = mode.label;
    answerMode.className = mode.classes;
    if (payload.fallback_reason === "ai_route_unavailable") sections.push(text("aiFallbackNotice"));
    if (payload.limitations?.length) sections.push(`${text("limitations")}: ${payload.limitations.join(" · ")}`);
    answerContent.textContent = sections.join("\n\n");
    await renderQuestionEvidence(payload.observed_facts || []);
  } catch (error) {
    answerMode.textContent = text("insufficientData");
    answerContent.textContent = classifyRequestError(error);
    renderAnswerEvidenceEmpty(answerEvidenceList, text("evidenceUnavailable"));
  } finally {
    clearTimeout(timeout);
    queryButton.disabled = false;
    querySpinner.classList.add("hidden");
    queryButtonText.classList.remove("hidden");
    document.getElementById("queryInput").disabled = false;
  }
}

function answerModePresentation(payload) {
  if (!payload.observed_facts?.length) {
    return { label: text("insufficientData"), classes: "rounded-full border border-amber-100 bg-amber-50 px-2.5 py-1 text-[11px] text-amber-800 font-medium" };
  }
  if (payload.answer_mode === "llm_routed") {
    const model = payload.model_used ? ` · ${payload.model_used}` : "";
    return { label: `${text("aiRouted")}${model}`, classes: "ai-mode rounded-full border px-2.5 py-1 text-[11px] font-medium" };
  }
  return { label: text("deterministicFallback"), classes: "rounded-full border border-line bg-surface px-2.5 py-1 text-[11px] text-subtext font-medium" };
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

function renderTimeline() {
  const container = document.getElementById("timelineList");
  if (!container) return;
  container.replaceChildren();
  const risks = currentAnalysis?.risks || [];
  const entries = [];
  const evidenceIds = new Set();
  risks.forEach((risk) => {
    risk.observed_data.forEach((evidence) => {
      if (evidenceIds.has(evidence.evidence_id)) return;
      evidenceIds.add(evidence.evidence_id);
      entries.push({
        type: evidence.source_file.replace(".csv", ""),
        timestamp: evidence.timestamp,
        zone: evidence.zone_id,
        facts: evidence.facts,
        label: Object.entries(evidence.facts).map(([key, value]) => `${key}: ${value ?? "—"}`).join(" · "),
        riskId: risk.risk_id,
        priority: risk.priority,
        source: `${evidence.source_file}:${evidence.source_row}`
      });
    });
    entries.push({
      type: "risk",
      timestamp: risk.detected_at,
      zone: risk.zone_id,
      facts: {},
      label: `${risk.title} · ${risk.score}/100`,
      riskId: risk.risk_id,
      priority: risk.priority,
      source: risk.risk_id
    });
  });
  const shiftEnd = currentAnalysis?.overview?.shift_ended_at ? new Date(currentAnalysis.overview.shift_ended_at) : null;
  const recentOnly = document.getElementById("timelineRecentOnly")?.checked;
  const filtered = entries.filter((entry) => {
    if (zoneFilter !== "all" && entry.zone !== zoneFilter) return false;
    if (entityFilter && !Object.values(entry.facts).some((value) => String(value) === entityFilter)) return false;
    if (recentOnly && shiftEnd && entry.timestamp) {
      return new Date(entry.timestamp) >= new Date(shiftEnd.getTime() - 30 * 60 * 1000);
    }
    return true;
  }).sort((first, second) => new Date(first.timestamp || 0) - new Date(second.timestamp || 0));
  if (!filtered.length) {
    renderRiskEmpty(container, text("noTimeline"));
    return;
  }
  filtered.forEach((entry) => {
    const button = document.createElement("button");
    button.type = "button";
    const emphasized = entry.type === "risk" && ["CRITICAL", "HIGH"].includes(entry.priority);
    button.className = `focus-ring grid grid-cols-[88px_88px_minmax(0,1fr)_auto] items-center gap-3 rounded-xl border px-3.5 py-3 text-left text-xs ${emphasized ? "border-rose-100 bg-rose-50" : "border-line bg-subtle/50"}`;
    button.innerHTML = `<span class="font-mono text-subtext">${formatDateTime(entry.timestamp)}</span><span class="font-medium text-heavy capitalize">${escapeHtml(entry.type)}</span><span class="min-w-0 break-words text-heavy">${escapeHtml(entry.label)}</span><span class="font-mono text-[11px] text-subtext">${escapeHtml(entry.source)}</span>`;
    button.addEventListener("click", () => {
      selectedRiskId = entry.riskId;
      renderRiskCards();
      renderSelectedRisk();
      document.getElementById("inspectorContainer").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    container.appendChild(button);
  });
}

function buildRiskReport(risk) {
  const overview = currentAnalysis.overview;
  return {
    analysis_id: currentAnalysis.analysis_id,
    analysis_metadata: currentAnalysis.metadata || null,
    generated_at: new Date().toISOString(),
    data_coverage: overview.files,
    overview,
    risk,
    risk_thresholds: riskThresholds
  };
}

function exportRiskJson(risk) {
  const report = buildRiskReport(risk);
  const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${risk.risk_id}-${new Date().toISOString().replaceAll(":", "-")}.json`;
  link.hidden = true;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function printRiskReport(risk) {
  const report = buildRiskReport(risk);
  const scoreRows = Object.entries(risk.score_breakdown).map(([key, value]) => `<tr><td>${escapeHtml(key)}</td><td>${value}</td></tr>`).join("");
  const evidenceRows = risk.observed_data.map((evidence) => `<tr><td>${formatDateTime(evidence.timestamp)}</td><td>${escapeHtml(evidence.zone_id || "—")}</td><td>${escapeHtml(evidence.source_file)}:${evidence.source_row}</td><td>${escapeHtml(JSON.stringify(evidence.facts))}</td></tr>`).join("");
  const fileRows = report.data_coverage.map((file) => `<tr><td>${escapeHtml(file.source_file || file.file_type)}</td><td>${file.received_records}</td><td>${file.valid_records}</td><td>${file.rejected_records}</td></tr>`).join("");
  const metadata = report.analysis_metadata;
  const auditLine = metadata
    ? `${escapeHtml(metadata.engine_version)} · ${escapeHtml(metadata.source_of_truth)} · ${escapeHtml(metadata.data_fingerprint)}`
    : "—";
  const printWindow = window.open("", "_blank");
  if (!printWindow) return;
  printWindow.opener = null;
  printWindow.document.write(`<!doctype html><html><head><title>${escapeHtml(risk.risk_id)}</title><style>body{font:14px Arial,sans-serif;color:#111;margin:32px}h1{font-size:24px}h2{font-size:16px;margin-top:24px}table{width:100%;border-collapse:collapse;margin-top:8px}th,td{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}.meta{color:#555;overflow-wrap:anywhere}.action{background:#fff8e8;padding:12px;border:1px solid #ead9b7}.limits{background:#fffbea;padding:12px}@media print{button{display:none}}</style></head><body><button onclick="window.print()">${escapeHtml(text("printReport"))}</button><h1>${escapeHtml(risk.title)}</h1><p class="meta">${escapeHtml(report.analysis_id)} · ${escapeHtml(report.generated_at)} · ${escapeHtml(risk.priority)} · ${risk.score}/100</p><p class="meta">Engine / source / SHA-256: ${auditLine}</p><p>${escapeHtml(risk.zone_id || "—")} · ${escapeHtml(risk.affected_entities.map((entity) => `${entity.type}: ${entity.id}`).join(" · "))}</p><h2>Data coverage</h2><table><tr><th>File</th><th>Received</th><th>Valid</th><th>Rejected</th></tr>${fileRows}</table><h2>${escapeHtml(text("evidenceHeader"))}</h2><table><tr><th>Time</th><th>Zone</th><th>Source</th><th>Observed values</th></tr>${evidenceRows}</table><h2>${escapeHtml(text("analysisReasoning"))}</h2><p>${escapeHtml(risk.interpretation)}</p><h2>${escapeHtml(text("recommendedProtocol"))}</h2><p class="action">${escapeHtml(risk.recommended_action)}</p><h2>${escapeHtml(text("limitations"))}</h2><div class="limits">${risk.limitations.map((item) => `<p>${escapeHtml(item)}</p>`).join("")}</div><h2>${escapeHtml(text("scoreBreakdown"))}</h2><table>${scoreRows}</table><h2>Thresholds</h2><pre>${escapeHtml(JSON.stringify(metadata?.thresholds || riskThresholds, null, 2))}</pre></body></html>`);
  printWindow.document.close();
  printWindow.focus();
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
changeLanguage(currentLanguage);
checkApiStatus();

const dropZone = document.getElementById("dropZone");
document.getElementById("clearFilesButton").addEventListener("click", (event) => {
  event.stopPropagation();
  clearFiles();
});
document.getElementById("replaceFileInput").addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file && replaceTarget && file.name.toLowerCase() === `${replaceTarget}.csv`) {
    selectFiles([file]);
  } else if (file) {
    showFileFeedback(text("unknownFileError", { name: file.name }), true);
  }
  replaceTarget = null;
  event.target.value = "";
});
document.getElementById("dataQualityPanel").addEventListener("toggle", savePreferences);
document.getElementById("timelineRecentOnly").addEventListener("change", renderTimeline);
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
