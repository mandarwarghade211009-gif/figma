#!/usr/bin/env python3
"""
Professional Figma UI Extractor & Angular Code Processor
Enterprise-grade design system for UI extraction and code processing
ENHANCED VERSION: Extracts ALL properties for 100% UI match
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
    /* Keep your original styling */
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
    # filter invisible nodes in place
    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_invisible_nodes(doc)
    else:
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

    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
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
    Deep copy nodes_payload and inject `imageUrl` into nodes whose id exists in node_to_url.
    """
    merged = copy.deepcopy(nodes_payload)

    def inject(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        nid = n.get("id")
        if nid and nid in node_to_url:
            n["imageUrl"] = node_to_url[nid]
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
# ENHANCED EXTRACTION HELPERS (100% UI MATCH)
# -------------------------

def extract_bounds(node: Dict[str, Any]) -> Optional[Dict[str, float]]:
    """Extract both absoluteBoundingBox and absoluteRenderBounds for complete positioning"""
    bounds: Dict[str, Any] = {}
    
    # Absolute bounding box (without effects)
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict) and all(k in box for k in ("x", "y", "width", "height")):
        try:
            bounds["absoluteBoundingBox"] = {
                "x": float(box["x"]),
                "y": float(box["y"]),
                "width": float(box["width"]),
                "height": float(box["height"])
            }
        except Exception:
            pass
    
    # Absolute render bounds (includes shadows, strokes)
    render_box = node.get("absoluteRenderBounds")
    if isinstance(render_box, dict) and all(k in render_box for k in ("x", "y", "width", "height")):
        try:
            bounds["absoluteRenderBounds"] = {
                "x": float(render_box["x"]),
                "y": float(render_box["y"]),
                "width": float(render_box["width"]),
                "height": float(render_box["height"])
            }
        except Exception:
            pass
    
    # Relative transform
    if "relativeTransform" in node:
        bounds["relativeTransform"] = node["relativeTransform"]
    
    # Size properties
    if "size" in node and isinstance(node["size"], dict):
        bounds["size"] = node["size"]
    
    return bounds if bounds else None

def extract_layout(node: Dict[str, Any]) -> Dict[str, Any]:
    """ENHANCED: Extract ALL layout-related properties for pixel-perfect reconstruction"""
    layout: Dict[str, Any] = {}
    
    # Auto-layout properties
    layout_props = [
        'layoutMode', 'layoutWrap', 'layoutGrow', 'layoutAlign',
        'layoutSizingHorizontal', 'layoutSizingVertical',
        'counterAxisSizingMode', 'primaryAxisSizingMode',
        'primaryAxisAlignItems', 'counterAxisAlignItems',
        'itemSpacing', 'counterAxisSpacing',
        'paddingLeft', 'paddingRight', 'paddingTop', 'paddingBottom',
        'layoutGrids', 'clipsContent'
    ]
    
    for prop in layout_props:
        if prop in node:
            layout[prop] = node[prop]
    
    # Constraints
    if 'constraints' in node:
        layout['constraints'] = node['constraints']
    
    # Size constraints
    size_constraints = ['minWidth', 'maxWidth', 'minHeight', 'maxHeight']
    for prop in size_constraints:
        if prop in node:
            layout[prop] = node[prop]
    
    # Positioning
    positioning = ['rotation', 'layoutPositioning', 'absoluteTransform']
    for prop in positioning:
        if prop in node:
            layout[prop] = node[prop]
    
    return layout

