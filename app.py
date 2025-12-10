#!/usr/bin/env python3
"""
Professional Figma UI Extractor
Enterprise-grade design system for UI extraction
"""

import streamlit as st
import requests
import json
import re
import datetime
from io import BytesIO
from typing import Any, Dict, List, Set, Tuple, Optional
import copy

# -----------------------------------------------------
# PROFESSIONAL THEMING - Modern SaaS Design
# -----------------------------------------------------
def apply_professional_styling():
    """Apply modern, professional gradient-based theme"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root Variables - Modern Purple/Blue Gradient Theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --accent-color: #667eea;
        --accent-hover: #764ba2;
        --dark-bg: #0f0f23;
        --card-bg: #1a1a2e;
        --text-primary: #ffffff;
        --text-secondary: #a0a0c0;
        --border-color: rgba(102, 126, 234, 0.2);
        --shadow-lg: 0 20px 60px rgba(102, 126, 234, 0.15);
        --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header Styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h1 {
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.2;
    }
    
    h2 {
        font-size: 2rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600;
    }
    
    /* Paragraph & Text */
    p, .stMarkdown {
        color: var(--text-secondary);
        font-size: 1.05rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Cards & Containers */
    .stTabs, .element-container, div[data-testid="stExpander"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        backdrop-filter: blur(10px);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1rem 2rem;
        border-radius: 12px 12px 0 0;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: rgba(26, 26, 46, 0.6) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        outline: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
        text-transform: none !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 172, 254, 0.5) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient) !important;
        border-radius: 10px;
    }
    
    .stProgress > div > div {
        background: rgba(102, 126, 234, 0.2) !important;
        border-radius: 10px;
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(26, 26, 46, 0.8) !important;
        border-left: 4px solid var(--accent-color) !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        color: var(--text-primary) !important;
    }
    
    .stSuccess {
        border-left-color: #00f2fe !important;
    }
    
    .stError {
        border-left-color: #f5576c !important;
    }
    
    .stInfo {
        border-left-color: #4facfe !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-secondary);
    }
    
    /* Code Blocks */
    .stCodeBlock, code {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #a0a0c0 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(26, 26, 46, 0.6) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: var(--accent-color) !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 2rem 0;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(26, 26, 46, 0.6);
        border: 2px dashed var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-color);
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-hover);
    }
    
    /* Custom Animation */
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
    
    /* Glassmorphism Effect */
    .glass-card {
        background: rgba(26, 26, 46, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Labels */
    label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Caption */
    .caption, small {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Config
st.set_page_config(
    page_title="Figma UI Extractor | Professional Edition",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_professional_styling()

# -----------------------------------------------------
# UTILITY HELPERS
# -----------------------------------------------------

def build_headers(token: str) -> Dict[str, str]:
    return {"Accept": "application/json", "X-Figma-Token": token}

def chunked(lst: List[str], n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def to_rgba(color: Dict[str, Any]) -> str:
    try:
        r = int(float(color.get("r", 0)) * 255)
        g = int(float(color.get("g", 0)) * 255)
        b = int(float(color.get("b", 0)) * 255)
        a = float(color.get("a", color.get("opacity", 1)))
        return f"rgba({r},{g},{b},{a})"
    except:
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

# -------------------------
# FIGMA API + NODE WALKERS
# -------------------------

def fetch_figma_nodes(file_key: str, node_ids: str, token: str, timeout: int = 60) -> Dict[str, Any]:
    """
    Fetch node(s) from Figma file. If node_ids is empty, fetch entire file document.
    Returns the raw JSON payload returned by the Figma API.
    """
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    params = {"ids": node_ids} if node_ids else {}
    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    if not r.ok:
        raise RuntimeError(f"Figma API error {r.status_code}: {r.text}")
    data = r.json()
    # filter invisible nodes in place (if present as document)
    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_invisible_nodes(doc)
    else:
        # fallback: if the payload contains a top-level document
        if isinstance(data.get("document"), dict):
            data["document"] = filter_invisible_nodes(data["document"])
    return data

def walk_nodes_collect_images_and_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, str]]]:
    """
    Walks the nodes payload and returns:
      - a set of image refs (imageHash / imageRef found in fills/strokes),
      - a list of node ids encountered (for render API),
      - a minimal node_meta mapping id -> {id, name, type}
    """
    image_refs: Set[str] = set()
    node_ids: List[str] = []
    node_meta: Dict[str, Dict[str, str]] = {}

    def visit(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        nid = n.get("id")
        if nid:
            node_ids.append(nid)
            node_meta[nid] = {"id": nid, "name": n.get("name", ""), "type": n.get("type", "")}
        # fills
        for f in n.get("fills", []) or []:
            if isinstance(f, dict) and f.get("type") == "IMAGE":
                ref = f.get("imageRef") or f.get("imageHash")
                if ref:
                    image_refs.add(ref)
        # strokes
        for s in n.get("strokes", []) or []:
            if isinstance(s, dict) and s.get("type") == "IMAGE":
                ref = s.get("imageRef") or s.get("imageHash")
                if ref:
                    image_refs.add(ref)
        # children
        for c in n.get("children", []) or []:
            visit(c)

    # nodes may be under 'nodes' dict (when using /nodes endpoint)
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    # or a top-level document
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])

    # de-duplicate node_ids preserving order
    seen = set()
    unique_node_ids = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_node_ids.append(nid)

    return image_refs, unique_node_ids, node_meta

def resolve_image_urls(file_key: str, image_refs: Set[str], node_ids: List[str], token: str, timeout: int = 60) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    """
    Resolve:
      - fills_map: mapping of imageRef -> url (from /images endpoint)
      - renders_map: mapping of nodeId -> rendered image url (from /images with ids param)
    Returns (filtered_fills_map, renders_map)
    """
    headers = build_headers(token)
    fills_map: Dict[str, str] = {}
    try:
        fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
        # Request all known imageRefs in one go if possible
        params = {}
        if image_refs:
            params["ids"] = ",".join(list(image_refs))
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

def build_icon_map(nodes_payload: Dict[str, Any], filtered_fills: Dict[str, str], renders_map: Dict[str, Optional[str]], node_meta: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    """
    For each node id in node_meta, find the first image reference in its fills (if any),
    prefer fills_map[imageRef] if available otherwise fallback to renders_map[nodeId].
    Returns node_id -> url mapping.
    """
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

    # Walk same places we walked earlier
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
    """
    Deep copy nodes_payload and inject `image_url` into nodes whose id exists in node_to_url.
    """
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

# -------------------------
# EXTRACTION HELPERS
# -------------------------

def extract_bounds(node: Dict[str, Any]) -> Optional[Dict[str, float]]:
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict) and all(k in box for k in ("x", "y", "width", "height")):
        try:
            return {"x": float(box["x"]), "y": float(box["y"]), "width": float(box["width"]), "height": float(box["height"])}
        except Exception:
            return None
    return None

def extract_layout(node: Dict[str, Any]) -> Dict[str, Any]:
    keys = ['layoutMode', 'constraints', 'paddingLeft', 'paddingRight', 'paddingTop', 'paddingBottom',
            'itemSpacing', 'counterAxisAlignItems', 'primaryAxisAlignItems', 'layoutGrow', 'layoutAlign',
            'layoutSizingHorizontal', 'layoutSizingVertical', 'counterAxisSizingMode', 'primaryAxisSizingMode',
            'clipsContent', 'layoutWrap', 'layoutGrids']
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
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    has_visual = bool(node.get("fills") or node.get("strokes") or node.get("effects") or node.get("image_url"))
    semantic = any(k in name for k in ['button', 'input', 'search', 'nav', 'menu', 'container', 'card', 'panel', 'header', 'footer', 'badge', 'chip'])
    vector_visible = (t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE'] and (node.get("strokes") or node.get("fills")))
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

def extract_components(root: Dict[str, Any], parent_path: str = "", out: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    if out is None:
        out = []
    if root is None or not isinstance(root, dict):
        return out
    path = f"{parent_path}/{root.get('name','Unnamed')}" if parent_path else (root.get('name') or 'Root')
    comp: Dict[str, Any] = {'id': root.get('id'), 'name': root.get('name'), 'type': root.get('type'), 'path': path}
    bounds = extract_bounds(root)
    if bounds:
        comp['position'] = bounds
    layout = extract_layout(root)
    if layout:
        comp['layout'] = layout
    styling = extract_visuals(root)
    if styling:
        comp['styling'] = styling
    # two possible keys for injected image url
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
    return roots

def organize_for_angular(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    organized = {
        'metadata': {'totalComponents': len(components), 'extractedAt': datetime.datetime.utcnow().isoformat() + 'Z', 'version': 1},
        'textElements': [], 'buttons': [], 'inputs': [], 'containers': [],
        'images': [], 'navigation': [], 'vectors': [], 'other': []
    }
    for c in components:
        organized.setdefault(classify_bucket(c), []).append(c)
    return organized

def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    roots = find_document_roots(merged_payload)
    if not roots:
        raise RuntimeError("No document roots found in payload")
    all_components: List[Dict[str, Any]] = []
    for r in roots:
        if isinstance(r, dict):
            extract_components(r, "", all_components)
    return organize_for_angular(all_components)

def remove_url_prefix_from_json(payload: Dict[str, Any], url_prefix: str) -> Dict[str, Any]:
    """
    Removes url_prefix from any imageUrl or image_url values in the payload.
    Returns a deep-copied processed payload.
    """
    p = copy.deepcopy(payload)
    def process(obj: Any):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k in ("imageUrl", "image_url") and isinstance(v, str):
                    if v.startswith(url_prefix):
                        obj[k] = v.replace(url_prefix, "", 1)
                else:
                    process(v)
        elif isinstance(obj, list):
            for item in obj:
                process(item)
    process(p)
    return p

# -------------------------
# STREAMLIT UI + WORKFLOW
# -------------------------

def main():
    # Hero Header with Gradient
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 2rem 0;'>
        <div style='display: inline-block; padding: 0.5rem 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); border-radius: 50px; border: 1px solid rgba(102, 126, 234, 0.3); margin-bottom: 1.5rem;'>
            <span style='font-size: 0.9rem; font-weight: 600; color: #667eea; text-transform: uppercase; letter-spacing: 0.1em;'>✨ Enterprise Edition</span>
        </div>
        <h1 style='margin-bottom: 0.8rem; font-size: 3.5rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.2rem; color: #a0a0c0; font-weight: 400; max-width: 700px; margin: 0 auto; line-height: 1.6;'>
            Extract, analyze, and export UI components from Figma with precision and elegance
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Dashboard")
        st.markdown("---")

        if 'stats' not in st.session_state:
            st.session_state['stats'] = {'files_processed': 0, 'downloads': 0}

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files", st.session_state['stats']['files_processed'])
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'])

        st.markdown("---")
        st.markdown("### 🎯 Features")
        st.markdown("""
        - **Smart Extraction** - Automated component detection
        - **Style Parsing** - Complete design token extraction
        - **Image Resolution** - SVG and raster support
        - **JSON Export** - Structured metadata output
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Docs](https://www.figma.com/developers/api)
        - [Angular Framework](https://angular.io)
        - [Design Systems](https://www.designsystems.com)
        """)
        
        st.markdown("---")
        st.markdown("### 🔐 Security")
        st.info("🔒 Tokens are never stored. All processing is session-based.")

    # Main Content
    st.markdown("### 🎯 Component Extraction")
    st.markdown("Extract UI components with complete metadata, styling information, and image assets from your Figma designs.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        file_key = st.text_input(
            "📁 Figma File Key", 
            value="", 
            help="Enter the file key from your Figma file URL (e.g., abc123xyz from figma.com/file/abc123xyz/...)",
            placeholder="abc123xyz..."
        )
    with col2:
        node_ids = st.text_input(
            "🔗 Node IDs (Optional)", 
            value="", 
            help="Comma-separated node IDs to extract specific components. Leave empty to extract entire file.",
            placeholder="123:456, 789:012"
        )

    token = st.text_input(
        "🔑 Figma Personal Access Token", 
        type="password", 
        help="Generate a personal access token in your Figma account settings under 'Personal Access Tokens'",
        placeholder="Enter your Figma token..."
    )

    st.markdown("")  # Spacing
    
    if st.button("🚀 Extract UI Components", type="primary"):
        if not token or not file_key:
            st.error("⚠️ Please provide both a file key and a Figma access token to proceed.")
        else:
            try:
                progress = st.progress(0)
                status = st.empty()

                status.text("📡 Connecting to Figma API...")
                progress.progress(5)
                nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                status.text("🖼️ Analyzing component structure...")
                progress.progress(25)
                image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                status.text("🔗 Resolving image assets...")
                progress.progress(50)
                filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                status.text("🎨 Processing design tokens...")
                progress.progress(70)
                node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                status.text("📦 Extracting components...")
                progress.progress(85)
                final_output = extract_ui_components(merged_payload)

                status.text("✨ Finalizing extraction...")
                progress.progress(95)
                sanitized = remove_url_prefix_from_json(final_output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                st.session_state['metadata_json'] = sanitized
                st.session_state['stats']['files_processed'] += 1
                progress.progress(100)
                status.empty()
                st.success("✅ Extraction completed successfully!")

                # Metrics Display
                st.markdown("### 📊 Extraction Summary")
                st.markdown("")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Components", sanitized['metadata']['totalComponents'])
                with col2:
                    st.metric("Text Elements", len(sanitized.get('textElements', [])))
                with col3:
                    st.metric("Buttons", len(sanitized.get('buttons', [])))
                with col4:
                    st.metric("Containers", len(sanitized.get('containers', [])))

                st.markdown("")
                
                # Additional metrics in expandable section
                with st.expander("📋 Detailed Category Breakdown", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    categories = {
                        'textElements': 'Text Elements',
                        'buttons': 'Buttons',
                        'inputs': 'Input Fields',
                        'containers': 'Containers',
                        'images': 'Images',
                        'navigation': 'Navigation',
                        'vectors': 'Vector Graphics',
                        'other': 'Other Components'
                    }
                    
                    items = list(categories.items())
                    mid = len(items) // 2
                    
                    with col1:
                        for key, label in items[:mid]:
                            count = len(sanitized.get(key, []))
                            if count > 0:
                                st.markdown(f"**{label}:** `{count}` components")
                    
                    with col2:
                        for key, label in items[mid:]:
                            count = len(sanitized.get(key, []))
                            if count > 0:
                                st.markdown(f"**{label}:** `{count}` components")

            except Exception as e:
                st.error(f"❌ Extraction failed: {str(e)}")
                st.info("💡 Make sure your token is valid and you have access to the specified file.")

    # Download Section
    if 'metadata_json' in st.session_state:
        st.markdown("---")
        st.markdown("### 💾 Export Options")
        st.markdown("Download the extracted component metadata in JSON format.")
        st.markdown("")
        
        json_str = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.download_button(
                "📥 Download metadata.json",
                data=json_str,
                file_name="metadata.json",
                mime="application/json",
                on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                use_container_width=True
            )
        with col2:
            st.metric("File Size", f"{len(json_str):,} bytes")
        with col3:
            st.metric("Format", "JSON")

        # Preview Section
        with st.expander("👁️ Preview JSON Structure", expanded=False):
            st.json(st.session_state['metadata_json']['metadata'])

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <p style='color: #6B7280; font-size: 0.95rem; margin: 0;'>
            Built with ❤️ using <strong>Streamlit</strong> • Professional Edition v1.0
        </p>
        <p style='color: #4B5563; font-size: 0.85rem; margin-top: 0.5rem;'>
            Powered by Figma API • Optimized for Angular Development
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
