import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="Figma to Angular: Minimal Metadata Extractor", layout="wide")
st.title("🎨 Figma to Angular Metadata Extractor (Optimized)")

# Sidebar config
st.sidebar.header("Figma API Configuration")
figma_token = st.sidebar.text_input("Figma Access Token", value=os.getenv("FIGMA_TOKEN", ""), type="password")
figma_file_key = st.sidebar.text_input("Figma File Key", value=os.getenv("FIGMA_FILE_KEY", "R5S3P10vjXm5bTdtZSIVq3"))
figma_node_ids = st.sidebar.text_input("Node IDs (comma-separated)", value=os.getenv("FIGMA_NODE_IDS", "19-4818"))

st.sidebar.markdown("---")
st.sidebar.header("Extraction Options")
max_depth = st.sidebar.slider("Max extraction depth", min_value=1, max_value=8, value=5)

ESSENTIAL_FIELDS = [
    "type", "name", "id", "absoluteBoundingBox", "fills", "strokes", "cornerRadius",
    "opacity", "characters", "style", "children", "constraints", "layoutMode",
    "componentProperties", "componentPropertyDefinitions", "imageRef"
]

def clean_node(node, depth=0, max_depth=5):
    if depth > max_depth:
        return None
    cleaned = {k: node[k] for k in ESSENTIAL_FIELDS if k in node}
    if "children" in cleaned:
        cleaned["children"] = [
            c for c in (clean_node(child, depth+1, max_depth) for child in cleaned["children"]) if c
        ]
    return cleaned

class FigmaAPI:
    def __init__(self, token: str):
        self.base = "https://api.figma.com/v1"
        self.headers = {"X-Figma-Token": token}

    def fetch_nodes(self, file_key: str, node_ids: str):
        url = f"{self.base}/files/{file_key}/nodes"
        resp = requests.get(url, headers=self.headers, params={"ids": node_ids})
        resp.raise_for_status()
        return resp.json()["nodes"]

if st.button("Extract Metadata", use_container_width=True):
    if not (figma_token and figma_file_key and figma_node_ids):
        st.error("Please provide all Figma credentials and node IDs.")
    else:
        try:
            figma = FigmaAPI(figma_token)
            nodes_data = figma.fetch_nodes(figma_file_key, figma_node_ids)
            output = {}
            for node_id, node_wrapper in nodes_data.items():
                if "document" in node_wrapper:
                    cleaned = clean_node(node_wrapper["document"], 0, max_depth)
                    if cleaned:
                        output[node_id] = cleaned
            st.success(f"Extracted {len(output)} node(s).")
            st.json(output)
            # Download button for clean JSON
            st.download_button("Download JSON", json.dumps(output, indent=2), file_name=f"figma_{figma_file_key}_meta.json")
        except requests.exceptions.HTTPError as e:
            st.error(f"API error: {e.response.status_code}")
        except Exception as ex:
            st.error(f"Failed: {str(ex)}")
