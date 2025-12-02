#!/usr/bin/env python3
"""
Optimized Figma UI Extractor & Angular Code Processor
Minimal field extraction for Angular Material code generation
"""

import streamlit as st
import requests
import json
import re
import datetime
import time
from io import BytesIO
from typing import Any, Dict, List, Set, Tuple, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch
import copy

# -----------------------------------------------------
# CONFIGURATION - OPTIMIZED FOR ANGULAR CODE GEN
# -----------------------------------------------------
ESSENTIAL_NODE_FIELDS = {
    'id', 'name', 'type', 'visible',
    'absoluteBoundingBox',  # Position/size
    'children',  # Hierarchy
    # Layout (Flexbox/Auto-layout)
    'layoutMode', 'primaryAxisAlignItems', 'counterAxisAlignItems',
    'paddingLeft', 'paddingRight', 'paddingTop', 'paddingBottom',
    'itemSpacing', 'layoutGrow',
    # Visual basics
    'fills', 'strokes', 'strokeWeight', 'cornerRadius',
    'backgroundColor', 'effects',
    # Text
    'characters', 'style',
    # Images
    'imageRef', 'imageHash'
}

MAX_BATCH_SIZE = 50  # Reduced from 200 to stay within rate limits
REQUEST_TIMEOUT = 30  # Reduced timeout
MAX_RETRIES = 2  # Retry logic for rate limits

# -----------------------------------------------------
# PROFESSIONAL THEMING
# -----------------------------------------------------
def apply_professional_styling():
    """Apply professional CSS theme"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .stDownloadButton>button {
        background: #10b981;
        color: white;
        border-radius: 6px;
    }
    
    .stExpander {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
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
# UTILITY HELPERS - OPTIMIZED
# -----------------------------------------------------

def build_headers(token: str) -> Dict[str, str]:
    return {
        "Accept": "application/json",
        "X-Figma-Token": token
    }

def api_request_with_retry(url: str, headers: Dict[str, str], params: Optional[Dict] = None, timeout: int = REQUEST_TIMEOUT) -> Dict[str, Any]:
    """Make API request with exponential backoff retry for rate limits"""
    for attempt in range(MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=headers, params=params, timeout=timeout)
            
            if r.status_code == 429:  # Rate limited
                if attempt < MAX_RETRIES:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff
                    st.warning(f"⏳ Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError("Rate limit exceeded. Please wait and try again.")
            
            if not r.ok:
                raise RuntimeError(f"API error {r.status_code}: {r.text[:200]}")
            
            return r.json()
            
        except requests.Timeout:
            if attempt < MAX_RETRIES:
                st.warning(f"⏳ Request timeout. Retrying... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(2)
                continue
            raise RuntimeError("Request timeout. Please check your connection.")
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            raise e
    
    raise RuntimeError("Max retries exceeded")

def to_rgba(color: Dict[str, Any]) -> str:
    """Convert Figma color to CSS rgba()"""
    try:
        r = int(float(color.get("r", 0)) * 255)
        g = int(float(color.get("g", 0)) * 255)
        b = int(float(color.get("b", 0)) * 255)
        a = float(color.get("a", color.get("opacity", 1)))
        return f"rgba({r},{g},{b},{a})"
    except:
        return "rgba(0,0,0,1)"

def is_visible(node: Dict[str, Any]) -> bool:
    """Check if node is visible"""
    v = node.get("visible")
    return True if v is None else bool(v)

def filter_node_fields(node: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only essential fields for Angular code generation"""
    if not isinstance(node, dict):
        return node
    
    # Filter out invisible nodes immediately
    if not is_visible(node):
        return None
    
    filtered = {k: v for k, v in node.items() if k in ESSENTIAL_NODE_FIELDS}
    
    # Recursively filter children
    if "children" in node:
        filtered_children = []
        for child in node.get("children", []):
            if isinstance(child, dict):
                fc = filter_node_fields(child)
                if fc is not None:
                    filtered_children.append(fc)
        if filtered_children:
            filtered["children"] = filtered_children
    
    return filtered

