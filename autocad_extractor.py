# requirements.txt
# streamlit==1.28.0
# ezdxf==1.1.0

import streamlit as st
import ezdxf
from io import StringIO
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="AutoCAD Metadata Extractor", page_icon="📐", layout="wide")

st.title("📐 AutoCAD Metadata Extractor")
st.markdown("Upload your AutoCAD DXF file to extract detailed metadata and information.")

# File uploader
uploaded_file = st.file_uploader("Choose a DXF file", type=['dxf'])

def extract_metadata(doc):
    """Extract comprehensive metadata from DXF document"""
    metadata = StringIO()
    
    # Header Information
    metadata.write("="*60 + "\n")
    metadata.write("AUTOCAD FILE METADATA\n")
    metadata.write("="*60 + "\n\n")
    
    # Drawing Information
    metadata.write("--- DRAWING INFORMATION ---\n")
    metadata.write(f"AutoCAD Version: {doc.dxfversion}\n")
    metadata.write(f"Extraction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Header variables
    if doc.header:
        metadata.write(f"\nDrawing Units: {doc.header.get('$INSUNITS', 'Not specified')}\n")
        metadata.write(f"Creation Date: {doc.header.get('$TDCREATE', 'Not available')}\n")
        metadata.write(f"Last Update: {doc.header.get('$TDUPDATE', 'Not available')}\n")
    
    metadata.write("\n" + "-"*60 + "\n\n")
    
    # Layers Information
    metadata.write("--- LAYERS ---\n")
    layers = list(doc.layers)
    metadata.write(f"Total Layers: {len(layers)}\n\n")
    for layer in layers:
        metadata.write(f"  • Layer: {layer.dxf.name}\n")
        metadata.write(f"    Color: {layer.dxf.color}\n")
        metadata.write(f"    Linetype: {layer.dxf.linetype}\n")
        metadata.write(f"    On/Off: {'On' if not layer.is_off() else 'Off'}\n")
        metadata.write(f"    Frozen: {'Yes' if layer.is_frozen() else 'No'}\n\n")
    
    metadata.write("-"*60 + "\n\n")
    
    # Entity Statistics
    metadata.write("--- ENTITY STATISTICS ---\n")
    msp = doc.modelspace()
    entities = list(msp)
    
    entity_counts = {}
    for entity in entities:
        entity_type = entity.dxftype()
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
    
    metadata.write(f"Total Entities: {len(entities)}\n\n")
    for entity_type, count in sorted(entity_counts.items()):
        metadata.write(f"  • {entity_type}: {count}\n")
    
    metadata.write("\n" + "-"*60 + "\n\n")
    
    # Text Entities
    metadata.write("--- TEXT CONTENT ---\n")
    text_entities = [e for e in entities if e.dxftype() in ['TEXT', 'MTEXT', 'ATTRIB']]
    metadata.write(f"Total Text Entities: {len(text_entities)}\n\n")
    
    for i, text in enumerate(text_entities[:50], 1):  # Limit to first 50
        if text.dxftype() == 'TEXT':
            metadata.write(f"{i}. {text.dxf.text} (Layer: {text.dxf.layer})\n")
        elif text.dxftype() == 'MTEXT':
            content = text.text[:100]  # Limit length
            metadata.write(f"{i}. {content} (Layer: {text.dxf.layer})\n")
        elif text.dxftype() == 'ATTRIB':
            metadata.write(f"{i}. {text.dxf.text} (Layer: {text.dxf.layer})\n")
    
    if len(text_entities) > 50:
        metadata.write(f"\n... and {len(text_entities) - 50} more text entities\n")
    
    metadata.write("\n" + "-"*60 + "\n\n")
    
    # Blocks Information
    metadata.write("--- BLOCKS ---\n")
    blocks = [b for b in doc.blocks if not b.name.startswith('*')]
    metadata.write(f"Total Block Definitions: {len(blocks)}\n\n")
    
    for block in blocks[:20]:  # Limit to first 20
        metadata.write(f"  • Block: {block.name}\n")
        block_entities = list(block)
        metadata.write(f"    Entities in block: {len(block_entities)}\n\n")
    
    if len(blocks) > 20:
        metadata.write(f"... and {len(blocks) - 20} more blocks\n")
    
    metadata.write("\n" + "-"*60 + "\n\n")
    
    # Detailed Entity Information (sample)
    metadata.write("--- DETAILED ENTITY SAMPLES (First 20) ---\n\n")
    for i, entity in enumerate(entities[:20], 1):
        metadata.write(f"{i}. Type: {entity.dxftype()}\n")
        metadata.write(f"   Layer: {entity.dxf.layer}\n")
        metadata.write(f"   Color: {entity.dxf.color}\n")
        
        if entity.dxftype() == 'LINE':
            metadata.write(f"   Start: ({entity.dxf.start.x:.2f}, {entity.dxf.start.y:.2f})\n")
            metadata.write(f"   End: ({entity.dxf.end.x:.2f}, {entity.dxf.end.y:.2f})\n")
        elif entity.dxftype() == 'CIRCLE':
            metadata.write(f"   Center: ({entity.dxf.center.x:.2f}, {entity.dxf.center.y:.2f})\n")
            metadata.write(f"   Radius: {entity.dxf.radius:.2f}\n")
        elif entity.dxftype() == 'TEXT':
            metadata.write(f"   Text: {entity.dxf.text}\n")
            metadata.write(f"   Position: ({entity.dxf.insert.x:.2f}, {entity.dxf.insert.y:.2f})\n")
        
        metadata.write("\n")
    
    metadata.write("="*60 + "\n")
    metadata.write("END OF METADATA REPORT\n")
    metadata.write("="*60 + "\n")
    
    return metadata.getvalue()

if uploaded_file is not None:
    try:
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Read the DXF file
        with st.spinner('Processing AutoCAD file...'):
            doc = ezdxf.readfile(tmp_file_path)
            metadata_text = extract_metadata(doc)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        st.success("✅ Metadata extracted successfully!")
        
        # Display metadata in text area
        st.text_area("Extracted Metadata", metadata_text, height=400)
        
        # Download button
        st.download_button(
            label="📥 Download Metadata as TXT",
            data=metadata_text,
            file_name=f"{uploaded_file.name.replace('.dxf', '')}_metadata.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Make sure you're uploading a valid DXF file.")

else:
    st.info("👆 Please upload a DXF file to begin extraction.")
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload** your AutoCAD DXF file using the file uploader above
        2. Wait for the processing to complete
        3. **Review** the extracted metadata in the text area
        4. **Download** the metadata as a TXT file using the download button
        
        ### What metadata is extracted?
        - Drawing information (version, units, dates)
        - Layer details (names, colors, properties)
        - Entity statistics (counts of lines, circles, text, etc.)
        - Text content from the drawing
        - Block definitions
        - Detailed entity information with coordinates
        
        ### Supported file format:
        - DXF (Drawing Exchange Format) files
        
        **Note:** For DWG files, please convert them to DXF format first using AutoCAD or a converter.
        """)