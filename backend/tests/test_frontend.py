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
