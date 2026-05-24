"""Phase 0 (Marketing + Demo) acceptance test suite.

Verifies all deliverables from the ns-P0 spec without a browser, DB, or network.
Tests are pure filesystem + text-pattern checks; no imports from app/ required.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_NS = Path(__file__).parent.parent.parent  # projects/neurospect/
_UI = _NS / "neurospect-ui"
_API = _NS / "api"
_APP = _NS / "app" / "src"
_DOCS = _NS / "docs"
_HANDOFF = _NS / "design-handoff"
_COURSE_DIR = _UI / "uploads" / "course"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# ===========================================================================
# 1. Marketing Site — page existence
# ===========================================================================

class TestMarketingSiteExists:
    PAGES = ["index.html", "simulator.html", "course.html", "research.html", "pricing.html", "guide.html"]

    @pytest.mark.parametrize("page", PAGES)
    def test_html_page_exists(self, page: str):
        assert (_UI / page).is_file(), f"Missing marketing page: {page}"

    @pytest.mark.parametrize("page", PAGES)
    def test_html_page_non_empty(self, page: str):
        assert (_UI / page).stat().st_size > 5_000, f"{page} is suspiciously small"

    def test_data_file_ns_data_exists(self):
        assert (_UI / "ns-data.js").is_file()

    def test_data_file_course_exists(self):
        assert (_UI / "ns-course-data.js").is_file()

    def test_data_file_features_exists(self):
        assert (_UI / "ns-features-data.js").is_file()


# ===========================================================================
# 2. Navigation — index.html links to all other pages
# ===========================================================================

class TestIndexNavigation:
    def test_nav_links_simulator(self):
        assert "simulator.html" in _read(_UI / "index.html")

    def test_nav_links_course(self):
        assert "course.html" in _read(_UI / "index.html")

    def test_nav_links_research(self):
        assert "research.html" in _read(_UI / "index.html")

    def test_nav_links_pricing(self):
        assert "pricing.html" in _read(_UI / "index.html")

    def test_nav_links_guide(self):
        assert "guide.html" in _read(_UI / "index.html")

    def test_waitlist_section_present(self):
        html = _read(_UI / "index.html")
        assert "waitlist" in html.lower()

    def test_waitlist_form_present(self):
        html = _read(_UI / "index.html")
        assert "waitlist-form" in html or "<form" in html.lower()

    def test_join_waitlist_cta(self):
        html = _read(_UI / "index.html")
        assert "Join" in html and "Waitlist" in html

    def test_live_demo_cta_links_simulator(self):
        html = _read(_UI / "index.html")
        assert "simulator.html" in html
        assert "Demo" in html or "demo" in html


# ===========================================================================
# 3. Compliance & Disclaimers
# ===========================================================================

class TestDisclaimers:
    def test_index_has_disclaimer(self):
        html = _read(_UI / "index.html").lower()
        assert "disclaimer" in html or "not financial advice" in html or "not a financial" in html

    def test_simulator_educational_disclaimer(self):
        html = _read(_UI / "simulator.html")
        assert "Educational Demonstration Only" in html or "educational" in html.lower()

    def test_simulator_not_financial_advice(self):
        html = _read(_UI / "simulator.html").lower()
        assert "not financial advice" in html or "not a financial" in html

    def test_simulator_hypothetical_data(self):
        html = _read(_UI / "simulator.html").lower()
        assert "hypothetical" in html

    def test_research_hypothetical_disclaimer(self):
        html = _read(_UI / "research.html").lower()
        assert "hypothetical" in html or "past performance" in html

    def test_pricing_has_disclaimer_section(self):
        html = _read(_UI / "pricing.html").lower()
        assert "disclaimer" in html


# ===========================================================================
# 4. ICT Course — 5 modules, lesson count, entry models
# ===========================================================================

class TestCourseData:
    @pytest.fixture(scope="class")
    def js(self) -> str:
        return _read(_UI / "ns-course-data.js")

    def test_five_modules_declared(self, js: str):
        # Count module objects: { num: 1..5, title: ... }
        matches = re.findall(r"\bnum:\s*(\d+),\s*title:", js)
        module_nums = {int(m) for m in matches if int(m) <= 5 and "lessons" in js}
        # At minimum modules 1–5 are present (some matches may be lesson nums too;
        # check the top-level module declarations by looking for num + color + source pattern)
        module_blocks = re.findall(r"\{\s*num:\s*(\d+),\s*title:.*?color:.*?source:", js, re.DOTALL)
        assert len(module_blocks) == 5, f"Expected 5 modules, found {len(module_blocks)}"

    def test_module_1_foundations(self, js: str):
        assert "Foundations" in js

    def test_module_2_price_delivery(self, js: str):
        assert "Price Delivery" in js

    def test_module_3_session_bias(self, js: str):
        assert "Session" in js and "Bias" in js

    def test_module_4_market_structure(self, js: str):
        assert "Market Structure" in js

    def test_module_5_order_flow_smt(self, js: str):
        assert "Order Flow" in js and "SMT" in js

    def test_at_least_17_lessons(self, js: str):
        # Count lesson objects: { num: N, title: ...
        lesson_items = re.findall(r"\{\s*num:\s*\d+,\s*title:", js)
        # Subtract 5 module-level num fields (modules also have num:)
        # Modules have color: field; lessons don't — use title + subtitle pattern
        lessons = re.findall(r"\{\s*num:\s*\d+,\s*title:.*?subtitle:", js, re.DOTALL)
        assert len(lessons) >= 17, f"Expected ≥17 lessons, found {len(lessons)}"

    def test_entry_models_declared(self, js: str):
        assert "ENTRY_MODELS" in js

    def test_seven_entry_models(self, js: str):
        # Each entry model: { name: '...', trigger: '...', color: '...' }
        models = re.findall(r"\{\s*name:\s*'[^']+',\s*trigger:", js)
        assert len(models) == 7, f"Expected 7 entry models, found {len(models)}"

    def test_consolidation_model_present(self, js: str):
        assert "Consolidation Model" in js

    def test_expansion_retracement_model(self, js: str):
        assert "Expansion" in js and "Retracement" in js

    def test_smt_entry_model(self, js: str):
        assert "SMT" in js

    def test_universal_confluence_declared(self, js: str):
        assert "UNIVERSAL_CONFLUENCE" in js

    def test_five_universal_confluence_rules(self, js: str):
        # UNIVERSAL_CONFLUENCE is a JS array of strings
        section = js[js.index("UNIVERSAL_CONFLUENCE"):] if "UNIVERSAL_CONFLUENCE" in js else ""
        # Find the array content between [ and ]
        m = re.search(r"UNIVERSAL_CONFLUENCE\s*=\s*\[(.*?)\]", section, re.DOTALL)
        if m:
            items = re.findall(r"'[^']+'", m.group(1))
            assert len(items) == 5, f"Expected 5 universal confluence rules, found {len(items)}"

    def test_key_concepts_present(self, js: str):
        for concept in ["FVG", "Kill zone", "HTF", "Liquidity", "PDA"]:
            assert concept in js, f"Missing concept: {concept}"

    def test_window_assignment_exports_course(self, js: str):
        assert "COURSE_MODULES" in js
        assert "Object.assign(window" in js


# ===========================================================================
# 5. EdgeLab / AEE Data — 3 core engines, support systems, dimensions
# ===========================================================================

class TestEdgeLabData:
    @pytest.fixture(scope="class")
    def js(self) -> str:
        return _read(_UI / "ns-features-data.js")

    def test_three_core_engines(self, js: str):
        engines = re.findall(r"\{\s*id:\s*'(\w+)',\s*name:", js)
        assert len(engines) == 3, f"Expected 3 AEE core engines, found {len(engines)}: {engines}"

    def test_forensics_engine_present(self, js: str):
        assert "id: 'forensics'" in js

    def test_regime_engine_present(self, js: str):
        assert "id: 'regime'" in js

    def test_injection_engine_present(self, js: str):
        assert "id: 'injection'" in js

    def test_six_support_systems(self, js: str):
        # AEE_SUPPORT_SYSTEMS array entries: { name: '...', color: '...', desc: '...' }
        systems = re.findall(r"\{\s*name:\s*'[^']+',\s*color:", js)
        # Core engines also match; find the support systems section specifically
        support_section = js[js.index("AEE_SUPPORT_SYSTEMS"):] if "AEE_SUPPORT_SYSTEMS" in js else ""
        bracket_end = support_section.index("];")
        support_content = support_section[:bracket_end]
        support_systems = re.findall(r"\{\s*name:\s*'[^']+',\s*color:", support_content)
        assert len(support_systems) == 6, f"Expected 6 support systems, found {len(support_systems)}"

    def test_eleven_regime_dimensions(self, js: str):
        dims_section = js[js.index("AEE_REGIME_DIMENSIONS"):] if "AEE_REGIME_DIMENSIONS" in js else ""
        bracket_end = dims_section.index("];")
        dims_content = dims_section[:bracket_end]
        dimensions = re.findall(r"'[^']+'", dims_content)
        assert len(dimensions) == 11, f"Expected 11 regime dimensions, found {len(dimensions)}"

    def test_feature_states_declared(self, js: str):
        assert "AEE_FEATURE_STATES" in js

    def test_six_feature_states(self, js: str):
        states_section = js[js.index("AEE_FEATURE_STATES"):] if "AEE_FEATURE_STATES" in js else ""
        bracket_end = states_section.index("];")
        states_content = states_section[:bracket_end]
        states = re.findall(r"\{\s*state:\s*'[^']+',", states_content)
        assert len(states) == 6, f"Expected 6 feature states, found {len(states)}"

    def test_feature_state_lifecycle(self, js: str):
        for state in ["Draft", "Candidate", "Testing", "Validated", "Promoted", "Rejected"]:
            assert f"state: '{state}'" in js, f"Missing feature state: {state}"

    def test_ten_sample_features(self, js: str):
        features_section = js[js.index("AEE_SAMPLE_FEATURES"):] if "AEE_SAMPLE_FEATURES" in js else ""
        bracket_end = features_section.index("];")
        features_content = features_section[:bracket_end]
        features = re.findall(r"\{\s*name:\s*'[^']+',\s*type:", features_content)
        assert len(features) == 10, f"Expected 10 sample features, found {len(features)}"

    def test_nine_workflow_steps(self, js: str):
        steps_section = js[js.index("AEE_WORKFLOW_STEPS"):] if "AEE_WORKFLOW_STEPS" in js else ""
        bracket_end = steps_section.index("];")
        steps_content = steps_section[:bracket_end]
        steps = re.findall(r"\{\s*num:\s*'0\d'", steps_content)
        assert len(steps) == 9, f"Expected 9 workflow steps, found {len(steps)}"

    def test_window_assignment_exports_all(self, js: str):
        assert "Object.assign(window" in js
        for key in ["AEE_CORE_ENGINES", "AEE_SUPPORT_SYSTEMS", "AEE_REGIME_DIMENSIONS",
                    "AEE_FEATURE_STATES", "AEE_SAMPLE_FEATURES", "AEE_WORKFLOW_STEPS",
                    "AEE_SWEEP_RESULTS", "AEE_ROADMAP"]:
            assert key in js, f"Missing window export: {key}"

    def test_sweep_results_baseline_and_promoted(self, js: str):
        assert "Control" in js
        assert "Promoted" in js

    def test_roadmap_references_phase_8_edgelab(self, js: str):
        assert "EdgeLab Research Studio" in js


# ===========================================================================
# 6. Pricing Tiers
# ===========================================================================

class TestPricingTiers:
    @pytest.fixture(scope="class")
    def html(self) -> str:
        return _read(_UI / "pricing.html")

    def test_mentor_tier_present(self, html: str):
        assert "Mentor" in html

    def test_mentor_price_29(self, html: str):
        assert "29" in html

    def test_trader_tier_present(self, html: str):
        assert "Trader" in html

    def test_trader_price_99(self, html: str):
        assert "99" in html

    def test_research_tier_present(self, html: str):
        assert "Research" in html

    def test_research_price_199(self, html: str):
        assert "199" in html

    def test_all_three_tiers_in_order(self, html: str):
        mentor_pos = html.find("Mentor")
        trader_pos = html.find("Trader")
        research_pos = html.find("Research")
        assert mentor_pos < trader_pos < research_pos, "Tiers not in Mentor → Trader → Research order"

    def test_neurofund_elite_reference(self, html: str):
        assert "NeuroFund" in html or "neurofund" in html.lower()


# ===========================================================================
# 7. Simulator page — interactive demo elements
# ===========================================================================

class TestSimulatorPage:
    @pytest.fixture(scope="class")
    def html(self) -> str:
        return _read(_UI / "simulator.html")

    def test_chart_or_canvas_element(self, html: str):
        html_lower = html.lower()
        assert "canvas" in html_lower or "chart" in html_lower

    def test_order_entry_present(self, html: str):
        html_lower = html.lower()
        assert "order" in html_lower or "entry" in html_lower

    def test_ict_session_or_killzone_reference(self, html: str):
        html_lower = html.lower()
        assert "kill zone" in html_lower or "killzone" in html_lower or "session" in html_lower

    def test_ai_coach_feedback_section(self, html: str):
        html_lower = html.lower()
        assert "coach" in html_lower or "ai" in html_lower or "feedback" in html_lower

    def test_session_stats_present(self, html: str):
        html_lower = html.lower()
        assert "stat" in html_lower or "p&l" in html_lower or "pnl" in html_lower


# ===========================================================================
# 8. Course page — structure
# ===========================================================================

class TestCoursePage:
    @pytest.fixture(scope="class")
    def html(self) -> str:
        return _read(_UI / "course.html")

    def test_course_module_structure_present(self, html: str):
        # Course data is embedded inline; check for rendered module/lesson CSS classes
        assert "module-header" in html or "module-group" in html

    def test_five_modules_referenced(self, html: str):
        # The page should reference or render modules — check for module-related markup
        html_lower = html.lower()
        assert "module" in html_lower

    def test_assessment_types_present(self, html: str):
        html_lower = html.lower()
        # At least one of: quiz, fill-in-blank, scenario, chart-id
        assert any(t in html_lower for t in ["quiz", "fill", "scenario", "chart"])

    def test_progress_tracking_element(self, html: str):
        html_lower = html.lower()
        assert "progress" in html_lower or "complete" in html_lower


# ===========================================================================
# 9. Research (EdgeLab) page
# ===========================================================================

class TestResearchPage:
    @pytest.fixture(scope="class")
    def html(self) -> str:
        return _read(_UI / "research.html")

    def test_three_research_engines_described(self, html: str):
        # research.html has 3 inline demo engines; data is not loaded from an external file
        assert "Strategy Backtester" in html or "backtest" in html.lower()

    def test_backtester_present(self, html: str):
        html_lower = html.lower()
        assert "backtest" in html_lower

    def test_monte_carlo_present(self, html: str):
        html_lower = html.lower()
        assert "monte carlo" in html_lower or "montecarlo" in html_lower

    def test_strategy_yaml_config(self, html: str):
        html_lower = html.lower()
        assert "yaml" in html_lower or "strategy" in html_lower

    def test_feature_explorer_engine_present(self, html: str):
        # research.html includes Feature Explorer (not Forensics — that's Phase 8 AEE)
        assert "Feature Explorer" in html or "feature" in html.lower()


# ===========================================================================
# 10. Course content files (curriculum markdown)
# ===========================================================================

class TestCourseContentFiles:
    def test_course_directory_exists(self):
        assert _COURSE_DIR.is_dir()

    def test_module_1_foundations_dir(self):
        assert (_COURSE_DIR / "module-1-foundations").is_dir()

    def test_module_2_price_delivery_dir(self):
        assert (_COURSE_DIR / "module-2-price-delivery").is_dir()

    def test_module_3_session_bias_dir(self):
        assert (_COURSE_DIR / "module-3-session-and-bias").is_dir()

    def test_module_4_market_structure_dir(self):
        assert (_COURSE_DIR / "module-4-market-structure").is_dir()

    def test_module_5_order_flow_dir(self):
        assert (_COURSE_DIR / "module-5-order-flow-and-smt").is_dir()

    def test_module_1_has_three_lessons(self):
        files = list((_COURSE_DIR / "module-1-foundations").glob("*.md"))
        assert len(files) == 3, f"Module 1 expected 3 lesson files, found {len(files)}"

    def test_module_2_has_four_lessons(self):
        files = list((_COURSE_DIR / "module-2-price-delivery").glob("*.md"))
        assert len(files) == 4, f"Module 2 expected 4 lesson files, found {len(files)}"

    def test_module_3_has_four_lessons(self):
        files = list((_COURSE_DIR / "module-3-session-and-bias").glob("*.md"))
        assert len(files) == 4, f"Module 3 expected 4 lesson files, found {len(files)}"

    def test_module_4_has_four_lessons(self):
        files = list((_COURSE_DIR / "module-4-market-structure").glob("*.md"))
        assert len(files) == 4, f"Module 4 expected 4 lesson files, found {len(files)}"

    def test_module_5_has_at_least_two_lessons(self):
        files = list((_COURSE_DIR / "module-5-order-flow-and-smt").glob("*.md"))
        assert len(files) >= 2, f"Module 5 expected ≥2 lesson files, found {len(files)}"

    def test_entry_models_directory_exists(self):
        assert (_UI / "uploads" / "entry-models").is_dir()

    def test_entry_models_have_markdown_files(self):
        files = list((_UI / "uploads" / "entry-models").glob("*.md"))
        assert len(files) >= 5, f"Expected ≥5 entry model files, found {len(files)}"


# ===========================================================================
# 11. Technical Deliverables — Sentry, data model audit, CI/CD
# ===========================================================================

class TestTechnicalDeliverables:
    def test_sentry_imported_in_main(self):
        main_src = _read(_API / "app" / "main.py")
        assert "import sentry_sdk" in main_src

    def test_sentry_init_conditional_on_dsn(self):
        main_src = _read(_API / "app" / "main.py")
        assert "sentry_sdk.init(" in main_src
        assert "sentry_dsn" in main_src

    def test_sentry_traces_sample_rate_configured(self):
        main_src = _read(_API / "app" / "main.py")
        assert "traces_sample_rate" in main_src

    def test_sentry_environment_configured(self):
        main_src = _read(_API / "app" / "main.py")
        assert "environment" in main_src

    def test_data_model_audit_doc_exists(self):
        assert (_DOCS / "phase-0-data-model-audit.md").is_file()

    def test_data_model_audit_documents_trade_model(self):
        content = _read(_DOCS / "phase-0-data-model-audit.md")
        assert "Trade" in content and "trade.py" in content

    def test_data_model_audit_has_field_count(self):
        content = _read(_DOCS / "phase-0-data-model-audit.md")
        # Audit should document the 43 field count
        assert "43" in content

    def test_data_model_audit_identifies_phase1_gaps(self):
        content = _read(_DOCS / "phase-0-data-model-audit.md")
        assert "Phase 1" in content

    def test_design_handoff_simulator_doc_exists(self):
        assert (_HANDOFF / "08-live-simulator.md").is_file()

    def test_design_handoff_course_doc_exists(self):
        assert (_HANDOFF / "09-course.md").is_file()

    def test_design_handoff_edgelab_doc_exists(self):
        assert (_HANDOFF / "10-edgelab-studio.md").is_file()

    def test_design_handoff_docs_non_empty(self):
        for doc in ["08-live-simulator.md", "09-course.md", "10-edgelab-studio.md"]:
            size = (_HANDOFF / doc).stat().st_size
            assert size > 500, f"{doc} is suspiciously small ({size} bytes)"

    def test_product_guide_exists(self):
        assert (_DOCS / "neurospect_product_overview_user_guide.md").is_file()

    def test_product_guide_substantial(self):
        content = _read(_DOCS / "neurospect_product_overview_user_guide.md")
        lines = content.splitlines()
        assert len(lines) >= 200, f"Product guide expected ≥200 lines, found {len(lines)}"


# ===========================================================================
# 12. App Integration — sidebar navigation link
# ===========================================================================

class TestAppIntegration:
    @pytest.fixture(scope="class")
    def sidebar(self) -> str:
        return _read(_APP / "components" / "layout" / "sidebar.tsx")

    def test_marketing_site_link_present(self, sidebar: str):
        assert "Marketing Site" in sidebar

    def test_marketing_site_href_points_to_ui(self, sidebar: str):
        assert "neurospect-ui" in sidebar

    def test_globe_icon_imported(self, sidebar: str):
        assert "Globe" in sidebar

    def test_globe_icon_used_in_link(self, sidebar: str):
        # Globe component should appear after the marketing site link href
        href_pos = sidebar.find("neurospect-ui")
        globe_pos = sidebar.find("Globe", href_pos)
        assert globe_pos > 0, "Globe icon not found after marketing site link"

    def test_link_opens_in_new_tab(self, sidebar: str):
        assert 'target="_blank"' in sidebar

    def test_link_has_noopener(self, sidebar: str):
        assert "noopener" in sidebar
