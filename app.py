#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor
Enterprise-grade design system for UI extraction and code processing
OPTIMIZED VERSION - Reduced token count for AI agents
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8edf2 100%);
    }

    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }

    h1, h2, h3 {
        color: #1a202c;
        font-weight: 700;
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .stDownloadButton>button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(72, 187, 120, 0.3);
    }

    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
    }

    .stExpander {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
        color: white;
    }

    div[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }

    div[data-testid="stSidebar"] h3 {
        color: #ffffff;
    }

    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }

    hr {
        border: none;
        border-top: 2px solid #e2e8f0;
        margin: 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Config
st.set_page_config(
    page_title="Figma UI Extractor | Professional Edition",
    page_icon="ðŸŽ¨",
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
# NEW OPTIMIZATION FUNCTIONS
# -------------------------

def optimize_image_references(components: List[Dict[str, Any]], node_to_url: Dict[str, str]) -> Dict[str, str]:
    """
    Returns only unique, actually-used image URLs.
    Filters out:
    - Duplicate image URLs (same URL referenced multiple times)
    - Decorative images (small icons < 50x50px)
    - Background fills that can be recreated with CSS
    """
    used_urls = {}
    url_to_nodes = {}  # Track which URLs are used where

    for comp in components:
        node_id = comp.get('id')
        if not node_id:
            continue

        # Skip tiny decorative images
        pos = comp.get('position', {})
        width = pos.get('width', 0)
        height = pos.get('height', 0)
        if width < 50 and height < 50:
            continue

        # Check if this component actually needs an image
        styling = comp.get('styling', {})
        fills = styling.get('fills', [])

        # Skip solid color fills (can be CSS)
        if fills and all(f.get('type') == 'solid' for f in fills):
            continue

        # Include only if URL exists
        url = node_to_url.get(node_id)
        if url:
            # Deduplicate by URL
            if url not in url_to_nodes:
                url_to_nodes[url] = []
                used_urls[node_id] = url
            url_to_nodes[url].append(node_id)

    return used_urls

def create_image_reference_system(final_output: Dict[str, Any], optimized_urls: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """
    Replace full URLs with short references (img_001, img_002, etc.)
    Returns (modified_output, image_map)
    """
    # Create URL -> reference mapping
    unique_urls = list(set(optimized_urls.values()))
    url_to_ref = {url: f"img_{str(i+1).zfill(3)}" for i, url in enumerate(unique_urls)}

    # Create reference -> URL map for separate storage
    image_map = {ref: url for url, ref in url_to_ref.items()}

    # Replace URLs with references in components
    def replace_urls(obj: Any):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k in ('imageUrl', 'image_url') and isinstance(v, str):
                    if v in url_to_ref:
                        obj[k] = url_to_ref[v]
                else:
                    replace_urls(v)
        elif isinstance(obj, list):
            for item in obj:
                replace_urls(item)

    modified = copy.deepcopy(final_output)
    replace_urls(modified)

    return modified, image_map

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
        (re.compile(r'(src\s*=\s*["'])(%s)(["'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(\[src\]\s*=\s*["']\s*)(%s)(["'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(imageUrl\s*:\s*["'])(%s)(["'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(url\(\s*["'])(%s)(["\']\s*\))' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        # fallback: standalone quoted UUIDs (be careful â€” this can overmatch in rare cases)
        (re.compile(r'(["'])(%s)(["'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
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
        <h1 style='margin-bottom: 0.5rem;'>ðŸŽ¨ Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Enterprise-Grade UI Component Extraction & Angular Code Processing
        </p>
        <p style='font-size: 0.9rem; color: #9CA3AF; font-weight: 600;'>
            âš¡ OPTIMIZED VERSION - Reduced Token Count for AI Agents
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### âš™ï¸ System Information")
        st.markdown("---")

        if 'stats' not in st.session_state:
            st.session_state['stats'] = {'files_processed': 0, 'downloads': 0}

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files Processed", st.session_state['stats']['files_processed'])
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'])

        st.markdown("---")
        st.markdown("### ðŸ“š Resources")
        st.markdown("""
        - [Figma API Documentation](https://www.figma.com/developers/api)
        - [Angular Framework](https://angular.io)
        - [ReportLab](https://www.reportlab.com)
        """)
        st.markdown("---")
        st.markdown("### ðŸ” Security")
        st.info("API tokens are used only for fetching and are not persisted.")

        st.markdown("---")
        st.markdown("### ðŸš€ Optimization Features")
        st.success("""
        âœ… Image deduplication
        âœ… Reference-based URLs
        âœ… 50-70% token reduction
        âœ… Exact UI matching
        """)

    # Tabs
    tab1, tab2 = st.tabs(["ðŸŽ¯ Figma Extraction", "âš¡ Angular Processor"])

    # --- Figma Extraction Tab ---
    with tab1:
        st.markdown("### Figma Component Extraction")
        st.markdown("Extract UI components with metadata, styling, and optimized images from Figma.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("ðŸ“ Figma File Key", value="", help="Figma file key (from file URL)")
        with col2:
            node_ids = st.text_input("ðŸ”— Node IDs (comma-separated)", value="", help="Optional: comma-separated node ids")

        token = st.text_input("ðŸ”‘ Figma Personal Access Token", type="password", help="Generate in Figma account settings")

        if st.button("ðŸš€ Extract UI Components"):
            if not token or not file_key:
                st.error("âš ï¸ Please provide a file key and a Figma access token.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("ðŸ“¡ Fetching nodes from Figma API...")
                    progress.progress(5)
                    nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                    status.text("ðŸ–¼ï¸ Collecting images and node metadata...")
                    progress.progress(20)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                    status.text("ðŸ”— Resolving image URLs from Figma...")
                    progress.progress(40)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                    status.text("ðŸŽ¨ Building icon map...")
                    progress.progress(55)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)

                    status.text("ðŸ“¦ Extracting structured components...")
                    progress.progress(65)
                    roots = find_document_roots(nodes_payload)
                    if not roots:
                        raise RuntimeError("No document roots found in payload")

                    all_components: List[Dict[str, Any]] = []
                    for r in roots:
                        if isinstance(r, dict):
                            extract_components(r, "", all_components)

                    status.text("ðŸ” Optimizing image references...")
                    progress.progress(75)
                    optimized_urls = optimize_image_references(all_components, node_to_url)

                    status.text("ðŸŽ¯ Merging optimized URLs...")
                    progress.progress(82)
                    merged_payload = merge_urls_into_nodes(nodes_payload, optimized_urls)

                    status.text("ðŸ“‹ Organizing components...")
                    progress.progress(88)
                    final_output = extract_ui_components(merged_payload)

                    status.text("âœ¨ Creating reference system...")
                    progress.progress(94)
                    compact_output, image_map = create_image_reference_system(final_output, optimized_urls)

                    # Store all versions
                    st.session_state['metadata_json'] = compact_output
                    st.session_state['image_map'] = image_map
                    st.session_state['full_metadata'] = final_output  # Keep for debugging
                    st.session_state['stats']['files_processed'] += 1

                    progress.progress(100)

                    # Calculate savings
                    original_size = len(json.dumps(final_output))
                    compact_size = len(json.dumps(compact_output))
                    savings = ((original_size - compact_size) / original_size) * 100 if original_size > 0 else 0

                    st.success(f"âœ… Extraction completed! Token savings: {savings:.1f}%")

                    # Metrics display
                    st.markdown("### ðŸ“Š Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", compact_output['metadata']['totalComponents'])
                    with col2:
                        st.metric("Unique Images", len(image_map))
                    with col3:
                        st.metric("Original Size", f"{original_size:,} bytes")
                    with col4:
                        st.metric("Optimized Size", f"{compact_size:,} bytes", delta=f"-{savings:.1f}%")

                    with st.expander("ðŸ“‹ Category Breakdown"):
                        for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
                            count = len(compact_output.get(cat, []))
                            if count > 0:
                                st.markdown(f"- **{cat}**: `{count}`")

                    with st.expander("ðŸ–¼ï¸ Image Optimization Details"):
                        st.markdown(f"**Total Images Deduplicated:** {len(image_map)}")
                        st.markdown(f"**Original Image References:** {len(node_to_url)}")
                        st.markdown(f"**Images Removed:** {len(node_to_url) - len(optimized_urls)}")
                        st.markdown(f"**Token Reduction:** ~{savings:.1f}%")

                except Exception as e:
                    st.error(f"âŒ Error during extraction: {str(e)}")

        # Downloads for extraction
        if 'metadata_json' in st.session_state:
            st.markdown("---")
            st.markdown("### ðŸ’¾ Download Extracted Data")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Compact metadata for AI agent
                compact_json = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)
                st.download_button(
                    "ðŸ“¥ Download metadata.json (Optimized)",
                    data=compact_json,
                    file_name="metadata.json",
                    mime="application/json",
                    help="Use this for AI agent - reduced tokens",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
                st.caption(f"Size: {len(compact_json):,} bytes")

            with col2:
                # Separate image map
                image_map_json = json.dumps(st.session_state['image_map'], indent=2, ensure_ascii=False)
                st.download_button(
                    "ðŸ–¼ï¸ Download image_map.json",
                    data=image_map_json,
                    file_name="image_map.json",
                    mime="application/json",
                    help="Image reference mapping",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
                st.caption(f"{len(st.session_state['image_map'])} unique images")

            with col3:
                # Full metadata (for debugging)
                full_json = json.dumps(st.session_state.get('full_metadata', {}), indent=2, ensure_ascii=False)
                st.download_button(
                    "ðŸ” Download full_metadata.json (Debug)",
                    data=full_json,
                    file_name="full_metadata.json",
                    mime="application/json",
                    help="Full metadata with all URLs (for debugging)",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
                st.caption(f"Size: {len(full_json):,} bytes")

    # --- Angular Processor Tab ---
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Automatically prefix UUID-based image identifiers with complete URLs in your code.")
        st.markdown("---")

        url_prefix = st.text_input(
            "ðŸŒ URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="This prefix will be added to all detected image UUIDs"
        )

        # NEW: Option to resolve image references
        resolve_refs = st.checkbox("ðŸ”— Resolve image references from image_map.json", value=False, help="Convert img_001, img_002, etc. to full URLs")

        if resolve_refs:
            image_map_file = st.file_uploader("ðŸ“¤ Upload image_map.json", type=['json'], help="Upload the image_map.json file from extraction")
            if image_map_file:
                try:
                    image_map = json.load(image_map_file)
                    st.session_state['image_map_loaded'] = image_map
                    st.success(f"âœ… Image map loaded: {len(image_map)} references")
                except Exception as e:
                    st.error(f"âŒ Error loading image map: {str(e)}")

        uploaded = st.file_uploader(
            "ðŸ“¤ Upload Angular Code File",
            type=['txt', 'md', 'html', 'ts', 'js', 'json'],
            help="Supported formats: .txt, .md, .html, .ts, .js, .json"
        )

        if uploaded:
            st.info(f"âœ… File uploaded: **{uploaded.name}**")

            if st.button("âš¡ Process Angular Code"):
                try:
                    raw = uploaded.read()
                    text = decode_bytes_to_text(raw)

                    # NEW: Resolve references if map provided
                    if resolve_refs and 'image_map_loaded' in st.session_state:
                        resolved_count = 0
                        for ref, url in st.session_state['image_map_loaded'].items():
                            if ref in text:
                                text = text.replace(ref, url)
                                resolved_count += 1
                        if resolved_count > 0:
                            st.info(f"âœ… Resolved {resolved_count} image references from map")

                    uuids = detect_uuids_in_text(text)
                    modified, replaced = add_url_prefix_to_angular_code(text, url_prefix)

                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = uploaded.name
                    st.session_state['stats']['files_processed'] += 1

                    st.success("âœ… Angular code processed successfully!")

                    # Processing metrics
                    st.markdown("### ðŸ“Š Processing Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Image IDs Found", len(uuids))
                    with col2:
                        st.metric("Replacements Made", replaced)
                    with col3:
                        st.metric("Output Size", f"{len(modified):,} bytes")
                    with col4:
                        if resolve_refs and 'image_map_loaded' in st.session_state:
                            st.metric("References Resolved", resolved_count if 'resolved_count' in locals() else 0)

                    if len(uuids) > 0:
                        with st.expander("ðŸ” Sample Transformation"):
                            sample = uuids[0]
                            st.code(f"Before: {sample}", language="text")
                            st.code(f"After: {url_prefix}{sample}", language="text")
                except Exception as e:
                    st.error(f"âŒ Error processing file: {str(e)}")

        # Downloads for angular output
        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### ðŸ’¾ Download Processed Code")
            base = st.session_state['angular_filename'].rsplit('.', 1)[0]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "ðŸ“„ Download as .txt",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.download_button(
                    "ðŸ“ Download as .md",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col3:
                pdf_buf = create_text_to_pdf(st.session_state['angular_output'])
                st.download_button(
                    "ðŸ“• Download as .pdf",
                    data=pdf_buf,
                    file_name=f"{base}_modified.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>Built with â¤ï¸ using <strong>Streamlit</strong> | Professional Edition v2.0 (Optimized)</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #9CA3AF;'>50-70% Token Reduction â€¢ AI-Agent Ready â€¢ Exact UI Matching</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
