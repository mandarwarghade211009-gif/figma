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

# ... [Keep all your existing helper functions unchanged until extract_ui_components] ...

def should_keep_imageurl(element: Dict[str, Any], category: str) -> bool:
    """
    Smart filter to determine if imageUrl should be kept for Angular agent.
    This reduces token usage while maintaining UI fidelity.
    """
    # Always keep for images category - these are actual visual assets
    if category == 'images':
        return True

    # Keep for buttons (likely contain icons or visual elements)
    if category == 'buttons':
        return True

    # For textElements, only keep if it's an icon font or very short text (likely icon)
    if category == 'textElements':
        text_content = element.get('text', {}).get('content', '')
        font_family = element.get('text', {}).get('typography', {}).get('fontFamily', '')

        # Check if it's an icon font
        is_icon_font = any(icon_font in font_family for icon_font in [
            'Font Awesome', 'Material Icons', 'Ionicons', 'Glyphicons', 'IcoFont', 
            'Material Design Icons', 'Feather', 'Heroicons'
        ])

        # Check if text is very short (likely an icon character)
        is_short = len(text_content.strip()) <= 3

        # Check if name suggests it's an icon
        name = element.get('name', '').lower()
        is_icon_name = any(keyword in name for keyword in ['icon', 'glyph', 'symbol'])

        return is_icon_font or (is_short and is_icon_name)

    # For navigation, keep if it's a logo, icon, or badge
    if category == 'navigation':
        name = element.get('name', '').lower()
        return any(keyword in name for keyword in ['logo', 'icon', 'badge', 'avatar', 'brand'])

    # For containers, only keep if there's an explicit image fill (background images)
    if category == 'containers':
        styling = element.get('styling', {})
        fills = styling.get('fills', [])
        return any(f.get('type') == 'image' for f in fills if isinstance(f, dict))

    # Default: don't keep for other categories
    return False

def optimize_imageurl_data(organized: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Remove unnecessary imageUrls to reduce token usage for Angular agent.
    Returns (optimized_data, optimization_stats)
    """
    optimized = copy.deepcopy(organized)

    stats = {
        'total_before': 0,
        'total_after': 0,
        'removed_by_category': {},
        'kept_categories': {}
    }

    # Process each category
    for category in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
        if category not in optimized:
            continue

        removed_count = 0
        kept_count = 0

        for element in optimized[category]:
            if 'imageUrl' in element:
                stats['total_before'] += 1

                if not should_keep_imageurl(element, category):
                    del element['imageUrl']
                    removed_count += 1
                else:
                    stats['total_after'] += 1
                    kept_count += 1

        if removed_count > 0:
            stats['removed_by_category'][category] = removed_count
        if kept_count > 0:
            stats['kept_categories'][category] = kept_count

    # Update metadata with optimization info
    if 'metadata' in optimized:
        optimized['metadata']['imageUrlOptimization'] = {
            'optimized': True,
            'totalBefore': stats['total_before'],
            'totalAfter': stats['total_after'],
            'removed': stats['total_before'] - stats['total_after'],
            'reductionPercent': round(((stats['total_before'] - stats['total_after']) / stats['total_before'] * 100), 1) if stats['total_before'] > 0 else 0
        }

    return optimized, stats

def extract_ui_components(merged_payload: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Extract UI components and return both organized data and optimization stats.
    Modified to return optimization statistics.
    """
    roots = find_document_roots(merged_payload)
    if not roots:
        raise RuntimeError("No document roots found in payload")

    all_components: List[Dict[str, Any]] = []
    for r in roots:
        if isinstance(r, dict):
            extract_components(r, "", all_components)

    organized = organize_for_angular(all_components)

    # Apply smart imageUrl optimization
    optimized, stats = optimize_imageurl_data(organized)

    return optimized, stats

# ... [Keep all other functions unchanged] ...

def main():
    # ... [Keep header and sidebar unchanged] ...

    # Tabs
    tab1, tab2 = st.tabs(["ðŸŽ¯ Figma Extraction", "âš¡ Angular Processor"])

    # --- Figma Extraction Tab ---
    with tab1:
        st.markdown("### Figma Component Extraction")
        st.markdown("Extract UI components with **smart imageURL optimization** for Angular agents.")
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
                    progress.progress(25)
                    image_refs, node_id_list, node_meta = walk_nodes_collect_images_and_ids(nodes_payload)

                    status.text("ðŸ”— Resolving image URLs from Figma...")
                    progress.progress(50)
                    filtered_fills, renders_map = resolve_image_urls(file_key, image_refs, node_id_list, token)

                    status.text("ðŸŽ¨ Building icon map and merging URLs into nodes...")
                    progress.progress(70)
                    node_to_url = build_icon_map(nodes_payload, filtered_fills, renders_map, node_meta)
                    merged_payload = merge_urls_into_nodes(nodes_payload, node_to_url)

                    status.text("ðŸ“¦ Extracting structured components with optimization...")
                    progress.progress(85)
                    final_output, optimization_stats = extract_ui_components(merged_payload)

                    status.text("âœ¨ Finalizing extraction...")
                    progress.progress(95)
                    # Keep full URLs in output for agent processing
                    st.session_state['metadata_json'] = final_output
                    st.session_state['optimization_stats'] = optimization_stats
                    st.session_state['stats']['files_processed'] += 1
                    progress.progress(100)
                    st.success("âœ… Extraction completed with smart optimization!")

                    # Enhanced metrics display
                    st.markdown("### ðŸ“Š Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Components", final_output['metadata']['totalComponents'])
                    with col2:
                        st.metric("Text Elements", len(final_output.get('textElements', [])))
                    with col3:
                        st.metric("Buttons", len(final_output.get('buttons', [])))
                    with col4:
                        st.metric("Containers", len(final_output.get('containers', [])))

                    # Show optimization results
                    if optimization_stats['total_before'] > 0:
                        st.markdown("### ðŸŽ¯ ImageURL Optimization")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Before", optimization_stats['total_before'])
                        with col2:
                            st.metric("After", optimization_stats['total_after'])
                        with col3:
                            reduction = optimization_stats['total_before'] - optimization_stats['total_after']
                            st.metric("Removed", reduction, 
                                     delta=f"-{round(reduction / optimization_stats['total_before'] * 100, 1)}%")

                    with st.expander("ðŸ“‹ Category Breakdown"):
                        for cat in ['textElements', 'buttons', 'inputs', 'containers', 'images', 'navigation', 'vectors', 'other']:
                            count = len(final_output.get(cat, []))
                            if count > 0:
                                kept = optimization_stats['kept_categories'].get(cat, 0)
                                st.markdown(f"- **{cat}**: `{count}` components, `{kept}` with imageUrl")

                except Exception as e:
                    st.error(f"âŒ Error during extraction: {str(e)}")

        # ... [Rest of the downloads section remains the same] ...

    # ... [Keep Angular Processor tab unchanged] ...

if __name__ == "__main__":
    main()
