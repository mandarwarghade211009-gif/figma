#!/usr/bin/env python3
"""
Figma UI Extractor — Premium Enterprise Edition
Ultra-professional SaaS design • Luxury gradients • Production-ready
"""

import streamlit as st
import requests
import json
import datetime
from typing import Any, Dict, List, Set, Tuple, Optional
import copy

# =====================================================
# PREMIUM LUXURY THEME — ULTRA PROFESSIONAL
# =====================================================
def apply_premium_styling():
    """Apply premium luxury gradient theme with professional polish"""
    st.markdown("""
    <style>
    /* Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    html, body {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
    }

    :root {
        /* Premium Gradient Palette */
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-accent: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gradient-warning: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --gradient-hero: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        
        /* Luxury Colors */
        --primary-purple: #667eea;
        --primary-violet: #764ba2;
        --accent-pink: #f093fb;
        --accent-coral: #f5576c;
        --success-cyan: #00f2fe;
        --success-blue: #4facfe;
        
        /* Sophisticated Neutrals */
        --bg-luxury: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        --surface-white: #ffffff;
        --surface-light: #fafbfc;
        --surface-elevated: rgba(255, 255, 255, 0.95);
        
        /* Typography */
        --text-primary: #1a1a2e;
        --text-secondary: #16213e;
        --text-muted: #6c757d;
        --text-soft: #8892a6;
        
        /* Borders & Effects */
        --border-subtle: rgba(102, 126, 234, 0.12);
        --border-medium: rgba(102, 126, 234, 0.25);
        --border-strong: rgba(102, 126, 234, 0.4);
        
        /* Premium Shadows */
        --shadow-luxury: 0 20px 60px rgba(102, 126, 234, 0.15);
        --shadow-elevated: 0 30px 80px rgba(118, 75, 162, 0.2);
        --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.08);
        --shadow-glow: 0 0 40px rgba(102, 126, 234, 0.3);
        
        /* Glass Effects */
        --glass-bg: rgba(255, 255, 255, 0.88);
        --glass-border: rgba(255, 255, 255, 0.4);
        --blur-premium: blur(20px);
    }

    /* Main App Container */
    .stApp {
        background: var(--bg-luxury);
        font-family: 'Sora', -apple-system, system-ui, 'Segoe UI', sans-serif;
        color: var(--text-primary);
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
    }

    /* Scrollable Content Area */
    .main .block-container {
        max-width: 1400px;
        padding: 2rem 2.5rem;
        margin: 0 auto;
        height: calc(100vh - 4rem);
        overflow-y: auto;
        overflow-x: hidden;
    }

    /* Premium Scrollbar */
    .main .block-container::-webkit-scrollbar {
        width: 12px;
    }
    .main .block-container::-webkit-scrollbar-track {
        background: linear-gradient(180deg, #f5f7fa 0%, #e9ecef 100%);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    .main .block-container::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 10px;
        border: 2px solid #f5f7fa;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .main .block-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Hide Streamlit Branding */
    #MainMenu, footer, header {
        visibility: hidden;
        height: 0;
    }
    .stDeployButton {
        display: none;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', 'Sora', system-ui;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }

    h1 {
        font-size: 3.2rem !important;
        background: var(--gradient-hero);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.8rem 0 !important;
        text-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    }

    h2 {
        font-size: 2rem !important;
        color: var(--text-primary);
        margin: 1rem 0 0.5rem 0 !important;
    }

    h3 {
        font-size: 1.4rem !important;
        color: var(--text-secondary);
        font-weight: 600;
        margin: 0.8rem 0 0.4rem 0 !important;
    }

    p, .stMarkdown {
        color: var(--text-muted);
        font-size: 1.05rem;
        line-height: 1.7;
        font-weight: 400;
        margin: 0.6rem 0;
    }

    /* ===== PREMIUM GLASS CARDS ===== */
    .luxury-card {
        background: var(--glass-bg);
        backdrop-filter: var(--blur-premium);
        border-radius: 24px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-luxury);
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .luxury-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .luxury-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-elevated);
        border-color: var(--border-medium);
    }

    .luxury-card:hover::before {
        opacity: 1;
    }

    .element-container {
        margin: 0.8rem 0 !important;
    }

    /* ===== PREMIUM TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--surface-light);
        border-radius: 16px;
        padding: 0.5rem;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-soft);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.8rem 1.8rem;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-muted);
        border: none;
        background: transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Space Grotesk', system-ui;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.08);
        color: var(--primary-purple);
    }

    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary) !important;
        color: white !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }

    /* ===== LUXURY INPUT FIELDS ===== */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: var(--surface-white) !important;
        border-radius: 16px !important;
        border: 2px solid var(--border-subtle) !important;
        padding: 1rem 1.4rem !important;
        font-size: 1rem !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', system-ui !important;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTextInput > div > div > input:hover,
    .stTextArea textarea:hover {
        border-color: var(--border-medium) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary-purple) !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), var(--shadow-glow) !important;
        outline: none !important;
    }

    label {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        font-family: 'Space Grotesk', system-ui !important;
        letter-spacing: -0.01em;
    }

    /* ===== PREMIUM BUTTONS ===== */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        font-family: 'Space Grotesk', system-ui !important;
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 40px rgba(102, 126, 234, 0.5);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Download Button */
    .stDownloadButton > button {
        background: var(--gradient-success) !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        font-family: 'Space Grotesk', system-ui !important;
        box-shadow: 0 12px 32px rgba(79, 172, 254, 0.4);
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 40px rgba(79, 172, 254, 0.5);
    }

    /* ===== LUXURY METRICS ===== */
    [data-testid="stMetric"] {
        background: var(--glass-bg);
        backdrop-filter: var(--blur-premium);
        border-radius: 20px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-luxury);
        padding: 1.5rem;
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-elevated);
        border-color: var(--border-medium);
    }

    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Space Grotesk', system-ui;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-soft) !important;
        font-weight: 600;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div > div > div {
        background: var(--gradient-primary) !important;
        border-radius: 10px;
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #e9ecef 0%, #f8f9fa 100%) !important;
        border-radius: 10px;
        height: 10px !important;
        border: 1px solid var(--border-subtle);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }

    /* ===== PREMIUM ALERTS ===== */
    .stAlert {
        border-radius: 20px !important;
        border: 1px solid var(--border-subtle) !important;
        background: var(--glass-bg) !important;
        backdrop-filter: var(--blur-premium);
        box-shadow: var(--shadow-luxury);
        padding: 1.2rem 1.5rem !important;
    }
    .stSuccess {
        border-left: 4px solid var(--success-blue) !important;
    }
    .stError {
        border-left: 4px solid var(--accent-coral) !important;
    }
    .stInfo {
        border-left: 4px solid var(--primary-purple) !important;
    }

    /* ===== LUXURY SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--surface-white) 0%, var(--surface-light) 100%);
        border-right: 1px solid var(--border-subtle);
        backdrop-filter: var(--blur-premium);
        box-shadow: 8px 0 32px rgba(102, 126, 234, 0.08);
        height: 100vh;
        overflow-y: auto;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1.5rem;
    }

    [data-testid="stSidebar"] h3 {
        font-size: 1.2rem !important;
        margin-bottom: 1rem !important;
    }

    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 8px;
    }
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: var(--surface-light);
    }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 10px;
    }

    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background: var(--surface-light) !important;
        border-radius: 16px !important;
        border: 1px solid var(--border-subtle) !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.05) !important;
        border-color: var(--border-medium) !important;
        box-shadow: var(--shadow-soft);
    }

    /* ===== JSON / CODE ===== */
    .stJson {
        max-height: 400px;
        overflow-y: auto;
        background: var(--surface-light);
        border-radius: 16px;
        border: 1px solid var(--border-subtle);
        padding: 1.2rem !important;
        font-family: 'JetBrains Mono', monospace;
    }

    code, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        background: var(--surface-light) !important;
        border-radius: 8px;
        padding: 0.2rem 0.5rem;
    }

    /* ===== COLUMNS ===== */
    [data-testid="column"] {
        padding: 0 0.6rem;
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--border-medium), transparent);
        margin: 2rem 0;
    }

    /* ===== PREMIUM BADGES ===== */
    .premium-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        background: var(--gradient-primary);
        color: white;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }

    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem;
            height: calc(100vh - 3rem);
        }
        h1 {
            font-size: 2.2rem !important;
        }
        h2 {
            font-size: 1.6rem !important;
        }
        [data-testid="column"] {
            min-width: 100% !important;
            padding: 0 0.3rem;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
        }
    }

    @media (min-width: 769px) and (max-width: 1199px) {
        .main .block-container {
            padding: 1.8rem 2rem;
            max-width: 100%;
        }
    }

    @media (min-width: 1440px) {
        .main .block-container {
            max-width: 1600px;
            padding: 2.5rem 3rem;
        }
        h1 {
            font-size: 3.6rem !important;
        }
    }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }

    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }

    .shimmer {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Figma UI Extractor | Premium Enterprise",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_premium_styling()

# =====================================================
# CORE UTILITY FUNCTIONS
# =====================================================
def build_headers(token: str) -> Dict[str, str]:
    """Build request headers with Figma authentication"""
    return {"Accept": "application/json", "X-Figma-Token": token}

def chunked(lst: List[str], n: int):
    """Split list into chunks of size n"""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def to_rgba(color: Dict[str, Any]) -> str:
    """Convert Figma color object to RGBA CSS string"""
    try:
        r = int(float(color.get("r", 0)) * 255)
        g = int(float(color.get("g", 0)) * 255)
        b = int(float(color.get("b", 0)) * 255)
        a = float(color.get("a", color.get("opacity", 1)))
        return f"rgba({r},{g},{b},{a})"
    except Exception:
        return "rgba(0,0,0,1)"

def is_nonempty_list(v: Any) -> bool:
    """Check if value is a non-empty list"""
    return isinstance(v, list) and len(v) > 0

def is_visible(node: Dict[str, Any]) -> bool:
    """Check if node is visible in Figma"""
    v = node.get("visible")
    return True if v is None else bool(v)

def filter_invisible_nodes(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Recursively filter out invisible nodes from tree"""
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

# =====================================================
# FIGMA API FUNCTIONS
# =====================================================
def fetch_figma_nodes(file_key: str, node_ids: str, token: str, timeout: int = 60) -> Dict[str, Any]:
    """Fetch nodes from Figma API"""
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    params = {"ids": node_ids} if node_ids else {}
    
    resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    
    if not resp.ok:
        raise RuntimeError(f"Figma API error {resp.status_code}: {resp.text}")
    
    data = resp.json()
    
    # Filter invisible nodes
    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_invisible_nodes(doc)
    elif isinstance(data.get("document"), dict):
        data["document"] = filter_invisible_nodes(data["document"])
    
    return data

def walk_nodes_collect_images_and_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, str]]]:
    """Walk node tree and collect image references and node metadata"""
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
                "type": n.get("type", "")
            }
        
        # Collect image fills
        for f in n.get("fills", []) or []:
            if isinstance(f, dict) and f.get("type") == "IMAGE":
                ref = f.get("imageRef") or f.get("imageHash")
                if ref:
                    image_refs.add(ref)
        
        # Collect image strokes
        for s in n.get("strokes", []) or []:
            if isinstance(s, dict) and s.get("type") == "IMAGE":
                ref = s.get("imageRef") or s.get("imageHash")
                if ref:
                    image_refs.add(ref)
        
        # Process children recursively
        for c in n.get("children", []) or []:
            visit(c)

    # Process payload
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])

    # Deduplicate node IDs
    seen = set()
    unique_ids: List[str] = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_ids.append(nid)

    return image_refs, unique_ids, node_meta

