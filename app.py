#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor
Enterprise-grade design system with RATE LIMIT HANDLING
"""

import streamlit as st
import requests
import json
import re
import datetime
import time
import random
from io import BytesIO
from typing import Any, Dict, List, Set, Tuple, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
import copy
from functools import wraps

# -----------------------------------------------------
# CONSTANTS & CONFIGURATION
# -----------------------------------------------------

IMAGE_WORTHY_TYPES = {'VECTOR', 'RECTANGLE', 'ELLIPSE', 'POLYGON', 'STAR', 'LINE', 'BOOLEAN_OPERATION'}
IMAGE_NAME_KEYWORDS = {'icon', 'logo', 'avatar', 'image', 'img', 'photo', 'picture', 'graphic', 'illustration', 'badge', 'emoji'}
DEFAULT_IMAGE_PREFIX = "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/"
API_BATCH_SIZE = 200
UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

# Rate limiting configuration
MAX_RETRIES = 6
INITIAL_RETRY_DELAY = 2  # seconds
MAX_RETRY_DELAY = 120    # seconds (2 minutes)
JITTER_MAX = 1.0         # seconds of random jitter

# -----------------------------------------------------
# RATE LIMIT HANDLING DECORATOR
# -----------------------------------------------------

def retry_with_exponential_backoff(max_retries=MAX_RETRIES):
    """
    Decorator that implements exponential backoff with jitter for API calls.
    Handles 429 rate limit errors from Figma API.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            retry_delay = INITIAL_RETRY_DELAY
            
            while retry_count <= max_retries:
                try:
                    response = func(*args, **kwargs)
                    return response
                    
                except requests.exceptions.HTTPError as e:
                    # Check if it's a 429 rate limit error
                    if e.response.status_code == 429:
                        retry_count += 1
                        
                        if retry_count > max_retries:
                            raise RuntimeError(
                                f"❌ Maximum retry attempts ({max_retries}) exceeded. "
                                f"Figma API rate limit still in effect. Please wait before retrying."
                            ) from e
                        
                        # Try to get Retry-After header from response
                        retry_after = e.response.headers.get('Retry-After')
                        
                        if retry_after:
                            try:
                                wait_time = int(retry_after)
                            except ValueError:
                                wait_time = retry_delay
                        else:
                            # Use exponential backoff with jitter
                            wait_time = min(retry_delay, MAX_RETRY_DELAY)
                            jitter = random.uniform(0, JITTER_MAX)
                            wait_time += jitter
                        
                        # Display user-friendly message
                        st.warning(
                            f"⏳ Rate limit hit (attempt {retry_count}/{max_retries}). "
                            f"Waiting {wait_time:.1f} seconds before retry..."
                        )
                        
                        # Wait before retrying
                        time.sleep(wait_time)
                        
                        # Exponentially increase delay for next attempt
                        retry_delay *= 2
                        
                    else:
                        # Not a rate limit error, re-raise
                        raise
                        
                except requests.exceptions.RequestException as e:
                    # Network or other request errors
                    raise RuntimeError(f"Network error: {str(e)}") from e
            
            # Should not reach here, but just in case
            raise RuntimeError("Unexpected error in retry logic")
        
        return wrapper
    return decorator

# -----------------------------------------------------
# PROFESSIONAL THEMING
# -----------------------------------------------------