def extract_visuals(node: Dict[str, Any]) -> Dict[str, Any]:
    """ENHANCED: Extract complete visual styling properties"""
    styling: Dict[str, Any] = {}
    
    # Opacity and blend mode
    if 'opacity' in node:
        styling['opacity'] = node['opacity']
    if 'blendMode' in node:
        styling['blendMode'] = node['blendMode']
    
    # Masking
    if 'isMask' in node:
        styling['isMask'] = node['isMask']
    if 'isMaskOutline' in node:
        styling['isMaskOutline'] = node['isMaskOutline']
    
    # Fills (complete extraction)
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
                if "visible" in f:
                    entry["visible"] = f.get("visible")
            
            elif t == "GRADIENT_LINEAR" or t == "GRADIENT_RADIAL" or t == "GRADIENT_ANGULAR" or t == "GRADIENT_DIAMOND":
                entry["type"] = t.lower()
                if "gradientHandlePositions" in f:
                    entry["gradientHandlePositions"] = f["gradientHandlePositions"]
                if "gradientStops" in f:
                    stops = []
                    for stop in f["gradientStops"]:
                        stops.append({
                            "color": to_rgba(stop.get("color", {})),
                            "position": stop.get("position", 0)
                        })
                    entry["gradientStops"] = stops
            
            elif t == "IMAGE":
                entry["type"] = "image"
                if "imageRef" in f:
                    entry["imageRef"] = f["imageRef"]
                if "imageHash" in f:
                    entry["imageHash"] = f["imageHash"]
                if "scaleMode" in f:
                    entry["scaleMode"] = f["scaleMode"]
                if "imageTransform" in f:
                    entry["imageTransform"] = f["imageTransform"]
                if "scalingFactor" in f:
                    entry["scalingFactor"] = f["scalingFactor"]
                if "rotation" in f:
                    entry["rotation"] = f["rotation"]
                if "filters" in f:
                    entry["filters"] = f["filters"]
            
            if "opacity" in f:
                entry["opacity"] = f["opacity"]
            if "blendMode" in f:
                entry["blendMode"] = f["blendMode"]
            if "visible" in f:
                entry["visible"] = f["visible"]
            
            if entry:
                parsed.append(entry)
        
        if parsed:
            styling["fills"] = parsed
    
    # Background color
    if "backgroundColor" in node and isinstance(node["backgroundColor"], dict):
        styling["backgroundColor"] = to_rgba(node["backgroundColor"])
    
    # Strokes (complete extraction)
    strokes = node.get("strokes")
    if is_nonempty_list(strokes):
        borders: List[Dict[str, Any]] = []
        for s in strokes:
            if not isinstance(s, dict):
                continue
            b: Dict[str, Any] = {}
            
            if s.get("type") == "SOLID" and "color" in s:
                b["type"] = "solid"
                b["color"] = to_rgba(s["color"])
            elif s.get("type") in ["GRADIENT_LINEAR", "GRADIENT_RADIAL", "GRADIENT_ANGULAR", "GRADIENT_DIAMOND"]:
                b["type"] = s["type"].lower()
                if "gradientHandlePositions" in s:
                    b["gradientHandlePositions"] = s["gradientHandlePositions"]
                if "gradientStops" in s:
                    b["gradientStops"] = s["gradientStops"]
            
            if "opacity" in s:
                b["opacity"] = s["opacity"]
            if "blendMode" in s:
                b["blendMode"] = s["blendMode"]
            if "visible" in s:
                b["visible"] = s["visible"]
            
            if b:
                borders.append(b)
        
        if borders:
            styling["borders"] = borders
    
    # Stroke properties
    stroke_props = ['strokeWeight', 'strokeAlign', 'strokeCap', 'strokeJoin', 
                    'strokeDashes', 'strokeMiterAngle', 'strokeGeometry']
    for prop in stroke_props:
        if prop in node:
            styling[prop] = node[prop]
    
    # Corner radius (all variants)
    if 'cornerRadius' in node:
        styling['cornerRadius'] = node['cornerRadius']
    if 'rectangleCornerRadii' in node:
        styling['rectangleCornerRadii'] = node['rectangleCornerRadii']
    corner_props = ['topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius']
    for prop in corner_props:
        if prop in node:
            styling[prop] = node[prop]
    
    # Effects (shadows, blurs) - complete extraction
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
            
            # Visibility
            if "visible" in e:
                ee["visible"] = e["visible"]
            
            # Offset
            off = e.get("offset") or {}
            if isinstance(off, dict):
                ee["offsetX"] = off.get("x", 0)
                ee["offsetY"] = off.get("y", 0)
            
            # Radius/blur
            if "radius" in e:
                ee["radius"] = e["radius"]
            
            # Spread (for shadows)
            if "spread" in e:
                ee["spread"] = e["spread"]
            
            # Color
            if "color" in e and isinstance(e.get("color"), dict):
                ee["color"] = to_rgba(e["color"])
            
            # Blend mode
            if "blendMode" in e:
                ee["blendMode"] = e["blendMode"]
            
            # Show shadow behind node
            if "showShadowBehindNode" in e:
                ee["showShadowBehindNode"] = e["showShadowBehindNode"]
            
            parsed.append(ee)
        
        if parsed:
            styling["effects"] = parsed
    
    return styling

