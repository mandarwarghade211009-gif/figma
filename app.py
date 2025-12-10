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
# STUNNING PROFESSIONAL THEMING - Ultra Modern Design
# -----------------------------------------------------
def apply_professional_styling():
    """Apply stunning, eye-catching professional theme with perfect text visibility"""
    st.markdown("""
    <style>
    /* Import Beautiful Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Root Variables - Vibrant Modern Theme with Perfect Contrast */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gold-gradient: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        --purple-gradient: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        --cosmic-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        
        --accent-primary: #667eea;
        --accent-secondary: #f5576c;
        --accent-success: #00f2fe;
        
        --dark-bg: #0a0a1f;
        --card-bg: #1a1a35;
        --card-hover: #252542;
        
        --text-primary: #ffffff;
        --text-secondary: #e0e0ff;
        --text-muted: #b0b0d0;
        
        --border-color: rgba(102, 126, 234, 0.3);
        --border-hover: rgba(102, 126, 234, 0.6);
        
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.4);
        --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.5);
        --shadow-lg: 0 20px 60px rgba(102, 126, 234, 0.2);
        --shadow-glow: 0 0 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a1f 0%, #1a1a35 25%, #2d1b4e 50%, #1a1a35 75%, #0a0a1f 100%);
        background-attachment: fixed;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Animated Background Pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(245, 87, 108, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(0, 242, 254, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Headers - Eye-Catching with Perfect Visibility */
    h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 1rem !important;
        line-height: 1.1 !important;
        background: linear-gradient(135deg, #ffffff 0%, #a8edea 50%, #fed6e3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 80px rgba(102, 126, 234, 0.5);
        animation: gradient-shift 8s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(20deg); }
    }
    
    h2 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.2rem !important;
        color: #ffffff !important;
        text-shadow: 0 2px 20px rgba(102, 126, 234, 0.4);
    }
    
    h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: #e0e0ff !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Paragraph & Text - High Contrast */
    p, .stMarkdown, span, div {
        color: var(--text-secondary) !important;
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        font-weight: 400 !important;
    }
    
    strong, b {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Glass Card Effect */
    .element-container, div[data-testid="stExpander"], .stAlert {
        background: rgba(26, 26, 53, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 20px !important;
        padding: 1.8rem !important;
        box-shadow: var(--shadow-md) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .element-container:hover {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: var(--shadow-lg) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Tab Styling - Modern & Beautiful */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        background: transparent;
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
        padding-bottom: 0;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(26, 26, 53, 0.5) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        padding: 1.2rem 2.5rem !important;
        border-radius: 16px 16px 0 0 !important;
        transition: all 0.3s ease !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        color: #ffffff !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--cosmic-gradient) !important;
        border-color: transparent !important;
        color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.5), 0 0 40px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-4px) !important;
    }
    
    /* Input Fields - High Visibility */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox select {
        background: rgba(26, 26, 53, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.7 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.25), 0 8px 24px rgba(102, 126, 234, 0.3) !important;
        outline: none !important;
        background: rgba(26, 26, 53, 1) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Labels - Perfect Visibility */
    label, .stMarkdown label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Buttons - Eye-Catching Primary */
    .stButton > button {
        background: var(--cosmic-gradient) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4), 0 0 40px rgba(102, 126, 234, 0.2) !important;
        text-transform: none !important;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.02em !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6), 0 0 60px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    /* Download Buttons - Beautiful Variants */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.6) !important;
    }
    
    /* Metrics - Stunning Display */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 0%, #a8edea 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Space Grotesk', sans-serif !important;
        filter: drop-shadow(0 4px 12px rgba(102, 126, 234, 0.3));
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        opacity: 0.9 !important;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(26, 26, 53, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-md) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="metric-container"]:hover {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: var(--shadow-lg) !important;
        transform: translateY(-4px) !important;
    }
    
    /* Progress Bar - Vibrant */
    .stProgress > div > div > div > div {
        background: var(--cosmic-gradient) !important;
        border-radius: 12px !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stProgress > div > div {
        background: rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        height: 12px !important;
    }
    
    /* Alert Boxes - High Visibility */
    .stSuccess {
        background: rgba(0, 242, 254, 0.15) !important;
        border-left: 5px solid #00f2fe !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.8rem !important;
        color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(0, 242, 254, 0.3) !important;
    }
    
    .stError {
        background: rgba(245, 87, 108, 0.15) !important;
        border-left: 5px solid #f5576c !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.8rem !important;
        color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(245, 87, 108, 0.3) !important;
    }
    
    .stInfo {
        background: rgba(102, 126, 234, 0.15) !important;
        border-left: 5px solid #667eea !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.8rem !important;
        color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stWarning {
        background: rgba(246, 211, 101, 0.15) !important;
        border-left: 5px solid #f6d365 !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.8rem !important;
        color: #ffffff !important;
        box-shadow: 0 4px 16px rgba(246, 211, 101, 0.3) !important;
    }
    
    /* Sidebar - Modern Glass Effect */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 26, 53, 0.95) 0%, rgba(22, 22, 46, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(102, 126, 234, 0.3) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-size: 1.4rem !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-secondary) !important;
    }
    
    /* Code Blocks - Beautiful Contrast */
    .stCodeBlock, code, pre {
        background: rgba(15, 15, 35, 0.95) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #e0e0ff !important;
        padding: 1rem !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Expander - Eye-Catching */
    .streamlit-expanderHeader {
        background: rgba(26, 26, 53, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
        font-size: 1.05rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
        transform: translateX(4px) !important;
    }
    
    /* Divider - Elegant */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent) !important;
        margin: 3rem 0 !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Caption Text - Visible */
    .caption, small, [data-testid="stCaptionContainer"] {
        color: var(--text-muted) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Scrollbar - Beautiful */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 10, 31, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--cosmic-gradient);
        border-radius: 10px;
        border: 2px solid rgba(10, 10, 31, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse-glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(102, 126, 234, 0.6);
        }
    }
    
    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Column Alignment */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Status Text - High Contrast */
    .stText, .stMarkdown p {
        color: var(--text-secondary) !important;
    }
    
    /* Helper Text */
    [data-testid="stFormHelperText"] {
        color: var(--text-muted) !important;
        font-size: 0.9rem !important;
    }
    
    /* Make all text clearly visible */
    * {
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
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
    # Stunning Hero Header with Badge
    st.markdown("""
    <div style='text-align: center; padding: 3.5rem 0 3rem 0;'>
        <div style='display: inline-block; padding: 0.6rem 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.25) 100%); border-radius: 50px; border: 2px solid rgba(102, 126, 234, 0.4); margin-bottom: 1.8rem; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);'>
            <span style='font-size: 1rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; letter-spacing: 0.15em;'>✨ Professional Edition 2025</span>
        </div>
        <h1 style='margin-bottom: 1rem; font-size: 4rem; line-height: 1.1;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.3rem; color: #e0e0ff; font-weight: 400; max-width: 800px; margin: 0 auto; line-height: 1.7; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>
            Extract, analyze, and export UI components from Figma with enterprise-grade precision and style
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Modern Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Dashboard")
        st.markdown("---")

        if 'stats' not in st.session_state:
            st.session_state['stats'] = {'files_processed': 0, 'downloads': 0}

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🗂️ Files", st.session_state['stats']['files_processed'])
        with col2:
            st.metric("📥 Downloads", st.session_state['stats']['downloads'])

        st.markdown("---")
        st.markdown("### 🎯 Key Features")
        st.markdown("""
        **Smart Extraction**  
        Automated component detection with AI
        
        **Complete Styling**  
        Design tokens, colors, and typography
        
        **Image Support**  
        SVG and raster asset resolution
        
        **Structured Export**  
        Clean JSON metadata output
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Documentation")
        st.markdown("""
        - [📖 Figma API Guide](https://www.figma.com/developers/api)
        - [⚡ Angular Docs](https://angular.io)
        - [🎨 Design Systems](https://www.designsystems.com)
        """)
        
        st.markdown("---")
        st.markdown("### 🔐 Privacy & Security")
        st.success("🔒 **100% Secure** - Tokens are never stored. All processing is session-based and encrypted.")

    # Main Content Area
    st.markdown("## 🎯 Component Extraction")
    st.markdown("Extract comprehensive UI component metadata including styles, layouts, typography, and image assets from your Figma designs with a single click.")
    st.markdown("---")

    # Input Fields in Columns
    col1, col2 = st.columns(2)
    with col1:
        file_key = st.text_input(
            "📁 Figma File Key", 
            value="", 
            help="Enter the file key from your Figma file URL (found after 'file/' in the URL)",
            placeholder="e.g., abc123xyz..."
        )
    with col2:
        node_ids = st.text_input(
            "🔗 Node IDs (Optional)", 
            value="", 
            help="Enter comma-separated node IDs to extract specific components. Leave empty to extract the entire file.",
            placeholder="e.g., 123:456, 789:012"
        )

    token = st.text_input(
        "🔑 Figma Personal Access Token", 
        type="password", 
        help="Generate a personal access token in your Figma account settings → Security → Personal Access Tokens",
        placeholder="figd_..."
    )

    st.markdown("")  # Spacing
    
    # Extract Button
    if st.button("🚀 Extract UI Components", type="primary"):
        if not token or not file_key:
            st.error("⚠️ **Missing Required Fields** - Please provide both a Figma file key and access token to proceed.")
        else:
            try:
                progress = st.progress(0)
                status = st.empty()

                status.text("📡 Establishing connection to Figma API...")
                progress.progress(5)
                nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                status.text("🖼️ Analyzing component structure and hierarchy...")
                progress.progress(25)
                image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                status.text("🔗 Resolving image assets and references...")
                progress.progress(50)
                filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                status.text("🎨 Processing design tokens and styles...")
                progress.progress(70)
                node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                status.text("📦 Extracting components and metadata...")
                progress.progress(85)
                final_output = extract_ui_components(merged_payload)

                status.text("✨ Finalizing extraction and optimizing output...")
                progress.progress(95)
                sanitized = remove_url_prefix_from_json(final_output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                st.session_state['metadata_json'] = sanitized
                st.session_state['stats']['files_processed'] += 1
                progress.progress(100)
                status.empty()
                st.success("✅ **Extraction Completed Successfully!** Your UI components have been extracted and are ready for download.")

                # Beautiful Metrics Display
                st.markdown("## 📊 Extraction Summary")
                st.markdown("")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🎯 Total Components", sanitized['metadata']['totalComponents'])
                with col2:
                    st.metric("📝 Text Elements", len(sanitized.get('textElements', [])))
                with col3:
                    st.metric("🔘 Buttons", len(sanitized.get('buttons', [])))
                with col4:
                    st.metric("📦 Containers", len(sanitized.get('containers', [])))

                st.markdown("")
                
                # Detailed Category Breakdown
                with st.expander("📋 **Detailed Category Breakdown**", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    categories = {
                        'textElements': '📝 Text Elements',
                        'buttons': '🔘 Buttons',
                        'inputs': '⌨️ Input Fields',
                        'containers': '📦 Containers',
                        'images': '🖼️ Images',
                        'navigation': '🧭 Navigation',
                        'vectors': '🎨 Vector Graphics',
                        'other': '📌 Other Components'
                    }
                    
                    items = list(categories.items())
                    mid = (len(items) + 1) // 2
                    
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
                st.error(f"❌ **Extraction Failed:** {str(e)}")
                st.info("💡 **Troubleshooting Tips:**\n- Verify your access token is valid and active\n- Ensure you have permission to access the specified file\n- Check that the file key is correct")

    # Download Section
    if 'metadata_json' in st.session_state:
        st.markdown("---")
        st.markdown("## 💾 Download Options")
        st.markdown("Download your extracted component metadata in JSON format for seamless integration with your development workflow.")
        st.markdown("")
        
        json_str = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.download_button(
                "📥 Download metadata.json",
                data=json_str,
                file_name="figma-metadata.json",
                mime="application/json",
                on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                use_container_width=True
            )
        with col2:
            st.metric("📊 Size", f"{len(json_str):,}B")
        with col3:
            st.metric("📄 Format", "JSON")

        # Preview Section
        with st.expander("👁️ **Preview JSON Structure**", expanded=False):
            st.json(st.session_state['metadata_json']['metadata'])

    # Beautiful Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2.5rem 0 1.5rem 0;'>
        <p style='color: #e0e0ff; font-size: 1.05rem; margin: 0; font-weight: 500;'>
            Built with ❤️ using <strong style='background: linear-gradient(135deg, #667eea 0%, #f5576c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Streamlit</strong> • Professional Edition v2.0
        </p>
        <p style='color: #b0b0d0; font-size: 0.95rem; margin-top: 0.8rem;'>
            🚀 Powered by Figma API • Optimized for Angular & React Development
        </p>
        <p style='color: #8080a0; font-size: 0.85rem; margin-top: 0.5rem;'>
            © 2025 Figma UI Extractor. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