# -------------------------
# FIGMA API - OPTIMIZED
# -------------------------

def fetch_figma_nodes_optimized(file_key: str, node_ids: str, token: str) -> Dict[str, Any]:
    """
    Optimized fetch: Gets only essential fields using depth parameter
    """
    headers = build_headers(token)
    
    if node_ids:
        # Specific nodes
        url = f"https://api.figma.com/v1/files/{file_key}/nodes"
        params = {
            "ids": node_ids,
            "depth": 10  # Limit depth to prevent huge payloads
        }
    else:
        # Full file - use regular files endpoint
        url = f"https://api.figma.com/v1/files/{file_key}"
        params = {"depth": 5}  # Shallower depth for full file
    
    data = api_request_with_retry(url, headers, params)
    
    # Filter to essential fields
    if isinstance(data.get("nodes"), dict):
        for k, v in list(data["nodes"].items()):
            doc = v.get("document")
            if isinstance(doc, dict):
                data["nodes"][k]["document"] = filter_node_fields(doc)
    elif isinstance(data.get("document"), dict):
        data["document"] = filter_node_fields(data["document"])
    
    return data

def collect_image_refs_and_node_ids(nodes_payload: Dict[str, Any]) -> Tuple[Set[str], List[str]]:
    """
    Lightweight walker - collects only image refs and node IDs
    """
    image_refs: Set[str] = set()
    node_ids: List[str] = []

    def visit(n: Dict[str, Any]):
        if not isinstance(n, dict):
            return
        
        nid = n.get("id")
        if nid:
            node_ids.append(nid)
        
        # Check fills for images
        for f in n.get("fills", []) or []:
            if isinstance(f, dict) and f.get("type") == "IMAGE":
                ref = f.get("imageRef") or f.get("imageHash")
                if ref:
                    image_refs.add(ref)
        
        # Check strokes for images
        for s in n.get("strokes", []) or []:
            if isinstance(s, dict) and s.get("type") == "IMAGE":
                ref = s.get("imageRef") or s.get("imageHash")
                if ref:
                    image_refs.add(ref)
        
        # Recurse children
        for c in n.get("children", []) or []:
            visit(c)

    # Walk nodes
    if isinstance(nodes_payload.get("nodes"), dict):
        for entry in nodes_payload["nodes"].values():
            doc = entry.get("document")
            if isinstance(doc, dict):
                visit(doc)
    if isinstance(nodes_payload.get("document"), dict):
        visit(nodes_payload["document"])

    # De-duplicate node_ids
    seen = set()
    unique_ids = []
    for nid in node_ids:
        if nid not in seen:
            seen.add(nid)
            unique_ids.append(nid)

    return image_refs, unique_ids

def resolve_image_urls_optimized(file_key: str, image_refs: Set[str], node_ids: List[str], token: str) -> Dict[str, str]:
    """
    Optimized: Only fetch images that are actually needed
    Uses smaller batches to avoid rate limits
    """
    headers = build_headers(token)
    node_to_url: Dict[str, str] = {}
    
    # Only fetch render images for nodes that don't have fill images
    # This significantly reduces API calls
    if node_ids and len(node_ids) <= 100:  # Only render small sets
        base_render = f"https://api.figma.com/v1/images/{file_key}"
        # Process in smaller batches
        for i in range(0, len(node_ids), MAX_BATCH_SIZE):
            batch = node_ids[i:i+MAX_BATCH_SIZE]
            try:
                params = {
                    "ids": ",".join(batch),
                    "format": "svg",
                    "scale": 1  # Lower scale to reduce payload
                }
                data = api_request_with_retry(base_render, headers, params)
                images_map = data.get("images", {}) or {}
                
                for nid in batch:
                    url = images_map.get(nid)
                    if url:
                        node_to_url[nid] = url
            except Exception as e:
                st.warning(f"⚠️ Batch image fetch failed: {str(e)}")
                continue
    
    return node_to_url