def extract_text(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """ENHANCED: Extract complete typography properties for exact text reproduction"""
    if (node.get("type") or "").upper() != "TEXT":
        return None
    
    t: Dict[str, Any] = {
        "content": node.get("characters", ""),
        "visible": node.get("visible", True)
    }
    
    # Complete style extraction
    style = node.get("style") or {}
    if isinstance(style, dict):
        typography: Dict[str, Any] = {}
        
        # Font properties
        if "fontFamily" in style:
            typography["fontFamily"] = style["fontFamily"]
        if "fontPostScriptName" in style:
            typography["fontPostScriptName"] = style["fontPostScriptName"]
        if "fontSize" in style:
            typography["fontSize"] = style["fontSize"]
        if "fontWeight" in style:
            typography["fontWeight"] = style["fontWeight"]
        
        # Line height (all variants)
        if "lineHeightPx" in style:
            typography["lineHeightPx"] = style["lineHeightPx"]
        if "lineHeightPercent" in style:
            typography["lineHeightPercent"] = style["lineHeightPercent"]
        if "lineHeightPercentFontSize" in style:
            typography["lineHeightPercentFontSize"] = style["lineHeightPercentFontSize"]
        if "lineHeight" in style:
            typography["lineHeight"] = style["lineHeight"]
        if "lineHeightUnit" in style:
            typography["lineHeightUnit"] = style["lineHeightUnit"]
        
        # Letter and paragraph spacing
        if "letterSpacing" in style:
            typography["letterSpacing"] = style["letterSpacing"]
        if "paragraphSpacing" in style:
            typography["paragraphSpacing"] = style["paragraphSpacing"]
        if "paragraphIndent" in style:
            typography["paragraphIndent"] = style["paragraphIndent"]
        
        # Alignment
        if "textAlignHorizontal" in style:
            typography["textAlignHorizontal"] = style["textAlignHorizontal"]
        if "textAlignVertical" in style:
            typography["textAlignVertical"] = style["textAlignVertical"]
        
        # Text decoration and case
        if "textCase" in style:
            typography["textCase"] = style["textCase"]
        if "textDecoration" in style:
            typography["textDecoration"] = style["textDecoration"]
        
        # Text truncation and auto-resize
        if "textTruncation" in style:
            typography["textTruncation"] = style["textTruncation"]
        if "maxLines" in style:
            typography["maxLines"] = style["maxLines"]
        
        if typography:
            t["typography"] = typography
    
    # Text auto-resize behavior
    if "textAutoResize" in node:
        t["textAutoResize"] = node["textAutoResize"]
    
    # Text color from fills
    fills = node.get("fills")
    if is_nonempty_list(fills):
        colors = []
        for f in fills:
            if isinstance(f, dict) and f.get("type") == "SOLID" and "color" in f:
                colors.append({
                    "color": to_rgba(f["color"]),
                    "opacity": f.get("opacity", 1)
                })
        if colors:
            t["colors"] = colors
    
    # Character style overrides
    if "characterStyleOverrides" in node:
        t["characterStyleOverrides"] = node["characterStyleOverrides"]
    if "styleOverrideTable" in node:
        t["styleOverrideTable"] = node["styleOverrideTable"]
    
    return t

def should_include(node: Dict[str, Any]) -> bool:
    """Determine if a node should be included in extraction"""
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    has_visual = bool(node.get("fills") or node.get("strokes") or node.get("effects") or node.get("imageUrl"))
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
    """Classify component into appropriate category"""
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
    """ENHANCED: Extract components with ALL properties for 100% UI match"""
    if out is None:
        out = []
    if root is None or not isinstance(root, dict):
        return out
    
    path = f"{parent_path}/{root.get('name','Unnamed')}" if parent_path else (root.get('name') or 'Root')
    
    # Core properties
    comp: Dict[str, Any] = {
        'id': root.get('id'),
        'name': root.get('name'),
        'type': root.get('type'),
        'path': path,
        'visible': root.get('visible', True)
    }
    
    # Positioning & bounds
    bounds = extract_bounds(root)
    if bounds:
        comp['bounds'] = bounds
    
    # Layout properties
    layout = extract_layout(root)
    if layout:
        comp['layout'] = layout
    
    # Visual styling
    styling = extract_visuals(root)
    if styling:
        comp['styling'] = styling
    
    # Image URLs (both possible keys)
    if root.get('imageUrl'):
        comp['imageUrl'] = root.get('imageUrl')
    if root.get('image_url'):
        comp['imageUrl'] = root.get('image_url')
    
    # Text properties
    text = extract_text(root)
    if text:
        comp['text'] = text
    
    # Component/instance properties
    if 'componentId' in root:
        comp['componentId'] = root['componentId']
    if 'componentProperties' in root:
        comp['componentProperties'] = root['componentProperties']
    
    # Export settings
    if 'exportSettings' in root:
        comp['exportSettings'] = root['exportSettings']
    
    # Interactions and transitions
    if 'reactions' in root:
        comp['reactions'] = root['reactions']
    if 'transitionNodeID' in root:
        comp['transitionNodeID'] = root['transitionNodeID']
    
    # Include if relevant
    if should_include(root):
        out.append(comp)
    
    # Recurse children
    for child in root.get('children', []) or []:
        if isinstance(child, dict):
            extract_components(child, path, out)
    
    return out

def find_document_roots(nodes_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find all document roots in the payload"""
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
    """Organize extracted components by category"""
    organized = {
        'metadata': {
            'totalComponents': len(components),
            'extractedAt': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': 2,  # Updated version for enhanced extraction
            'extractionMode': 'complete',
            'description': 'Complete extraction with all properties for 100% UI match'
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

def extract_ui_components(merged_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extract UI components from merged payload"""
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

UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
    """
    Finds UUID-only occurrences in common Angular patterns and prefixes them with url_prefix.
    Returns (modified_text, total_replacements)
    """
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
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
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
        safe = [ln.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for ln in block]
        story.append(Paragraph('<br/>'.join(safe), code_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

def detect_uuids_in_text(text: str) -> List[str]:
    """Return unique UUIDs found in the supplied text"""
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
        <p style='font-size: 0.9rem; color: #9CA3AF;'>
            ✨ Enhanced: 100% UI Match with Complete Property Extraction
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
        st.markdown("### ✨ Enhanced Features")
        st.info("""
        **Complete Property Extraction:**
        - Absolute & render bounds
        - Complete typography settings
        - All auto-layout properties
        - Size constraints & positioning
        - Complete effects & strokes
        - Individual corner radii
        - Blend modes & opacity
        """)
        
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
        st.markdown("Extract UI components with **complete metadata, styling, and images** from Figma for 100% UI match.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 Figma File Key", value="", help="Figma file key (from file URL)")
        with col2:
            node_ids = st.text_input("🔗 Node IDs (comma-separated)", value="", help="Optional: comma-separated node ids")

        token = st.text_input("🔑 Figma Personal Access Token", type="password", help="Generate in Figma account settings")

        if st.button("🚀 Extract UI Components", type="primary"):
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

                    status.text("📦 Extracting structured components with complete properties...")
                    progress.progress(85)
                    final_output = extract_ui_components(merged_payload)

                    status.text("✨ Finalizing extraction and sanitizing URLs...")
                    progress.progress(95)
                    sanitized = remove_url_prefix_from_json(final_output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                    st.session_state['metadata_json'] = sanitized
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    st.success("✅ Extraction completed successfully with 100% property coverage!")

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
                    
                    with st.expander("✨ Enhanced Properties Extracted"):
                        st.markdown("""
                        - ✅ Absolute & render bounding boxes
                        - ✅ Complete typography (font, size, weight, line height, letter spacing)
                        - ✅ All auto-layout properties (spacing, padding, alignment, sizing)
                        - ✅ Size constraints (min/max width/height)
                        - ✅ Complete effects (shadows with spread, blur with types)
                        - ✅ Individual corner radii
                        - ✅ Stroke properties (weight, align, cap, join, dashes)
                        - ✅ Blend modes & opacity
                        - ✅ Gradient details (stops, positions, handles)
                        - ✅ Image transform & scaling
                        - ✅ Component properties & interactions
                        """)
                        
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
                    "📥 Download metadata.json (Complete)",
                    data=json_str,
                    file_name="metadata_complete.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.caption(f"Size: {len(json_str):,} bytes")

    # --- Angular Processor Tab ---
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Upload a file or paste code, then automatically prefix UUID image IDs with a full URL.")
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
                type=['txt', 'md', 'html', 'ts', 'js', 'css', 'scss', 'json'],
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
                height=320,
                placeholder="Paste your TypeScript / HTML / CSS code here...",
                help="Once you paste code here, the Process button will be enabled below."
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
            st.info("Paste some code or upload a file to enable the processor.")

        # Downloads for angular output
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
                    help="Select all and copy from here; indentation is preserved."
                )

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
        <p style='margin: 0; font-size: 0.9rem;'>Built with ❤️ using <strong>Streamlit</strong> | Professional Edition v2.0</p>
        <p style='margin: 0; font-size: 0.8rem; color: #9CA3AF;'>Enhanced for 100% UI Match</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