def resolve_image_urls(
    file_key: str, 
    image_refs: Set[str], 
    node_ids: List[str], 
    token: str, 
    timeout: int = 60
) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    """Resolve image URLs from Figma API"""
    headers = build_headers(token)
    fills_map: Dict[str, str] = {}
    
    # Fetch fill images
    try:
        fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
        params = {"ids": ",".join(list(image_refs))} if image_refs else {}
        r = requests.get(fills_url, headers=headers, params=params or None, timeout=timeout)
        if r.ok:
            fills_map = r.json().get("images", {}) or {}
    except Exception:
        fills_map = {}

    # Fetch rendered images
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

def build_icon_map(
    nodes_payload: Dict[str, Any],
    filtered_fills: Dict[str, str],
    renders_map: Dict[str, Optional[str]],
    node_meta: Dict[str, Dict[str, str]]
) -> Dict[str, str]:
    """Build mapping of node IDs to image URLs"""
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

    # Process payload
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                map_first_image(doc)
    
    if isinstance(nodes_payload.get("document"), dict):
        map_first_image(nodes_payload["document"])

    # Build final mapping
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
    """Deep copy payload and inject image URLs into nodes"""
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

# =====================================================
# COMPONENT EXTRACTION LOGIC
# =====================================================
def extract_bounds(node: Dict[str, Any]) -> Optional[Dict[str, float]]:
    """Extract absolute bounding box"""
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict) and all(k in box for k in ("x", "y", "width", "height")):
        try:
            return {
                "x": float(box["x"]),
                "y": float(box["y"]),
                "width": float(box["width"]),
                "height": float(box["height"])
            }
        except Exception:
            return None
    return None

