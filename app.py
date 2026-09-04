import json
import os
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="VIT Placement Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def render(*html_parts):
    """Render raw HTML via st.markdown.

    A blank line inside a raw HTML block ends the block for Streamlit's
    markdown parser, so an empty interpolated value (e.g. "") can silently
    turn the rest of the block into escaped text. Flattening to one line
    avoids that regardless of what's interpolated.
    """
    html = "".join(p for p in html_parts if p)
    html = " ".join(line.strip() for line in html.splitlines() if line.strip())
    st.markdown(html, unsafe_allow_html=True)


st.markdown("""
<style>
    :root, html, body {
        color-scheme: light !important;
        background-color: #f5f5f7 !important;
        color: #1d1d1f !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    * {
        color-scheme: light !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, "Helvetica Neue", sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"] {
        display: none !important;
        height: 0 !important;
    }

    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 880px !important;
    }

    .apple-hero { text-align: center; padding: 0 0 36px 0; }
    .apple-eyebrow {
        font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.1em; color: #86868b; margin-bottom: 8px;
    }
    .apple-title {
        font-size: 2.6rem; font-weight: 700; letter-spacing: -0.03em;
        color: #1d1d1f; margin: 0 0 10px 0; line-height: 1.1;
        text-wrap: balance;
    }
    .apple-subtitle {
        font-size: 1.02rem; font-weight: 400; color: #86868b;
        max-width: 480px; margin: 0 auto; line-height: 1.5;
        text-wrap: pretty;
    }

    .company-name { font-size: 1.9rem; font-weight: 700; letter-spacing: -0.025em; color: #1d1d1f; }
    .apple-badge {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 12px; border-radius: 9999px; font-size: 0.74rem; font-weight: 600;
        background: #f5f5f7; color: #48484a;
    }
    .badge-dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }
    .badge-cdc .badge-dot { background-color: #34c759; }
    .badge-offcampus .badge-dot { background-color: #ff9500; }
    .badge-ghosted .badge-dot { background-color: #ff3b30; }

    .card {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid rgba(0, 0, 0, 0.04);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 8px 24px -12px rgba(0, 0, 0, 0.08);
        padding: 26px 28px;
        margin: 0 0 16px 0;
    }

    .stat-row { display: flex; }
    .stat { flex: 1; text-align: center; border-right: 1px solid #e5e5ea; }
    .stat:last-child { border-right: none; }
    .stat-val { font-size: 2.1rem; font-weight: 700; letter-spacing: -0.03em; color: #1d1d1f; font-variant-numeric: tabular-nums; }
    .stat-val.accent { color: #0071e3; }
    .stat-label { font-size: 0.78rem; color: #86868b; margin-top: 6px; }
    .stat-trend { font-size: 0.78rem; font-weight: 600; margin-top: 4px; min-height: 1.1em; }
    .stat-trend.up { color: #248a3d; }
    .stat-trend.down { color: #d70015; }

    .section-title { font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #86868b; margin-bottom: 16px; }
    .subsection-title { font-size: 0.82rem; font-weight: 600; color: #1d1d1f; margin: 18px 0 8px 0; }
    .subsection-title:first-of-type { margin-top: 0; }

    .fact-row { display: flex; justify-content: space-between; align-items: baseline; padding: 11px 0; border-bottom: 1px solid #f0f0f2; font-size: 0.92rem; }
    .fact-row:last-child { border-bottom: none; padding-bottom: 0; }
    .fact-row:first-child { padding-top: 0; }
    .fact-label { color: #86868b; }
    .fact-val { color: #1d1d1f; font-weight: 600; text-align: right; }

    .campus-bar-wrap { display: flex; height: 10px; border-radius: 9999px; overflow: hidden; background: #e5e5ea; margin: 4px 0 14px 0; }
    .seg-vellore { background-color: #0071e3; }
    .seg-chennai { background-color: #64b5f6; }
    .seg-bhopal { background-color: #b0b0b5; }
    .seg-amaravati { background-color: #d2d2d7; }
    .campus-legend { display: flex; flex-wrap: wrap; gap: 20px 28px; margin-bottom: 20px; }
    .campus-legend:last-child { margin-bottom: 0; }
    .campus-item { display: flex; align-items: center; gap: 9px; }
    .campus-swatch { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
    .campus-name { font-size: 0.85rem; color: #1d1d1f; }
    .campus-count { font-size: 0.85rem; color: #86868b; margin-left: 4px; }
    .campus-empty-note { font-size: 0.82rem; color: #86868b; margin: -8px 0 20px 0; }

    div[data-baseweb="select"] > div { background-color: #ffffff !important; border-radius: 12px !important; border: 1px solid #d2d2d7 !important; box-shadow: none !important; }
    div[data-baseweb="select"] input, div[data-baseweb="select"] * { background-color: transparent !important; color: #1d1d1f !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"], li[role="option"] { background-color: #ffffff !important; color: #1d1d1f !important; }
    li[role="option"] { transition: background-color 120ms ease, color 120ms ease; }
    li[role="option"]:hover, li[role="option"][aria-selected="true"] { background-color: #f5f5f7 !important; color: #0071e3 !important; }

    /* Streamlit 1.44's st.pills renders [role="radiogroup"] > button, not
       the [data-testid="stPills"] wrapper you'd guess. Unselected buttons
       are data-testid="stBaseButton-pills"; the active one switches to
       "stBaseButton-pillsActive" — there's no [aria-selected] here. */
    button[data-testid^="stBaseButton-pills"] {
        border-radius: 9999px !important; font-weight: 500 !important; font-size: 0.82rem !important;
        border: 1px solid #d2d2d7 !important; background-color: transparent !important; color: #1d1d1f !important;
        padding: 9px 16px !important; box-shadow: none !important;
        /* Streamlit sets height/min-height: 32px directly on this button,
           which padding can't grow past under border-box sizing. */
        height: auto !important; min-height: 40px !important;
        transition-property: background-color, color, border-color, transform;
        transition-duration: 150ms;
        transition-timing-function: ease;
    }
    button[data-testid^="stBaseButton-pills"]:active { transform: scale(0.96); }
    button[data-testid="stBaseButton-pillsActive"] {
        background-color: #1d1d1f !important; color: #ffffff !important; border-color: #1d1d1f !important;
    }
    button[data-testid="stBaseButton-pillsActive"] * { color: #ffffff !important; }

    div[data-testid="stDownloadButton"] button {
        border-radius: 9999px !important; font-weight: 500 !important; font-size: 0.86rem !important;
        border: 1px solid #d2d2d7 !important; background-color: #ffffff !important; color: #1d1d1f !important;
        padding: 11px 20px !important; width: 100%; box-shadow: none !important;
        transition-property: color, border-color, transform;
        transition-duration: 150ms;
        transition-timing-function: ease;
    }
    div[data-testid="stDownloadButton"] button:hover { border-color: #0071e3 !important; color: #0071e3 !important; }
    div[data-testid="stDownloadButton"] button:active { transform: scale(0.96); }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 20px !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 8px 24px -12px rgba(0, 0, 0, 0.08) !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"] summary { padding: 18px 24px !important; }
    div[data-testid="stExpander"] summary span { color: #1d1d1f !important; font-weight: 600 !important; font-size: 0.85rem !important; }
    div[data-testid="stExpanderDetails"] { padding: 4px 24px 24px 24px !important; }

    [data-testid="stDataFrame"] { border: 1px solid #e5e5ea !important; border-radius: 12px !important; }

    /* The hiring timeline uses st.container(border=True, key="timeline_card")
       so it can be restyled to match .card (its native border is a thin
       gray 8px-radius box with no shadow). The key lands as a class on the
       inner stVerticalBlock, but the actual border/background render one
       level up on its parent stVerticalBlockBorderWrapper — so that parent
       is targeted via :has() (safe here since the class is unique, unlike
       matching on "contains a dataframe", which also caught the whole-page
       wrapper). The inner block is reset to transparent to avoid a double
       outline. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-timeline_card) {
        background: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid rgba(0, 0, 0, 0.04) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 8px 24px -12px rgba(0, 0, 0, 0.08) !important;
        padding: 26px 28px !important;
        margin: 0 0 16px 0 !important;
    }
    .st-key-timeline_card {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_companies():
    with open("companies_unified_db.json", "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def build_directory(companies_db):
    """Flatten the full company DB into the table shown in the directory
    expander. Cached separately from load_companies so this ~750-row scan
    only runs once per session instead of on every rerun."""
    rows = []
    for name, data in companies_db.items():
        b26, b25 = data.get("batch_2026", {}), data.get("batch_2025", {})
        dist_26 = data.get("campus_breakdown", {}).get("batch_2026", {}).get("distribution", {})
        ctc_str = str(b26.get("avg_ctc")).strip() if b26.get("avg_ctc") is not None else "—"
        rows.append({
            "Company": str(name),
            "2026 Placed": int(b26.get("total_selections", 0) or 0),
            "2025 Placed": int(b25.get("total_selections", 0) or 0),
            "2026 Avg CTC": ctc_str,
            "Vellore": int(dist_26.get("Vellore", 0) or 0),
            "Chennai": int(dist_26.get("Chennai", 0) or 0),
            "Bhopal": int(dist_26.get("Bhopal", 0) or 0),
            "Amaravati": int(dist_26.get("Amaravati", 0) or 0),
            "Status": str(data.get("eligibility", {}).get("status_tag", "Regular")),
        })
    return pd.DataFrame(rows)


CAMPUSES = [("Vellore", "seg-vellore"), ("Chennai", "seg-chennai"), ("Bhopal", "seg-bhopal"), ("Amaravati", "seg-amaravati")]


def campus_breakdown_html(distribution):
    """One bar + legend for a single year's campus split, or an explanatory
    note when this recruiter has no per-campus data tracked."""
    counts = {name: distribution.get(name, 0) for name, _ in CAMPUSES}
    total = sum(counts.values())

    if total == 0:
        return '<div class="campus-empty-note">No campus-wise data tracked for this recruiter.</div>'

    segments = "".join(
        f'<div class="{cls}" style="width:{counts[name] / total * 100}%;"></div>'
        for name, cls in CAMPUSES
    )
    legend = "".join(
        f'<div class="campus-item"><span class="campus-swatch {cls}"></span>'
        f'<span class="campus-name">{name}</span><span class="campus-count">{counts[name]}</span></div>'
        for name, cls in CAMPUSES
    )
    return f'<div class="campus-bar-wrap">{segments}</div><div class="campus-legend">{legend}</div>'


companies_db = load_companies()
all_company_names = sorted(companies_db.keys())

render("""
<div class="apple-hero">
    <div class="apple-eyebrow">VIT Placement Intelligence</div>
    <div class="apple-title">Company Placement Tracker</div>
    <div class="apple-subtitle">Selection numbers, campus distribution, compensation, and eligibility across 740+ recruiters.</div>
</div>
""")

popular_chips = ["LTIMindtree", "AMD", "TCS", "Deloitte India", "10xConstruction", "Qualcomm PPO", "Adobe PPO"]

if "curr_company" not in st.session_state:
    st.session_state.curr_company = "AMD"

chip_selection = st.pills("Popular Recruiters", popular_chips, default=None, key="popular_pills")
if chip_selection and chip_selection != st.session_state.curr_company:
    st.session_state.curr_company = chip_selection
    st.rerun()

curr_idx = all_company_names.index(st.session_state.curr_company) if st.session_state.curr_company in all_company_names else 0
selected_company = st.selectbox("Search or select a company", all_company_names, index=curr_idx, label_visibility="collapsed")
if selected_company != st.session_state.curr_company:
    st.session_state.curr_company = selected_company
    st.rerun()

comp = companies_db.get(selected_company, {})
b26 = comp.get("batch_2026", {})
b25 = comp.get("batch_2025", {})
elig = comp.get("eligibility", {})
campus = comp.get("campus_breakdown", {})
dist_26 = campus.get("batch_2026", {}).get("distribution", {})
dist_25 = campus.get("batch_2025", {}).get("distribution", {})

status_tag = elig.get("status_tag", "CDC Regular Hiring")
if "Ghosted" in status_tag:
    badge_html = '<span class="apple-badge badge-ghosted"><span class="badge-dot"></span>Ghosted</span>'
elif "Off-Campus" in status_tag:
    badge_html = '<span class="apple-badge badge-offcampus"><span class="badge-dot"></span>Off-Campus</span>'
else:
    badge_html = '<span class="apple-badge badge-cdc"><span class="badge-dot"></span>CDC Recruiter</span>'

render(f"""
<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin:36px 0 20px 0;">
    <div class="company-name">{selected_company}</div>
    <div>{badge_html}</div>
</div>
""")

s26 = b26.get("total_selections", 0) or 0
s25 = b25.get("total_selections", 0) or 0
ctc_26 = b26.get("avg_ctc") or "—"

trend_html = '<div class="stat-trend"></div>'
if s25:
    diff = s26 - s25
    pct_change = diff / s25 * 100
    direction = "up" if diff >= 0 else "down"
    arrow = "↑" if diff >= 0 else "↓"
    sign = "+" if diff >= 0 else ""
    trend_html = f"<div class='stat-trend {direction}'>{arrow} {abs(pct_change):.0f}% YoY ({sign}{diff})</div>"

render(f"""
<div class="card stat-row">
    <div class="stat">
        <div class="stat-val accent">{s26:,}</div>
        <div class="stat-label">2026 Batch Offers</div>
        {trend_html}
    </div>
    <div class="stat">
        <div class="stat-val">{s25:,}</div>
        <div class="stat-label">2025 Batch Offers</div>
        <div class="stat-trend"></div>
    </div>
    <div class="stat">
        <div class="stat-val">{ctc_26}</div>
        <div class="stat-label">Average CTC (2026)</div>
        <div class="stat-trend"></div>
    </div>
</div>
""")

render(f"""
<div class="card">
    <div class="section-title">Campus-wise Selections</div>
    <div class="subsection-title">2026 Batch</div>
    {campus_breakdown_html(dist_26)}
    <div class="subsection-title">2025 Batch</div>
    {campus_breakdown_html(dist_25)}
</div>
""")

bce_26 = b26.get("bce_placed")
fact_rows = [
    ("Offer Types (2026)", ", ".join(b26.get("offer_types", [])) or "—"),
    ("Hiring Month(s), 2026", ", ".join(b26.get("months", [])) or "—"),
    ("Highest Package (2026)", b26.get("max_ctc") or ctc_26),
    ("2025 Average CTC", b25.get("avg_ctc") or "—"),
    ("CSE (BCE) Placements, 2026", f"{bce_26:,}" if bce_26 is not None else "—"),
]
facts_html = "".join(f'<div class="fact-row"><span class="fact-label">{k}</span><span class="fact-val">{v}</span></div>' for k, v in fact_rows)
render(f'<div class="card"><div class="section-title">Selection Details</div>{facts_html}</div>')

h9 = elig.get("hired_9_pointers", 0)
hn9 = elig.get("hired_non_9_pointers", 0)
elig_rows = [
    ("Academic Cutoff", elig.get("criteria_summary", "Standard Placement Criteria")),
    ("CGPA Policy", elig.get("nine_pointer_policy", "Open Criteria")),
    ("9-Pointers Selected", f"{h9} students"),
    ("Non-9-Pointers Selected", f"{hn9} students"),
    ("Eligible Disciplines", elig.get("eligible_branches", "CSE, IT, ECE and allied")),
]
elig_html = "".join(f'<div class="fact-row"><span class="fact-label">{k}</span><span class="fact-val">{v}</span></div>' for k, v in elig_rows)
render(f'<div class="card"><div class="section-title">Eligibility & Cutoffs</div>{elig_html}</div>')

# st.container, not a hand-written <div>: an open tag in one st.markdown
# call and closed in another wouldn't actually wrap the dataframe (see the
# CSS comment on .st-key-timeline_card above).
rounds_26 = b26.get("rounds", [])
if rounds_26:
    with st.container(border=True, key="timeline_card"):
        render('<div class="section-title">2026 Hiring Timeline</div>')
        timeline_df = pd.DataFrame(rounds_26).fillna("—")
        timeline_df.columns = [c.replace("_", " ").title() for c in timeline_df.columns]
        st.dataframe(timeline_df, use_container_width=True, hide_index=True)

st.write("")

with st.expander("Explore all recruiters"):
    directory_df = build_directory(companies_db)
    search_query = st.text_input("Filter by name", "", key="dir_search_filter", label_visibility="collapsed", placeholder="Filter by name")
    view_df = directory_df[directory_df["Company"].str.contains(search_query, case=False, na=False)] if search_query else directory_df.sort_values("2026 Placed", ascending=False)
    st.dataframe(view_df, use_container_width=True, hide_index=True)

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        if os.path.exists("placement_data.xlsx"):
            with open("placement_data.xlsx", "rb") as f:
                st.download_button("Download Excel (.xlsx)", f, file_name="VIT_Placement_Master.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="btn_dl_excel")
    with dl_col2:
        if os.path.exists("companies_unified_db.json"):
            with open("companies_unified_db.json", "rb") as f:
                st.download_button("Download JSON (.json)", f, file_name="VIT_Companies_Database.json", mime="application/json", key="btn_dl_json")

render('<div style="text-align:center; color:#86868b; font-size:0.78rem; margin-top:40px; padding-bottom:20px;">VIT Placement & Eligibility Intelligence</div>')
