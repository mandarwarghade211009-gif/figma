#!/usr/bin/env python3
"""
Professional Figma UI Extractor - Light Theme Edition
Enterprise-grade design system with caching and full responsiveness
Optimized for Laptop, Mac, Tablet, and Mobile devices
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
# PROFESSIONAL LIGHT THEME - Responsive Design
# -----------------------------------------------------
def apply_professional_styling():
    """Apply modern, professional light theme with full responsive support"""
    st.markdown("""
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Reset and Viewport Control */
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
    
    /* Root Variables - Professional Light Theme */
    :root {
        /* Primary Colors - Professional Blue/Purple */
        --primary-color: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        
        /* Secondary Colors */
        --secondary-color: #10b981;
        --secondary-light: #34d399;
        --accent-color: #f59e0b;
        --accent-pink: #ec4899;
        
        /* Neutral Colors - Light Theme */
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --bg-card: #ffffff;
        --bg-hover: #f1f5f9;
        
        /* Text Colors */
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-tertiary: #64748b;
        --text-muted: #94a3b8;
        
        /* Border Colors */
        --border-light: #e2e8f0;
        --border-medium: #cbd5e1;
        --border-dark: #94a3b8;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-primary: 0 4px 12px rgba(99, 102, 241, 0.2);
        
        /* Status Colors */
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --info: #3b82f6;
    }
    
    /* Main App Container - Viewport Fit */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--text-primary);
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
    }
    
    /* Main Content Area - Scrollable Container */
    .main .block-container {
        max-width: 100%;
        padding: 1.5rem 2rem;
        height: calc(100vh - 3rem);
        overflow-y: auto;
        overflow-x: hidden;
    }
    
    /* Custom Scrollbar - Light Theme */
    .main .block-container::-webkit-scrollbar {
        width: 10px;
    }
    
    .main .block-container::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 10px;
    }
    
    .main .block-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        border-radius: 10px;
        border: 2px solid var(--bg-secondary);
    }
    
    .main .block-container::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Professional Header Styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text-primary);
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        line-height: 1.2;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.75rem !important;
        color: var(--text-primary);
    }
    
    h3 {
        font-size: 1.25rem !important;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    /* Paragraph & Text */
    p, .stMarkdown {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
        margin: 0.5rem 0;
    }
    
    /* Professional Cards & Containers */
    .stTabs, .element-container, div[data-testid="stExpander"] {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        margin: 0.75rem 0;
        transition: all 0.3s ease;
    }
    
    .element-container:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--border-medium);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--bg-secondary);
        border-radius: 12px 12px 0 0;
        padding: 0.5rem;
        border-bottom: 2px solid var(--border-light);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-hover);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        box-shadow: var(--shadow-primary);
    }
    
    /* Professional Input Fields */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: var(--bg-primary) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: var(--shadow-sm);
    }
    
    .stTextInput > div > div > input:hover,
    .stTextArea textarea:hover {
        border-color: var(--border-medium) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1), var(--shadow-md) !important;
        outline: none !important;
        background: var(--bg-primary) !important;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-primary) !important;
        text-transform: none !important;
        font-family: 'Inter', sans-serif !important;
        width: 100%;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
        background: linear-gradient(135deg, var(--primary-light), #a78bfa) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--secondary-color), var(--secondary-light)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Metrics - Professional Cards */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--primary-light);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
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
        background: var(--bg-tertiary) !important;
        border-radius: 10px;
        height: 8px !important;
        border: 1px solid var(--border-light);
    }
    
    /* Alert Boxes */
    .stAlert {
        background: var(--bg-card) !important;
        border-left: 4px solid var(--primary-color) !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
        color: var(--text-primary) !important;
        margin: 0.75rem 0 !important;
        box-shadow: var(--shadow-sm);
    }
    
    .stSuccess {
        border-left-color: var(--success) !important;
        background: #f0fdf4 !important;
    }
    
    .stError {
        border-left-color: var(--error) !important;
        background: #fef2f2 !important;
    }
    
    .stInfo {
        border-left-color: var(--info) !important;
        background: #eff6ff !important;
    }
    
    .stWarning {
        border-left-color: var(--warning) !important;
        background: #fffbeb !important;
    }
    
    /* Sidebar - Professional Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        border-right: 1px solid var(--border-light);
        height: 100vh;
        overflow-y: auto;
        overflow-x: hidden;
        box-shadow: var(--shadow-lg);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-secondary);
        font-size: 0.95rem;
    }
    
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary);
        font-size: 1.1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar Scrollbar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 8px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    /* Code Blocks */
    .stCodeBlock, code {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--text-primary) !important;
        font-size: 0.875rem !important;
        padding: 0.5rem !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-hover) !important;
        border-color: var(--primary-color) !important;
        box-shadow: var(--shadow-sm);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-medium), transparent);
        margin: 1.5rem 0;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: var(--bg-secondary);
        border: 2px dashed var(--border-medium);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-color);
        background: var(--bg-hover);
    }
    
    /* Labels */
    label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Caption */
    .caption, small {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
    }
    
    /* Column Spacing */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Badge/Tag Styling */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-sm);
    }
    
    /* Professional Card Hover Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-light);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        box-shadow: var(--shadow-xl);
        transform: translateY(-2px);
    }
    
    /* JSON Display */
    .stJson {
        max-height: 350px;
        overflow-y: auto;
        font-size: 0.875rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Remove Extra Spacing */
    .element-container {
        margin: 0.5rem 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.75rem;
    }
    
    /* ============================================ */
    /* RESPONSIVE BREAKPOINTS */
    /* ============================================ */
    
    /* Mobile Devices (320px - 767px) */
    @media only screen and (max-width: 767px) {
        .main .block-container {
            padding: 1rem;
            height: calc(100vh - 2rem);
        }
        
        h1 {
            font-size: 1.75rem !important;
        }
        
        h2 {
            font-size: 1.35rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        [data-testid="column"] {
            padding: 0 0.25rem;
            min-width: 100% !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
        }
        
        .stButton > button {
            padding: 0.65rem 1.25rem !important;
            font-size: 0.9rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.75rem;
            font-size: 0.85rem;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    
    /* Tablets (768px - 1023px) */
    @media only screen and (min-width: 768px) and (max-width: 1023px) {
        .main .block-container {
            padding: 1.25rem 1.5rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        [data-testid="column"] {
            padding: 0 0.4rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
    }
    
    /* Laptops and Small Desktops (1024px - 1439px) */
    @media only screen and (min-width: 1024px) and (max-width: 1439px) {
        .main .block-container {
            padding: 1.5rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: 2.25rem !important;
        }
    }
    
    /* Large Desktops and Mac (1440px+) */
    @media only screen and (min-width: 1440px) {
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: 2.75rem !important;
        }
        
        h2 {
            font-size: 2rem !important;
        }
    }
    
    /* High Resolution Displays (Retina, 4K) */
    @media only screen and (min-width: 1920px) {
        .main .block-container {
            max-width: 1600px;
        }
    }
    
    /* Landscape Orientation for Mobile/Tablet */
    @media only screen and (max-height: 500px) and (orientation: landscape) {
        .main .block-container {
            padding: 0.75rem 1rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        [data-testid="stMetric"] {
            padding: 0.5rem;
        }
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
    """Build request headers with authentication token"""
    return {"Accept": "application/json", "X-Figma-Token": token}

def chunked(lst: List[str], n: int):
    """Split list into chunks of size n"""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def to_rgba(color: Dict[str, Any]) -> str:
    """Convert Figma color object to RGBA string"""
    try:
        r = int(float(color.get("r", 0)) * 255)
        g = int(float(color.get("g", 0)) * 255)
        b = int(float(color.get("b", 0)) * 255)
        a = float(color.get("a", color.get("opacity", 1)))
        return f"rgba({r},{g},{b},{a})"
    except:
        return "rgba(0,0,0,1)"

def is_nonempty_list(v: Any) -> bool:
    """Check if value is a non-empty list"""
    return isinstance(v, list) and len(v) > 0

def is_visible(node: Dict[str, Any]) -> bool:
    """Check if node is visible"""
    v = node.get("visible")
    return True if v is None else bool(v)

def filter_invisible_nodes(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Recursively filter out invisible nodes"""
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
# CACHED FIGMA API FUNCTIONS
# -------------------------

@st.cache_data(show_spinner="Fetching Figma data...", ttl=3600)
def fetch_figma_nodes(file_key: str, node_ids: str, token: str, timeout: int = 60) -> Dict[str, Any]:
    """
    Fetch node(s) from Figma file with caching.
    Cache expires after 1 hour (3600 seconds).
    
    Args:
        file_key: Figma file identifier
        node_ids: Comma-separated node IDs (empty for entire file)
        token: Figma API access token
        timeout: Request timeout in seconds
    
    Returns:
        Raw JSON payload from Figma API
    """
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    params = {"ids": node_ids} if node_ids else {}
    
    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    
    if not r.ok:
        raise RuntimeError(f"Figma API error {r.status_code}: {r.text}")
    
    data = r.json()
    
    # Filter invisible nodes
    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_invisible_nodes(doc)
    else:
        if isinstance(data.get("document"), dict):
            data["document"] = filter_invisible_nodes(data["document"])
    
    return data

@st.cache_data(show_spinner="Processing component tree...", ttl=3600)
def walk_nodes_collect_images_and_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, str]]]:
    """
    Walk node tree and collect image references and IDs (cached).
    
    Returns:
        - Set of image refs (imageHash/imageRef)
        - List of node IDs
        - Node metadata dictionary
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
        
        # Process children
        for c in n.get("children", []) or []:
            visit(c)

    # Process nodes payload
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])

    # De-duplicate node IDs
    seen = set()
    unique_node_ids = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_node_ids.append(nid)

    return image_refs, unique_node_ids, node_meta

@st.cache_data(show_spinner="Resolving image URLs...", ttl=3600)
def resolve_image_urls(
    file_key: str, 
    image_refs: Set[str], 
    node_ids: List[str], 
    token: str, 
    timeout: int = 60
) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    """
    Resolve image URLs from Figma API (cached).
    
    Returns:
        - fills_map: imageRef -> URL mapping
        - renders_map: nodeId -> rendered image URL mapping
    """
    headers = build_headers(token)
    fills_map: Dict[str, str] = {}
    
    # Fetch fill images
    try:
        fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
        params = {}
        if image_refs:
            params["ids"] = ",".join(list(image_refs))
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
    """
    Build node ID to image URL mapping.
    Prefers fills_map URLs over renders_map.
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
    """
    Deep copy payload and inject image_url into nodes.
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
    """Extract absolute bounding box from node"""
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
    """Extract layout-related properties"""
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
    """Extract visual styling properties (fills, strokes, effects)"""
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
    """Classify component into category bucket"""
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
    
    # Handle image URLs
    if root.get('image_url'):
        comp['imageUrl'] = root.get('image_url')
    if root.get('imageUrl'):
        comp['imageUrl'] = root.get('imageUrl')
    
    text = extract_text(root)
    if text:
        comp['text'] = text
    
    if should_include(root):
        out.append(comp)
    
    # Process children
    for child in root.get('children', []) or []:
        if isinstance(child, dict):
            extract_components(child, path, out)
    
    return out

def find_document_roots(nodes_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find all document root nodes in payload"""
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
    """Organize components into categorized structure"""
    organized = {
        'metadata': {
            'totalComponents': len(components), 
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
    
    for c in components:
        organized.setdefault(classify_bucket(c), []).append(c)
    
    return organized

@st.cache_data(show_spinner="Extracting UI components...", ttl=3600)
def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and organize all UI components from merged payload (cached).
    """
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
    Remove URL prefix from imageUrl/image_url values.
    Returns deep-copied processed payload.
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
    """Main application entry point"""
    
    # Professional Hero Header
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
        <div style='display: inline-block; padding: 0.4rem 1.2rem; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); border-radius: 50px; border: 1px solid rgba(99, 102, 241, 0.3); margin-bottom: 1rem;'>
            <span style='font-size: 0.8rem; font-weight: 600; color: #6366f1; text-transform: uppercase; letter-spacing: 0.1em;'>✨ Enterprise Edition</span>
        </div>
        <h1 style='margin-bottom: 0.6rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #64748b; font-weight: 400; max-width: 700px; margin: 0 auto; line-height: 1.6;'>
            Extract, analyze, and export UI components from Figma with enterprise-grade precision
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Professional Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Dashboard")
        st.markdown("---")

        # Initialize session state
        if 'stats' not in st.session_state:
            st.session_state['stats'] = {
                'files_processed': 0, 
                'downloads': 0,
                'cache_hits': 0
            }

        # Stats Display
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files", st.session_state['stats']['files_processed'], delta=None)
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'], delta=None)

        st.markdown("---")
        st.markdown("### 🎯 Features")
        st.markdown("""
        - ⚡ **Smart Caching** - Lightning-fast re-extraction
        - 🎨 **Style Parsing** - Complete design tokens
        - 🖼️ **Image Resolution** - SVG & raster support
        - 📦 **JSON Export** - Structured metadata
        - 📱 **Fully Responsive** - Works on all devices
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Docs](https://www.figma.com/developers/api)
        - [Angular Material](https://material.angular.io)
        - [Design Tokens](https://designtokens.org)
        """)
        
        st.markdown("---")
        st.markdown("### 🔐 Security & Performance")
        st.info("🔒 Tokens are never stored\n⚡ Smart caching enabled\n🌐 Session-based processing")
        
        # Cache management
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared successfully!")

    # Main Content
    st.markdown("### 🎯 Component Extraction")
    st.markdown("Extract UI components with complete metadata, styling information, and image assets from your Figma designs.")
    
    st.markdown("")
    
    # Input Fields
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

    st.markdown("")
    
    # Extract Button
    if st.button("🚀 Extract UI Components", type="primary", use_container_width=True):
        if not token or not file_key:
            st.error("⚠️ Please provide both a file key and a Figma access token to proceed.")
        else:
            try:
                progress = st.progress(0)
                status = st.empty()

                # Step 1: Fetch nodes
                status.text("📡 Connecting to Figma API...")
                progress.progress(5)
                nodes_payload = fetch_figma_nodes(
                    file_key=file_key, 
                    node_ids=node_ids, 
                    token=token
                )

                # Step 2: Analyze structure
                status.text("🖼️ Analyzing component structure...")
                progress.progress(25)
                image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                # Step 3: Resolve images
                status.text("🔗 Resolving image assets...")
                progress.progress(50)
                filtered_fills, renders_map = resolve_image_urls(
                    file_key, 
                    image_refs, 
                    node_id_list, 
                    token
                )

                # Step 4: Process tokens
                status.text("🎨 Processing design tokens...")
                progress.progress(70)
                node_to_url = build_icon_map(
                    nodes_payload, 
                    filtered_fills, 
                    renders_map, 
                    node_meta
                )
                merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                # Step 5: Extract components
                status.text("📦 Extracting components...")
                progress.progress(85)
                final_output = extract_ui_components(merged_payload)

                # Step 6: Finalize
                status.text("✨ Finalizing extraction...")
                progress.progress(95)
                sanitized = remove_url_prefix_from_json(
                    final_output, 
                    "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/"
                )
                
                st.session_state['metadata_json'] = sanitized
                st.session_state['stats']['files_processed'] += 1
                
                progress.progress(100)
                status.empty()
                
                st.success("✅ Extraction completed successfully!")
                st.balloons()

                # Metrics Display
                st.markdown("### 📊 Extraction Summary")
                st.markdown("")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        "Total Components", 
                        sanitized['metadata']['totalComponents'],
                        delta=None
                    )
                with col2:
                    st.metric(
                        "Text Elements", 
                        len(sanitized.get('textElements', [])),
                        delta=None
                    )
                with col3:
                    st.metric(
                        "Buttons", 
                        len(sanitized.get('buttons', [])),
                        delta=None
                    )
                with col4:
                    st.metric(
                        "Containers", 
                        len(sanitized.get('containers', [])),
                        delta=None
                    )

                st.markdown("")
                
                # Detailed Breakdown
                with st.expander("📋 Detailed Category Breakdown", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    categories = {
                        'textElements': '📝 Text Elements',
                        'buttons': '🔘 Buttons',
                        'inputs': '📥 Input Fields',
                        'containers': '📦 Containers',
                        'images': '🖼️ Images',
                        'navigation': '🧭 Navigation',
                        'vectors': '✏️ Vector Graphics',
                        'other': '🔧 Other Components'
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
        st.markdown("Download the extracted component metadata in JSON format for use in your development workflow.")
        st.markdown("")
        
        json_str = json.dumps(
            st.session_state['metadata_json'], 
            indent=2, 
            ensure_ascii=False
        )

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.download_button(
                "📥 Download metadata.json",
                data=json_str,
                file_name="figma_metadata.json",
                mime="application/json",
                on_click=lambda: st.session_state['stats'].update({
                    'downloads': st.session_state['stats']['downloads'] + 1
                }),
                use_container_width=True
            )
        with col2:
            file_size = len(json_str.encode('utf-8'))
            if file_size < 1024:
                size_str = f"{file_size}B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f}KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f}MB"
            st.metric("File Size", size_str)
        with col3:
            st.metric("Format", "JSON")

        # Preview Section
        with st.expander("👁️ Preview JSON Structure"):
            st.json(st.session_state['metadata_json']['metadata'])
        
        # Component Details
        with st.expander("🔍 Component Details"):
            metadata = st.session_state['metadata_json']
            
            tab1, tab2, tab3, tab4 = st.tabs(["📝 Text", "🔘 Buttons", "📦 Containers", "📊 All Categories"])
            
            with tab1:
                if metadata.get('textElements'):
                    st.json(metadata['textElements'][:3])  # Show first 3
                    st.caption(f"Showing 3 of {len(metadata['textElements'])} text elements")
                else:
                    st.info("No text elements found")
            
            with tab2:
                if metadata.get('buttons'):
                    st.json(metadata['buttons'][:3])
                    st.caption(f"Showing 3 of {len(metadata['buttons'])} buttons")
                else:
                    st.info("No buttons found")
            
            with tab3:
                if metadata.get('containers'):
                    st.json(metadata['containers'][:3])
                    st.caption(f"Showing 3 of {len(metadata['containers'])} containers")
                else:
                    st.info("No containers found")
            
            with tab4:
                category_summary = {
                    cat: len(metadata.get(cat, [])) 
                    for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']
                }
                st.json(category_summary)

    # Professional Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
        <p style='color: #64748b; font-size: 0.95rem; margin: 0;'>
            Built with ❤️ using <strong>Streamlit</strong> • Professional Edition v2.0
        </p>
        <p style='color: #94a3b8; font-size: 0.85rem; margin-top: 0.5rem;'>
            Powered by Figma API • Optimized for Angular Development • Fully Responsive
        </p>
        <p style='color: #cbd5e1; font-size: 0.8rem; margin-top: 0.5rem;'>
            © 2025 • Enterprise-grade design system extraction
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
