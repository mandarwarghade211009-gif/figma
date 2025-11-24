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

# -----------------------------------------------------
# PROFESSIONAL THEMING
# -----------------------------------------------------
def apply_professional_styling():
    """Apply professional, modern enterprise CSS theme with 2025 design trends"""
    st.markdown("""
    <style>
    /* =====================================================
       PROFESSIONAL ENTERPRISE THEME 2025
       Modern, Clean, and Highly Attractive Design System
    ===================================================== */
    
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* ==================== ROOT VARIABLES ==================== */
    :root {
        /* Primary Brand Colors - Modern Blue Palette */
        --primary-blue: #2563EB;
        --primary-blue-dark: #1E40AF;
        --primary-blue-light: #3B82F6;
        --accent-cyan: #06B6D4;
        --accent-orange: #F97316;
        
        /* Neutral Grays - Professional Palette */
        --gray-50: #F9FAFB;
        --gray-100: #F3F4F6;
        --gray-200: #E5E7EB;
        --gray-300: #D1D5DB;
        --gray-400: #9CA3AF;
        --gray-500: #6B7280;
        --gray-600: #4B5563;
        --gray-700: #374151;
        --gray-800: #1F2937;
        --gray-900: #111827;
        
        /* Semantic Colors */
        --success: #10B981;
        --success-light: #D1FAE5;
        --warning: #F59E0B;
        --warning-light: #FEF3C7;
        --error: #EF4444;
        --error-light: #FEE2E2;
        --info: #3B82F6;
        --info-light: #DBEAFE;
        
        /* Background Gradients */
        --bg-gradient-primary: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        --bg-gradient-secondary: linear-gradient(135deg, #F093FB 0%, #F5576C 100%);
        --bg-gradient-success: linear-gradient(135deg, #4FACFE 0%, #00F2FE 100%);
        --bg-gradient-warm: linear-gradient(135deg, #FA709A 0%, #FEE140 100%);
        --bg-gradient-cool: linear-gradient(135deg, #30CFD0 0%, #330867 100%);
        
        /* Shadows - Professional Depth */
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-glow: 0 0 20px rgba(37, 99, 235, 0.3);
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.5rem;
        --radius-full: 9999px;
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ==================== BASE STYLES ==================== */
    .stApp {
        background: linear-gradient(to bottom right, #F9FAFB 0%, #EFF6FF 50%, #F0F9FF 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main Content Container */
    .main .block-container {
        padding: 2rem 3rem 3rem 3rem;
        max-width: 1400px;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: var(--radius-2xl);
        box-shadow: var(--shadow-xl);
        margin: 1.5rem auto;
    }
    
    /* ==================== TYPOGRAPHY ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--gray-900);
    }
    
    h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }
    
    h2 {
        font-size: 1.75rem;
        color: var(--gray-800);
        border-bottom: 3px solid var(--primary-blue);
        padding-bottom: 0.75rem;
        margin: 2rem 0 1.5rem 0;
        position: relative;
    }
    
    h2::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: var(--accent-cyan);
        border-radius: var(--radius-full);
    }
    
    h3 {
        font-size: 1.35rem;
        color: var(--gray-700);
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    p, li, span {
        color: var(--gray-600);
        line-height: 1.7;
        font-size: 0.975rem;
    }
    
    code {
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        background: var(--gray-100);
        padding: 0.2rem 0.5rem;
        border-radius: var(--radius-sm);
        color: var(--primary-blue-dark);
        font-size: 0.875rem;
        border: 1px solid var(--gray-200);
    }
    
    /* ==================== SIDEBAR STYLING ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: var(--shadow-2xl);
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        padding: 0.5rem 0;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15);
        margin: 1.5rem 0;
    }
    
    /* Sidebar Links */
    [data-testid="stSidebar"] a {
        color: #60A5FA !important;
        text-decoration: none;
        transition: var(--transition-base);
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] a:hover {
        color: #93C5FD !important;
        text-decoration: underline;
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: var(--shadow-lg);
        transition: all var(--transition-base);
        text-transform: none;
        letter-spacing: 0.01em;
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
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: var(--transition-slow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-xl), var(--shadow-glow);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-md);
    }
    
    /* ==================== INPUTS ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: 0.75rem 1rem;
        font-size: 0.975rem;
        transition: all var(--transition-base);
        background: white;
        color: var(--gray-800);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        outline: none;
    }
    
    /* Input Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stFileUploader > label {
        color: var(--gray-700);
        font-weight: 600;
        font-size: 0.925rem;
        margin-bottom: 0.5rem;
    }
    
    /* ==================== TABS ==================== */
    .stTabs {
        background: white;
        border-radius: var(--radius-xl);
        padding: 1.5rem;
        box-shadow: var(--shadow-lg);
        margin: 2rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--gray-50);
        padding: 0.5rem;
        border-radius: var(--radius-lg);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: var(--gray-600);
        transition: all var(--transition-base);
        border: none;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: white;
        color: var(--primary-blue);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 2rem 0.5rem 0.5rem 0.5rem;
    }
    
    /* ==================== METRICS ==================== */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue-dark);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--gray-600);
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        padding: 1.5rem;
        border-radius: var(--radius-xl);
        border: 2px solid var(--gray-100);
        box-shadow: var(--shadow-md);
        transition: all var(--transition-base);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-blue);
    }
    
    /* ==================== PROGRESS BAR ==================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-cyan) 100%);
        border-radius: var(--radius-full);
        height: 12px;
        box-shadow: var(--shadow-sm);
    }
    
    .stProgress > div > div {
        background: var(--gray-200);
        border-radius: var(--radius-full);
        height: 12px;
    }
    
    /* ==================== ALERTS & MESSAGES ==================== */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-light) 0%, #ECFDF5 100%);
        border-left: 4px solid var(--success);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        color: #065F46;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .stInfo {
        background: linear-gradient(135deg, var(--info-light) 0%, #EFF6FF 100%);
        border-left: 4px solid var(--info);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        color: #1E40AF;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .stWarning {
        background: linear-gradient(135deg, var(--warning-light) 0%, #FFFBEB 100%);
        border-left: 4px solid var(--warning);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        color: #92400E;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .stError {
        background: linear-gradient(135deg, var(--error-light) 0%, #FEF2F2 100%);
        border-left: 4px solid var(--error);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        color: #991B1B;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FFFFFF 0%, var(--gray-50) 100%);
        border: 2px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: var(--gray-800);
        transition: all var(--transition-base);
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--primary-blue);
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
        box-shadow: var(--shadow-md);
    }
    
    .streamlit-expanderContent {
        border: 2px solid var(--gray-200);
        border-top: none;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        padding: 1.5rem;
        background: white;
    }
    
    /* ==================== FILE UPLOADER ==================== */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #FFFFFF 0%, var(--gray-50) 100%);
        border: 2px dashed var(--gray-300);
        border-radius: var(--radius-xl);
        padding: 2rem;
        transition: all var(--transition-base);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-blue);
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
        box-shadow: var(--shadow-md);
    }
    
    /* ==================== DOWNLOAD BUTTON ==================== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        font-size: 0.925rem;
        box-shadow: var(--shadow-md);
        transition: all var(--transition-base);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* ==================== COLUMNS ==================== */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* ==================== DATAFRAME ==================== */
    .dataframe {
        border: 2px solid var(--gray-200);
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
        color: white;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: var(--gray-50);
    }
    
    .dataframe tbody tr:hover {
        background: var(--info-light);
        transition: var(--transition-fast);
    }
    
    /* ==================== DIVIDER ==================== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--gray-300) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* ==================== CODE BLOCKS ==================== */
    .stCodeBlock {
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        border: 1px solid var(--gray-200);
    }
    
    /* ==================== SELECTBOX ==================== */
    .stSelectbox > div > div {
        border-radius: var(--radius-lg);
        border: 2px solid var(--gray-200);
        transition: all var(--transition-base);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* ==================== RADIO BUTTONS ==================== */
    .stRadio > div {
        background: linear-gradient(135deg, #FFFFFF 0%, var(--gray-50) 100%);
        border: 2px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
    }
    
    .stRadio > div > label {
        font-weight: 600;
        color: var(--gray-700);
    }
    
    /* ==================== CODE OUTPUT BOX ==================== */
    .code-output-box {
        background: #1E293B;
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        border: 2px solid var(--gray-700);
        box-shadow: var(--shadow-lg);
        position: relative;
        margin: 1.5rem 0;
    }
    
    .code-output-box pre {
        margin: 0;
        color: #E2E8F0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
        line-height: 1.6;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    .copy-button-container {
        position: absolute;
        top: 1rem;
        right: 1rem;
    }
    
    /* ==================== CUSTOM UTILITY CLASSES ==================== */
    .gradient-text {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .card {
        background: white;
        border-radius: var(--radius-xl);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--gray-100);
        transition: all var(--transition-base);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-2xl);
    }
    
    /* ==================== ANIMATIONS ==================== */
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
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* Apply fade-in animation to main content */
    .main .block-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* ==================== RESPONSIVE DESIGN ==================== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        h1 {
            font-size: 1.875rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.65rem 1.5rem;
            font-size: 0.925rem;
        }
    }
    
    /* ==================== SCROLLBAR STYLING ==================== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--gray-100);
        border-radius: var(--radius-full);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
        border-radius: var(--radius-full);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-blue-dark) 0%, #1E3A8A 100%);
    }
    
    /* ==================== SELECTION STYLING ==================== */
    ::selection {
        background: rgba(37, 99, 235, 0.2);
        color: var(--gray-900);
    }
    
    ::-moz-selection {
        background: rgba(37, 99, 235, 0.2);
        color: var(--gray-900);
    }
    
    /* ==================== CAPTION STYLING ==================== */
    .stCaption {
        color: var(--gray-500);
        font-size: 0.825rem;
        font-style: italic;
    }
    
    /* ==================== SPINNER ==================== */
    .stSpinner > div {
        border-color: var(--primary-blue) transparent transparent transparent;
    }
    
    /* ==================== FOOTER ENHANCEMENTS ==================== */
    footer {
        background: linear-gradient(135deg, var(--gray-50) 0%, white 100%);
        padding: 2rem;
        border-radius: var(--radius-xl);
        margin-top: 3rem;
        box-shadow: var(--shadow-md);
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
# STREAMLIT UI + WORKFLOW
# -------------------------

def main():
    # Header / Hero
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='margin-bottom: 0.5rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Enterprise-Grade UI Component Extraction & Angular Code Processing
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
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Documentation](https://www.figma.com/developers/api)
        - [Angular Framework](https://angular.io)
        - [ReportLab](https://www.reportlab.com)
        """)
        st.markdown("---")
        st.markdown("### 🔐 Security")
        st.info("API tokens are used only for fetching and are not persisted.")

    # Tabs
    tab1, tab2 = st.tabs(["🎯 Figma Extraction", "⚡ Angular Processor"])

    # --- Figma Extraction Tab ---
    with tab1:
        st.markdown("### Figma Component Extraction")
        st.markdown("Extract UI components with metadata, styling, and images from Figma.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 Figma File Key", value="", help="Figma file key (from file URL)")
        with col2:
            node_ids = st.text_input("🔗 Node IDs (comma-separated)", value="", help="Optional: comma-separated node ids")

        token = st.text_input("🔑 Figma Personal Access Token", type="password", help="Generate in Figma account settings")

        if st.button("🚀 Extract UI Components"):
            if not token or not file_key:
                st.error("⚠️ Please provide a file key and a Figma access token.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("📡 Fetching nodes from Figma API...")
                    progress.progress(5)
                    nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                    status.text("🖼️ Collecting images and node metadata...")
                    progress.progress(25)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                    status.text("🔗 Resolving image URLs from Figma...")
                    progress.progress(50)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                    status.text("🎨 Building icon map and merging URLs into nodes...")
                    progress.progress(70)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                    merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                    status.text("📦 Extracting structured components...")
                    progress.progress(85)
                    final_output = extract_ui_components(merged_payload)

                    status.text("✨ Finalizing extraction and sanitizing URLs...")
                    progress.progress(95)
                    # remove absolute prefix so output is portable; use default figma prefix commonly returned
                    sanitized = remove_url_prefix_from_json(final_output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                    st.session_state['metadata_json'] = sanitized
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    st.success("✅ Extraction completed successfully!")

                    # Metrics display
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

                    with st.expander("📋 Category Breakdown"):
                        for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
                            count = len(sanitized.get(cat, []))
                            if count > 0:
                                st.markdown(f"- **{cat}**: `{count}`")
                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")

        # Downloads for extraction
        if 'metadata_json' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Extracted Data")
            json_str = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download metadata.json",
                    data=json_str,
                    file_name="metadata.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.caption(f"Size: {len(json_str):,} bytes")

    # --- Angular Processor Tab ---
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Automatically prefix UUID-based image identifiers with complete URLs in your code.")
        st.markdown("---")

        url_prefix = st.text_input(
            "🌐 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="This prefix will be added to all detected image UUIDs"
        )

        st.markdown("#### 📥 Choose Input Method")
        input_method = st.radio(
            "Select how you want to provide your code:",
            options=["📤 Upload File", "📝 Paste Code"],
            horizontal=True,
            label_visibility="collapsed"
        )

        code_text = ""
        source_filename = "code"

        if input_method == "📤 Upload File":
            uploaded = st.file_uploader(
                "📤 Upload Angular Code File",
                type=['txt', 'md', 'html', 'ts', 'js', 'css', 'scss', 'json', 'component.ts'],
                help="Supported formats: .txt, .md, .html, .ts, .js, .css, .scss, .json"
            )
            if uploaded:
                st.info(f"✅ File uploaded: **{uploaded.name}**")
                try:
                    raw = uploaded.read()
                    code_text = decode_bytes_to_text(raw)
                    source_filename = uploaded.name.rsplit('.', 1)[0] if '.' in uploaded.name else uploaded.name
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
        else:
            code_text = st.text_area(
                "📝 Paste Your Angular Code Here",
                height=300,
                placeholder="Paste your TypeScript, HTML, CSS, or any Angular code here...\n\nExample:\n<img src='uuid-here'>\nimageUrl: 'uuid-here'",
                help="Paste your code directly. The processor will find and update all UUID image references."
            )
            source_filename = "pasted_code"

        if code_text:
            if st.button("⚡ Process Angular Code", type="primary"):
                try:
                    uuids = detect_uuids_in_text(code_text)
                    modified, replaced = add_url_prefix_to_angular_code(code_text, url_prefix)

                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = source_filename
                    st.session_state['stats']['files_processed'] += 1

                    st.success("✅ Angular code processed successfully!")

                    # Processing metrics
                    st.markdown("### 📊 Processing Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Image IDs Found", len(uuids))
                    with col2:
                        st.metric("Replacements Made", replaced)
                    with col3:
                        st.metric("Output Size", f"{len(modified):,} bytes")

                    if len(uuids) > 0:
                        with st.expander("🔍 Sample Transformation"):
                            sample = uuids[0]
                            st.code(f"Before: {sample}", language="text")
                            st.code(f"After: {url_prefix}{sample}", language="text")
                except Exception as e:
                    st.error(f"❌ Error processing code: {str(e)}")

        # Output section - display and download/copy
        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 📤 Processed Output")
            
            # Display formatted code with copy button
            st.markdown("#### 💻 View & Copy Code")
            
            # Create a code block with proper formatting
            st.code(st.session_state['angular_output'], language="typescript", line_numbers=True)
            
            # Alternative: Display in a text area for easy copying
            with st.expander("📋 Raw Output (Click to Expand & Copy)", expanded=False):
                st.text_area(
                    "Processed Code",
                    value=st.session_state['angular_output'],
                    height=400,
                    label_visibility="collapsed",
                    help="You can select all text and copy from here"
                )
            
            st.markdown("#### 💾 Download Options")
            base = st.session_state['angular_filename']

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.download_button(
                    "📄 .txt",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    "📝 .md",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            with col3:
                st.download_button(
                    "💻 .ts",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.ts",
                    mime="text/typescript",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            with col4:
                pdf_buf = create_text_to_pdf(st.session_state['angular_output'])
                st.download_button(
                    "📕 .pdf",
                    data=pdf_buf,
                    file_name=f"{base}_modified.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            
            # File info
            st.caption(f"📦 Output ready: **{base}_modified** • Size: {len(st.session_state['angular_output']):,} bytes")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>Built with ❤️ using <strong>Streamlit</strong> | Professional Edition v2.0</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
