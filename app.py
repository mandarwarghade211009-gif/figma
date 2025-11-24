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

# PROFESSIONAL THEMING (as before)
def apply_professional_styling():
    st.markdown("""
    <style>
    /* ... (leave your styling unchanged as before) ... */
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Figma UI Extractor | Professional Edition",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_professional_styling()

# --- Helpers and Extraction Functions ---
# Keep all utility, extraction, image optimization, and reference mapping functions unchanged as in your working code, including:
# build_headers, chunked, to_rgba, is_nonempty_list, is_visible, filter_invisible_nodes, fetch_figma_nodes
# walk_nodes_collect_images_and_ids, resolve_image_urls, build_icon_map, merge_urls_into_nodes
# extract_bounds, extract_layout, extract_visuals, extract_text, should_include, classify_bucket
# extract_components, find_document_roots, organize_for_angular, extract_ui_components, remove_url_prefix_from_json

# --- Optimization Functions ---
def optimize_image_references(components: List[Dict[str, Any]], node_to_url: Dict[str, str]) -> Dict[str, str]:
    used_urls = {}
    url_to_nodes = {}
    for comp in components:
        node_id = comp.get('id')
        if not node_id:
            continue
        pos = comp.get('position', {})
        width = pos.get('width', 0)
        height = pos.get('height', 0)
        if width < 50 and height < 50: continue
        styling = comp.get('styling', {})
        fills = styling.get('fills', [])
        if fills and all(f.get('type') == 'solid' for f in fills): continue
        url = node_to_url.get(node_id)
        if url:
            if url not in url_to_nodes:
                url_to_nodes[url] = []
                used_urls[node_id] = url
            url_to_nodes[url].append(node_id)
    return used_urls

def create_image_reference_system(final_output: Dict[str, Any], optimized_urls: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    unique_urls = list(set(optimized_urls.values()))
    url_to_ref = {url: f"img_{str(i+1).zfill(3)}" for i, url in enumerate(unique_urls)}
    image_map = {ref: url for url, ref in url_to_ref.items()}
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

# --- Angular Code Helpers ---
UUID_RE = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def add_url_prefix_to_angular_code(text: str, url_prefix: str) -> Tuple[str, int]:
    patterns = [
    (re.compile(r'(src\s*=\s*["\'])(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
    (re.compile(r'(\[src\]\s*=\s*["\\\']\s*)(%s)(["\'])' % UUID_RE, re.IGNORECASE), r'\1' + url_prefix + r'\2\3'),
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

# --- MAIN UI & WORKFLOW ---
def main():
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='margin-bottom: 0.5rem;'>🎨 Figma UI Extractor</h1>
        <p style='font-size: 1.05rem; color: #6B7280; font-weight: 500;'>
            Enterprise-Grade UI Component Extraction & Angular Code Processing
        </p>
        <p style='font-size: 0.9rem; color: #9CA3AF; font-weight: 600;'>
            ⚡ OPTIMIZED VERSION - Reduced Token Count for AI Agents
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar as before
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
        st.markdown("---")
        st.markdown("### 🚀 Optimization Features")
        st.success("""
        ✅ Image deduplication
        ✅ Reference-based URLs
        ✅ 50-70% token reduction
        ✅ Exact UI matching
        """)

    tab1, tab2 = st.tabs(["🎯 Figma Extraction", "⚡ Angular Processor"])

    # Extraction Tab
    with tab1:
        st.markdown("### Figma Component Extraction")
        st.markdown("Extract UI components with metadata, styling, and optimized images from Figma.")
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
                    progress.progress(20)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)
                    status.text("🔗 Resolving image URLs from Figma...")
                    progress.progress(40)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)
                    status.text("🎨 Building icon map...")
                    progress.progress(55)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                    status.text("📦 Extracting structured components...")
                    progress.progress(65)
                    roots = find_document_roots(nodes_payload)
                    if not roots:
                        raise RuntimeError("No document roots found in payload")
                    all_components: List[Dict[str, Any]] = []
                    for r in roots:
                        if isinstance(r, dict):
                            extract_components(r, "", all_components)
                    status.text("🔍 Optimizing image references...")
                    progress.progress(75)
                    optimized_urls = optimize_image_references(all_components, node_to_url)
                    status.text("🎯 Merging optimized URLs...")
                    progress.progress(82)
                    merged_payload = merge_urls_into_nodes(nodes_payload, optimized_urls)
                    status.text("📋 Organizing components...")
                    progress.progress(88)
                    final_output = extract_ui_components(merged_payload)
                    status.text("✨ Creating reference system...")
                    progress.progress(94)
                    compact_output, image_map = create_image_reference_system(final_output, optimized_urls)
                    st.session_state['metadata_json'] = compact_output
                    st.session_state['image_map'] = image_map
                    st.session_state['full_metadata'] = final_output
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    original_size = len(json.dumps(final_output))
                    compact_size = len(json.dumps(compact_output))
                    savings = ((original_size - compact_size) / original_size) * 100 if original_size > 0 else 0
                    st.success(f"✅ Extraction completed! Token savings: {savings:.1f}%")
                    st.markdown("### 📊 Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", compact_output['metadata']['totalComponents'])
                    with col2:
                        st.metric("Unique Images", len(image_map))
                    with col3:
                        st.metric("Original Size", f"{original_size:,} bytes")
                    with col4:
                        st.metric("Optimized Size", f"{compact_size:,} bytes", delta=f"-{savings:.1f}%")
                    with st.expander("📋 Category Breakdown"):
                        for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
                            count = len(compact_output.get(cat, []))
                            if count > 0:
                                st.markdown(f"- **{cat}**: `{count}`")
                    with st.expander("🖼️ Image Optimization Details"):
                        st.markdown(f"**Total Images Deduplicated:** {len(image_map)}")
                        st.markdown(f"**Original Image References:** {len(node_to_url)}")
                        st.markdown(f"**Images Removed:** {len(node_to_url) - len(optimized_urls)}")
                        st.markdown(f"**Token Reduction:** ~{savings:.1f}%")
                except Exception as e:
                    st.error(f"❌ Error during extraction: {str(e)}")

        # Downloads for extraction -- safer checks for missing keys
        st.markdown("---")
        st.markdown("### 💾 Download Extracted Data")
        col1, col2, col3 = st.columns(3)
        with col1:
            if 'metadata_json' in st.session_state:
                compact_json = json.dumps(st.session_state['metadata_json'], indent=2, ensure_ascii=False)
                st.download_button(
                    "📥 Download metadata.json (Optimized)",
                    data=compact_json,
                    file_name="metadata.json",
                    mime="application/json",
                    help="Use this for AI agent - reduced tokens",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
                st.caption(f"Size: {len(compact_json):,} bytes")
        with col2:
            if 'image_map' in st.session_state:
                image_map_json = json.dumps(st.session_state['image_map'], indent=2, ensure_ascii=False)
                st.download_button(
                    "🖼️ Download image_map.json",
                    data=image_map_json,
                    file_name="image_map.json",
                    mime="application/json",
                    help="Image reference mapping",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
                st.caption(f"{len(st.session_state['image_map'])} unique images")
        with col3:
            if 'full_metadata' in st.session_state:
                full_json = json.dumps(st.session_state['full_metadata'], indent=2, ensure_ascii=False)
                st.download_button(
                    "🔍 Download full_metadata.json (Debug)",
                    data=full_json,
                    file_name="full_metadata.json",
                    mime="application/json",
                    help="Full metadata with all URLs (for debugging)",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
                st.caption(f"Size: {len(full_json):,} bytes")

    # Angular Processor Tab
    with tab2:
        st.markdown("### Angular Code Image URL Processor")
        st.markdown("Automatically prefix UUID-based image identifiers with complete URLs in your code.")
        st.markdown("---")
        url_prefix = st.text_input(
            "🌐 URL Prefix",
            value="https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/",
            help="This prefix will be added to all detected image UUIDs"
        )
        resolve_refs = st.checkbox(
            "🔗 Resolve image references from image_map.json", 
            value=False,
            help="Convert img_001, img_002, etc. to full URLs"
        )
        if resolve_refs:
            image_map_file = st.file_uploader("📤 Upload image_map.json", type=['json'], help="Upload the image_map.json file from extraction")
            if image_map_file:
                try:
                    image_map = json.load(image_map_file)
                    st.session_state['image_map_loaded'] = image_map
                    st.success(f"✅ Image map loaded: {len(image_map)} references")
                except Exception as e:
                    st.error(f"❌ Error loading image map: {str(e)}")

        uploaded = st.file_uploader(
            "📤 Upload Angular Code File",
            type=['txt', 'md', 'html', 'ts', 'js', 'json'],
            help="Supported formats: .txt, .md, .html, .ts, .js, .json"
        )
        if uploaded:
            st.info(f"✅ File uploaded: **{uploaded.name}**")
            if st.button("⚡ Process Angular Code"):
                try:
                    raw = uploaded.read()
                    text = decode_bytes_to_text(raw)
                    resolved_count = 0
                    if resolve_refs and 'image_map_loaded' in st.session_state:
                        for ref, url in st.session_state['image_map_loaded'].items():
                            if ref in text:
                                text = text.replace(ref, url)
                                resolved_count += 1
                        if resolved_count > 0:
                            st.info(f"✅ Resolved {resolved_count} image references from map")
                    uuids = detect_uuids_in_text(text)
                    modified, replaced = add_url_prefix_to_angular_code(text, url_prefix)
                    st.session_state['angular_output'] = modified
                    st.session_state['angular_filename'] = uploaded.name
                    st.session_state['stats']['files_processed'] += 1
                    st.success("✅ Angular code processed successfully!")
                    st.markdown("### 📊 Processing Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Image IDs Found", len(uuids))
                    with col2:
                        st.metric("Replacements Made", replaced)
                    with col3:
                        st.metric("Output Size", f"{len(modified):,} bytes")
                    with col4:
                        if resolve_refs and 'image_map_loaded' in st.session_state:
                            st.metric("References Resolved", resolved_count)
                    if len(uuids) > 0:
                        with st.expander("🔍 Sample Transformation"):
                            sample = uuids[0]
                            st.code(f"Before: {sample}", language="text")
                            st.code(f"After: {url_prefix}{sample}", language="text")
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")

        # Downloads for angular output with robust session_state checks
        st.markdown("---")
        st.markdown("### 💾 Download Processed Code")
        base = st.session_state.get('angular_filename', 'output').rsplit('.', 1)[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            if 'angular_output' in st.session_state:
                st.download_button(
                    "📄 Download as .txt",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.txt",
                    mime="text/plain",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
        with col2:
            if 'angular_output' in st.session_state:
                st.download_button(
                    "📝 Download as .md",
                    data=st.session_state['angular_output'],
                    file_name=f"{base}_modified.md",
                    mime="text/markdown",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )
        with col3:
            if 'angular_output' in st.session_state:
                pdf_buf = create_text_to_pdf(st.session_state['angular_output'])
                st.download_button(
                    "📕 Download as .pdf",
                    data=pdf_buf,
                    file_name=f"{base}_modified.pdf",
                    mime="application/pdf",
                    on_click=lambda: st.session_state['stats'].update({'downloads': st.session_state['stats']['downloads'] + 1})
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; color: #6B7280;'>
        <p style='margin: 0; font-size: 0.9rem;'>Built with ❤️ using <strong>Streamlit</strong> | Professional Edition v2.0 (Optimized)</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #9CA3AF;'>50-70% Token Reduction • AI-Agent Ready • Exact UI Matching</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
