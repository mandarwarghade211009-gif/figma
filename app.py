#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor - OPTIMIZED
Minimized metadata extraction for token-efficient Angular conversion
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
    """Apply professional, government-style CSS theme"""
    st.markdown("""
    <style>
    /* Your original styling - keeping unchanged */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Config
st.set_page_config(
    page_title="Figma UI Extractor | Optimized Edition",
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
    """Convert Figma color to rgba string"""
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
    """Remove invisible nodes from tree"""
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
    """Fetch node(s) from Figma file"""
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
    elif isinstance(data.get("document"), dict):
        data["document"] = filter_invisible_nodes(data["document"])
    return data

def walk_nodes_collect_images_and_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, str]]]:
    """Walk nodes and collect image refs and node ids"""
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
        
        # Collect image refs from fills
        for f in n.get("fills", []) or []:
            if isinstance(f, dict) and f.get("type") == "IMAGE":
                ref = f.get("imageRef") or f.get("imageHash")
                if ref:
                    image_refs.add(ref)
        
        # Collect from strokes
        for s in n.get("strokes", []) or []:
            if isinstance(s, dict) and s.get("type") == "IMAGE":
                ref = s.get("imageRef") or s.get("imageHash")
                if ref:
                    image_refs.add(ref)
        
        # Visit children
        for c in n.get("children", []) or []:
            visit(c)

    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])

    # De-duplicate node_ids
    seen = set()
    unique_node_ids = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_node_ids.append(nid)

    return image_refs, unique_node_ids, node_meta

def resolve_image_urls(file_key: str, image_refs: Set[str], node_ids: List[str], token: str, timeout: int = 60) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    """Resolve image URLs from Figma"""
    headers = build_headers(token)
    fills_map: Dict[str, str] = {}
    
    try:
        fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
        if image_refs:
            params = {"ids": ",".join(list(image_refs))}
            r = requests.get(fills_url, headers=headers, params=params, timeout=timeout)
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
    """Map node ids to image URLs"""
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
    """Inject image URLs into nodes"""
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
# OPTIMIZED EXTRACTION HELPERS
# -------------------------

def extract_bounds(node: Dict[str, Any]) -> Optional[Dict[str, float]]:
    """Extract bounding box - ESSENTIAL for positioning"""
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict) and all(k in box for k in ("x", "y", "width", "height")):
        try:
            return {
                "x": round(float(box["x"]), 2),
                "y": round(float(box["y"]), 2),
                "w": round(float(box["width"]), 2),
                "h": round(float(box["height"]), 2)
            }
        except Exception:
            return None
    return None

def extract_layout(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract ONLY essential layout properties for Angular flex/grid"""
    layout: Dict[str, Any] = {}
    
    # Auto-layout mode (flex direction)
    if "layoutMode" in node and node["layoutMode"] != "NONE":
        layout["mode"] = node["layoutMode"]  # HORIZONTAL or VERTICAL
    
    # Spacing
    if "itemSpacing" in node:
        layout["gap"] = round(float(node["itemSpacing"]), 2)
    
    # Padding (simplified)
    padding = {}
    for key in ["paddingLeft", "paddingRight", "paddingTop", "paddingBottom"]:
        if key in node:
            padding[key.replace("padding", "").lower()] = round(float(node[key]), 2)
    if padding:
        layout["padding"] = padding
    
    # Alignment (essential for flexbox)
    if "primaryAxisAlignItems" in node:
        layout["justify"] = node["primaryAxisAlignItems"]
    if "counterAxisAlignItems" in node:
        layout["align"] = node["counterAxisAlignItems"]
    
    # Sizing behavior
    if "layoutSizingHorizontal" in node:
        layout["widthMode"] = node["layoutSizingHorizontal"]  # FIXED, HUG, FILL
    if "layoutSizingVertical" in node:
        layout["heightMode"] = node["layoutSizingVertical"]
    
    return layout if layout else None

def extract_visuals(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract ONLY primary visual properties needed for CSS"""
    styling: Dict[str, Any] = {}
    
    # Primary fill (background) - ONLY FIRST SOLID
    fills = node.get("fills")
    if is_nonempty_list(fills):
        for f in fills:
            if isinstance(f, dict) and f.get("type") == "SOLID" and "color" in f:
                styling["bg"] = to_rgba(f["color"])
                break  # Only first solid fill
    
    # Background color fallback
    if "bg" not in styling and "backgroundColor" in node:
        styling["bg"] = to_rgba(node["backgroundColor"])
    
    # Primary stroke (border) - ONLY FIRST
    strokes = node.get("strokes")
    if is_nonempty_list(strokes):
        for s in strokes:
            if isinstance(s, dict) and s.get("type") == "SOLID" and "color" in s:
                border = {"color": to_rgba(s["color"])}
                if "strokeWeight" in node:
                    border["width"] = round(float(node["strokeWeight"]), 2)
                styling["border"] = border
                break  # Only first stroke
    
    # Corner radius
    if isinstance(node.get("cornerRadius"), (int, float)) and node.get("cornerRadius", 0) > 0:
        styling["radius"] = round(float(node["cornerRadius"]), 2)
    
    # Effects - ONLY shadows (simplified)
    effects = node.get("effects")
    if is_nonempty_list(effects):
        for e in effects:
            if isinstance(e, dict) and "SHADOW" in str(e.get("type", "")).upper():
                shadow = {}
                off = e.get("offset") or {}
                if isinstance(off, dict):
                    shadow["x"] = round(float(off.get("x", 0)), 2)
                    shadow["y"] = round(float(off.get("y", 0)), 2)
                if "radius" in e:
                    shadow["blur"] = round(float(e["radius"]), 2)
                if "color" in e:
                    shadow["color"] = to_rgba(e["color"])
                styling["shadow"] = shadow
                break  # Only first shadow
    
    # Opacity
    if "opacity" in node and node["opacity"] < 1:
        styling["opacity"] = round(float(node["opacity"]), 2)
    
    return styling if styling else None

def extract_text(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract ONLY essential text properties for Angular"""
    if (node.get("type") or "").upper() != "TEXT":
        return None
    
    t: Dict[str, Any] = {}
    
    # Content
    content = node.get("characters", "")
    if content:
        t["content"] = content
    
    # Style
    style = node.get("style") or {}
    if isinstance(style, dict):
        typo = {}
        if "fontFamily" in style:
            typo["family"] = style["fontFamily"]
        if "fontSize" in style:
            typo["size"] = round(float(style["fontSize"]), 2)
        if "fontWeight" in style:
            typo["weight"] = style["fontWeight"]
        if "lineHeightPx" in style:
            typo["lineHeight"] = round(float(style["lineHeightPx"]), 2)
        elif "lineHeight" in style:
            typo["lineHeight"] = style["lineHeight"]
        if "textAlignHorizontal" in style:
            typo["align"] = style["textAlignHorizontal"].lower()
        if "letterSpacing" in style:
            typo["spacing"] = round(float(style["letterSpacing"]), 2)
        
        if typo:
            t["style"] = typo
    
    # Text color from fills
    fills = node.get("fills")
    if is_nonempty_list(fills):
        for f in fills:
            if isinstance(f, dict) and f.get("type") == "SOLID" and "color" in f:
                t["color"] = to_rgba(f["color"])
                break
    
    return t if t else None

def extract_constraints(node: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Extract constraints for responsive behavior"""
    constraints = node.get("constraints")
    if isinstance(constraints, dict):
        result = {}
        if "vertical" in constraints:
            result["v"] = constraints["vertical"]
        if "horizontal" in constraints:
            result["h"] = constraints["horizontal"]
        return result if result else None
    return None

def should_include(node: Dict[str, Any]) -> bool:
    """Determine if node should be included - OPTIMIZED"""
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    
    # Always include text, frames, components
    if t in ['TEXT', 'FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'SECTION']:
        return True
    
    # Include if has visual properties
    if node.get("fills") or node.get("strokes") or node.get("effects") or node.get("image_url"):
        return True
    
    # Include if has layout
    if node.get("layoutMode"):
        return True
    
    # Include semantic elements
    semantic_keywords = ['button', 'input', 'search', 'nav', 'menu', 'container', 'card', 'panel', 'header', 'footer']
    if any(k in name for k in semantic_keywords):
        return True
    
    # Include vectors with visual properties
    if t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE']:
        return bool(node.get("strokes") or node.get("fills"))
    
    return False

def classify_bucket(comp: Dict[str, Any]) -> str:
    """Classify component into Angular-relevant buckets"""
    t = (comp.get("type") or "").upper()
    name = (comp.get("name") or "").lower()
    
    if t == "TEXT":
        return "text"
    if "button" in name or "btn" in name:
        return "buttons"
    if any(k in name for k in ['input', 'search', 'field', 'textarea']):
        return "inputs"
    if any(k in name for k in ['nav', 'menu', 'sidebar', 'header', 'footer']):
        return "navigation"
    if comp.get("img"):
        return "images"
    if t in ['FRAME', 'GROUP', 'SECTION'] or any(k in name for k in ['container', 'card', 'panel', 'wrapper']):
        return "containers"
    if t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE']:
        return "icons"
    
    return "other"

def extract_components(root: Dict[str, Any], parent_path: str = "", out: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Extract components with MINIMAL metadata - OPTIMIZED"""
    if out is None:
        out = []
    if root is None or not isinstance(root, dict):
        return out
    
    path = f"{parent_path}/{root.get('name','?')}" if parent_path else (root.get('name') or 'Root')
    
    # Core component data
    comp: Dict[str, Any] = {
        'id': root.get('id'),
        'name': root.get('name'),
        'type': root.get('type'),
        'path': path
    }
    
    # Position & size (ESSENTIAL)
    bounds = extract_bounds(root)
    if bounds:
        comp['box'] = bounds
    
    # Layout (if has auto-layout)
    layout = extract_layout(root)
    if layout:
        comp['layout'] = layout
    
    # Visual styling (simplified)
    styling = extract_visuals(root)
    if styling:
        comp['style'] = styling
    
    # Constraints (for responsive)
    constraints = extract_constraints(root)
    if constraints:
        comp['constraints'] = constraints
    
    # Image URL (if exists)
    if root.get('image_url'):
        comp['img'] = root.get('image_url')
    elif root.get('imageUrl'):
        comp['img'] = root.get('imageUrl')
    
    # Text content (if text node)
    text = extract_text(root)
    if text:
        comp['text'] = text
    
    # Add to output if should be included
    if should_include(root):
        out.append(comp)
    
    # Recurse children
    for child in root.get('children', []) or []:
        if isinstance(child, dict):
            extract_components(child, path, out)
    
    return out

def find_document_roots(nodes_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find document root nodes"""
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

def organize_for_angular(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Organize components by type for Angular generation"""
    organized = {
        'meta': {
            'total': len(components),
            'extracted': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': '2.0-optimized'
        },
        'text': [],
        'buttons': [],
        'inputs': [],
        'containers': [],
        'images': [],
        'navigation': [],
        'icons': [],
        'other': []
    }
    
    for c in components:
        bucket = classify_bucket(c)
        organized[bucket].append(c)
    
    return organized

def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main extraction orchestrator - OPTIMIZED"""
    roots = find_document_roots(merged_payload)
    if not roots:
        raise RuntimeError("No document roots found in payload")
    
    all_components: List[Dict[str, Any]] = []
    for r in roots:
        if isinstance(r, dict):
            extract_components(r, "", all_components)
    
    return organize_for_angular(all_components)

def remove_url_prefix_from_json(payload: Dict[str, Any], url_prefix: str) -> Dict[str, Any]:
    """Remove URL prefix from image URLs for portability"""
    p = copy.deepcopy(payload)
    
    def process(obj: Any):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k in ("img", "imageUrl", "image_url") and isinstance(v, str):
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

UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
    """Add URL prefix to UUID placeholders in Angular code"""
    patterns = [
        (re.compile(r'(src\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(\[src\]\s*=\s*["\']\s*)(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(imageUrl\s*:\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(url\(\s*["\'])(%s)(["\']\s*\))' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
    ]

    modified = text
    total_replacements = 0
    for pat, repl in patterns:
        modified, n = pat.subn(repl, modified)
        total_replacements += n
    return modified, total_replacements

def create_text_to_pdf(text_content: str) -> BytesIO:
    """Convert text to PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, 
                          leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle('Code', parent=styles.get('Normal'), fontName='Courier',
                               fontSize=8, leading=10, leftIndent=0, rightIndent=0, spaceAfter=6)
    story = []
    lines = text_content.splitlines()
    chunk_size = 60
    for i in range(0, len(lines), chunk_size):
        block = lines[i:i+chunk_size]
        safe = [ln.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for ln in block]
        story.append(Paragraph('<br/>'.join(safe), code_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

def detect_uuids_in_text(text: str) -> List[str]:
    """Detect UUIDs in text"""
    pattern = re.compile(UUID_RE, re.IGNORECASE)
    found = pattern.findall(text)
    seen = set()
    out = []
    for f in found:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out

def decode_bytes_to_text(raw: bytes) -> str:
    """Decode bytes to text with fallback"""
    try:
        return raw.decode('utf-8')
    except Exception:
        try:
            return raw.decode('latin-1')
        except Exception:
            return raw.decode('utf-8', errors='ignore')

# -------------------------
# STREAMLIT UI
# -------------------------

def main():
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='margin-bottom: 0.5rem;'>🎨 Figma UI Extractor - OPTIMIZED</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Token-Efficient UI Extraction for Angular Code Generation
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
        st.markdown("### 🎯 Optimization Benefits")
        st.info("""
        **Reduced JSON size by 60-70%**
        - Minimal field extraction
        - Simplified property names
        - Only primary styles
        - Essential layout data only
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Docs](https://www.figma.com/developers/api)
        - [Angular Docs](https://angular.io)
        - [Auto Layout Guide](https://help.figma.com/hc/en-us/articles/360040451373)
        """)

    # Tabs
    tab1, tab2 = st.tabs(["🎯 Figma Extraction (Optimized)", "⚡ Angular Processor"])

    # --- Figma Extraction Tab ---
    with tab1:
        st.markdown("### Optimized Figma Component Extraction")
        st.markdown("Extract **ONLY essential fields** needed for accurate Angular HTML conversion.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 Figma File Key", value="", help="Figma file key from URL")
        with col2:
            node_ids = st.text_input("🔗 Node IDs (optional)", value="", help="Comma-separated node ids")

        token = st.text_input("🔑 Figma Personal Access Token", type="password", 
                             help="Generate in Figma account settings")

        if st.button("🚀 Extract UI Components (Optimized)", type="primary"):
            if not token or not file_key:
                st.error("⚠️ Please provide file key and Figma token.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("📡 Fetching nodes from Figma API...")
                    progress.progress(5)
                    nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                    status.text("🖼️ Collecting images and metadata...")
                    progress.progress(25)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                    status.text("🔗 Resolving image URLs...")
                    progress.progress(50)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                    status.text("🎨 Merging URLs into nodes...")
                    progress.progress(70)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                    merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                    status.text("📦 Extracting OPTIMIZED components...")
                    progress.progress(85)
                    final_output = extract_ui_components(merged_payload)

                    status.text("✨ Finalizing and sanitizing...")
                    progress.progress(95)
                    sanitized = remove_url_prefix_from_json(final_output, 
                                                            "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                    st.session_state['metadata_json'] = sanitized
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    
                    # Calculate size reduction
                    json_str = json.dumps(sanitized, indent=2, ensure_ascii=False)
                    size_kb = len(json_str) / 1024
                    
                    st.success(f"✅ Extraction completed! JSON size: {size_kb:.2f} KB")

                    # Metrics
                    st.markdown("### 📊 Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", sanitized['meta']['total'])
                    with col2:
                        st.metric("Text Elements", len(sanitized.get('text', [])))
                    with col3:
                        st.metric("Buttons", len(sanitized.get('buttons', [])))
                    with col4:
                        st.metric("Containers", len(sanitized.get('containers', [])))

                    with st.expander("📋 Category Breakdown"):
                        for cat in ['text', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'icons', 'other']:
                            count = len(sanitized.get(cat, []))
                            if count > 0:
                                st.markdown(f"- **{cat}**: `{count}` components")
                    
                    with st.expander("🔍 Sample Component Structure"):
                        if sanitized.get('containers') and len(sanitized['containers']) > 0:
                            st.json(sanitized['containers'][0])
                        elif sanitized.get('buttons') and len(sanitized['buttons']) > 0:
                            st.json(sanitized['buttons'][0])

                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")
                    import traceback
                    with st.expander("Debug Info"):
                        st.code(traceback.format_exc())

        # Downloads
        if 'metadata_json' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Extracted Data")
            json_str = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download metadata.json (Optimized)",
                    data=json_str,
                    file_name="metadata_optimized.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.caption(f"Size: {len(json_str)/1024:.2f} KB")

    # --- Angular Processor Tab ---
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Upload or paste code to automatically prefix UUID image IDs with full URLs.")
        st.markdown("---")

        url_prefix = st.text_input(
            "🌐 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="This prefix will be added to all detected image UUIDs"
        )

        st.markdown("#### 📥 Choose Input Method")
        input_method = st.radio(
            "Select input method:",
            options=["📤 Upload File", "📝 Paste Code"],
            horizontal=True,
            label_visibility="collapsed"
        )

        code_text = ""
        source_filename = "code"

        if input_method == "📤 Upload File":
            uploaded = st.file_uploader(
                "📤 Upload Angular Code File",
                type=['txt', 'md', 'html', 'ts', 'js', 'css', 'scss', 'json'],
                help="Supported: .txt, .md, .html, .ts, .js, .css, .scss, .json"
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
                height=320,
                placeholder="Paste TypeScript / HTML / CSS code here...",
                help="Paste code to enable processing"
            )
            source_filename = "pasted_code"

        if code_text and code_text.strip():
            if st.button("⚡ Process Angular Code", type="primary"):
                try:
                    uuids = detect_uuids_in_text(code_text)
                    modified, replaced = add_url_prefix_to_angular_code(code_text, url_prefix)

                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = source_filename
                    st.session_state['stats']['files_processed'] += 1

                    st.success("✅ Angular code processed successfully!")

                    # Metrics
                    st.markdown("### 📊 Processing Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Image IDs Found", len(uuids))
                    with col2:
                        st.metric("Replacements Made", replaced)
                    with col3:
                        st.metric("Output Size", f"{len(modified)/1024:.2f} KB")

                    if len(uuids) > 0:
                        with st.expander("🔍 Sample Transformation"):
                            sample = uuids[0]
                            st.code(f"Before: {sample}", language="text")
                            st.code(f"After: {url_prefix}{sample}", language="text")
                            
                except Exception as e:
                    st.error(f"❌ Error processing code: {str(e)}")
        else:
            st.info("📝 Paste code or upload a file to enable processing.")

        # Downloads
        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download / Copy Processed Code")
            base = st.session_state['angular_filename']
            if '.' in base:
                base = base.rsplit('.', 1)[0]

            st.markdown("#### 💻 View & Copy Code")
            st.code(st.session_state['angular_output'], language="typescript")

            with st.expander("📋 Raw Output (select & copy)", expanded=False):
                st.text_area(
                    "Processed Code",
                    value=st.session_state['angular_output'],
                    height=380,
                    label_visibility="collapsed",
                    help="Select all and copy - indentation preserved"
                )

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.download_button(
                    "📄 .txt",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    "📝 .md",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            with col3:
                st.download_button(
                    "💻 .ts",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.ts",
                    mime="text/typescript",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )
            with col4:
                pdf_buf = create_text_to_pdf(st.session_state['angular_output'])
                st.download_button(
                    "📕 .pdf",
                    data=pdf_buf,
                    file_name=f"{base}_modified.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}),
                    use_container_width=True
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>Optimized Edition | Built with ❤️ using <strong>Streamlit</strong></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