def inject_image_urls(nodes_payload: Dict[str, Any], node_to_url: Dict[str, str]) -> Dict[str, Any]:
    """Inject image_url into nodes"""
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
# EXTRACTION - MINIMAL
# -------------------------

def extract_minimal_component(node: Dict[str, Any]) -> Dict[str, Any]:
    """Extract only fields needed for Angular Material generation"""
    comp: Dict[str, Any] = {
        'id': node.get('id'),
        'name': node.get('name'),
        'type': node.get('type')
    }
    
    # Position (for layout)
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict):
        try:
            comp['bounds'] = {
                "w": float(box["width"]),
                "h": float(box["height"])
            }
        except:
            pass
    
    # Layout (Auto-layout = Flexbox)
    if node.get('layoutMode'):
        comp['layout'] = {
            'mode': node.get('layoutMode'),
            'align': node.get('primaryAxisAlignItems'),
            'spacing': node.get('itemSpacing'),
            'padding': [
                node.get('paddingTop', 0),
                node.get('paddingRight', 0),
                node.get('paddingBottom', 0),
                node.get('paddingLeft', 0)
            ]
        }
    
    # Visual - only primary fill/stroke
    fills = node.get("fills")
    if isinstance(fills, list) and len(fills) > 0:
        f = fills[0]  # Only first fill
        if isinstance(f, dict):
            if f.get("type") == "SOLID" and "color" in f:
                comp['fill'] = to_rgba(f["color"])
    
    strokes = node.get("strokes")
    if isinstance(strokes, list) and len(strokes) > 0:
        s = strokes[0]
        if isinstance(s, dict) and s.get("type") == "SOLID":
            comp['stroke'] = {
                'color': to_rgba(s.get("color", {})),
                'width': node.get("strokeWeight", 1)
            }
    
    if node.get("cornerRadius"):
        comp['radius'] = node.get("cornerRadius")
    
    # Text - essential only
    if node.get("type") == "TEXT":
        comp['text'] = node.get("characters", "")
        style = node.get("style") or {}
        if isinstance(style, dict):
            comp['font'] = {
                'family': style.get("fontFamily"),
                'size': style.get("fontSize"),
                'weight': style.get("fontWeight")
            }
    
    # Image URL
    if node.get('image_url'):
        comp['img'] = node.get('image_url')
    
    return comp

def should_extract(node: Dict[str, Any]) -> bool:
    """Determine if node is relevant for Angular components"""
    t = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    
    # Text elements
    if t == 'TEXT':
        return True
    
    # Interactive elements
    if any(k in name for k in ['button', 'input', 'field', 'select', 'checkbox', 'radio']):
        return True
    
    # Layout containers
    if node.get('layoutMode'):  # Has auto-layout
        return True
    
    # Frames/components
    if t in ['FRAME', 'COMPONENT', 'INSTANCE']:
        return True
    
    # Has visual styling
    if node.get("fills") or node.get("cornerRadius"):
        return True
    
    return False

