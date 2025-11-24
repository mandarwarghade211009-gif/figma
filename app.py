#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor
Optimized for icon/logo/symbol images only.
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
    /* keep your original styling here */
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
# GENERIC HELPERS
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
# FIGMA FETCH & ICON FILTERING
# -----------------------------------------------------
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

def is_logo_or_icon_node(node: Dict[str, Any]) -> bool:
    """
    Heuristic: decide if this node represents a logo/icon/symbol we care about.
    You can refine this for your file naming conventions.
    """
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    path = "/".join(node.get("path_parts", [])) if node.get("path_parts") else ""

    # text-based fontawesome icons
    style = node.get("style") or {}
    font_family = (style.get("fontFamily") or "").lower()

    if "logo" in name or "brand" in name or "symbol" in name:
        return True
    if "icon" in name or "glyph" in name or "fa-" in name:
        return True
    if "font awesome" in font_family:
        return True
    if any(k in path.lower() for k in ["iconset", "icons", "logo", "symbols"]):
        return True
    if t in ["COMPONENT", "INSTANCE"] and ("icon" in name or "logo" in name):
        return True

    return False

def annotate_paths(root: Dict[str, Any], parent_path: Optional[List[str]] = None):
    """
    Attach a 'path_parts' array to each node for better name-based heuristics.
    """
    if parent_path is None:
        parent_path = []
    if not isinstance(root, dict):
        return
    name = root.get("name") or "Unnamed"
    current_path = parent_path + [name]
    root["path_parts"] = current_path
    for c in root.get("children", []) or []:
        if isinstance(c, dict):
            annotate_paths(c, current_path)

