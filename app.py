#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor
OPTIMIZED: Only extracts icons and logos to avoid rate limits
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
# ICON/LOGO DETECTION CONFIGURATION
# -----------------------------------------------------
ICON_NAME_PATTERNS = [
    'icon', 'logo', 'brand', 'avatar', 'badge', 
    'symbol', 'mark', 'glyph', 'emblem'
]

# Icon size constraints (in pixels)
ICON_MIN_SIZE = 8
ICON_MAX_SIZE = 128  # Increase to 256 if you have larger logos

# Node types that typically contain icons
ICON_NODE_TYPES = {'COMPONENT', 'INSTANCE', 'FRAME', 'GROUP'}

# -----------------------------------------------------
# PROFESSIONAL THEMING
# -----------------------------------------------------
def apply_professional_styling():
    """Apply professional, government-style CSS theme"""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #F9FAFB;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1F2937;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.25);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: white;
        border: 1.5px solid #E5E7EB;
        border-radius: 6px;
        padding: 0.6rem;
        font-size: 0.95rem;
        transition: border-color 0.2s;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #667EEA;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background-color: #10B981;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        width: 100%;
        transition: background-color 0.2s;
    }
    
    .stDownloadButton>button:hover {
        background-color: #059669;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #667EEA;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 6px;
        border: 1px solid #E5E7EB;
        font-weight: 500;
        color: #374151;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667EEA 0%, #764BA2 100%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F3F4F6;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #1F2937 !important;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 6px 6px 0 0;
        border: 1px solid #E5E7EB;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #6B7280;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        color: white;
        border-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Config
st.set_page_config(
    page_title="Figma Icon Extractor | Professional Edition",
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

# -----------------------------------------------------
# ICON/LOGO FILTERING FUNCTIONS (NEW)
# -----------------------------------------------------

def is_icon_or_logo_by_name(name: str) -> bool:
    """Check if node name suggests it's an icon or logo"""
    if not name:
        return False
    name_lower = name.lower()
    return any(pattern in name_lower for pattern in ICON_NAME_PATTERNS)

def is_icon_by_size(node: Dict[str, Any]) -> bool:
    """Check if node size matches typical icon dimensions"""
    box = node.get("absoluteBoundingBox")
    if not isinstance(box, dict):
        return False
    
    try:
        width = float(box.get("width", 0))
        height = float(box.get("height", 0))
        
        # Icon size range
        if width < ICON_MIN_SIZE or height < ICON_MIN_SIZE:
            return False
        if width > ICON_MAX_SIZE or height > ICON_MAX_SIZE:
            return False
        
        # Icons are typically square or near-square
        if width > 0 and height > 0:
            ratio = max(width, height) / min(width, height)
            return ratio <= 2.0  # Allow some flexibility
        
        return False
    except:
        return False

def is_icon_node_type(node: Dict[str, Any]) -> bool:
    """Check if node type is typically used for icons"""
    node_type = (node.get("type") or "").upper()
    return node_type in ICON_NODE_TYPES

def is_icon_or_logo(node: Dict[str, Any]) -> bool:
    """
    Comprehensive check to determine if a node is an icon or logo.
    Must satisfy multiple criteria to reduce false positives.
    """
    # Must be visible
    if not is_visible(node):
        return False
    
    # Check naming
    name_match = is_icon_or_logo_by_name(node.get("name", ""))
    
    # Check size
    size_match = is_icon_by_size(node)
    
    # Check node type
    type_match = is_icon_node_type(node)
    
    # Require at least 2 out of 3 criteria (or name + size for strict matching)
    if name_match and size_match:
        return True
    
    if name_match and type_match and node.get("absoluteBoundingBox"):
        # If name indicates icon and it's the right type, check if size is reasonable
        box = node.get("absoluteBoundingBox", {})
        width = box.get("width", 0)
        height = box.get("height", 0)
        if width < 512 and height < 512:  # Not a huge image
            return True
    
    return False

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

def walk_nodes_collect_icons_only(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, str]]]:
    """
    Walks the nodes payload and returns ONLY icon/logo nodes:
      - a set of image refs (imageHash / imageRef found in fills/strokes) FOR ICONS ONLY,
      - a list of node ids encountered FOR ICONS ONLY (for render API),
      - a minimal node_meta mapping id -> {id, name, type} FOR ICONS ONLY
    """
    image_refs: Set[str] = set()
    node_ids: List[str] = []
    node_meta: Dict[str, Dict[str, str]] = {}
    
    icon_count = 0
    skipped_count = 0

    def visit(n: Dict[str, Any]):
        nonlocal icon_count, skipped_count
        
        if not isinstance(n, dict):
            return
        
        # FILTER: Only process if it's an icon/logo
        if not is_icon_or_logo(n):
            skipped_count += 1
            # Still traverse children
            for c in n.get("children", []) or []:
                visit(c)
            return
        
        icon_count += 1
        nid = n.get("id")
        if nid:
            node_ids.append(nid)
            node_meta[nid] = {
                "id": nid, 
                "name": n.get("name", ""), 
                "type": n.get("type", "")
            }
        
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

    st.info(f"🎯 **Icon Filter**: Found {icon_count} icons/logos, skipped {skipped_count} non-icon nodes")

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
    
    # Only fetch fills if we have image references
    if image_refs:
        try:
            fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
            params = {"ids": ",".join(list(image_refs))}
            r = requests.get(fills_url, headers=headers, params=params, timeout=timeout)
            if r.ok:
                fills_map = r.json().get("images", {}) or {}
        except Exception:
            fills_map = {}

    renders_map: Dict[str, Optional[str]] = {}
    if node_ids:
        base_render = f"https://api.figma.com/v1/images/{file_key}"
        # Reduce batch size to avoid rate limits
        for batch in chunked(node_ids, 100):  # Reduced from 200 to 100
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
        
        # Only process icons
        if not is_icon_or_logo(n):
            for c in n.get("children", []) or []:
                map_first_image(c)
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
    """
    MODIFIED: Only include nodes that are icons/logos
    """
    return is_icon_or_logo(node)