def extract_layout(node: Dict[str, Any]) -> Dict[str, Any]:
    """Extract layout properties"""
    keys = [
        'layoutMode', 'constraints', 'paddingLeft', 'paddingRight',
        'paddingTop', 'paddingBottom', 'itemSpacing', 'counterAxisAlignItems',
        'primaryAxisAlignItems', 'layoutGrow', 'layoutAlign',
        'layoutSizingHorizontal', 'layoutSizingVertical',
        'counterAxisSizingMode', 'primaryAxisSizingMode',
        'clipsContent', 'layoutWrap', 'layoutGrids'
    ]
    layout: Dict[str, Any] = {}
    for k in keys:
        if k in node:
            layout[k] = node[k]
    return layout

def extract_visuals(node: Dict[str, Any]) -> Dict[str, Any]:
    """Extract visual styling properties"""
    styling: Dict[str, Any] = {}
    
    # Process fills
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

    # Background color
    if "backgroundColor" in node and isinstance(node["backgroundColor"], dict):
        styling["backgroundColor"] = to_rgba(node["backgroundColor"])

    # Process strokes
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

    # Corner radius
    if isinstance(node.get("cornerRadius"), (int, float)) and node.get("cornerRadius", 0) > 0:
        styling["cornerRadius"] = node.get("cornerRadius")

    # Process effects
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
    """Extract text content and typography"""
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
            "textCase": (style.get("textCase") or "none").lower()
        }
    
    fills = node.get("fills")
    if is_nonempty_list(fills):
        for f in fills:
            if isinstance(f, dict) and f.get("type") == "SOLID" and "color" in f:
                t["color"] = to_rgba(f["color"])
                break
    
    return t

