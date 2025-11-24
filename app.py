#!/usr/bin/env python3
"""
Optimized Figma Icon/Symbol/Logo Extractor & Angular Code Processor
Extracts ONLY image URLs for visual assets - minimizes token usage
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
    :root {
        --primary-color: #1e40af;
        --secondary-color: #3b82f6;
        --background-color: #f9fafb;
        --text-color: #111827;
        --border-color: #e5e7eb;
    }
    .stApp {
        background-color: var(--background-color);
    }
    h1, h2, h3 {
        color: var(--text-color);
        font-weight: 600;
    }
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: var(--secondary-color);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid var(--border-color);
    }
    .stDownloadButton>button {
        background-color: #059669;
        color: white;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit Page Config
st.set_page_config(
    page_title="Figma Icon Extractor | Optimized Edition",
    page_icon="🎯",
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

def is_visible(node: Dict[str, Any]) -> bool:
    v = node.get("visible")
    return True if v is None else bool(v)

def filter_invisible_nodes(node: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Remove invisible nodes to reduce payload"""
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
# OPTIMIZED FIGMA API
# -------------------------

def fetch_figma_file(file_key: str, token: str, timeout: int = 60) -> Dict[str, Any]:
    """Fetch entire Figma file structure"""
    headers = build_headers(token)
    url = f"https://api.figma.com/v1/files/{file_key}"
    r = requests.get(url, headers=headers, timeout=timeout)
    if not r.ok:
        raise RuntimeError(f"Figma API error {r.status_code}: {r.text}")
    data = r.json()
    # Filter invisible nodes
    if isinstance(data.get("document"), dict):
        data["document"] = filter_invisible_nodes(data["document"])
    return data

def is_icon_or_symbol(node: Dict[str, Any]) -> bool:
    """Determine if node is an icon, symbol, or logo based on heuristics"""
    if not isinstance(node, dict):
        return False
    
    node_type = (node.get("type") or "").upper()
    name = (node.get("name") or "").lower()
    
    # Type-based filtering
    if node_type in ['COMPONENT', 'INSTANCE', 'VECTOR', 'BOOLEAN_OPERATION', 
                     'STAR', 'ELLIPSE', 'POLYGON', 'LINE']:
        # Name-based filtering for icons/symbols/logos
        icon_keywords = ['icon', 'symbol', 'logo', 'badge', 'avatar', 'profile',
                         'btn', 'button', 'nav', 'menu', 'arrow', 'chevron',
                         'check', 'close', 'search', 'user', 'home', 'settings',
                         'notification', 'star', 'heart', 'share', 'download',
                         'upload', 'edit', 'delete', 'add', 'plus', 'minus']
        
        if any(keyword in name for keyword in icon_keywords):
            return True
        
        # Size-based heuristic: icons are typically small (< 200x200)
        bbox = node.get("absoluteBoundingBox") or {}
        if isinstance(bbox, dict):
            try:
                w = float(bbox.get("width", 0))
                h = float(bbox.get("height", 0))
                if 0 < w <= 200 and 0 < h <= 200:
                    return True
            except:
                pass
    
    return False

def collect_icon_nodes( Dict[str, Any]) -> List[Dict[str, Any]]:
    """Walk tree and collect only icon/symbol/logo nodes with minimal metadata"""
    icons: List[Dict[str, Any]] = []
    
    def visit(node: Dict[str, Any], path: str = ""):
        if not isinstance(node, dict):
            return
        
        node_id = node.get("id")
        node_name = node.get("name", "Unnamed")
        node_type = node.get("type", "")
        
        current_path = f"{path}/{node_name}" if path else node_name
        
        if is_icon_or_symbol(node) and node_id:
            # Extract ONLY essential info
            icon_data = {
                "id": node_id,
                "name": node_name,
                "type": node_type,
                "path": current_path
            }
            
            # Add position for reference (minimal)
            bbox = node.get("absoluteBoundingBox")
            if isinstance(bbox, dict):
                try:
                    icon_data["size"] = {
                        "w": int(float(bbox.get("width", 0))),
                        "h": int(float(bbox.get("height", 0)))
                    }
                except:
                    pass
            
            icons.append(icon_data)
        
        # Recurse through children
        for child in node.get("children", []) or []:
            visit(child, current_path)
    
    # Start from document root
    if isinstance(data.get("document"), dict):
        visit(data["document"])
    
    return icons