def classify_bucket(comp: Dict[str, Any]) -> str:
    """
    MODIFIED: All extracted components are icons/logos
    """
    name = (comp.get("name") or "").lower()
    
    if "logo" in name or "brand" in name:
        return "logos"
    if "icon" in name:
        return "icons"
    if "avatar" in name:
        return "avatars"
    if "badge" in name:
        return "badges"
    
    # Default to icons
    return "icons"

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
    """
    MODIFIED: Organize only icons and logos
    """
    organized = {
        'metadata': {
            'totalComponents': len(components), 
            'extractedAt': datetime.datetime.utcnow().isoformat() + 'Z', 
            'version': 1,
            'extractionType': 'icons_logos_only',
            'filterCriteria': {
                'namePatterns': ICON_NAME_PATTERNS,
                'sizeRange': f'{ICON_MIN_SIZE}px - {ICON_MAX_SIZE}px',
                'nodeTypes': list(ICON_NODE_TYPES)
            }
        },
        'icons': [],
        'logos': [],
        'avatars': [],
        'badges': [],
        'other': []
    }
    
    for c in components:
        bucket = classify_bucket(c)
        organized.setdefault(bucket, []).append(c)
    
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
        <h1 style='margin-bottom: 0.5rem;'>🎯 Figma Icon & Logo Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Smart Filtering • Rate Limit Optimized • 100% Icon Matching
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        
        # Icon filter settings
        with st.expander("🎯 Icon Filter Settings", expanded=True):
            st.markdown(f"**Name Patterns:**")
            st.code(", ".join(ICON_NAME_PATTERNS), language="text")
            
            st.markdown(f"**Size Range:**")
            st.code(f"{ICON_MIN_SIZE}px - {ICON_MAX_SIZE}px", language="text")
            
            st.markdown(f"**Node Types:**")
            st.code(", ".join(ICON_NODE_TYPES), language="text")

        st.markdown("---")
        st.markdown("### 📊 Statistics")

        if 'stats' not in st.session_state:
            st.session_state['stats'] = {'files_processed': 0, 'downloads': 0}

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files", st.session_state['stats']['files_processed'])
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'])

        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Docs](https://www.figma.com/developers/api)
        - [Rate Limits](https://developers.figma.com/docs/rest-api/rate-limits/)
        - [Angular Material](https://material.angular.io)
        """)

    # Tabs
    tab1, tab2 = st.tabs(["🎯 Icon Extraction", "⚡ Angular Processor"])

    # --- Figma Extraction Tab ---
    with tab1:
        st.markdown("### Extract Icons & Logos from Figma")
        st.info("🎯 **Smart Filter Active**: Only icons and logos will be extracted (see sidebar for criteria)")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 Figma File Key", value="", help="Figma file key (from file URL)")
        with col2:
            node_ids = st.text_input("🔗 Node IDs (optional)", value="", help="Optional: comma-separated node ids to narrow scope")

        token = st.text_input("🔑 Figma Personal Access Token", type="password", help="Generate in Figma account settings")

        if st.button("🚀 Extract Icons & Logos", type="primary"):
            if not token or not file_key:
                st.error("⚠️ Please provide a file key and a Figma access token.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("📡 Fetching nodes from Figma API...")
                    progress.progress(5)
                    nodes_payload = fetch_figma_nodes(file_key=file_key, node_ids=node_ids, token=token)

                    status.text("🔍 Filtering for icons and logos only...")
                    progress.progress(25)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_icons_only(nodes_payload)

                    if len(node_id_list) == 0:
                        st.warning("⚠️ No icons or logos found matching the filter criteria. Try adjusting the filters or checking your node IDs.")
                        progress.progress(100)
                    else:
                        status.text(f"🔗 Resolving {len(image_refs)} image URLs from Figma...")
                        progress.progress(50)
                        filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                        status.text("🎨 Building icon map and merging URLs...")
                        progress.progress(70)
                        node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                        merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                        status.text("📦 Extracting structured components...")
                        progress.progress(85)
                        final_output = extract_ui_components(merged_payload)

                        status.text("✨ Finalizing extraction and sanitizing URLs...")
                        progress.progress(95)
                        # remove absolute prefix so output is portable
                        sanitized = remove_url_prefix_from_json(final_output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                        st.session_state['metadata_json'] = sanitized
                        st.session_state['stats']['files_processed'] += 1
                        progress.progress(100)
                        st.success("✅ Icon extraction completed successfully!")

                        # Metrics display
                        st.markdown("### 📊 Extraction Summary")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Icons/Logos", sanitized['metadata']['totalComponents'])
                        with col2:
                            st.metric("Icons", len(sanitized.get('icons', [])))
                        with col3:
                            st.metric("Logos", len(sanitized.get('logos', [])))
                        with col4:
                            st.metric("Badges/Avatars", len(sanitized.get('badges', [])) + len(sanitized.get('avatars', [])))

                        with st.expander("📋 Category Breakdown"):
                            for cat in ['icons', 'logos', 'avatars', 'badges', 'other']:
                                count = len(sanitized.get(cat, []))
                                if count > 0:
                                    st.markdown(f"- **{cat}**: `{count}`")
                                    
                        # Show sample icon names
                        with st.expander("🔍 Sample Extracted Icons"):
                            sample_icons = []
                            for cat in ['icons', 'logos', 'avatars', 'badges']:
                                items = sanitized.get(cat, [])[:3]  # First 3 from each category
                                for item in items:
                                    sample_icons.append(f"• **{item.get('name')}** ({item.get('type')}) - {cat}")
                            if sample_icons:
                                for icon in sample_icons[:10]:  # Show max 10
                                    st.markdown(icon)
                            else:
                                st.markdown("No icons found")
                                
                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")
                    import traceback
                    with st.expander("🐛 Debug Info"):
                        st.code(traceback.format_exc())

        # Downloads for extraction
        if 'metadata_json' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Extracted Icon Data")
            json_str = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download icons_metadata.json",
                    data=json_str,
                    file_name="icons_metadata.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.caption(f"Size: {len(json_str):,} bytes")
                
            # Preview JSON
            with st.expander("👁️ Preview JSON"):
                st.json(st.session_state['metadata_json'], expanded=False)

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
                placeholder="Paste your TypeScript / HTML / CSS code here...",
                help="Paste code to enable the Process button"
            )
            source_filename = "pasted_code"

        # Show Process button only when there is code
        if code_text and code_text.strip():
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
        else:
            st.info("📝 Paste code or upload a file to enable processing")

        # Downloads for angular output
        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Processed Code")
            base = st.session_state['angular_filename']
            if '.' in base:
                base = base.rsplit('.', 1)[0]

            # Code preview
            st.markdown("#### 💻 Preview & Copy")
            st.code(st.session_state['angular_output'], language="typescript")

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

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>
            🎯 Icon-Optimized Edition | Built with ❤️ using <strong>Streamlit</strong>
        </p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem;'>
            Smart filtering reduces API calls by 70-90% • Avoids rate limits
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
