#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor with Smart ImageURL Optimization
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
# SMART IMAGEURL FILTER CONFIGURATION
# -----------------------------------------------------
# The category and keyword lists used for strict icon/logo detection
logo_keywords = ['logo', 'brand', 'company', 'trademark', 'wellsky']
icon_keywords = [
    'icon', 'glyph', 'symbol', 'badge', 'avatar', 'star', 'check', 'arrow',
    'menu', 'hamburger', 'close', 'search', 'notification', 'bell', 'user',
    'profile', 'gift', 'question', 'help', 'caret', 'dropdown', 'expand'
]
icon_fonts = ['Font Awesome', 'Material Icons', 'Ionicons', 'Glyphicons', 'IcoFont', 
              'Material Design Icons', 'Feather', 'Heroicons']

# Size thresholds for filtering decorative images
MIN_ICON_SIZE = 8  # pixels
MAX_ICON_SIZE = 128  # pixels
MIN_LOGO_SIZE = 16
MAX_LOGO_SIZE = 256

# -----------------------------------------------------
# PROFESSIONAL THEMING
# -----------------------------------------------------
def apply_professional_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 6px;
        border: 2px solid #E5E7EB;
        padding: 0.625rem;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .stMetric {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #E5E7EB;
    }
    </style>
    """, unsafe_allow_html=True)

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
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    params = {"ids": node_ids} if node_ids else {}
    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    if not r.ok:
        raise RuntimeError(f"Figma API error {r.status_code}: {r.text}")
    data = r.json()
    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_invisible_nodes(doc)
    else:
        if isinstance(data.get("document"), dict):
            data["document"] = filter_invisible_nodes(data["document"])
    return data

def walk_nodes_collect_images_and_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, Any]]]:
    image_refs: Set[str] = set()
    node_ids: List[str] = []
    node_meta: Dict[str, Dict[str, Any]] = {}
    
    def visit(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        nid = n.get("id")
        if nid:
            node_ids.append(nid)
            # Extract comprehensive metadata for filtering
            meta = {
                "id": nid,
                "name": n.get("name", ""),
                "type": n.get("type", ""),
                "absoluteBoundingBox": n.get("absoluteBoundingBox", {}),
                "fills": n.get("fills", []),
                "strokes": n.get("strokes", []),
                "characters": n.get("characters", ""),
                "style": n.get("style", {})
            }
            node_meta[nid] = meta
        
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
    unique_node_ids = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_node_ids.append(nid)
    return image_refs, unique_node_ids, node_meta

def resolve_image_urls(file_key: str, image_refs: Set[str], node_ids: List[str], token: str, timeout: int = 60) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    headers = build_headers(token)
    fills_map: Dict[str, str] = {}
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

def is_icon_or_logo_node(meta: Dict[str, Any]) -> bool:
    """
    Determine if a node is an icon or logo based on comprehensive metadata analysis[web:4][web:8]
    """
    name = meta.get("name", "").lower()
    node_type = meta.get("type", "").upper()
    
    # Check name-based keywords
    is_logo = any(keyword in name for keyword in logo_keywords)
    is_icon = any(keyword in name for keyword in icon_keywords)
    
    # Check size constraints
    bbox = meta.get("absoluteBoundingBox", {})
    if isinstance(bbox, dict) and "width" in bbox and "height" in bbox:
        width = bbox.get("width", 0)
        height = bbox.get("height", 0)
        
        # Icon size check
        is_icon_sized = (MIN_ICON_SIZE <= width <= MAX_ICON_SIZE and 
                        MIN_ICON_SIZE <= height <= MAX_ICON_SIZE)
        
        # Logo size check
        is_logo_sized = (MIN_LOGO_SIZE <= width <= MAX_LOGO_SIZE and 
                        MIN_LOGO_SIZE <= height <= MAX_LOGO_SIZE)
    else:
        is_icon_sized = False
        is_logo_sized = False
    
    # Check if it's a text element with icon font
    if node_type == "TEXT":
        style = meta.get("style", {})
        font_family = style.get("fontFamily", "")
        is_icon_font = any(icon_font in font_family for icon_font in icon_fonts)
        
        characters = meta.get("characters", "")
        is_short_text = len(characters.strip()) <= 3
        
        return is_icon_font or (is_short_text and is_icon)
    
    # Check if node has image fills (actual images, not decorative backgrounds)
    fills = meta.get("fills", [])
    has_image_fill = any(f.get("type") == "IMAGE" for f in fills if isinstance(f, dict))
    
    # Final decision logic
    if is_logo and is_logo_sized:
        return True
    if is_icon and (is_icon_sized or has_image_fill):
        return True
    if node_type in ["VECTOR", "GROUP", "COMPONENT", "INSTANCE"] and (is_icon or is_logo):
        return True
    
    return False

def build_icon_map(nodes_payload: Dict[str, Any], filtered_fills: Dict[str, str], 
                   renders_map: Dict[str, Optional[str]], node_meta: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """
    Build icon map with strict filtering based on metadata analysis
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
    
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                map_first_image(doc)
    if isinstance(nodes_payload.get("document"), dict):
        map_first_image(nodes_payload["document"])
    
    node_to_url: Dict[str, str] = {}
    for nid, meta in node_meta.items():
        # Only include imageUrl if node passes strict icon/logo filter
        if not is_icon_or_logo_node(meta):
            continue
            
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
    keys = [
        'layoutMode', 'constraints', 'paddingLeft', 'paddingRight', 'paddingTop', 'paddingBottom',
        'itemSpacing', 'counterAxisAlignItems', 'primaryAxisAlignItems', 'layoutGrow', 'layoutAlign',
        'layoutSizingHorizontal', 'layoutSizingVertical', 'counterAxisSizingMode', 'primaryAxisSizingMode',
        'clipsContent', 'layoutWrap', 'layoutGrids'
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
        'metadata': {
            'totalComponents': len(components), 
            'extractedAt': datetime.datetime.utcnow().isoformat() + 'Z', 
            'version': 1,
            'filteringApplied': {
                'iconKeywords': icon_keywords,
                'logoKeywords': logo_keywords,
                'iconFonts': icon_fonts,
                'sizeThresholds': {
                    'minIconSize': MIN_ICON_SIZE,
                    'maxIconSize': MAX_ICON_SIZE,
                    'minLogoSize': MIN_LOGO_SIZE,
                    'maxLogoSize': MAX_LOGO_SIZE
                }
            }
        },
        'textElements': [], 'buttons': [], 'inputs': [], 'containers': [],
        'images': [], 'navigation': [], 'vectors': [], 'other': []
    }
    for c in components:
        organized.setdefault(classify_bucket(c), []).append(c)
    return organized

