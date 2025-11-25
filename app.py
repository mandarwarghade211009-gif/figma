#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor
Enterprise-grade design system for UI extraction and code processing
"""

import streamlit as st
import requests
import json
import re
import datetime
from io import BytesIO
from typing import Any, Dict, List, Set, Tuple, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
import copy
import os

# -----------------------------------------------------
# PROFESSIONAL THEMING - ENHANCED WITH LIGHT COLORS
# -----------------------------------------------------
def apply_professional_styling():
    """Apply professional, modern light-themed CSS with high contrast"""
    st.markdown("""
    <style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Reset and Base Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main App Background - Light Professional */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    
    /* Sidebar Styling - Clean White */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fb 100%);
        border-right: 2px solid #e1e8ed;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.04);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #1a202c;
    }
    
    /* Headers - High Contrast Dark Text */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
        color: #1a202c !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.75rem !important;
        color: #2d3748 !important;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
    }
    
    h3 {
        font-size: 1.35rem !important;
        color: #2d3748 !important;
    }
    
    /* Paragraph and Body Text - High Contrast */
    p, div, span, label {
        color: #2d3748 !important;
        line-height: 1.7;
    }
    
    /* Buttons - Modern Professional */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.025em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Buttons - Stylish Teal/Cyan Gradient */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.75rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.35), 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stDownloadButton > button:before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important;
        box-shadow: 0 6px 25px rgba(6, 182, 212, 0.5), 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-3px) scale(1.02) !important;
    }
    
    .stDownloadButton > button:hover:before {
        left: 100% !important;
    }
    
    .stDownloadButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
        box-shadow: 0 2px 10px rgba(6, 182, 212, 0.3) !important;
    }
    
    /* Add download icon effect */
    .stDownloadButton > button::after {
        content: '⬇' !important;
        margin-left: 8px !important;
        font-size: 1.1rem !important;
        display: inline-block !important;
        transition: transform 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover::after {
        transform: translateY(3px) !important;
        animation: bounce 0.6s infinite !important;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(5px); }
    }
    
    /* Input Fields - Clean and Professional */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #1a202c !important;
        font-size: 0.95rem !important;
        padding: 0.75rem !important;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Labels - Dark and Clear */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stRadio > label {
        color: #1a202c !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Metrics - Modern Card Style */
    [data-testid="stMetricValue"] {
        color: #1e40af !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    div[data-testid="metric-container"] {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    /* Tabs - Clean Professional */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #64748b !important;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f1f5f9;
        color: #3b82f6 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
    }
    
    /* Expander - Modern Card Style */
    .streamlit-expanderHeader {
        background-color: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #1a202c !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #3b82f6 !important;
        background-color: #f8fafc !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Code Blocks - Professional Monospace */
    .stCodeBlock, code {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        border: 2px solid #334155 !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 0.9rem !important;
    }
    
    /* Info/Success/Warning/Error Boxes - High Contrast */
    .stAlert {
        border-radius: 8px !important;
        border-left: 4px solid !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    [data-baseweb="notification"] {
        background-color: white !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stSuccess {
        background-color: #ecfdf5 !important;
        border-left-color: #10b981 !important;
        color: #065f46 !important;
    }
    
    .stInfo {
        background-color: #eff6ff !important;
        border-left-color: #3b82f6 !important;
        color: #1e40af !important;
    }
    
    .stWarning {
        background-color: #fffbeb !important;
        border-left-color: #f59e0b !important;
        color: #92400e !important;
    }
    
    .stError {
        background-color: #fef2f2 !important;
        border-left-color: #ef4444 !important;
        color: #991b1b !important;
    }
    
    /* Progress Bar - Modern Gradient */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
        border-radius: 10px !important;
    }
    
    /* Radio Buttons - Clean Style */
    .stRadio > div {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    
    .stRadio > div > label > div[role="radiogroup"] > label {
        background-color: #f8fafc;
        padding: 0.75rem 1.25rem;
        border-radius: 6px;
        border: 2px solid #cbd5e1;
        margin: 0.25rem;
        transition: all 0.2s ease;
        color: #1a202c !important;
        font-weight: 500;
    }
    
    .stRadio > div > label > div[role="radiogroup"] > label:hover {
        border-color: #3b82f6;
        background-color: #eff6ff;
    }
    
    /* File Uploader - Professional */
    [data-testid="stFileUploader"] {
        background-color: white;
        border: 2px dashed #cbd5e1;
        border-radius: 10px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #3b82f6;
        background-color: #f8fafc;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid #e2e8f0 !important;
        margin: 2rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    /* Caption and Helper Text */
    .caption, small {
        color: #64748b !important;
        font-size: 0.875rem !important;
    }
    
    /* Links */
    a {
        color: #3b82f6 !important;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #2563eb !important;
        text-decoration: underline;
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
# ANGULAR CODE PROCESSING + EXPORTS
# -------------------------

# UUID pattern used in Angular/HTML code for image placeholders
UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
    """
    Finds UUID-only occurrences in common Angular patterns and prefixes them with url_prefix.
    Returns (modified_text, total_replacements)
    """
    # Patterns target common usages: src="UUID", [src]="'UUID'", imageUrl: 'UUID', url('UUID'), plain 'UUID'
    patterns = [
        (re.compile(r'(src\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(\[src\]\s*=\s*["\']\s*)(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(imageUrl\s*:\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(url\(\s*["\'])(%s)(["\']\s*\))' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        # fallback: standalone quoted UUIDs (be careful — this can overmatch in rare cases)
        (re.compile(r'(["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
    ]

    modified = text
    total_replacements = 0
    for pat, repl in patterns:
        modified, n = pat.subn(repl, modified)
        total_replacements += n
    return modified, total_replacements

def create_text_to_pdf(text_content: str) -> BytesIO:
    """
    Convert plain text (or processed code) into a simple PDF stored in-memory (BytesIO).
    Uses a monospace font style for code readability.
    """
    buffer = BytesIO()
    # Basic single-column document with narrow margins
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    # Use Normal as parent and Courier-like font name for monospace appearance
    code_style = ParagraphStyle(
        'Code',
        parent=styles.get('Normal'),
        fontName='Courier',  # fallback to Courier
        fontSize=8,
        leading=10,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=6
    )
    story = []
    # Split into manageable chunks to avoid giant paragraphs
    lines = text_content.splitlines()
    chunk_size = 60
    for i in range(0, len(lines), chunk_size):
        block = lines[i:i+chunk_size]
        # Escape XML-sensitive characters
        safe = [ln.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for ln in block]
        story.append(Paragraph('<br/>'.join(safe), code_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

def detect_uuids_in_text(text: str) -> List[str]:
    """Return unique UUIDs found in the supplied text (order-preserving)."""
    pattern = re.compile(UUID_RE, re.IGNORECASE)
    found = pattern.findall(text)
    # pattern.findall returns list of strings (UUIDs) if pattern has no groups
    # unify and preserve order
    seen = set()
    out = []
    for f in found:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out

# Small utility to safely read uploaded file bytes and decode as utf-8 (fallback)
def decode_bytes_to_text(raw: bytes) -> str:
    try:
        return raw.decode('utf-8')
    except Exception:
        try:
            return raw.decode('latin-1')
        except Exception:
            return raw.decode('utf-8', errors='ignore')

# -------------------------
# GITHUB ZIP DOWNLOAD HELPER
# -------------------------

@st.cache_data(ttl=3600)
def fetch_github_zip(url: str) -> bytes:
    """Fetch zip file from GitHub with caching"""
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.content
    raise RuntimeError(f"Failed to fetch from GitHub: {response.status_code}")

# -------------------------
# STREAMLIT UI + WORKFLOW
# -------------------------

def main():
    # Header / Hero with enhanced styling
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 3rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);'>
        <h1 style='margin-bottom: 0.75rem; color: white !important; -webkit-text-fill-color: white !important; font-size: 3rem !important;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.2rem; color: rgba(255,255,255,0.95) !important; font-weight: 500; margin: 0;'>
            Enterprise-Grade UI Component Extraction & Angular Code Processing
        </p>
        <p style='font-size: 0.95rem; color: rgba(255,255,255,0.8) !important; margin-top: 0.5rem;'>
            Professional Tools for Modern Development Workflows
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ System Information")
        st.markdown("---")

        if 'stats' not in st.session_state:
            st.session_state['stats'] = {'files_processed': 0, 'downloads': 0}

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files Processed", st.session_state['stats']['files_processed'])
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'])

        st.markdown("---")
        
        # Angular 19 Boilerplate Download Section - Updated with GitHub URL
        st.markdown("### 📦 Angular Boilerplate")
        st.markdown("Download the Angular 19 skeleton/boilerplate code to get started quickly.")
        
        github_zip_url = "https://raw.githubusercontent.com/mandarwarghade211009-gif/figma/main/skeleton%20angular%2019.zip"
        
        try:
            angular_zip_bytes = fetch_github_zip(github_zip_url)
            
            st.download_button(
                label="📥 Download Angular 19 Boilerplate",
                data=angular_zip_bytes,
                file_name="angular19_skeleton.zip",
                mime="application/zip",
                on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                use_container_width=True
            )
            st.caption(f"Size: {len(angular_zip_bytes):,} bytes")
            
        except Exception as e:
            st.error(f"❌ Error downloading from GitHub: {str(e)}")
            st.info("💡 Check your internet connection or verify the GitHub URL is accessible.")
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Documentation](https://www.figma.com/developers/api)
        - [Angular Framework](https://angular.io)
        - [Angular Material](https://material.angular.io)
        - [ReportLab PDF](https://www.reportlab.com)
        """)
        st.markdown("---")
        st.markdown("### 🔐 Security & Privacy")
        st.info("🔒 API tokens are used only for fetching and are never stored or logged.")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px;'>
            <p style='color: white !important; font-weight: 600; margin: 0; font-size: 0.9rem;'>
                💡 Built with Streamlit
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Tabs with enhanced styling
    tab1, tab2 = st.tabs(["🎯 Figma Extraction", "⚡ Angular Processor"])

    # --- Figma Extraction Tab ---
    with tab1:
        st.markdown("### 🎯 Figma Component Extraction")
        st.markdown("Extract UI components with comprehensive metadata, styling information, and high-resolution images from your Figma designs.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 Figma File Key", value="", help="Enter the Figma file key from your design file URL", placeholder="e.g., aBc123dEf456...")
        with col2:
            node_ids = st.text_input("🔗 Node IDs", value="", help="Optional: Enter comma-separated node IDs to extract specific components", placeholder="123:456, 789:012 (optional)")

        token = st.text_input("🔑 Figma Personal Access Token", type="password", help="Generate your token in Figma Account Settings → Personal Access Tokens", placeholder="Enter your Figma API token")

        st.markdown("")
        
        if st.button("🚀 Extract UI Components", type="primary", use_container_width=True):
            if not token or not file_key:
                st.error("⚠️ Please provide both a Figma file key and a personal access token to proceed.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.info("📡 Connecting to Figma API and fetching design nodes...")
                    progress.progress(5)
                    nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                    status.info("🖼️ Analyzing images and collecting node metadata...")
                    progress.progress(25)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                    status.info("🔗 Resolving image URLs and assets from Figma servers...")
                    progress.progress(50)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                    status.info("🎨 Building comprehensive icon map and merging data...")
                    progress.progress(70)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                    merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                    status.info("📦 Extracting and organizing component structure...")
                    progress.progress(85)
                    final_output = extract_ui_components(merged_payload)

                    status.info("✨ Finalizing extraction and sanitizing URLs for portability...")
                    progress.progress(95)
                    # remove absolute prefix so output is portable; use default figma prefix commonly returned
                    sanitized = remove_url_prefix_from_json(final_output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                    st.session_state['metadata_json'] = sanitized
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    status.empty()
                    st.success("✅ Extraction completed successfully! Your UI components are ready for download.")

                    # Enhanced metrics display
                    st.markdown("### 📊 Extraction Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", sanitized['metadata']['totalComponents'])
                    with col2:
                        st.metric("Text Elements", len(sanitized.get('textElements', [])))
                    with col3:
                        st.metric("Buttons", len(sanitized.get('buttons', [])))
                    with col4:
                        st.metric("Containers", len(sanitized.get('containers', [])))

                    st.markdown("---")
                    
                    # Component breakdown
                    st.markdown("### 📋 Component Breakdown")
                    
                    categories = {
                        'Text Elements': len(sanitized.get('textElements', [])),
                        'Buttons': len(sanitized.get('buttons', [])),
                        'Inputs': len(sanitized.get('inputs', [])),
                        'Containers': len(sanitized.get('containers', [])),
                        'Images': len(sanitized.get('images', [])),
                        'Navigation': len(sanitized.get('navigation', [])),
                        'Vectors': len(sanitized.get('vectors', [])),
                        'Other': len(sanitized.get('other', []))
                    }
                    
                    for category, count in categories.items():
                        if count > 0:
                            st.write(f"**{category}:** {count}")
                    
                    st.markdown("---")
                    
                    # Download options
                    st.markdown("### 💾 Download Options")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        json_str = json.dumps(sanitized, indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"figma_ui_components_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    
                    with col2:
                        pdf_buffer = create_text_to_pdf(json_str)
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_buffer,
                            file_name=f"figma_ui_components_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    # Preview
                    with st.expander("🔍 Preview JSON Data", expanded=False):
                        st.json(sanitized)

                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.info("💡 Please verify your Figma file key, node IDs, and API token are correct.")

    # --- Angular Processor Tab ---
    with tab2:
        st.markdown("### ⚡ Angular Code Processor")
        st.markdown("Process Angular files by adding URL prefixes to image references (UUIDs) for proper asset loading.")
        st.markdown("---")
        
        url_prefix = st.text_input(
            "🔗 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="Enter the base URL to prepend to all UUID image references",
            placeholder="https://your-cdn.com/images/"
        )
        
        st.markdown("### 📤 Upload Angular Files")
        uploaded_files = st.file_uploader(
            "Choose Angular files (.ts, .html, .css, .scss)",
            type=['ts', 'html', 'css', 'scss'],
            accept_multiple_files=True,
            help="Upload one or more Angular component files to process"
        )
        
        if uploaded_files:
            st.markdown(f"### 📁 Uploaded Files: {len(uploaded_files)}")
            
            if st.button("🔄 Process Files", type="primary", use_container_width=True):
                processed_files = []
                total_replacements = 0
                
                progress = st.progress(0)
                status = st.empty()
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    status.info(f"Processing {uploaded_file.name}...")
                    progress.progress((idx + 1) / len(uploaded_files))
                    
                    try:
                        file_content = decode_bytes_to_text(uploaded_file.read())
                        modified_content, replacements = add_url_prefix_to_angular_code(file_content, url_prefix)
                        total_replacements += replacements
                        
                        processed_files.append({
                            'name': uploaded_file.name,
                            'original': file_content,
                            'modified': modified_content,
                            'replacements': replacements
                        })
                    except Exception as e:
                        st.warning(f"⚠️ Error processing {uploaded_file.name}: {str(e)}")
                
                progress.progress(1.0)
                status.empty()
                
                st.success(f"✅ Processing complete! Made {total_replacements} replacements across {len(processed_files)} files.")
                
                # Summary
                st.markdown("### 📊 Processing Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Files Processed", len(processed_files))
                with col2:
                    st.metric("Total Replacements", total_replacements)
                with col3:
                    avg_replacements = total_replacements / len(processed_files) if processed_files else 0
                    st.metric("Avg per File", f"{avg_replacements:.1f}")
                
                st.markdown("---")
                
                # Individual file results
                st.markdown("### 📋 File Details")
                
                for pf in processed_files:
                    with st.expander(f"📄 {pf['name']} - {pf['replacements']} replacements"):
                        
                        tab_orig, tab_mod, tab_diff = st.tabs(["Original", "Modified", "Changes"])
                        
                        with tab_orig:
                            st.code(pf['original'], language='typescript' if pf['name'].endswith('.ts') else 'html')
                        
                        with tab_mod:
                            st.code(pf['modified'], language='typescript' if pf['name'].endswith('.ts') else 'html')
                        
                        with tab_diff:
                            st.info(f"Made {pf['replacements']} UUID prefix replacements")
                            
                            # Show UUIDs found
                            uuids_found = detect_uuids_in_text(pf['original'])
                            if uuids_found:
                                st.markdown("**UUIDs Found:**")
                                for uuid in uuids_found:
                                    st.code(f"{uuid} → {url_prefix}{uuid}")
                        
                        # Download individual file
                        st.download_button(
                            label=f"📥 Download {pf['name']}",
                            data=pf['modified'],
                            file_name=f"processed_{pf['name']}",
                            mime="text/plain",
                            key=f"download_{pf['name']}",
                            use_container_width=True
                        )
                
                st.markdown("---")
                
                # Download all as PDF
                st.markdown("### 💾 Bulk Download")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Combine all modified files
                    combined_text = "\n\n" + "="*80 + "\n\n".join([
                        f"FILE: {pf['name']}\n{'='*80}\n\n{pf['modified']}"
                        for pf in processed_files
                    ])
                    
                    st.download_button(
                        label="📥 Download All (TXT)",
                        data=combined_text,
                        file_name=f"angular_processed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    pdf_buffer = create_text_to_pdf(combined_text)
                    st.download_button(
                        label="📥 Download All (PDF)",
                        data=pdf_buffer,
                        file_name=f"angular_processed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        else:
            st.info("👆 Upload Angular files above to begin processing")
            
            st.markdown("---")
            st.markdown("### 💡 How It Works")
            st.markdown("""
            This tool automatically:
            1. Detects UUID patterns in your Angular code (e.g., `abc123...`)
            2. Prepends your specified URL prefix to make them valid URLs
            3. Works with common patterns: `src="UUID"`, `[src]="'UUID'"`, `imageUrl: 'UUID'`, etc.
            4. Preserves all other code intact
            
            **Supported file types:** TypeScript (.ts), HTML, CSS, SCSS
            """)

if __name__ == "__main__":
    main()