def walk_for_icon_image_refs(nodes_payload: Dict[str, Any]) -> Set[str]:
    """
    Walk the Figma document and collect ONLY imageRef/imageHash that:
      - belong to nodes classified as logo/icon/symbol, OR
      - are fills/strokes on those nodes.
    """
    refs: Set[str] = set()

    def visit(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        if is_logo_or_icon_node(n):
            for f in n.get("fills", []) or []:
                if isinstance(f, dict) and f.get("type") == "IMAGE":
                    ref = f.get("imageRef") or f.get("imageHash")
                    if ref:
                        refs.add(ref)
            for s in n.get("strokes", []) or []:
                if isinstance(s, dict) and s.get("type") == "IMAGE":
                    ref = s.get("imageRef") or s.get("imageHash")
                    if ref:
                        refs.add(ref)
        for c in n.get("children", []) or []:
            visit(c)

    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                annotate_paths(doc)
                visit(doc)
    elif isinstance(nodes_payload.get("document"), dict):
        doc = nodes_payload["document"]
        annotate_paths(doc)
        visit(doc)

    return refs

def resolve_icon_image_urls(file_key: str, image_refs: Set[str], token: str, timeout: int = 60) -> Dict[str, str]:
    """
    Resolve ONLY the imageRefs for logo/icon/symbol nodes using /files/{key}/images.
    Returns mapping imageRef -> full URL.
    """
    headers = build_headers(token)
    base_url = f"https://api.figma.com/v1/files/{file_key}/images"
    out: Dict[str, str] = {}

    if not image_refs:
        return out

    ids_list = list(image_refs)
    for batch in chunked(ids_list, 200):
        params = {"ids": ",".join(batch)}
        try:
            r = requests.get(base_url, headers=headers, params=params, timeout=timeout)
            if not r.ok:
                st.warning(f"Figma /images error {r.status_code}: {r.text}")
                continue
            data = r.json() or {}
            images_map = data.get("images", {}) or {}
            for img_id, url in images_map.items():
                if url:
                    out[img_id] = url
        except Exception as e:
            st.error(f"Error resolving icon images: {e}")
    return out

def merge_icon_urls_into_nodes(nodes_payload: Dict[str, Any], icon_ref_to_url: Dict[str, str]) -> Dict[str, Any]:
    """
    Deep copy payload and only inject imageUrl for nodes classified as logo/icon/symbol.
    """
    merged = copy.deepcopy(nodes_payload)

    def visit(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        if is_logo_or_icon_node(n):
            # attach first relevant image URL if any
            for f in n.get("fills", []) or []:
                if isinstance(f, dict) and f.get("type") == "IMAGE":
                    ref = f.get("imageRef") or f.get("imageHash")
                    if ref and ref in icon_ref_to_url:
                        n["imageUrl"] = icon_ref_to_url[ref]
                        break
        for c in n.get("children", []) or []:
            visit(c)

    if isinstance(merged.get("nodes"), dict):
        for entry in merged["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                annotate_paths(doc)
                visit(doc)
    elif isinstance(merged.get("document"), dict):
        doc = merged["document"]
        annotate_paths(doc)
        visit(doc)

    return merged

# -----------------------------------------------------
# EXTRACTION HELPERS (CLEAN JSON FOR ANGULAR)
# -----------------------------------------------------
def extract_bounds(node: Dict[str, Any]) -> Optional[Dict[str, float]]:
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
    has_visual = bool(node.get("fills") or node.get("strokes") or node.get("effects") or node.get("imageUrl"))
    semantic = any(k in name for k in [
        'button', 'input', 'search', 'nav', 'menu', 'container', 'card', 'panel',
        'header', 'footer', 'badge', 'chip', 'logo', 'icon'
    ])
    vector_visible = (
        t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE']
        and (node.get("strokes") or node.get("fills"))
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
    if comp.get("imageUrl"):
        # These should now be only logo/icon/symbol
        return "images"
    if t in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE']:
        return "vectors"
    if t in ['FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'SECTION'] or any(
        k in name for k in ['container', 'card', 'panel', 'section']
    ):
        return "containers"
    return "other"

def extract_components(root: Dict[str, Any], parent_path: str = "", out: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
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

    # Only nodes flagged earlier as logo/icon/symbol will have imageUrl
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

def organize_for_angular(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    organized = {
        'metadata': {
            'totalComponents': len(components),
            'extractedAt': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': 1
        },
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
    Strip Figma host from imageUrl for portability.
    """
    p = copy.deepcopy(payload)

    def process(obj: Any):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k == "imageUrl" and isinstance(v, str) and v.startswith(url_prefix):
                    obj[k] = v.replace(url_prefix, "", 1)
                else:
                    process(v)
        elif isinstance(obj, list):
            for item in obj:
                process(item)

    process(p)
    return p

# -----------------------------------------------------
# ANGULAR CODE + FOCUSED URL RESOLUTION
# -----------------------------------------------------
UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def detect_uuids_in_text(text: str) -> List[str]:
    pattern = re.compile(UUID_RE, re.IGNORECASE)
    found = pattern.findall(text)
    seen = set()
    out = []
    for f in found:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out

def resolve_image_urls_for_uuids(
    file_key: str,
    uuids: List[str],
    token: str,
    timeout: int = 60
) -> Dict[str, str]:
    """
    Resolve full Figma URLs ONLY for UUIDs from Angular code.
    """
    headers = build_headers(token)
    base_url = f"https://api.figma.com/v1/files/{file_key}/images"
    uuid_to_url: Dict[str, str] = {}
    unique_uuids = list(dict.fromkeys(uuids))

    for batch in chunked(unique_uuids, 200):
        params = {"ids": ",".join(batch)}
        try:
            r = requests.get(base_url, headers=headers, params=params, timeout=timeout)
            if not r.ok:
                st.warning(f"Figma /images error {r.status_code}: {r.text}")
                continue
            data = r.json() or {}
            images_map = data.get("images", {}) or {}
            for img_id, url in images_map.items():
                if url:
                    uuid_to_url[img_id] = url
        except Exception as e:
            st.error(f"Exception while resolving UUID images: {e}")
    return uuid_to_url

def add_full_urls_to_angular_code(text: str, uuid_to_url: Dict[str, str]) -> Tuple[str, int]:
    """
    Replace quoted UUIDs with their full Figma URLs when available.
    """
    total_replacements = 0

    def repl(m: re.Match) -> str:
        nonlocal total_replacements
        q1, uuid, q2 = m.groups()
        url = uuid_to_url.get(uuid)
        if not url:
            return m.group(0)
        total_replacements += 1
        return f"{q1}{url}{q2}"

    pattern = re.compile(r'(["\'])(' + UUID_RE + r')(["\'])', re.IGNORECASE)
    modified = pattern.sub(repl, text)
    return modified, total_replacements

def create_text_to_pdf(text_content: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch
    )
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle(
        'Code',
        parent=styles.get('Normal'),
        fontName='Courier',
        fontSize=8,
        leading=10,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=6
    )
    story = []
    lines = text_content.splitlines()
    chunk_size = 60
    for i in range(0, len(lines), chunk_size):
        block = lines[i:i+chunk_size]
        safe = [
            ln.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            for ln in block
        ]
        story.append(Paragraph('<br/>'.join(safe), code_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

def decode_bytes_to_text(raw: bytes) -> str:
    try:
        return raw.decode('utf-8')
    except Exception:
        try:
            return raw.decode('latin-1')
        except Exception:
            return raw.decode('utf-8', errors='ignore')

# -----------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------
def main():
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='margin-bottom: 0.5rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Optimized Icon/Logo Extraction & Angular Code URL Injection
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

    tab1, tab2 = st.tabs(["🎯 Figma Extraction", "⚡ Angular Processor"])

    # -------- Figma Extraction --------
    with tab1:
        st.markdown("### Figma Component Extraction (Icons/Logos Only for imageUrl)")
        st.markdown("Metadata is extracted for all components; imageUrl is only set for logo/icon/symbol nodes.")
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
                    progress.progress(10)
                    nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                    status.text("🎯 Collecting logo/icon image references only...")
                    progress.progress(30)
                    icon_refs = walk_for_icon_image_refs(nodes_payload)

                    status.text("🔗 Resolving icon/logo URLs from Figma...")
                    progress.progress(55)
                    icon_ref_to_url = resolve_icon_image_urls(file_key, icon_refs, token)

                    status.text("🎨 Merging icon URLs into nodes (imageUrl only on icons/logos)...")
                    progress.progress(75)
                    merged_payload = merge_icon_urls_into_nodes(nodes_payload, icon_ref_to_url)

                    status.text("📦 Extracting structured components...")
                    progress.progress(90)
                    final_output = extract_ui_components(merged_payload)

                    # Optional: keep UUIDs only in JSON (strip prefix), or keep full URLs if you prefer.
                    # Here we keep UUIDs (cleaner for Angular mapping).
                    sanitized = remove_url_prefix_from_json(
                        final_output,
                        "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/"
                    )

                    st.session_state['metadata_json'] = sanitized
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    st.success("✅ Extraction completed successfully!")

                    st.markdown("### 📊 Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", sanitized['metadata']['totalComponents'])
                    with col2:
                        st.metric("Text Elements", len(sanitized.get('textElements', [])))
                    with col3:
                        st.metric("Buttons", len(sanitized.get('buttons', [])))
                    with col4:
                        st.metric("Icon/Logo Images", len(sanitized.get('images', [])))

                    with st.expander("📋 Category Breakdown"):
                        for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
                            count = len(sanitized.get(cat, []))
                            if count > 0:
                                st.markdown(f"- **{cat}**: `{count}`")
                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")

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
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}
                    )
                )
            with col2:
                st.caption(f"Size: {len(json_str):,} bytes")

    # -------- Angular Processor --------
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Resolve ONLY UUIDs used in Angular code to full Figma image URLs and rewrite the code.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key_for_urls = st.text_input(
                "📁 Figma File Key (for URL resolution)",
                value="",
                help="Used to resolve image URLs for UUIDs detected in the uploaded code."
            )
        with col2:
            token_for_urls = st.text_input(
                "🔑 Figma Token (for URL resolution)",
                type="password",
                help="Figma token for resolving image URLs."
            )

        uploaded = st.file_uploader(
            "📤 Upload Angular Code File",
            type=['txt', 'md', 'html', 'ts', 'js', 'pdf'],
            help="Supported formats: .txt, .md, .html, .ts, .js, .pdf"
        )

        if uploaded:
            st.info(f"✅ File uploaded: **{uploaded.name}**")

            if st.button("⚡ Process Angular Code"):
                try:
                    raw = uploaded.read()
                    text = decode_bytes_to_text(raw)
                    if uploaded.name.lower().endswith('.pdf'):
                        st.warning("⚠️ PDF->text extraction is basic; results may vary.")

                    uuids = detect_uuids_in_text(text)
                    if not uuids:
                        st.warning("No UUIDs detected in the uploaded file.")
                        return

                    if not file_key_for_urls or not token_for_urls:
                        st.error("Please provide Figma file key and token to resolve full URLs.")
                        return

                    st.info(f"Resolving {len(uuids)} UUIDs from Figma...")
                    uuid_to_url = resolve_image_urls_for_uuids(
                        file_key=file_key_for_urls,
                        uuids=uuids,
                        token=token_for_urls
                    )

                    if not uuid_to_url:
                        st.error("No image URLs could be resolved from Figma for the detected UUIDs.")
                        return

                    modified, replaced = add_full_urls_to_angular_code(text, uuid_to_url)

                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = uploaded.name
                    st.session_state['stats']['files_processed'] += 1

                    st.success("✅ Angular code processed successfully!")

                    st.markdown("### 📊 Processing Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("UUIDs Found", len(uuids))
                    with col2:
                        st.metric("URLs Resolved", len(uuid_to_url))
                    with col3:
                        st.metric("Replacements Made", replaced)

                    with st.expander("🔍 Sample Mapping"):
                        sample_uuid = next(iter(uuid_to_url.keys()))
                        st.code(f"UUID: {sample_uuid}", language="text")
                        st.code(f"URL:  {uuid_to_url[sample_uuid]}", language="text")

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
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}
                    )
                )
            with col2:
                st.download_button(
                    "📝 Download as .md",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}
                    )
                )
            with col3:
                pdf_buf = create_text_to_pdf(st.session_state['angular_output'])
                st.download_button(
                    "📕 Download as .pdf",
                    data=pdf_buf,
                    file_name=f"{base}_modified.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1}
                    )
                )

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>Built with ❤️ using <strong>Streamlit</strong> | Professional Edition</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