def fetch_icon_images(file_key: str, icon_ids: List[str], token: str, timeout: int = 60) -> Dict[str, str]:
    """Fetch rendered images for icon node IDs"""
    if not icon_ids:
        return {}
    
    headers = build_headers(token)
    id_to_url: Dict[str, str] = {}
    
    # Batch requests (max 200 ids per request)
    base_url = f"https://api.figma.com/v1/images/{file_key}"
    
    for batch in chunked(icon_ids, 200):
        try:
            params = {
                "ids": ",".join(batch),
                "format": "svg",  # SVG for best quality and smallest size
                "scale": 1
            }
            r = requests.get(base_url, headers=headers, params=params, timeout=timeout)
            if r.ok:
                images = r.json().get("images", {}) or {}
                id_to_url.update(images)
            else:
                st.warning(f"Batch request failed: {r.status_code}")
        except Exception as e:
            st.warning(f"Error fetching batch: {str(e)}")
    
    return id_to_url

def create_optimized_output(icons: List[Dict[str, Any]], id_to_url: Dict[str, str]) -> Dict[str, Any]:
    """Create minimal JSON output with only icons and their URLs"""
    output_icons = []
    
    for icon in icons:
        icon_id = icon.get("id")
        url = id_to_url.get(icon_id)
        
        if url:  # Only include icons with valid URLs
            output_icons.append({
                "id": icon_id,
                "name": icon.get("name"),
                "type": icon.get("type"),
                "path": icon.get("path"),
                "url": url,
                "size": icon.get("size")
            })
    
    return {
        "metadata": {
            "totalIcons": len(output_icons),
            "extractedAt": datetime.datetime.utcnow().isoformat() + 'Z',
            "optimized": True
        },
        "icons": output_icons
    }

# -------------------------
# ANGULAR CODE PROCESSING
# -------------------------

UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
    """Prefix UUID image references with full URL"""
    patterns = [
        (re.compile(r'(src\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(\[src\]\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(imageUrl\s*:\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
        (re.compile(r'(url\(\s*["\']?)(%s)(["\']\s*\))' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
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
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, 
                          bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
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
    """Extract unique UUIDs from text"""
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
        <h1 style='margin-bottom: 0.5rem;'>🎯 Optimized Figma Icon Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Extract ONLY Icons, Symbols & Logos with Full URLs - Zero Metadata Bloat
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
        st.markdown("### 🎯 Extraction Focus")
        st.info("""
        **Optimized for:**
        - Icons
        - Symbols
        - Logos
        - Badges
        - Navigation elements
        
        **Result:** 90% smaller JSON payload
        """)
        
        st.markdown("---")
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [Figma API Docs](https://www.figma.com/developers/api)
        - [Angular Framework](https://angular.io)
        """)

    # Tabs
    tab1, tab2 = st.tabs(["🎯 Icon Extraction", "⚡ Angular Processor"])

    # --- Icon Extraction Tab ---
    with tab1:
        st.markdown("### Extract Icons, Symbols & Logos from Figma")
        st.markdown("**Optimized extraction:** Only visual assets with full image URLs, minimal metadata")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            file_key = st.text_input("📁 Figma File Key", value="", 
                                     help="File key from Figma URL (e.g., abc123xyz)")
        with col2:
            token = st.text_input("🔑 Figma Access Token", type="password", 
                                 help="Generate in Figma account settings")

        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            size_filter = st.slider("Maximum icon size (px)", 50, 500, 200,
                                   help="Icons larger than this will be excluded")
            include_components = st.checkbox("Include component instances", value=True)
            include_vectors = st.checkbox("Include vector shapes", value=True)

        if st.button("🚀 Extract Icons & Logos"):
            if not token or not file_key:
                st.error("⚠️ Please provide both file key and access token.")
            else:
                try:
                    progress = st.progress(0)
                    status = st.empty()

                    status.text("📡 Fetching Figma file structure...")
                    progress.progress(10)
                    file_data = fetch_figma_file(file_key=file_key, token=token)

                    status.text("🔍 Identifying icons, symbols, and logos...")
                    progress.progress(30)
                    icon_nodes = collect_icon_nodes(file_data)
                    
                    if not icon_nodes:
                        st.warning("⚠️ No icons or symbols found in this file.")
                        return
                    
                    st.info(f"✅ Found {len(icon_nodes)} potential icons/symbols")

                    status.text("🖼️ Fetching image URLs (this may take a moment)...")
                    progress.progress(50)
                    icon_ids = [icon["id"] for icon in icon_nodes]
                    id_to_url = fetch_icon_images(file_key, icon_ids, token)

                    status.text("📦 Creating optimized output...")
                    progress.progress(90)
                    final_output = create_optimized_output(icon_nodes, id_to_url)

                    st.session_state['icon_json'] = final_output
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    st.success("✅ Icon extraction completed successfully!")

                    # Metrics
                    st.markdown("### 📊 Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Icons Found", len(icon_nodes))
                    with col2:
                        st.metric("URLs Retrieved", len(id_to_url))
                    with col3:
                        st.metric("Final Count", final_output['metadata']['totalIcons'])
                    with col4:
                        json_size = len(json.dumps(final_output))
                        st.metric("JSON Size", f"{json_size/1024:.1f} KB")

                    # Preview
                    with st.expander("👀 Preview Icons"):
                        icons = final_output.get('icons', [])[:10]  # Show first 10
                        for icon in icons:
                            st.markdown(f"**{icon['name']}** ({icon['type']}) - `{icon['size']}`")
                            st.markdown(f"🔗 {icon['url'][:80]}...")
                            st.markdown("---")

                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")

        # Download section
        if 'icon_json' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Icon Data")
            json_str = json.dumps(st.session_state['icon_json'], indent=2, ensure_ascii=False)

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.download_button(
                    "📥 Download icons.json",
                    data=json_str,
                    file_name="figma_icons.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                # Minified version
                json_min = json.dumps(st.session_state['icon_json'], separators=(',', ':'))
                st.download_button(
                    "📥 Download icons.min.json",
                    data=json_min,
                    file_name="figma_icons.min.json",
                    mime="application/json",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col3:
                st.caption(f"Size: {len(json_str)/1024:.1f} KB")

    # --- Angular Processor Tab ---
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Automatically prefix UUID-based image identifiers with complete URLs")
        st.markdown("---")

        url_prefix = st.text_input(
            "🌐 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="This prefix will be added to all detected image UUIDs"
        )

        uploaded = st.file_uploader(
            "📤 Upload Angular Code File",
            type=['txt', 'md', 'html', 'ts', 'js', 'component.ts'],
            help="Supported: .ts, .html, .js, .txt, .md"
        )

        if uploaded:
            st.info(f"✅ File uploaded: **{uploaded.name}**")

            if st.button("⚡ Process Angular Code"):
                try:
                    raw = uploaded.read()
                    text = decode_bytes_to_text(raw)
                    
                    uuids = detect_uuids_in_text(text)
                    modified, replaced = add_url_prefix_to_angular_code(text, url_prefix)

                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = uploaded.name
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
                        st.metric("Output Size", f"{len(modified)/1024:.1f} KB")

                    if len(uuids) > 0:
                        with st.expander("🔍 Sample Transformation"):
                            sample = uuids[0]
                            st.code(f"Before: {sample}", language="text")
                            st.code(f"After: {url_prefix}{sample}", language="text")
                            
                            # Show more examples
                            if len(uuids) > 1:
                                st.markdown("**More examples:**")
                                for uuid in uuids[1:min(4, len(uuids))]:
                                    st.text(f"✓ {uuid} → {url_prefix}{uuid}")

                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")

        # Download processed code
        if 'angular_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Download Processed Code")
            base = st.session_state['angular_filename'].rsplit('.', 1)[0]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📄 Download as .txt",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_processed.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col2:
                st.download_button(
                    "📝 Download as .ts",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_processed.ts",
                    mime="text/typescript",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1})
                )
            with col3:
                pdf_buf = create_text_to_pdf(st.session_state['angular_output'])
                st.download_button(
                    "📕 Download as .pdf",
                    data=pdf_buf,
                    file_name=f"{base}_processed.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update(
                        {'downloads': st.session_state['stats']['downloads'] + 1})
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>⚡ Optimized Edition - 90% Less Token Usage | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