def extract_components_recursive(root: Dict[str, Any], out: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Recursively extract minimal component data"""
    if out is None:
        out = []
    
    if not isinstance(root, dict):
        return out
    
    if should_extract(root):
        comp = extract_minimal_component(root)
        if comp.get('id'):  # Valid component
            out.append(comp)
    
    # Recurse children
    for child in root.get('children', []) or []:
        if isinstance(child, dict):
            extract_components_recursive(child, out)
    
    return out

def organize_minimal(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Organize components for Angular Material mapping"""
    organized = {
        'meta': {
            'total': len(components),
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'version': '2.0-optimized'
        },
        'text': [],
        'buttons': [],
        'inputs': [],
        'containers': [],
        'other': []
    }
    
    for c in components:
        t = (c.get("type") or "").upper()
        name = (c.get("name") or "").lower()
        
        if t == "TEXT":
            organized['text'].append(c)
        elif "button" in name:
            organized['buttons'].append(c)
        elif any(k in name for k in ['input', 'field', 'select']):
            organized['inputs'].append(c)
        elif c.get('layout') or t in ['FRAME', 'COMPONENT']:
            organized['containers'].append(c)
        else:
            organized['other'].append(c)
    
    return organized

def extract_ui_components_optimized(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main extraction with minimal fields"""
    # Find document roots
    roots = []
    if isinstance(payload.get('nodes'), dict):
        for v in payload['nodes'].values():
            if isinstance(v, dict) and isinstance(v.get('document'), dict):
                roots.append(v['document'])
    if isinstance(payload.get('document'), dict):
        roots.append(payload['document'])
    
    if not roots:
        raise RuntimeError("No document found in payload")
    
    # Extract
    all_components: List[Dict[str, Any]] = []
    for r in roots:
        extract_components_recursive(r, all_components)
    
    return organize_minimal(all_components)

def sanitize_urls(payload: Dict[str, Any], prefix: str) -> Dict[str, Any]:
    """Remove URL prefix for portability"""
    p = copy.deepcopy(payload)
    def clean(obj: Any):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k == "img" and isinstance(v, str) and v.startswith(prefix):
                    obj[k] = v.replace(prefix, "", 1)
                else:
                    clean(v)
        elif isinstance(obj, list):
            for item in obj:
                clean(item)
    clean(p)
    return p

# -------------------------
# ANGULAR CODE PROCESSING
# -------------------------

UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def add_url_prefix_to_code(text: str, prefix: str) -> Tuple[str, int]:
    """Add URL prefix to UUIDs in Angular code"""
    patterns = [
        (re.compile(r'(src\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.I), r'\1' + prefix + r'\2\3'),
        (re.compile(r'(\[src\]\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.I), r'\1' + prefix + r'\2\3'),
        (re.compile(r'(img\s*:\s*["\'])(%s)(["\'])' % UUID_RE, re.I), r'\1' + prefix + r'\2\3'),
        (re.compile(r'(url\(\s*["\'])(%s)(["\']\s*\))' % UUID_RE, re.I), r'\1' + prefix + r'\2\3'),
    ]
    
    modified = text
    total = 0
    for pat, repl in patterns:
        modified, n = pat.subn(repl, modified)
        total += n
    return modified, total

def create_pdf(text: str) -> BytesIO:
    """Create PDF from text"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10
    )
    
    story = []
    lines = text.splitlines()
    for i in range(0, len(lines), 50):
        chunk = lines[i:i+50]
        safe = [l.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for l in chunk]
        story.append(Paragraph('<br/>'.join(safe), style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# -------------------------
# STREAMLIT UI
# -------------------------

def main():
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1>🎨 Figma UI Extractor <span style='font-size: 0.5em; color: #667eea;'>Optimized</span></h1>
        <p style='font-size: 1rem; color: #6B7280;'>
            Minimal Field Extraction for Angular Material Code Generation
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### ⚙️ System Stats")
        st.markdown("---")
        
        if 'stats' not in st.session_state:
            st.session_state['stats'] = {'processed': 0, 'downloads': 0}
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Processed", st.session_state['stats']['processed'])
        with col2:
            st.metric("Downloads", st.session_state['stats']['downloads'])
        
        st.markdown("---")
        st.markdown("### 🚀 Optimizations")
        st.info(f"""
        - **Batch Size**: {MAX_BATCH_SIZE}
        - **Essential Fields Only**
        - **Rate Limit Handling**
        - **Retry Logic**: {MAX_RETRIES}x
        """)

    tab1, tab2 = st.tabs(["🎯 Figma Extract", "⚡ Code Processor"])

    # TAB 1: Figma Extraction
    with tab1:
        st.markdown("### Optimized Figma Extraction")
        st.info("🎯 Extracts only essential fields for Angular Material code generation")
        
        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 File Key", help="From Figma URL")
        with col2:
            node_ids = st.text_input("🔗 Node IDs (optional)", help="Comma-separated")
        
        token = st.text_input("🔑 Figma Token", type="password")
        
        if st.button("🚀 Extract Components", type="primary"):
            if not token or not file_key:
                st.error("⚠️ Provide file key and token")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()
                    
                    status.text("📡 Fetching minimal node data...")
                    progress.progress(20)
                    nodes = fetch_figma_nodes_optimized(file_key, node_ids, token)
                    
                    status.text("🖼️ Collecting image references...")
                    progress.progress(40)
                    img_refs, node_id_list = collect_image_refs_and_node_ids(nodes)
                    
                    status.text("🔗 Resolving images (optimized batches)...")
                    progress.progress(60)
                    urls = resolve_image_urls_optimized(file_key, img_refs, node_id_list, token)
                    
                    status.text("📦 Merging and extracting...")
                    progress.progress(80)
                    merged = inject_image_urls(nodes, urls)
                    output = extract_ui_components_optimized(merged)
                    
                    status.text("✨ Sanitizing URLs...")
                    progress.progress(95)
                    clean = sanitize_urls(output, "https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/")
                    
                    st.session_state['metadata'] = clean
                    st.session_state['stats']['processed'] += 1
                    progress.progress(100)
                    st.success("✅ Extraction complete!")
                    
                    # Metrics
                    st.markdown("### 📊 Results")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total", clean['meta']['total'])
                    with col2:
                        st.metric("Text", len(clean.get('text', [])))
                    with col3:
                        st.metric("Buttons", len(clean.get('buttons', [])))
                    with col4:
                        st.metric("Containers", len(clean.get('containers', [])))
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        if 'metadata' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download")
            json_data = json.dumps(st.session_state['metadata'], indent=2)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    "📥 Download metadata.json",
                    data=json_data,
                    file_name="metadata_optimized.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.caption(f"{len(json_data):,} bytes")

    # TAB 2: Code Processor
    with tab2:
        st.markdown("### Angular Code Processor")
        st.info("⚡ Adds URL prefix to image UUIDs in your code")
        
        prefix = st.text_input(
            "🌐 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/"
        )
        
        method = st.radio("Input Method", ["📤 Upload", "📝 Paste"], horizontal=True, label_visibility="collapsed")
        
        code = ""
        filename = "code"
        
        if method == "📤 Upload":
            uploaded = st.file_uploader("Upload Code File", type=['txt', 'ts', 'html', 'css', 'json'])
            if uploaded:
                st.success(f"✅ {uploaded.name}")
                code = uploaded.read().decode('utf-8', errors='ignore')
                filename = uploaded.name.rsplit('.', 1)[0]
        else:
            code = st.text_area("Paste Code", height=300)
            filename = "pasted"
        
        if code and code.strip():
            if st.button("⚡ Process", type="primary"):
                try:
                    modified, count = add_url_prefix_to_code(code, prefix)
                    st.session_state['output'] = modified
                    st.session_state['filename'] = filename
                    st.session_state['stats']['processed'] += 1
                    
                    st.success(f"✅ Processed! {count} replacements made")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Lines", len(modified.splitlines()))
                    with col2:
                        st.metric("Replacements", count)
                    
                except Exception as e:
                    st.error(f"❌ {str(e)}")
        
        if 'output' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Processed Code")
            
            st.code(st.session_state['output'][:1000] + "..." if len(st.session_state['output']) > 1000 else st.session_state['output'], language="typescript")
            
            base = st.session_state['filename']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.download_button(
                    "📄 .txt",
                    data=st.session_state['output'],
                    file_name=f"{base}_processed.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.download_button(
                    "💻 .ts",
                    data=st.session_state['output'],
                    file_name=f"{base}_processed.ts",
                    mime="text/typescript",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col3:
                st.download_button(
                    "📝 .html",
                    data=st.session_state['output'],
                    file_name=f"{base}_processed.html",
                    mime="text/html",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col4:
                pdf = create_pdf(st.session_state['output'])
                st.download_button(
                    "📕 .pdf",
                    data=pdf,
                    file_name=f"{base}_processed.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280;'>
        <p>🚀 Optimized for Angular Material | Minimal API Calls | Rate Limit Safe</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