def apply_professional_styling():
    """Apply professional, government-style CSS theme"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 700;
        color: #1a202c;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
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
    
    .stTextInput>div>div>input {
        border: 2px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
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
    """Build authorization headers for Figma API"""
    return {"Accept": "application/json", "X-Figma-Token": token}

def chunked(lst: List[str], n: int):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def to_rgba(color: Dict[str, Any]) -> str:
    """Convert Figma color object to CSS rgba string"""
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
        filtered_children = []
        for child in node["children"]:
            if isinstance(child, dict):
                filtered_child = filter_invisible_nodes(child)
                if filtered_child:
                    filtered_children.append(filtered_child)
        node["children"] = filtered_children
    
    return node

def is_image_worthy_node(node: Dict[str, Any]) -> bool:
    """Determines if a node should receive image URL assignment"""
    if not isinstance(node, dict):
        return False
    
    node_type = (node.get("type") or "").upper()
    type_match = node_type in IMAGE_WORTHY_TYPES
    
    node_name = (node.get("name") or "").lower()
    name_match = any(keyword in node_name for keyword in IMAGE_NAME_KEYWORDS)
    
    has_image_fill = False
    fills = node.get("fills") or []
    if isinstance(fills, list):
        for fill in fills:
            if isinstance(fill, dict) and fill.get("type") == "IMAGE":
                has_image_fill = True
                break
    
    criteria_met = sum([type_match, name_match, has_image_fill])
    return criteria_met >= 2 or has_image_fill

# -----------------------------------------------------
# FIGMA API OPERATIONS WITH RATE LIMITING
# -----------------------------------------------------

@retry_with_exponential_backoff(max_retries=MAX_RETRIES)
def fetch_figma_api(url: str, headers: Dict[str, str], params: Dict[str, Any], timeout: int) -> requests.Response:
    """
    Low-level Figma API fetch with automatic retry on 429 errors.
    This function is wrapped with exponential backoff decorator.
    """
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    return response

def fetch_figma_nodes(file_key: str, node_ids: str, token: str, timeout: int = 60) -> Dict[str, Any]:
    """
    Fetch nodes from Figma file with rate limit handling.
    """
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}"
    
    if node_ids:
        url += "/nodes"
        params = {"ids": node_ids}
    else:
        params = {}
    
    # Use rate-limited API call
    response = fetch_figma_api(url, headers, params, timeout)
    data = response.json()
    
    # Filter invisible nodes
    if isinstance(data.get("nodes"), dict):
        for key, value in list(data["nodes"].items()):
            doc = value.get("document")
            if isinstance(doc, dict):
                data["nodes"][key]["document"] = filter_invisible_nodes(doc)
    elif isinstance(data.get("document"), dict):
        data["document"] = filter_invisible_nodes(data["document"])
    
    return data

# -----------------------------------------------------
# NODE WALKING & DATA COLLECTION
# -----------------------------------------------------

def walk_nodes_collect_data(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str], Dict[str, Dict[str, Any]]]:
    """Single-pass node walking for data collection"""
    image_refs: Set[str] = set()
    node_ids: List[str] = []
    node_meta: Dict[str, Dict[str, Any]] = {}
    
    def visit(node: Dict[str, Any]):
        if not isinstance(node, dict):
            return
        
        node_id = node.get("id")
        if not node_id:
            for child in node.get("children", []) or []:
                visit(child)
            return
        
        node_ids.append(node_id)
        
        node_meta[node_id] = {
            "id": node_id,
            "name": node.get("name", ""),
            "type": node.get("type", ""),
            "is_image_worthy": is_image_worthy_node(node),
            "has_image_fill": False,
            "first_image_ref": None
        }
        
        fills = node.get("fills") or []
        if isinstance(fills, list):
            for fill in fills:
                if isinstance(fill, dict) and fill.get("type") == "IMAGE":
                    ref = fill.get("imageRef") or fill.get("imageHash")
                    if ref:
                        image_refs.add(ref)
                        node_meta[node_id]["has_image_fill"] = True
                        if not node_meta[node_id]["first_image_ref"]:
                            node_meta[node_id]["first_image_ref"] = ref
        
        strokes = node.get("strokes") or []
        if isinstance(strokes, list):
            for stroke in strokes:
                if isinstance(stroke, dict) and stroke.get("type") == "IMAGE":
                    ref = stroke.get("imageRef") or stroke.get("imageHash")
                    if ref:
                        image_refs.add(ref)
        
        for child in node.get("children", []) or []:
            visit(child)
    
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])
    
    # Deduplicate
    seen = set()
    unique_node_ids = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_node_ids.append(nid)
    
    return image_refs, unique_node_ids, node_meta

# -----------------------------------------------------
# IMAGE URL RESOLUTION WITH RATE LIMITING
# -----------------------------------------------------

def resolve_image_urls(
    file_key: str,
    image_refs: Set[str],
    node_meta: Dict[str, Dict[str, Any]],
    token: str,
    timeout: int = 60
) -> Tuple[Dict[str, str], Dict[str, Optional[str]]]:
    """
    Resolve image URLs with intelligent rate limit handling.
    """
    headers = build_headers(token)
    fills_map: Dict[str, str] = {}
    
    # Fetch fill images
    if image_refs:
        try:
            fills_url = f"https://api.figma.com/v1/files/{file_key}/images"
            # Use rate-limited fetch
            response = fetch_figma_api(fills_url, headers, {}, timeout)
            fills_map = response.json().get("images", {}) or {}
        except Exception as e:
            st.warning(f"⚠️ Could not fetch fill images: {str(e)}")
            fills_map = {}
    
    # Only fetch renders for image-worthy nodes
    image_worthy_ids = [
        nid for nid, meta in node_meta.items()
        if meta.get("is_image_worthy", False)
    ]
    
    renders_map: Dict[str, Optional[str]] = {}
    
    if image_worthy_ids:
        base_render_url = f"https://api.figma.com/v1/images/{file_key}"
        total_batches = (len(image_worthy_ids) + API_BATCH_SIZE - 1) // API_BATCH_SIZE
        
        for batch_idx, batch in enumerate(chunked(image_worthy_ids, API_BATCH_SIZE)):
            try:
                # Show progress
                st.text(f"🖼️ Fetching image batch {batch_idx + 1}/{total_batches}...")
                
                params = {"ids": ",".join(batch), "format": "svg"}
                
                # Use rate-limited fetch with automatic retry
                response = fetch_figma_api(base_render_url, headers, params, timeout)
                images_map = response.json().get("images", {}) or {}
                renders_map.update(images_map)
                
                # Small delay between batches to be API-friendly
                if batch_idx < total_batches - 1:
                    time.sleep(0.5)
                    
            except Exception as e:
                st.warning(f"⚠️ Batch {batch_idx + 1}/{total_batches} failed: {str(e)}")
                for nid in batch:
                    renders_map[nid] = None
    
    return fills_map, renders_map

def build_selective_icon_map(
    node_meta: Dict[str, Dict[str, Any]],
    fills_map: Dict[str, str],
    renders_map: Dict[str, Optional[str]]
) -> Dict[str, str]:
    """Build icon map only for image-worthy nodes"""
    node_to_url: Dict[str, str] = {}
    
    for node_id, meta in node_meta.items():
        if not meta.get("is_image_worthy", False):
            continue
        
        url = None
        first_ref = meta.get("first_image_ref")
        if first_ref:
            url = fills_map.get(first_ref)
        
        if not url:
            url = renders_map.get(node_id)
        
        if url:
            node_to_url[node_id] = url
    
    return node_to_url

def merge_urls_into_nodes(nodes_payload: Dict[str, Any], node_to_url: Dict[str, str]) -> Dict[str, Any]:
    """Merge URLs into nodes payload"""
    merged = copy.deepcopy(nodes_payload)
    url_node_ids = set(node_to_url.keys())
    
    def inject(node: Dict[str, Any]):
        if not isinstance(node, dict):
            return
        
        node_id = node.get("id")
        if node_id and node_id in url_node_ids:
            node["image_url"] = node_to_url[node_id]
        
        for child in node.get("children", []) or []:
            inject(child)
    
    if isinstance(merged.get("nodes"), dict):
        for entry in merged["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                inject(doc)
    
    if isinstance(merged.get("document"), dict):
        inject(merged["document"])
    
    return merged

# -----------------------------------------------------
# EXTRACTION HELPERS (keeping previous implementations)
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
    layout_keys = [
        'layoutMode', 'constraints', 'paddingLeft', 'paddingRight',
        'paddingTop', 'paddingBottom', 'itemSpacing', 'counterAxisAlignItems',
        'primaryAxisAlignItems', 'layoutGrow', 'layoutAlign',
        'layoutSizingHorizontal', 'layoutSizingVertical',
        'counterAxisSizingMode', 'primaryAxisSizingMode',
        'clipsContent', 'layoutWrap', 'layoutGrids'
    ]
    return {k: node[k] for k in layout_keys if k in node}

def extract_visuals(node: Dict[str, Any]) -> Dict[str, Any]:
    styling: Dict[str, Any] = {}
    
    fills = node.get("fills")
    if is_nonempty_list(fills):
        parsed_fills = []
        for fill in fills:
            if not isinstance(fill, dict):
                continue
            
            entry: Dict[str, Any] = {}
            fill_type = fill.get("type")
            
            if fill_type == "SOLID" and "color" in fill:
                entry["type"] = "solid"
                entry["color"] = to_rgba(fill["color"])
                if "opacity" in fill:
                    entry["opacity"] = fill["opacity"]
            else:
                if fill_type:
                    entry["type"] = fill_type.lower()
                if "imageRef" in fill:
                    entry["imageRef"] = fill["imageRef"]
                if "scaleMode" in fill:
                    entry["scaleMode"] = fill["scaleMode"]
            
            if entry:
                parsed_fills.append(entry)
        
        if parsed_fills:
            styling["fills"] = parsed_fills
    
    bg_color = node.get("backgroundColor")
    if isinstance(bg_color, dict):
        styling["backgroundColor"] = to_rgba(bg_color)
    
    strokes = node.get("strokes")
    if is_nonempty_list(strokes):
        borders = []
        stroke_weight = node.get("strokeWeight")
        stroke_align = node.get("strokeAlign")
        
        for stroke in strokes:
            if not isinstance(stroke, dict):
                continue
            
            border: Dict[str, Any] = {}
            
            if stroke.get("type") == "SOLID" and "color" in stroke:
                border["color"] = to_rgba(stroke["color"])
            
            if "opacity" in stroke:
                border["opacity"] = stroke["opacity"]
            
            if stroke_weight is not None:
                border["width"] = stroke_weight
            
            if stroke_align:
                border["align"] = stroke_align
            
            if border:
                borders.append(border)
        
        if borders:
            styling["borders"] = borders
    
    corner_radius = node.get("cornerRadius")
    if isinstance(corner_radius, (int, float)) and corner_radius > 0:
        styling["cornerRadius"] = corner_radius
    
    effects = node.get("effects")
    if is_nonempty_list(effects):
        parsed_effects = []
        
        for effect in effects:
            if not isinstance(effect, dict):
                continue
            
            effect_type = effect.get("type")
            if not effect_type:
                continue
            
            parsed_effect: Dict[str, Any] = {"type": effect_type.lower()}
            
            offset = effect.get("offset") or {}
            if isinstance(offset, dict):
                parsed_effect["x"] = offset.get("x", 0)
                parsed_effect["y"] = offset.get("y", 0)
            
            if "radius" in effect:
                parsed_effect["blur"] = effect["radius"]
            
            effect_color = effect.get("color")
            if isinstance(effect_color, dict):
                parsed_effect["color"] = to_rgba(effect_color)
            
            parsed_effects.append(parsed_effect)
        
        if parsed_effects:
            styling["effects"] = parsed_effects
    
    return styling

def extract_text(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if node.get("type", "").upper() != "TEXT":
        return None
    
    text_ Dict[str, Any] = {
        "content": node.get("characters", "")
    }
    
    style = node.get("style")
    if isinstance(style, dict):
        text_data["typography"] = {
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
        for fill in fills:
            if isinstance(fill, dict) and fill.get("type") == "SOLID" and "color" in fill:
                text_data["color"] = to_rgba(fill["color"])
                break
    
    return text_data

def should_include(node: Dict[str, Any]) -> bool:
    node_type = node.get("type", "").upper()
    node_name = node.get("name", "").lower()
    
    if node_type == "TEXT":
        return True
    
    has_visual = bool(
        node.get("fills") or
        node.get("strokes") or
        node.get("effects") or
        node.get("image_url")
    )
    
    semantic_keywords = [
        'button', 'input', 'search', 'nav', 'menu',
        'container', 'card', 'panel', 'header', 'footer',
        'badge', 'chip', 'toolbar', 'sidebar'
    ]
    has_semantic_name = any(keyword in node_name for keyword in semantic_keywords)
    
    is_vector_shape = (
        node_type in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE'] and
        (node.get("strokes") or node.get("fills"))
    )
    
    has_corner_radius = (
        isinstance(node.get('cornerRadius'), (int, float)) and
        node.get('cornerRadius', 0) > 0
    )
    
    has_layout = bool(node.get('layoutMode'))
    
    is_structural = node_type in [
        'FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'SECTION'
    ]
    
    return any([
        has_visual,
        is_vector_shape,
        has_corner_radius,
        has_layout,
        is_structural,
        has_semantic_name
    ])

def classify_bucket(comp: Dict[str, Any]) -> str:
    comp_type = comp.get("type", "").upper()
    comp_name = comp.get("name", "").lower()
    
    if comp_type == "TEXT":
        return "textElements"
    
    if "button" in comp_name or "btn" in comp_name:
        return "buttons"
    
    input_keywords = ['input', 'search', 'textfield', 'field', 'textarea']
    if any(keyword in comp_name for keyword in input_keywords):
        return "inputs"
    
    nav_keywords = ['nav', 'menu', 'sidebar', 'toolbar', 'header', 'footer', 'breadcrumb', 'tab']
    if any(keyword in comp_name for keyword in nav_keywords):
        return "navigation"
    
    if comp.get("imageUrl") or comp.get("image_url"):
        return "images"
    
    if comp_type in ['VECTOR', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'RECTANGLE']:
        return "vectors"
    
    container_types = ['FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'SECTION']
    container_keywords = ['container', 'card', 'panel', 'section', 'wrapper', 'box']
    if comp_type in container_types or any(keyword in comp_name for keyword in container_keywords):
        return "containers"
    
    return "other"

def extract_components(
    root: Dict[str, Any],
    parent_path: str = "",
    out: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    if out is None:
        out = []
    
    if not isinstance(root, dict):
        return out
    
    node_name = root.get('name', 'Unnamed')
    path = f"{parent_path}/{node_name}" if parent_path else node_name
    
    comp: Dict[str, Any] = {
        'id': root.get('id'),
        'name': node_name,
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
    
    image_url = root.get('image_url') or root.get('imageUrl')
    if image_url:
        comp['imageUrl'] = image_url
    
    text = extract_text(root)
    if text:
        comp['text'] = text
    
    if should_include(root):
        out.append(comp)
    
    children = root.get('children', []) or []
    for child in children:
        if isinstance(child, dict):
            extract_components(child, path, out)
    
    return out

def find_document_roots(nodes_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    roots: List[Dict[str, Any]] = []
    
    nodes = nodes_payload.get('nodes')
    if isinstance(nodes, dict):
        for value in nodes.values():
            if isinstance(value, dict):
                doc = value.get('document')
                if isinstance(doc, dict):
                    roots.append(doc)
        
        if roots:
            return roots
    
    document = nodes_payload.get('document')
    if isinstance(document, dict):
        roots.append(document)
    
    return roots

def organize_for_angular(components: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    
    for comp in components:
        bucket = classify_bucket(comp)
        organized.setdefault(bucket, []).append(comp)
    
    return organized

def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    roots = find_document_roots(merged_payload)
    
    if not roots:
        raise RuntimeError("No document roots found in payload")
    
    all_components: List[Dict[str, Any]] = []
    
    for root in roots:
        if isinstance(root, dict):
            extract_components(root, "", all_components)
    
    return organize_for_angular(all_components)

def remove_url_prefix_from_json(payload: Dict[str, Any], url_prefix: str) -> Dict[str, Any]:
    processed = copy.deepcopy(payload)
    
    def strip_prefix(obj: Any):
        if isinstance(obj, dict):
            for key, value in list(obj.items()):
                if key in ("imageUrl", "image_url") and isinstance(value, str):
                    if value.startswith(url_prefix):
                        obj[key] = value[len(url_prefix):]
                else:
                    strip_prefix(value)
        elif isinstance(obj, list):
            for item in obj:
                strip_prefix(item)
    
    strip_prefix(processed)
    return processed

# -----------------------------------------------------
# ANGULAR CODE PROCESSING
# -----------------------------------------------------

def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
    patterns = [
        (re.compile(r'(src\s*=\s*["\'])(' + UUID_RE + r')(["\'])', re.IGNORECASE),
         r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(\[src\]\s*=\s*["\']?\s*)(' + UUID_RE + r')(["\']?)', re.IGNORECASE),
         r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(imageUrl\s*:\s*["\'])(' + UUID_RE + r')(["\'])', re.IGNORECASE),
         r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(url\(\s*["\'])(' + UUID_RE + r')(["\']\s*\))', re.IGNORECASE),
         r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(["\'])(' + UUID_RE + r')(["\'])', re.IGNORECASE),
         r'\1' + url_prefix + r'\2\3'),
    ]
    
    modified = text
    total_replacements = 0
    
    for pattern, replacement in patterns:
        modified, count = pattern.subn(replacement, modified)
        total_replacements += count
    
    return modified, total_replacements

def create_text_to_pdf(text_content: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    styles = getSampleStyleSheet()
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
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
        chunk_lines = lines[i:i+chunk_size]
        safe_lines = [
            line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            for line in chunk_lines
        ]
        story.append(Paragraph('<br/>'.join(safe_lines), code_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def detect_uuids_in_text(text: str) -> List[str]:
    pattern = re.compile(UUID_RE, re.IGNORECASE)
    found = pattern.findall(text)
    
    seen = set()
    unique = []
    for uuid in found:
        if uuid not in seen:
            seen.add(uuid)
            unique.append(uuid)
    
    return unique

def decode_bytes_to_text(raw: bytes) -> str:
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    
    return raw.decode('utf-8', errors='ignore')

# -----------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------

def main():
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='margin-bottom: 0.5rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Enterprise-Grade UI Component Extraction with Rate Limit Protection
        </p>
        <p style='font-size: 0.9rem; color: #9CA3AF;'>
            ⚡ Auto-retry • Exponential Backoff • Smart Throttling
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
        st.markdown("### 🛡️ Rate Limit Protection")
        st.success(f"""
        **Active Features:**
        - Max Retries: {MAX_RETRIES}
        - Initial Delay: {INITIAL_RETRY_DELAY}s
        - Max Delay: {MAX_RETRY_DELAY}s
        - Jitter: {JITTER_MAX}s
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 Extraction Criteria")
        st.info("""
        **Images extracted only from:**
        - Vector/shape layers
        - Names: icon, logo, avatar, image
        - Layers with IMAGE fills
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Rate Limits](https://developers.figma.com/docs/rest-api/rate-limits/)
        - [Angular Framework](https://angular.io)
        """)

    tab1, tab2 = st.tabs(["🎯 Figma Extraction", "⚡ Angular Processor"])

    with tab1:
        st.markdown("### Figma Component Extraction")
        st.markdown("Extract UI components with automatic rate limit handling and intelligent retries.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input(
                "📁 Figma File Key",
                value="",
                help="Figma file key from the file URL"
            )
        with col2:
            node_ids = st.text_input(
                "🔗 Node IDs (comma-separated)",
                value="",
                help="Optional: specific node IDs to extract"
            )

        token = st.text_input(
            "🔑 Figma Personal Access Token",
            type="password",
            help="Generate in Figma account settings"
        )

        if st.button("🚀 Extract UI Components", type="primary"):
            if not token or not file_key:
                st.error("⚠️ Please provide both a file key and Figma access token.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("📡 Fetching nodes from Figma API...")
                    progress.progress(10)
                    nodes_payload = fetch_figma_nodes(
                        file_key=file_key,
                        node_ids=node_ids,
                        token=token
                    )

                    status.text("🔍 Analyzing nodes and collecting metadata...")
                    progress.progress(30)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_data(nodes_payload)
                    
                    total_nodes = len(node_meta)
                    image_worthy_count = sum(1 for m in node_meta.values() if m.get('is_image_worthy'))
                    status.text(f"📊 Found {total_nodes} nodes ({image_worthy_count} image-worthy)")

                    status.text("🖼️ Resolving image URLs (with rate limit protection)...")
                    progress.progress(55)
                    fills_map, renders_map = resolve_image_urls(
                        file_key, image_refs, node_meta, token
                    )

                    status.text("🎨 Building selective icon map...")
                    progress.progress(75)
                    node_to_url = build_selective_icon_map(node_meta, fills_map, renders_map)
                    
                    status.text(f"✨ Assigned {len(node_to_url)} image URLs")

                    status.text("📦 Merging URLs into node tree...")
                    progress.progress(85)
                    merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                    status.text("🏗️ Extracting structured components...")
                    progress.progress(92)
                    final_output = extract_ui_components(merged_payload)

                    status.text("🧹 Sanitizing URLs for portability...")
                    progress.progress(98)
                    sanitized = remove_url_prefix_from_json(
                        final_output,
                        DEFAULT_IMAGE_PREFIX
                    )
                    
                    st.session_state['metadata_json'] = sanitized
                    st.session_state['extraction_stats'] = {
                        'total_nodes': total_nodes,
                        'image_worthy': image_worthy_count,
                        'images_extracted': len(node_to_url)
                    }
                    st.session_state['stats']['files_processed'] += 1
                    
                    progress.progress(100)
                    status.empty()
                    
                    st.success("✅ Extraction completed successfully!")

                    st.markdown("### 📊 Extraction Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", sanitized['metadata']['totalComponents'])
                    with col2:
                        st.metric("Images Extracted", len(node_to_url))
                    with col3:
                        st.metric("Text Elements", len(sanitized.get('textElements', [])))
                    with col4:
                        st.metric("Containers", len(sanitized.get('containers', [])))

                    with st.expander("📋 Detailed Category Breakdown"):
                        categories = [
                            ('textElements', 'Text Elements'),
                            ('buttons', 'Buttons'),
                            ('inputs', 'Input Fields'),
                            ('containers', 'Containers'),
                            ('images', 'Images'),
                            ('navigation', 'Navigation'),
                            ('vectors', 'Vector Shapes'),
                            ('other', 'Other')
                        ]
                        
                        for key, label in categories:
                            count = len(sanitized.get(key, []))
                            if count > 0:
                                st.markdown(f"**{label}:** `{count}` components")
                    
                    with st.expander("⚡ Optimization Stats"):
                        stats = st.session_state.get('extraction_stats', {})
                        st.markdown(f"""
                        - **Total Nodes Analyzed:** {stats.get('total_nodes', 0)}
                        - **Image-Worthy Nodes:** {stats.get('image_worthy', 0)}
                        - **Images Actually Extracted:** {stats.get('images_extracted', 0)}
                        - **Extraction Selectivity:** {(stats.get('images_extracted', 0) / max(stats.get('total_nodes', 1), 1) * 100):.1f}%
                        """)

                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")
                    import traceback
                    with st.expander("🔍 Error Details"):
                        st.code(traceback.format_exc())

        if 'metadata_json' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Extracted Data")
            
            json_str = json.dumps(
                st.session_state['metadata_json'],
                indent=2,
                ensure_ascii=False
            )

            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download metadata.json",
                    data=json_str,
                    file_name="metadata.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update({
                        'downloads': st.session_state['stats']['downloads'] + 1
                    })
                )
            with col2:
                st.caption(f"Size: {len(json_str):,} bytes")

    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Automatically prefix UUID-based image identifiers with complete URLs.")
        st.markdown("---")

        url_prefix = st.text_input(
            "🌐 URL Prefix",
            value=DEFAULT_IMAGE_PREFIX,
            help="This prefix will be added to all detected image UUIDs"
        )

        uploaded = st.file_uploader(
            "📤 Upload Angular Code File",
            type=['txt', 'md', 'html', 'ts', 'js', 'css', 'scss'],
            help="Supported: .txt, .md, .html, .ts, .js, .css, .scss"
        )

        if uploaded:
            st.info(f"✅ File uploaded: **{uploaded.name}** ({uploaded.size:,} bytes)")

            if st.button("⚡ Process Angular Code", type="primary"):
                try:
                    raw_bytes = uploaded.read()
                    text_content = decode_bytes_to_text(raw_bytes)
                    
                    uuids_found = detect_uuids_in_text(text_content)
                    
                    modified_text, replacements_made = add_url_prefix_to_angular_code(
                        text_content,
                        url_prefix
                    )
                    
                    st.session_state['angular_output'] = modified_text
                    st.session_state['angular_filename'] = uploaded.name
                    st.session_state['angular_stats'] = {
                        'uuids_found': len(uuids_found),
                        'replacements': replacements_made,
                        'sample_uuids': uuids_found[:5]
                    }
                    st.session_state['stats']['files_processed'] += 1
                    
                    st.success("✅ Angular code processed successfully!")

                    st.markdown("### 📊 Processing Summary")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("UUIDs Found", len(uuids_found))
                    with col2:
                        st.metric("Replacements Made", replacements_made)
                    with col3:
                        st.metric("Output Size", f"{len(modified_text):,} bytes")

                    if len(uuids_found) > 0:
                        with st.expander("🔍 Sample Transformation"):
                            sample_uuid = uuids_found[0]
                            st.markdown("**Before:**")
                            st.code(sample_uuid, language="text")
                            st.markdown("**After:**")
                            st.code(f"{url_prefix}{sample_uuid}", language="text")
                    
                    if len(uuids_found) > 0:
                        with st.expander(f"📝 All UUIDs Found ({len(uuids_found)})"):
                            for idx, uuid in enumerate(uuids_found[:20], 1):
                                st.code(f"{idx}. {uuid}", language="text")
                            if len(uuids_found) > 20:
                                st.info(f"... and {len(uuids_found) - 20} more")

                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    import traceback
                    with st.expander("🔍 Error Details"):
                        st.code(traceback.format_exc())

        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Processed Code")
            
            base_filename = st.session_state['angular_filename'].rsplit('.', 1)[0]
            output_text = st.session_state['angular_output']

            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📄 Download as .txt",
                    data=output_text,
                    file_name=f"{base_filename}_modified.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update({
                        'downloads': st.session_state['stats']['downloads'] + 1
                    })
                )
            
            with col2:
                st.download_button(
                    "📝 Download as .md",
                    data=output_text,
                    file_name=f"{base_filename}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update({
                        'downloads': st.session_state['stats']['downloads'] + 1
                    })
                )
            
            with col3:
                pdf_buffer = create_text_to_pdf(output_text)
                st.download_button(
                    "📕 Download as .pdf",
                    data=pdf_buffer,
                    file_name=f"{base_filename}_modified.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update({
                        'downloads': st.session_state['stats']['downloads'] + 1
                    })
                )

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>
            Built with ❤️ using <strong>Streamlit</strong> | Professional Edition v3.0 (Rate-Limit Protected)
        </p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #9CA3AF;'>
            🛡️ Auto-retry • Exponential backoff • Smart throttling • Selective extraction
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
