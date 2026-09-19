from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_frontend_is_offline_and_exposes_required_overview_fields() -> None:
    html = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")

    assert 'href="styles.css"' in html
    assert "cdn.tailwindcss.com" not in html
    assert "cdn.jsdelivr.net" not in html
    assert "fonts.googleapis.com" not in html
    assert 'id="statWorkers"' in html
    assert 'id="statEquipment"' in html
    assert 'id="statEvents"' in html
    assert 'id="statHighRisks"' in html
    assert 'id="dropZone"' in html
    assert 'id="selectedFileList"' in html


def test_frontend_exposes_grounding_and_quality_sections() -> None:
    html = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")
    javascript = (PROJECT_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="evidenceList"' in html
    assert 'id="detailReasoning"' in html
    assert 'id="detailAction"' in html
    assert 'id="scoreBreakdown"' in html
    assert 'id="dataQualityPanel"' in html
    assert "overview?.high_priority_risks" in javascript
    assert "overview?.processing_summary" in javascript
    assert 'dropZone.addEventListener("drop"' in javascript
    assert "selectFiles(event.dataTransfer.files)" in javascript


def test_frontend_exposes_ai_status_and_managed_uploads() -> None:
    html = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")
    javascript = (PROJECT_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="aiStatus"' in html
    assert 'id="clearFilesButton"' in html
    assert 'id="replaceFileInput"' in html
    assert 'id="detailLimitations"' in html
    assert 'id="answerMode"' in html
    assert 'fetch(apiUrl("/api/config/ai")' in javascript
    assert "function removeFile" in javascript
    assert "payload.fallback_reason === \"ai_route_unavailable\"" in javascript
    assert "currentAnalysis.metadata || null" in javascript
    assert "payload.model_used" in javascript
    assert "function beginReplaceFile" in javascript
    assert "maxFileBytes" in javascript
    assert "answerModePresentation" in javascript