def should_include(node: Dict[str, Any]) -> bool:
    """Determine if node should be included in extraction"""
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    has_visual = bool(
        node.get("fills") or 
        node.get("strokes") or 
        node.get("effects") or 
        node.get("image_url")
    )
    semantic = any(k in name for k in [
        'button', 'input', 'search', 'nav', 'menu',
        'container', 'card', 'panel', 'header',
        'footer', 'badge', 'chip'
    ])
    vector_visible = (
        t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE'] and 
        (node.get("strokes") or node.get("fills"))
    )
    
    return any([
        t == 'TEXT',
        has_visual,
        vector_visible,
        isinstance(node.get('cornerRadius'), (int, float)) and node.get('cornerRadius', 0) > 0,
        bool(node.get('layoutMode')),
        t in ['FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'SECTION'],
        semantic
    ])

def classify_bucket(comp: Dict[str, Any]) -> str:
    """Classify component into category"""
    t = (comp.get("type") or "").upper()
    name = (comp.get("name") or "").lower()
    
    if t == "TEXT":
        return "textElements"
    if "button" in name:
        return "buttons"
    if any(k in name for k in ['input', 'search', 'textfield', 'field']):
        return "inputs"
    if any(k in name for k in ['nav', 'menu', 'sidebar', 'toolbar', 'header', 'footer', 'breadcrumb']):
        return "navigation"
    if comp.get("imageUrl") or comp.get("image_url"):
        return "images"
    if t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE']:
        return "vectors"
    if t in ['FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'SECTION'] or any(k in name for k in ['container', 'card', 'panel', 'section']):
        return "containers"
    
    return "other"

def extract_components(
    root: Dict[str, Any],
    parent_path: str = "",
    out: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """Recursively extract components from node tree"""
    if out is None:
        out = []
    if root is None or not isinstance(root, dict):
        return out
    
    path = f"{parent_path}/{root.get('name','Unnamed')}" if parent_path else (root.get('name') or 'Root')
    
    comp: Dict[str, Any] = {
        'id': root.get('id'),
        'name': root.get('name'),
        'type': root.get('type'),
        'path': path
    }
    
    bounds = extract_bounds(root)
    if bounds:
        comp['position'] = bounds
    
    layout = extract_layout(root)
    if layout:
        comp['layout'] = layout
    
    styling = extract_visuals(root)
    if styling:
        comp['styling'] = styling
    
    if root.get('image_url'):
        comp['imageUrl'] = root.get('image_url')
    if root.get('imageUrl'):
        comp['imageUrl'] = root.get('imageUrl')
    
    text = extract_text(root)
    if text:
        comp['text'] = text
    
    if should_include(root):
        out.append(comp)
    
    for child in root.get('children', []) or []:
        if isinstance(child, dict):
            extract_components(child, path, out)
    
    return out

def find_document_roots(nodes_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find all document root nodes"""
    roots: List[Dict[str, Any]] = []
    
    if isinstance(nodes_payload.get('nodes'), dict):
        for v in nodes_payload['nodes'].values():
            if isinstance(v, dict) and isinstance(v.get('document'), dict):
                roots.append(v['document'])
        if roots:
            return roots
    
    if isinstance(nodes_payload.get('document'), dict):
        roots.append(nodes_payload['document'])
    
    return roots

def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and organize all UI components"""
    roots = find_document_roots(merged_payload)
    if not roots:
        raise RuntimeError("No document roots found in payload")
    
    all_components: List[Dict[str, Any]] = []
    for r in roots:
        if isinstance(r, dict):
            extract_components(r, "", all_components)
    
    organized = {
        'metadata': {
            'totalComponents': len(all_components),
            'extractedAt': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': 1
        },
        'textElements': [],
        'buttons': [],
        'inputs': [],
        'containers': [],
        'images': [],
        'navigation': [],
        'vectors': [],
        'other': []
    }
    
    for c in all_components:
        organized.setdefault(classify_bucket(c), []).append(c)
    
    return organized

def remove_url_prefix_from_json(payload: Dict[str, Any], url_prefix: str) -> Dict[str, Any]:
    """Remove URL prefix from image URLs"""
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

# =====================================================
# MAIN UI
# =====================================================
def main():
    """Main application interface"""
    
    # Premium Hero Section
    st.markdown("""
    <div class="luxury-card" style="margin-bottom: 2rem; text-align: center;">
        <div class="premium-badge" style="margin-bottom: 1.2rem;">
            <span>✨</span>
            <span>Premium Enterprise Edition</span>
        </div>
        <h1>Figma UI Extractor</h1>
        <p style="font-size: 1.15rem; max-width: 700px; margin: 0.8rem auto; color: var(--text-muted);">
            Extract structured UI metadata, design tokens, and image assets from Figma with enterprise-grade precision and professional workflow automation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Luxury Sidebar
    with st.sidebar:
        st.markdown("### 📊 Analytics Dashboard")
        st.markdown("---")

        if 'stats' not in st.session_state:
            st.session_state['stats'] = {
                'files_processed': 0,
                'downloads': 0,
                'total_components': 0
            }

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files Processed", st.session_state['stats']['files_processed'])
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'])

        if st.session_state['stats']['total_components'] > 0:
            st.metric("Components Extracted", st.session_state['stats']['total_components'])

        st.markdown("---")
        st.markdown("### ✨ Premium Features")
        st.markdown("""
        - **🎯 Smart Component Discovery** – Automated detection
        - **🎨 Design Token Extraction** – Complete styling data
        - **🖼️ Image Resolution** – SVG & raster support
        - **📦 Structured Export** – Angular-ready JSON
        - **⚡ High Performance** – Optimized API calls
        - **🔒 Enterprise Security** – Token protection
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Documentation")
        st.markdown("""
        - [Figma API Reference](https://www.figma.com/developers/api)
        - [Angular Material Design](https://material.angular.io)
        - [Design System Tokens](https://designtokens.org)
        """)
        
        st.markdown("---")
        st.markdown("### 🔐 Security & Privacy")
        st.info("🔒 All tokens are processed in-memory only and never stored or logged. Your data remains completely private and secure.")

    # Main Extraction Interface
    st.markdown("### 🎯 Component Extraction Workspace")
    st.markdown("Configure your Figma file details below to generate a comprehensive, structured component catalog.")
    
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        file_key = st.text_input(
            "📁 Figma File Key",
            value="",
            placeholder="e.g., AbCdEf123XYZ",
            help="Extract the file key from your Figma file URL: figma.com/file/[FILE_KEY]/..."
        )
    with col2:
        node_ids = st.text_input(
            "🔗 Node IDs (Optional)",
            value="",
            placeholder="123:456, 789:012",
            help="Comma-separated node IDs to extract specific components. Leave empty to extract the entire file."
        )

    token = st.text_input(
        "🔑 Figma Personal Access Token",
        type="password",
        placeholder="Enter your Figma Personal Access Token...",
        help="Generate a PAT from: Figma → Settings → Account → Personal Access Tokens"
    )

    st.markdown("")

    if st.button("🚀 Start Extraction", use_container_width=True):
        if not token or not file_key:
            st.error("❌ Please provide both a Figma file key and a personal access token to proceed.")
        else:
            try:
                progress = st.progress(0)
                status = st.empty()

                # Step 1: Fetch nodes
                status.info("📡 Connecting to Figma API...")
                progress.progress(10)
                nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                # Step 2: Analyze structure
                status.info("🔍 Analyzing component structure...")
                progress.progress(30)
                image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                # Step 3: Resolve images
                status.info("🖼️ Resolving image assets...")
                progress.progress(55)
                filtered_fills, renders_map = resolve_image_urls(
                    file_key, image_refs, node_id_list, token
                )

                # Step 4: Process tokens
                status.info("🎨 Processing design tokens...")
                progress.progress(75)
                node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                # Step 5: Extract components
                status.info("📦 Extracting UI components...")
                progress.progress(90)
                final_output = extract_ui_components(merged_payload)

                # Step 6: Finalize
                status.info("✨ Finalizing extraction...")
                progress.progress(98)
                sanitized = remove_url_prefix_from_json(
                    final_output,
                    "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/"
                )
                
                st.session_state['metadata_json'] = sanitized
                st.session_state['stats']['files_processed'] += 1
                st.session_state['stats']['total_components'] = sanitized['metadata']['totalComponents']
                
                progress.progress(100)
                status.empty()
                
                st.success("✅ Extraction completed successfully!")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Extraction failed: {str(e)}")
                st.info("💡 Please verify your file key, token validity, and Figma permissions.")

    # Results Display
    if 'metadata_json' in st.session_state:
        data = st.session_state['metadata_json']
        
        st.markdown("---")
        st.markdown("### 📊 Extraction Summary")
        st.markdown("")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Components", data['metadata']['totalComponents'])
        with col2:
            st.metric("Text Elements", len(data.get('textElements', [])))
        with col3:
            st.metric("Buttons", len(data.get('buttons', [])))
        with col4:
            st.metric("Containers", len(data.get('containers', [])))

        st.markdown("")

        with st.expander("📋 Detailed Category Breakdown", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            categories = [
                ('textElements', '📝 Text', col1),
                ('buttons', '🔘 Buttons', col2),
                ('inputs', '📥 Inputs', col3),
                ('containers', '📦 Containers', col4),
                ('images', '🖼️ Images', col1),
                ('navigation', '🧭 Navigation', col2),
                ('vectors', '✏️ Vectors', col3),
                ('other', '🔧 Other', col4)
            ]
            
            for key, label, col in categories:
                with col:
                    count = len(data.get(key, []))
                    st.markdown(f"**{label}**")
                    st.markdown(f"`{count}` components")
                    st.markdown("")

        st.markdown("---")
        st.markdown("### 💾 Export & Download")
        st.markdown("Download your extracted component metadata in structured JSON format.")
        st.markdown("")

        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.download_button(
                "📥 Download metadata.json",
                data=json_str,
                file_name="figma_ui_metadata.json",
                mime="application/json",
                on_click=lambda: st.session_state['stats'].update({
                    'downloads': st.session_state['stats']['downloads'] + 1
                }),
                use_container_width=True
            )
        with col2:
            size_bytes = len(json_str.encode('utf-8'))
            if size_bytes < 1024:
                size = f"{size_bytes}B"
            elif size_bytes < 1024 * 1024:
                size = f"{size_bytes/1024:.1f}KB"
            else:
                size = f"{size_bytes/(1024*1024):.2f}MB"
            st.metric("File Size", size)
        with col3:
            st.metric("Format", "JSON")

        st.markdown("")

        # Preview Sections
        with st.expander("👁️ Metadata Preview"):
            st.json(data['metadata'])

        with st.expander("🔍 Component Samples"):
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Elements", "🔘 Buttons", "📦 Containers", "📊 All Categories"])
            
            with tab1:
                if data.get('textElements'):
                    st.json(data['textElements'][:3])
                    if len(data['textElements']) > 3:
                        st.caption(f"Showing 3 of {len(data['textElements'])} text elements")
                else:
                    st.info("No text elements found")
            
            with tab2:
                if data.get('buttons'):
                    st.json(data['buttons'][:3])
                    if len(data['buttons']) > 3:
                        st.caption(f"Showing 3 of {len(data['buttons'])} buttons")
                else:
                    st.info("No buttons found")
            
            with tab3:
                if data.get('containers'):
                    st.json(data['containers'][:3])
                    if len(data['containers']) > 3:
                        st.caption(f"Showing 3 of {len(data['containers'])} containers")
                else:
                    st.info("No containers found")
            
            with tab4:
                category_counts = {
                    cat: len(data.get(cat, []))
                    for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']
                }
                st.json(category_counts)

    # Premium Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <p style="color: var(--text-muted); font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600;">
            Built with ❤️ for Design Systems & Enterprise Teams
        </p>
        <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 0.8rem;">
            Premium Enterprise Edition • Powered by Figma API • Production-Ready Architecture
        </p>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; margin-top: 1rem;">
            <span style="color: var(--text-soft); font-size: 0.85rem;">🎨 Luxury Gradients</span>
            <span style="color: var(--text-soft); font-size: 0.85rem;">⚡ High Performance</span>
            <span style="color: var(--text-soft); font-size: 0.85rem;">📱 Fully Responsive</span>
            <span style="color: var(--text-soft); font-size: 0.85rem;">🔒 Enterprise Secure</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