def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract UI components with metadata-based imageURL optimization already applied
    """
    roots = find_document_roots(merged_payload)
    if not roots:
        raise RuntimeError("No document roots found in payload")
    all_components: List[Dict[str, Any]] = []
    for r in roots:
        if isinstance(r, dict):
            extract_components(r, "", all_components)
    organized = organize_for_angular(all_components)
    
    # Calculate statistics
    total_with_imageurl = sum(1 for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']
                              for elem in organized.get(cat, []) if 'imageUrl' in elem)
    
    stats_by_category = {}
    for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
        count = sum(1 for elem in organized.get(cat, []) if 'imageUrl' in elem)
        if count > 0:
            stats_by_category[cat] = count
    
    organized['metadata']['imageUrlStats'] = {
        'totalIncluded': total_with_imageurl,
        'byCategory': stats_by_category,
        'optimizationStrategy': 'metadata-based filtering with size and keyword analysis'
    }
    
    return organized

# -----------------------------------------------------
# STREAMLIT UI + WORKFLOW
# -----------------------------------------------------
def main():
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='margin-bottom: 0.5rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Enterprise-Grade UI Component Extraction with Smart ImageURL Optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
        st.markdown("### 🎯 Filter Configuration")
        st.markdown(f"**Icon Size:** {MIN_ICON_SIZE}-{MAX_ICON_SIZE}px")
        st.markdown(f"**Logo Size:** {MIN_LOGO_SIZE}-{MAX_LOGO_SIZE}px")
        st.markdown(f"**Icon Keywords:** {len(icon_keywords)}")
        st.markdown(f"**Logo Keywords:** {len(logo_keywords)}")
        
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

    tab1, tab2 = st.tabs(["🎯 Figma Extraction", "⚡ Angular Processor"])
    
    with tab1:
        st.markdown("### Figma Component Extraction")
        st.markdown("Extract UI components with **metadata-based imageURL optimization** for Angular agents.")
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
                    
                    status.text("🖼️ Collecting images and comprehensive node metadata...")
                    progress.progress(25)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)
                    
                    status.text("🔗 Resolving image URLs from Figma...")
                    progress.progress(50)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)
                    
                    status.text("🎨 Applying metadata-based filtering and building icon map...")
                    progress.progress(70)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                    
                    merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)
                    
                    status.text("📦 Extracting structured components...")
                    progress.progress(85)
                    final_output = extract_ui_components(merged_payload)
                    
                    status.text("✨ Finalizing extraction...")
                    progress.progress(95)
                    
                    st.session_state['metadata_json'] = final_output
                    st.session_state['stats']['files_processed'] += 1
                    
                    progress.progress(100)
                    st.success("✅ Extraction completed with metadata-based optimization!")
                    
                    st.markdown("### 📊 Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", final_output['metadata']['totalComponents'])
                    with col2:
                        st.metric("Text Elements", len(final_output.get('textElements', [])))
                    with col3:
                        st.metric("Buttons", len(final_output.get('buttons', [])))
                    with col4:
                        st.metric("Containers", len(final_output.get('containers', [])))
                    
                    img_stats = final_output['metadata'].get('imageUrlStats', {})
                    if img_stats.get('totalIncluded', 0) > 0:
                        st.markdown("### 🎯 ImageURL Optimization Results")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total imageUrls Included", img_stats['totalIncluded'])
                        with col2:
                            st.info("✨ Only icons, logos, and semantic images included")
                        
                        with st.expander("📋 ImageURL Distribution by Category"):
                            for cat, count in img_stats.get('byCategory', {}).items():
                                st.markdown(f"- **{cat}**: `{count}` imageUrls")
                    
                    with st.expander("📋 Full Category Breakdown"):
                        for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
                            total_count = len(final_output.get(cat, []))
                            img_count = sum(1 for elem in final_output.get(cat, []) if 'imageUrl' in elem)
                            if total_count > 0:
                                st.markdown(f"- **{cat}**: `{total_count}` components, `{img_count}` with imageUrl")
                
                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())

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

    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Automatically prefix UUID-based image identifiers with complete URLs in your code.")
        st.markdown("---")
        
        url_prefix = st.text_input(
            "🌐 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="This prefix will be added to all detected image UUIDs"
        )
        
        uploaded = st.file_uploader(
            "📤 Upload Angular Code File",
            type=['txt', 'md', 'html', 'ts', 'js', 'pdf'],
            help="Supported formats: .txt, .md, .html, .ts, .js, .pdf"
        )
        
        def decode_bytes_to_text(raw: bytes) -> str:
            try:
                return raw.decode('utf-8')
            except Exception:
                try:
                    return raw.decode('latin-1')
                except Exception:
                    return raw.decode('utf-8', errors='ignore')
        
        UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
        
        def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
            import re
            patterns = [
                (re.compile(r'(src\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
                (re.compile(r'(\[src\]\s*=\s*["\\']\s*)(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
                (re.compile(r'(imageUrl\s*:\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
                (re.compile(r'(url\(\s*["\'])(%s)(["\\']\s*\))' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
                (re.compile(r'(["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
            ]
            modified = text
            total_replacements = 0
            for pat, repl in patterns:
                modified, n = pat.subn(repl, modified)
                total_replacements += n
            return modified, total_replacements
        
        if uploaded:
            st.info(f"✅ File uploaded: **{uploaded.name}**")
            if st.button("⚡ Process Angular Code"):
                try:
                    raw = uploaded.read()
                    text = decode_bytes_to_text(raw)
                    if uploaded.name.lower().endswith('.pdf'):
                        st.warning("⚠️ PDF->text extraction is basic; results may vary.")
                    
                    pattern = re.compile(UUID_RE, re.IGNORECASE)
                    uuids = pattern.findall(text)
                    
                    modified, replaced = add_url_prefix_to_angular_code(text, url_prefix)
                    
                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = uploaded.name
                    st.session_state['stats']['files_processed'] += 1
                    
                    st.success("✅ Angular code processed successfully!")
                    
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
                    st.error(f"❌ Error processing file: {str(e)}")
        
        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Processed Code")
            base = st.session_state['angular_filename'].rsplit('.', 1)[0]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📄 Download as .txt",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.download_button(
                    "📝 Download as .md",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )

if __name__ == "__main__":
    main()
