#!/usr/bin/env python3
"""
Figma UI Extractor – Enterprise Glassmorphism Edition
Light, premium SaaS design • Advanced Streamlit caching • Fully responsive
"""

import streamlit as st
import requests
import json
import datetime
from typing import Any, Dict, List, Set, Tuple, Optional
import copy

# -----------------------------------------------------
# ADVANCED STYLING – GLASSMORPHISM SAAS UI
# -----------------------------------------------------
def apply_professional_styling():
    """Apply modern glassmorphism light theme with responsive layout"""
    st.markdown(
        """
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    html, body {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }

    :root {
        /* Brand / Primary */
        --primary-500: #6366F1;
        --primary-400: #818CF8;
        --primary-600: #4F46E5;
        --primary-300: #A5B4FC;

        /* Accent */
        --accent-emerald: #10B981;
        --accent-amber: #F59E0B;
        --accent-pink: #EC4899;

        /* Backgrounds */
        --bg-gradient: radial-gradient(circle at top left, #EEF2FF 0%, #F9FAFB 40%, #ECFEFF 80%);
        --bg-surface: rgba(255, 255, 255, 0.9);
        --bg-elevated: rgba(255, 255, 255, 0.88);
        --bg-elevated-strong: rgba(250, 250, 255, 0.96);

        /* Text */
        --text-strong: #020617;
        --text-main: #0F172A;
        --text-soft: #475569;
        --text-muted: #94A3B8;

        /* Borders & Shadows */
        --border-subtle: rgba(148, 163, 184, 0.35);
        --border-strong: rgba(148, 163, 184, 0.6);
        --shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.08);
        --shadow-strong: 0 25px 60px rgba(15, 23, 42, 0.14);

        /* Glassmorphism */
        --glass-border: 1px solid rgba(148, 163, 184, 0.35);
        --glass-blur: blur(18px);
    }

    .stApp {
        background: var(--bg-gradient);
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--text-main);
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
    }

    /* Main scroll area inside viewport */
    .main .block-container {
        max-width: 1320px;
        padding: 1.75rem 2rem 2rem 2rem;
        margin: 0 auto;
        height: calc(100vh - 3rem);
        overflow-y: auto;
        overflow-x: hidden;
    }

    .main .block-container::-webkit-scrollbar {
        width: 10px;
    }
    .main .block-container::-webkit-scrollbar-track {
        background: rgba(226, 232, 240, 0.8);
        border-radius: 999px;
    }
    .main .block-container::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary-400), var(--primary-600));
        border-radius: 999px;
        border: 2px solid #E5E7EB;
    }

    #MainMenu, footer, header {
        visibility: hidden;
        height: 0;
    }
    .stDeployButton { display: none; }

    /* Headings ---------------------------------------------------*/
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', 'Inter', system-ui;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-top: 0.4rem !important;
        margin-bottom: 0.4rem !important;
    }

    h1 {
        font-size: 2.6rem !important;
        line-height: 1.15;
        background: linear-gradient(120deg, #0F172A 0%, #6366F1 45%, #EC4899 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2 {
        font-size: 1.7rem !important;
        color: var(--text-main);
    }

    h3 {
        font-size: 1.25rem !important;
        color: var(--text-soft);
        font-weight: 600;
    }

    p, .stMarkdown {
        color: var(--text-soft);
        font-size: 0.98rem;
        line-height: 1.6;
        margin: 0.4rem 0;
    }

    /* Glass cards ------------------------------------------------*/
    .glass-card {
        background: var(--bg-elevated);
        backdrop-filter: var(--glass-blur);
        border-radius: 20px;
        border: var(--glass-border);
        box-shadow: var(--shadow-soft);
        padding: 1.5rem 1.5rem;
        transition: box-shadow 0.25s ease, transform 0.25s ease, border-color 0.25s ease;
    }
    .glass-card:hover {
        box-shadow: var(--shadow-strong);
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.55);
    }

    .element-container {
        margin: 0.6rem 0 !important;
    }

    /* Tabs -------------------------------------------------------*/
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 999px;
        padding: 0.35rem;
        border: 1px solid rgba(148, 163, 184, 0.45);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px !important;
        padding: 0.55rem 1.4rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text-soft);
        border: none;
        background: transparent;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(148, 163, 184, 0.12);
        color: var(--text-main);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, var(--primary-500), var(--primary-300)) !important;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.32);
    }

    /* Inputs -----------------------------------------------------*/
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 999px !important;
        border: 1px solid rgba(148, 163, 184, 0.7) !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
        color: var(--text-main) !important;
        box-shadow: 0 6px 15px rgba(148, 163, 184, 0.25);
        transition: all 0.2s ease !important;
    }

    .stTextArea textarea {
        border-radius: 14px !important;
    }

    .stTextInput > div > div > input:hover,
    .stTextArea textarea:hover {
        border-color: var(--primary-400) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary-500) !important;
        box-shadow: 0 0 0 1px rgba(129, 140, 248, 0.7), 0 10px 28px rgba(79, 70, 229, 0.22) !important;
    }

    label {
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: var(--text-main) !important;
    }

    /* Buttons ----------------------------------------------------*/
    .stButton > button {
        background: radial-gradient(circle at 20% 0, #A5B4FC 0, #6366F1 30%, #4F46E5 70%);
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: none !important;
        padding: 0.7rem 1.8rem !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        box-shadow: 0 14px 35px rgba(79, 70, 229, 0.45);
        transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
        cursor: pointer;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        filter: brightness(1.05);
        box-shadow: 0 18px 38px rgba(79, 70, 229, 0.55);
    }

    .stButton > button:active {
        transform: translateY(1px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.35);
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #10B981 0%, #22C55E 40%, #14B8A6 80%) !important;
        color: white !important;
        border-radius: 999px !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.93rem !important;
        box-shadow: 0 14px 30px rgba(16, 185, 129, 0.45);
    }

    .stDownloadButton > button:hover {
        filter: brightness(1.05);
        transform: translateY(-1px);
    }

    /* Metrics ----------------------------------------------------*/
    [data-testid="stMetric"] {
        background: var(--bg-elevated-strong);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.4);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
        padding: 0.9rem 1rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        background: linear-gradient(120deg, var(--primary-500), var(--accent-emerald));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted) !important;
    }

    /* Progress bar -----------------------------------------------*/
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-400), var(--accent-pink)) !important;
        border-radius: 999px;
    }
    .stProgress > div > div {
        background: rgba(226, 232, 240, 0.9) !important;
        border-radius: 999px;
        height: 9px !important;
        border: 1px solid rgba(148, 163, 184, 0.5);
    }

    /* Alerts -----------------------------------------------------*/
    .stAlert {
        border-radius: 16px !important;
        border-left: 4px solid var(--primary-500) !important;
        background: rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 16px 38px rgba(15, 23, 42, 0.12);
    }
    .stSuccess {
        border-left-color: var(--accent-emerald) !important;
    }
    .stError {
        border-left-color: #EF4444 !important;
    }
    .stInfo {
        border-left-color: #3B82F6 !important;
    }

    /* Sidebar ----------------------------------------------------*/
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(248, 250, 252, 0.95), rgba(239, 246, 255, 0.98));
        border-right: 1px solid rgba(148, 163, 184, 0.4);
        backdrop-filter: blur(24px);
        box-shadow: 10px 0 40px rgba(15, 23, 42, 0.12);
        height: 100vh;
        overflow-y: auto;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.3rem 1rem 1.5rem 1rem;
    }

    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.85);
        border-radius: 999px;
    }

    /* Expanders --------------------------------------------------*/
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(148, 163, 184, 0.5) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: var(--text-main) !important;
    }

    /* JSON / code ------------------------------------------------*/
    .stJson {
        max-height: 360px;
        overflow-y: auto;
        background: rgba(248, 250, 252, 0.9);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.55);
        padding: 0.75rem !important;
    }
    code, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.86rem !important;
    }

    /* Columns ----------------------------------------------------*/
    [data-testid="column"] {
        padding: 0 0.45rem;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.8), transparent);
        margin: 1.4rem 0;
    }

    /* Responsive -------------------------------------------------*/
    @media (max-width: 767px) {
        .main .block-container {
            padding: 1.2rem;
            height: calc(100vh - 2rem);
        }
        h1 { font-size: 1.9rem !important; }
        [data-testid="column"] { min-width: 100% !important; padding: 0 0.1rem; }
    }

    @media (min-width: 768px) and (max-width: 1199px) {
        .main .block-container {
            padding: 1.5rem 1.4rem;
            max-width: 100%;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Figma UI Extractor | Enterprise",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_professional_styling()

# -----------------------------------------------------
# CORE HELPERS
# -----------------------------------------------------
def build_headers(token: str) -> Dict[str, str]:
    return {"Accept": "application/json", "X-Figma-Token": token}


def chunked(lst: List[str], n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def to_rgba(color: Dict[str, Any]) -> str:
    try:
        r = int(float(color.get("r", 0)) * 255)
        g = int(float(color.get("g", 0)) * 255)
        b = int(float(color.get("b", 0)) * 255)
        a = float(color.get("a", color.get("opacity", 1)))
        return f"rgba({r},{g},{b},{a})"
    except Exception:
        return "rgba(0,0,0,1)"


def is_nonempty_list(v: Any) -> bool:
    return isinstance(v, list) and len(v) > 0


def is_visible(node: Dict[str, Any]) -> bool:
    v = node.get("visible")
    return True if v is None else bool(v)


def filter_invisible_nodes(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not is_visible(node):
        return None
    if "children" in node:
        filtered = []
        for c in node["children"]:
            if isinstance(c, dict):
                fc = filter_invisible_nodes(c)
                if fc:
                    filtered.append(fc)
        node["children"] = filtered
    return node

# -----------------------------------------------------
# ADVANCED CACHING LAYER
# -----------------------------------------------------
# Use data cache for pure data, resource cache for session-wide resources.[web:11][web:34]

@st.cache_data(show_spinner="📡 Fetching Figma document…", ttl=datetime.timedelta(hours=2), max_entries=64)
def fetch_figma_nodes(file_key: str, node_ids: str, token: str, timeout: int = 60) -> Dict[str, Any]:
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    params = {"ids": node_ids} if node_ids else {}
    resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    if not resp.ok:
        raise RuntimeError(f"Figma API error {resp.status_code}: {resp.text}")
    data = resp.json()

    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_invisible_nodes(doc)
    elif isinstance(data.get("document"), dict):
        data["document"] = filter_invisible_nodes(data["document"])
    return data


@st.cache_data(show_spinner="🧩 Walking node tree…", ttl=datetime.timedelta(hours=2), max_entries=128)
def walk_nodes_collect_images_and_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, str]]]:
    image_refs: Set[str] = set()
    node_ids: List[str] = []
    node_meta: Dict[str, Dict[str, str]] = {}

    def visit(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        nid = n.get("id")
        if nid:
            node_ids.append(nid)
            node_meta[nid] = {
                "id": nid,
                "name": n.get("name", ""),
                "type": n.get("type", ""),
            }
        for f in n.get("fills", []) or []:
            if isinstance(f, dict) and f.get("type") == "IMAGE":
                ref = f.get("imageRef") or f.get("imageHash")
                if ref:
                    image_refs.add(ref)
        for s in n.get("strokes", []) or []:
            if isinstance(s, dict) and s.get("type") == "IMAGE":
                ref = s.get("imageRef") or s.get("imageHash")
                if ref:
                    image_refs.add(ref)
        for c in n.get("children", []) or []:
            visit(c)

    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])

    seen = set()
    uniq_ids: List[str] = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            uniq_ids.append(nid)

    return image_refs, uniq_ids, node_meta


@st.cache_data(show_spinner="🖼 Resolving image URLs…", ttl=datetime.timedelta(hours=2), max_entries=64)
def resolve_image_urls(
    file_key: str, image_refs: Set[str], node_ids: List[str], token: str, timeout: int = 60
) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    headers = build_headers(token)

    fills_map: Dict[str, str] = {}
    try:
        fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
        params = {"ids": ",".join(list(image_refs))} if image_refs else {}
        r = requests.get(fills_url, headers=headers, params=params or None, timeout=timeout)
        if r.ok:
            fills_map = r.json().get("images", {}) or {}
    except Exception:
        fills_map = {}

    renders_map: Dict[str, Optional[str]] = {}
    if node_ids:
        base_render = f"https://api.figma.com/v1/images/{file_key}"
        for batch in chunked(node_ids, 200):
            try:
                params = {"ids": ",".join(batch), "format": "svg"}
                r = requests.get(base_render, headers=headers, params=params, timeout=timeout)
                if r.ok:
                    images_map = r.json().get("images", {}) or {}
                    for nid in batch:
                        renders_map[nid] = images_map.get(nid) or None
                else:
                    for nid in batch:
                        renders_map[nid] = None
            except Exception:
                for nid in batch:
                    renders_map[nid] = None
    return {k: v for k, v in fills_map.items() if k in image_refs}, renders_map

# -----------------------------------------------------
# EXTRACTION LOGIC
# -----------------------------------------------------
def build_icon_map(
    nodes_payload: Dict[str, Any],
    filtered_fills: Dict[str, str],
    renders_map: Dict[str, Optional[str]],
    node_meta: Dict[str, Dict[str, str]],
) -> Dict[str, str]:
    node_first_ref: Dict[str, str] = {}

    def map_first_image(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        nid = n.get("id")
        if nid:
            for f in n.get("fills", []) or []:
                if isinstance(f, dict) and f.get("type") == "IMAGE":
                    ref = f.get("imageRef") or f.get("imageHash")
                    if ref:
                        node_first_ref[nid] = ref
                        break
        for c in n.get("children", []) or []:
            map_first_image(c)

    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                map_first_image(doc)
    if isinstance(nodes_payload.get("document"), dict):
        map_first_image(nodes_payload["document"])

    node_to_url: Dict[str, str] = {}
    for nid in node_meta.keys():
        url = None
        ref = node_first_ref.get(nid)
        if ref:
            url = filtered_fills.get(ref) or None
        if not url:
            url = renders_map.get(nid) or None
        if url:
            node_to_url[nid] = url
    return node_to_url


def merge_urls_into_nodes(nodes_payload: Dict[str, Any], node_to_url: Dict[str, str]) -> Dict[str, Any]:
    merged = copy.deepcopy(nodes_payload)

    def inject(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        nid = n.get("id")
        if nid and nid in node_to_url:
            n["image_url"] = node_to_url[nid]
        for c in n.get("children", []) or []:
            inject(c)

    if isinstance(merged.get("nodes"), dict):
        for entry in merged["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                inject(doc)
    if isinstance(merged.get("document"), dict):
        inject(merged["document"])
    return merged


def extract_bounds(node: Dict[str, Any]) -> Optional[Dict[str, float]]:
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict) and all(k in box for k in ("x", "y", "width", "height")):
        try:
            return {
                "x": float(box["x"]),
                "y": float(box["y"]),
                "width": float(box["width"]),
                "height": float(box["height"]),
            }
        except Exception:
            return None
    return None


def extract_layout(node: Dict[str, Any]) -> Dict[str, Any]:
    keys = [
        "layoutMode",
        "constraints",
        "paddingLeft",
        "paddingRight",
        "paddingTop",
        "paddingBottom",
        "itemSpacing",
        "counterAxisAlignItems",
        "primaryAxisAlignItems",
        "layoutGrow",
        "layoutAlign",
        "layoutSizingHorizontal",
        "layoutSizingVertical",
        "counterAxisSizingMode",
        "primaryAxisSizingMode",
        "clipsContent",
        "layoutWrap",
        "layoutGrids",
    ]
    layout: Dict[str, Any] = {}
    for k in keys:
        if k in node:
            layout[k] = node[k]
    return layout


def extract_visuals(node: Dict[str, Any]) -> Dict[str, Any]:
    styling: Dict[str, Any] = {}
    fills = node.get("fills")
    if is_nonempty_list(fills):
        parsed: List[Dict[str, Any]] = []
        for f in fills:
            if not isinstance(f, dict):
                continue
            entry: Dict[str, Any] = {}
            t = f.get("type")
            if t == "SOLID" and "color" in f:
                entry["type"] = "solid"
                entry["color"] = to_rgba(f["color"])
                if "opacity" in f:
                    entry["opacity"] = f.get("opacity")
            else:
                if t:
                    entry["type"] = (t or "").lower()
                if "imageRef" in f:
                    entry["imageRef"] = f.get("imageRef")
                if "scaleMode" in f:
                    entry["scaleMode"] = f.get("scaleMode")
            if entry:
                parsed.append(entry)
        if parsed:
            styling["fills"] = parsed

    if "backgroundColor" in node and isinstance(node["backgroundColor"], dict):
        styling["backgroundColor"] = to_rgba(node["backgroundColor"])

    strokes = node.get("strokes")
    if is_nonempty_list(strokes):
        borders: List[Dict[str, Any]] = []
        for s in strokes:
            if not isinstance(s, dict):
                continue
            b: Dict[str, Any] = {}
            if s.get("type") == "SOLID" and "color" in s:
                b["color"] = to_rgba(s["color"])
            if "opacity" in s:
                b["opacity"] = s.get("opacity")
            if "strokeWeight" in node:
                b["width"] = node.get("strokeWeight")
            if "strokeAlign" in node:
                b["align"] = node.get("strokeAlign")
            if b:
                borders.append(b)
        if borders:
            styling["borders"] = borders

    if isinstance(node.get("cornerRadius"), (int, float)) and node.get("cornerRadius", 0) > 0:
        styling["cornerRadius"] = node.get("cornerRadius")

    effects = node.get("effects")
    if is_nonempty_list(effects):
        parsed: List[Dict[str, Any]] = []
        for e in effects:
            if not isinstance(e, dict):
                continue
            et = e.get("type")
            if not et:
                continue
            ee: Dict[str, Any] = {"type": et.lower()}
            off = e.get("offset") or {}
            if isinstance(off, dict):
                ee["x"] = off.get("x", 0)
                ee["y"] = off.get("y", 0)
            if "radius" in e:
                ee["blur"] = e.get("radius")
            if "color" in e and isinstance(e.get("color"), dict):
                ee["color"] = to_rgba(e["color"])
            parsed.append(ee)
        if parsed:
            styling["effects"] = parsed

    return styling


def extract_text(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if (node.get("type") or "").upper() != "TEXT":
        return None
    t: Dict[str, Any] = {"content": node.get("characters", "")}
    style = node.get("style") or {}
    if isinstance(style, dict):
        t["typography"] = {
            "fontFamily": style.get("fontFamily"),
            "fontSize": style.get("fontSize"),
            "fontWeight": style.get("fontWeight"),
            "lineHeight": style.get("lineHeightPx", style.get("lineHeight")),
            "letterSpacing": style.get("letterSpacing"),
            "textAlign": (style.get("textAlignHorizontal") or "left").lower(),
            "textCase": (style.get("textCase") or "none").lower(),
        }
    fills = node.get("fills")
    if is_nonempty_list(fills):
        for f in fills:
            if isinstance(f, dict) and f.get("type") == "SOLID" and "color" in f:
                t["color"] = to_rgba(f["color"])
                break
    return t


def should_include(node: Dict[str, Any]) -> bool:
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    has_visual = bool(
        node.get("fills") or node.get("strokes") or node.get("effects") or node.get("image_url")
    )
    semantic = any(
        k in name
        for k in [
            "button",
            "input",
            "search",
            "nav",
            "menu",
            "container",
            "card",
            "panel",
            "header",
            "footer",
            "badge",
            "chip",
        ]
    )
    vector_visible = t in ["VECTOR", "LINE", "ELLIPSE", "POLYGON", "STAR", "RECTANGLE"] and (
        node.get("strokes") or node.get("fills")
    )
    return any(
        [
            t == "TEXT",
            has_visual,
            vector_visible,
            isinstance(node.get("cornerRadius"), (int, float))
            and node.get("cornerRadius", 0) > 0,
            bool(node.get("layoutMode")),
            t in ["FRAME", "GROUP", "COMPONENT", "INSTANCE", "SECTION"],
            semantic,
        ]
    )


def classify_bucket(comp: Dict[str, Any]) -> str:
    t = (comp.get("type") or "").upper()
    name = (comp.get("name") or "").lower()
    if t == "TEXT":
        return "textElements"
    if "button" in name:
        return "buttons"
    if any(k in name for k in ["input", "search", "textfield", "field"]):
        return "inputs"
    if any(k in name for k in ["nav", "menu", "sidebar", "toolbar", "header", "footer", "breadcrumb"]):
        return "navigation"
    if comp.get("imageUrl") or comp.get("image_url"):
        return "images"
    if t in ["VECTOR", "LINE", "ELLIPSE", "POLYGON", "STAR", "RECTANGLE"]:
        return "vectors"
    if t in ["FRAME", "GROUP", "COMPONENT", "INSTANCE", "SECTION"] or any(
        k in name for k in ["container", "card", "panel", "section"]
    ):
        return "containers"
    return "other"


def extract_components(
    root: Dict[str, Any], parent_path: str = "", out: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    if out is None:
        out = []
    if root is None or not isinstance(root, dict):
        return out
    path = f"{parent_path}/{root.get('name','Unnamed')}" if parent_path else (root.get("name") or "Root")
    comp: Dict[str, Any] = {
        "id": root.get("id"),
        "name": root.get("name"),
        "type": root.get("type"),
        "path": path,
    }
    bounds = extract_bounds(root)
    if bounds:
        comp["position"] = bounds
    layout = extract_layout(root)
    if layout:
        comp["layout"] = layout
    styling = extract_visuals(root)
    if styling:
        comp["styling"] = styling
    if root.get("image_url"):
        comp["imageUrl"] = root.get("image_url")
    if root.get("imageUrl"):
        comp["imageUrl"] = root.get("imageUrl")
    text = extract_text(root)
    if text:
        comp["text"] = text
    if should_include(root):
        out.append(comp)
    for child in root.get("children", []) or []:
        if isinstance(child, dict):
            extract_components(child, path, out)
    return out


def find_document_roots(nodes_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    roots: List[Dict[str, Any]] = []
    if isinstance(nodes_payload.get("nodes"), dict):
        for v in nodes_payload["nodes"].values():
            if isinstance(v, dict) and isinstance(v.get("document"), dict):
                roots.append(v["document"])
        if roots:
            return roots
    if isinstance(nodes_payload.get("document"), dict):
        roots.append(nodes_payload["document"])
    return roots


@st.cache_data(show_spinner="📦 Building component catalog…", ttl=datetime.timedelta(hours=2), max_entries=64)
def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    roots = find_document_roots(merged_payload)
    if not roots:
        raise RuntimeError("No document roots found in payload")
    all_components: List[Dict[str, Any]] = []
    for r in roots:
        if isinstance(r, dict):
            extract_components(r, "", all_components)
    organized = {
        "metadata": {
            "totalComponents": len(all_components),
            "extractedAt": datetime.datetime.utcnow().isoformat() + "Z",
            "version": 1,
        },
        "textElements": [],
        "buttons": [],
        "inputs": [],
        "containers": [],
        "images": [],
        "navigation": [],
        "vectors": [],
        "other": [],
    }
    for c in all_components:
        organized.setdefault(classify_bucket(c), []).append(c)
    return organized


def remove_url_prefix_from_json(payload: Dict[str, Any], url_prefix: str) -> Dict[str, Any]:
    p = copy.deepcopy(payload)

    def process(obj: Any):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k in ("imageUrl", "image_url") and isinstance(v, str) and v.startswith(url_prefix):
                    obj[k] = v.replace(url_prefix, "", 1)
                else:
                    process(v)
        elif isinstance(obj, list):
            for item in obj:
                process(item)

    process(p)
    return p

# -----------------------------------------------------
# UI LAYOUT
# -----------------------------------------------------
def main():
    # Hero
    st.markdown(
        """
    <div class="glass-card" style="margin-bottom: 1.5rem; padding: 1.4rem 1.6rem;">
      <div style="display:flex; flex-direction:column; gap:0.6rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
          <div>
            <div style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.25rem 0.7rem; border-radius:999px; background:rgba(129,140,248,0.10); border:1px solid rgba(129,140,248,0.35); font-size:0.78rem; font-weight:600; color:#4F46E5; letter-spacing:0.08em; text-transform:uppercase;">
              <span>Enterprise Glassmorphism Edition</span>
            </div>
            <h1 style="margin-top:0.5rem; margin-bottom:0.25rem;">🎨 Figma UI Extractor</h1>
            <p style="margin:0; max-width:520px;">
              Extract structured UI metadata, design tokens, and image assets from Figma with a cached, production-ready workflow.
            </p>
          </div>
          <div style="display:flex; gap:0.75rem; align-items:flex-end;">
            <div style="text-align:right;">
              <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em; color:#94A3B8; margin-bottom:0.15rem;">
                Session Snapshot
              </div>
              <div style="font-size:0.9rem; color:#475569;">
                Cached extraction and responsive UI, designed for real-world teams.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Session Dashboard")
        st.markdown("---")

        if "stats" not in st.session_state:
            st.session_state["stats"] = {
                "files_processed": 0,
                "downloads": 0,
            }

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Files", st.session_state["stats"]["files_processed"])
        with col_b:
            st.metric("Downloads", st.session_state["stats"]["downloads"])

        st.markdown("---")
        st.markdown("### 🎯 Key Capabilities")
        st.markdown(
            """
        - Automated component discovery  
        - Design token extraction  
        - Image URL resolution (SVG-first)  
        - Angular-ready JSON structure  
        - Smart API response caching  
        """
        )

        st.markdown("---")
        st.markdown("### 🧠 Caching Controls")
        if st.button("🗑 Clear cached data", use_container_width=True):
            st.cache_data.clear()
            st.success("Cached data cleared for this app session.")

        st.markdown("---")
        st.markdown("### 🔐 Security")
        st.info("Tokens are used in-memory only and never persisted or logged.")

    # Extraction form
    st.markdown("### 🎯 Component Extraction")
    st.markdown(
        "Provide your Figma file details to build a reusable, structured component catalog."
    )

    col1, col2 = st.columns(2)
    with col1:
        file_key = st.text_input(
            "📁 Figma File Key",
            value="",
            placeholder="e.g. AbCdEf123XYZ",
            help="Paste the file key from your Figma file URL.",
        )
    with col2:
        node_ids = st.text_input(
            "🔗 Node IDs (optional)",
            value="",
            placeholder="123:456, 789:012",
            help="Comma-separated node IDs to scope extraction; leave empty for full file.",
        )

    token = st.text_input(
        "🔑 Figma Personal Access Token",
        type="password",
        placeholder="Your Figma PAT…",
        help="Generate from Figma → Settings → Personal access tokens.",
    )

    st.markdown("")

    if st.button("🚀 Run Extraction", use_container_width=True):
        if not token or not file_key:
            st.error("Please provide both a Figma file key and a personal access token.")
        else:
            try:
                progress = st.progress(0)
                status = st.empty()

                status.info("📡 Connecting to Figma…")
                progress.progress(8)
                nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                status.info("🧩 Scanning component tree…")
                progress.progress(28)
                image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                status.info("🖼 Resolving image assets…")
                progress.progress(52)
                filtered_fills, renders_map = resolve_image_urls(
                    file_key, image_refs, node_id_list, token
                )

                status.info("🎨 Merging design tokens…")
                progress.progress(72)
                node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                status.info("📦 Building component catalog…")
                progress.progress(90)
                final_output = extract_ui_components(merged_payload)

                status.info("🧼 Normalizing output…")
                sanitized = remove_url_prefix_from_json(
                    final_output,
                    "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
                )

                st.session_state["metadata_json"] = sanitized
                st.session_state["stats"]["files_processed"] += 1

                progress.progress(100)
                status.empty()
                st.success("Extraction completed successfully.")
                st.balloons()

            except Exception as e:
                st.error(f"Extraction failed: {e}")
                st.info("Check file key, token validity, and your Figma permissions.")

    # Output
    if "metadata_json" in st.session_state:
        data = st.session_state["metadata_json"]
        st.markdown("---")
        st.markdown("### 📊 Extraction Summary")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Components", data["metadata"]["totalComponents"])
        with col2:
            st.metric("Text", len(data.get("textElements", [])))
        with col3:
            st.metric("Buttons", len(data.get("buttons", [])))
        with col4:
            st.metric("Containers", len(data.get("containers", [])))

        with st.expander("📋 Category breakdown", expanded=True):
            cols = st.columns(4)
            labels = [
                ("textElements", "Text"),
                ("buttons", "Buttons"),
                ("inputs", "Inputs"),
                ("containers", "Containers"),
                ("images", "Images"),
                ("navigation", "Navigation"),
                ("vectors", "Vectors"),
                ("other", "Other"),
            ]
            for idx, (key, label) in enumerate(labels):
                with cols[idx % 4]:
                    st.markdown(f"**{label}**")
                    st.write(len(data.get(key, [])))

        st.markdown("---")
        st.markdown("### 💾 Export & Inspect")

        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        col_d1, col_d2, col_d3 = st.columns([2, 1, 1])
        with col_d1:
            st.download_button(
                "📥 Download metadata.json",
                data=json_str,
                file_name="figma_metadata.json",
                mime="application/json",
                on_click=lambda: st.session_state["stats"].update(
                    {"downloads": st.session_state["stats"]["downloads"] + 1}
                ),
                use_container_width=True,
            )
        with col_d2:
            size_bytes = len(json_str.encode("utf-8"))
            if size_bytes < 1024:
                size = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                size = f"{size_bytes/1024:.1f} KB"
            else:
                size = f"{size_bytes/(1024*1024):.2f} MB"
            st.metric("File size", size)
        with col_d3:
            st.metric("Format", "JSON")

        with st.expander("👁️ Metadata header"):
            st.json(data["metadata"])

        with st.expander("🔍 Sample components"):
            t1, t2, t3, t4 = st.tabs(["Text", "Buttons", "Containers", "Other"])
            if data.get("textElements"):
                with t1:
                    st.json(data["textElements"][:3])
            if data.get("buttons"):
                with t2:
                    st.json(data["buttons"][:3])
            if data.get("containers"):
                with t3:
                    st.json(data["containers"][:3])
            with t4:
                st.json(
                    {
                        "inputs": len(data.get("inputs", [])),
                        "images": len(data.get("images", [])),
                        "navigation": len(data.get("navigation", [])),
                        "vectors": len(data.get("vectors", [])),
                        "other": len(data.get("other", [])),
                    }
                )

    st.markdown(
        """
    <hr/>
    <div style="text-align:center; padding:0.8rem 0 0.5rem 0; font-size:0.85rem; color:#94A3B8;">
      Built for modern design systems • Glassmorphism SaaS UI • Cached API pipeline
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
