# # requirements.txt
# # streamlit==1.28.0
# # ezdxf==1.1.0

# import streamlit as st
# import ezdxf
# from io import StringIO
# import tempfile
# import os
# from datetime import datetime

# st.set_page_config(page_title="AutoCAD Metadata Extractor", page_icon="📐", layout="wide")

# st.title("📐 AutoCAD Metadata Extractor")
# st.markdown("Upload your AutoCAD DXF file to extract detailed metadata and information.")

# # File uploader
# uploaded_file = st.file_uploader("Choose a DXF file", type=['dxf'])

# def extract_metadata(doc):
#     """Extract comprehensive metadata from DXF document"""
#     metadata = StringIO()
    
#     # Header Information
#     metadata.write("="*60 + "\n")
#     metadata.write("AUTOCAD FILE METADATA\n")
#     metadata.write("="*60 + "\n\n")
    
#     # Drawing Information
#     metadata.write("--- DRAWING INFORMATION ---\n")
#     metadata.write(f"AutoCAD Version: {doc.dxfversion}\n")
#     metadata.write(f"Extraction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
#     # Header variables
#     if doc.header:
#         metadata.write(f"\nDrawing Units: {doc.header.get('$INSUNITS', 'Not specified')}\n")
#         metadata.write(f"Creation Date: {doc.header.get('$TDCREATE', 'Not available')}\n")
#         metadata.write(f"Last Update: {doc.header.get('$TDUPDATE', 'Not available')}\n")
    
#     metadata.write("\n" + "-"*60 + "\n\n")
    
#     # Layers Information
#     metadata.write("--- LAYERS ---\n")
#     layers = list(doc.layers)
#     metadata.write(f"Total Layers: {len(layers)}\n\n")
#     for layer in layers:
#         metadata.write(f"  • Layer: {layer.dxf.name}\n")
#         metadata.write(f"    Color: {layer.dxf.color}\n")
#         metadata.write(f"    Linetype: {layer.dxf.linetype}\n")
#         metadata.write(f"    On/Off: {'On' if not layer.is_off() else 'Off'}\n")
#         metadata.write(f"    Frozen: {'Yes' if layer.is_frozen() else 'No'}\n\n")
    
#     metadata.write("-"*60 + "\n\n")
    
#     # Entity Statistics
#     metadata.write("--- ENTITY STATISTICS ---\n")
#     msp = doc.modelspace()
#     entities = list(msp)
    
#     entity_counts = {}
#     for entity in entities:
#         entity_type = entity.dxftype()
#         entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
    
#     metadata.write(f"Total Entities: {len(entities)}\n\n")
#     for entity_type, count in sorted(entity_counts.items()):
#         metadata.write(f"  • {entity_type}: {count}\n")
    
#     metadata.write("\n" + "-"*60 + "\n\n")
    
#     # Text Entities
#     metadata.write("--- TEXT CONTENT ---\n")
#     text_entities = [e for e in entities if e.dxftype() in ['TEXT', 'MTEXT', 'ATTRIB']]
#     metadata.write(f"Total Text Entities: {len(text_entities)}\n\n")
    
#     for i, text in enumerate(text_entities, 1):  # Show ALL text entities
#         if text.dxftype() == 'TEXT':
#             metadata.write(f"{i}. {text.dxf.text} (Layer: {text.dxf.layer})\n")
#         elif text.dxftype() == 'MTEXT':
#             content = text.text  # Show full content
#             metadata.write(f"{i}. {content} (Layer: {text.dxf.layer})\n")
#         elif text.dxftype() == 'ATTRIB':
#             metadata.write(f"{i}. {text.dxf.text} (Layer: {text.dxf.layer})\n")
    
#     metadata.write("\n" + "-"*60 + "\n\n")
    
#     # Blocks Information
#     metadata.write("--- BLOCKS ---\n")
#     blocks = [b for b in doc.blocks if not b.name.startswith('*')]
#     metadata.write(f"Total Block Definitions: {len(blocks)}\n\n")
    
#     for block in blocks:  # Show ALL blocks
#         metadata.write(f"  • Block: {block.name}\n")
#         block_entities = list(block)
#         metadata.write(f"    Entities in block: {len(block_entities)}\n\n")
    
#     metadata.write("\n" + "-"*60 + "\n\n")
    
#     # Detailed Entity Information (ALL entities)
#     metadata.write("--- DETAILED ENTITY INFORMATION (ALL ENTITIES) ---\n")
#     metadata.write(f"Total Entities to Detail: {len(entities)}\n\n")
    
#     for i, entity in enumerate(entities, 1):  # Show ALL entities, no limit
#         metadata.write(f"{i}. Type: {entity.dxftype()}\n")
#         metadata.write(f"   Layer: {entity.dxf.layer}\n")
#         metadata.write(f"   Color: {entity.dxf.color}\n")
        
#         try:
#             if entity.dxftype() == 'LINE':
#                 metadata.write(f"   Start: ({entity.dxf.start.x:.2f}, {entity.dxf.start.y:.2f})\n")
#                 metadata.write(f"   End: ({entity.dxf.end.x:.2f}, {entity.dxf.end.y:.2f})\n")
#             elif entity.dxftype() == 'CIRCLE':
#                 metadata.write(f"   Center: ({entity.dxf.center.x:.2f}, {entity.dxf.center.y:.2f})\n")
#                 metadata.write(f"   Radius: {entity.dxf.radius:.2f}\n")
#             elif entity.dxftype() == 'ARC':
#                 metadata.write(f"   Center: ({entity.dxf.center.x:.2f}, {entity.dxf.center.y:.2f})\n")
#                 metadata.write(f"   Radius: {entity.dxf.radius:.2f}\n")
#             elif entity.dxftype() == 'TEXT':
#                 metadata.write(f"   Text: {entity.dxf.text}\n")
#                 metadata.write(f"   Position: ({entity.dxf.insert.x:.2f}, {entity.dxf.insert.y:.2f})\n")
#             elif entity.dxftype() == 'MTEXT':
#                 metadata.write(f"   Text: {entity.text}\n")
#                 metadata.write(f"   Position: ({entity.dxf.insert.x:.2f}, {entity.dxf.insert.y:.2f})\n")
#             elif entity.dxftype() == 'POLYLINE':
#                 try:
#                     vertex_count = len(list(entity.virtual_entities()))
#                     metadata.write(f"   Vertices: {vertex_count}\n")
#                 except:
#                     metadata.write(f"   Polyline entity\n")
#         except Exception as e:
#             metadata.write(f"   [Could not extract detailed info: {str(e)}]\n")
        
#         metadata.write("\n")
    
#     metadata.write("="*60 + "\n")
#     metadata.write("END OF METADATA REPORT\n")
#     metadata.write("="*60 + "\n")
    
#     return metadata.getvalue()

# if uploaded_file is not None:
#     try:
#         # Create a temporary file to save the uploaded content
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             tmp_file_path = tmp_file.name
        
#         # Read the DXF file
#         with st.spinner('Processing AutoCAD file...'):
#             doc = ezdxf.readfile(tmp_file_path)
#             metadata_text = extract_metadata(doc)
        
#         # Clean up temporary file
#         os.unlink(tmp_file_path)
        
#         st.success("✅ Metadata extracted successfully!")
        
#         # Display metadata in text area
#         st.text_area("Extracted Metadata", metadata_text, height=400)
        
#         # Download button
#         st.download_button(
#             label="📥 Download Metadata as TXT",
#             data=metadata_text,
#             file_name=f"{uploaded_file.name.replace('.dxf', '')}_metadata.txt",
#             mime="text/plain"
#         )
        
#     except Exception as e:
#         st.error(f"❌ Error processing file: {str(e)}")
#         st.info("Make sure you're uploading a valid DXF file.")

# else:
#     st.info("👆 Please upload a DXF file to begin extraction.")
    
#     # Instructions
#     with st.expander("ℹ️ How to use"):
#         st.markdown("""
#         1. **Upload** your AutoCAD DXF file using the file uploader above
#         2. Wait for the processing to complete
#         3. **Review** the extracted metadata in the text area
#         4. **Download** the metadata as a TXT file using the download button
        
#         ### What metadata is extracted?
#         - Drawing information (version, units, dates)
#         - Layer details (names, colors, properties)
#         - Entity statistics (counts of lines, circles, text, etc.)
#         - Text content from the drawing
#         - Block definitions
#         - Detailed entity information with coordinates
        
#         ### Supported file format:
#         - DXF (Drawing Exchange Format) files
        
#         **Note:** For DWG files, please convert them to DXF format first using AutoCAD or a converter.
#         """)

# requirements.txt
# streamlit==1.28.0
# ezdxf==1.1.0
# PyPDF2==3.0.1

import streamlit as st
import ezdxf
from io import StringIO
import tempfile
import os
from datetime import datetime
import PyPDF2

st.set_page_config(page_title="CAD & PDF Metadata Extractor", page_icon="📐", layout="wide")

st.title("📐 CAD & PDF Metadata Extractor")
st.markdown("Upload your AutoCAD DWG/DXF or PDF file to extract metadata and information.")

# File uploader - now accepts DWG, DXF and PDF
uploaded_file = st.file_uploader("Choose a DWG, DXF or PDF file", type=['dwg', 'dxf', 'pdf'])

def extract_dxf_metadata(doc):
    """Extract comprehensive metadata from DXF document"""
    metadata = StringIO()
    
    # Header Information
    metadata.write("="*60 + "\n")
    metadata.write("AUTOCAD FILE METADATA (DXF)\n")
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
    
    for i, text in enumerate(text_entities, 1):
        if text.dxftype() == 'TEXT':
            metadata.write(f"{i}. {text.dxf.text} (Layer: {text.dxf.layer})\n")
        elif text.dxftype() == 'MTEXT':
            content = text.text
            metadata.write(f"{i}. {content} (Layer: {text.dxf.layer})\n")
        elif text.dxftype() == 'ATTRIB':
            metadata.write(f"{i}. {text.dxf.text} (Layer: {text.dxf.layer})\n")
    
    metadata.write("\n" + "-"*60 + "\n\n")
    
    # Blocks Information
    metadata.write("--- BLOCKS ---\n")
    blocks = [b for b in doc.blocks if not b.name.startswith('*')]
    metadata.write(f"Total Block Definitions: {len(blocks)}\n\n")
    
    for block in blocks:
        metadata.write(f"  • Block: {block.name}\n")
        block_entities = list(block)
        metadata.write(f"    Entities in block: {len(block_entities)}\n\n")
    
    metadata.write("\n" + "-"*60 + "\n\n")
    
    # Detailed Entity Information
    metadata.write("--- DETAILED ENTITY INFORMATION (ALL ENTITIES) ---\n")
    metadata.write(f"Total Entities to Detail: {len(entities)}\n\n")
    
    for i, entity in enumerate(entities, 1):
        metadata.write(f"{i}. Type: {entity.dxftype()}\n")
        metadata.write(f"   Layer: {entity.dxf.layer}\n")
        metadata.write(f"   Color: {entity.dxf.color}\n")
        
        try:
            if entity.dxftype() == 'LINE':
                metadata.write(f"   Start: ({entity.dxf.start.x:.2f}, {entity.dxf.start.y:.2f})\n")
                metadata.write(f"   End: ({entity.dxf.end.x:.2f}, {entity.dxf.end.y:.2f})\n")
            elif entity.dxftype() == 'CIRCLE':
                metadata.write(f"   Center: ({entity.dxf.center.x:.2f}, {entity.dxf.center.y:.2f})\n")
                metadata.write(f"   Radius: {entity.dxf.radius:.2f}\n")
            elif entity.dxftype() == 'ARC':
                metadata.write(f"   Center: ({entity.dxf.center.x:.2f}, {entity.dxf.center.y:.2f})\n")
                metadata.write(f"   Radius: {entity.dxf.radius:.2f}\n")
            elif entity.dxftype() == 'TEXT':
                metadata.write(f"   Text: {entity.dxf.text}\n")
                metadata.write(f"   Position: ({entity.dxf.insert.x:.2f}, {entity.dxf.insert.y:.2f})\n")
            elif entity.dxftype() == 'MTEXT':
                metadata.write(f"   Text: {entity.text}\n")
                metadata.write(f"   Position: ({entity.dxf.insert.x:.2f}, {entity.dxf.insert.y:.2f})\n")
            elif entity.dxftype() == 'POLYLINE':
                try:
                    vertex_count = len(list(entity.virtual_entities()))
                    metadata.write(f"   Vertices: {vertex_count}\n")
                except:
                    metadata.write(f"   Polyline entity\n")
        except Exception as e:
            metadata.write(f"   [Could not extract detailed info: {str(e)}]\n")
        
        metadata.write("\n")
    
    metadata.write("="*60 + "\n")
    metadata.write("END OF METADATA REPORT\n")
    metadata.write("="*60 + "\n")
    
    return metadata.getvalue()


def extract_pdf_metadata(pdf_file):
    """Extract text and metadata from PDF document"""
    metadata = StringIO()
    
    # Header Information
    metadata.write("="*60 + "\n")
    metadata.write("PDF FILE METADATA & TEXT EXTRACTION\n")
    metadata.write("="*60 + "\n\n")
    
    metadata.write("⚠️ NOTE: PDF extraction provides text content only.\n")
    metadata.write("For complete CAD metadata (layers, entities, coordinates),\n")
    metadata.write("please convert your PDF to DXF format first.\n")
    metadata.write("\n" + "-"*60 + "\n\n")
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Basic PDF Information
        metadata.write("--- PDF DOCUMENT INFORMATION ---\n")
        metadata.write(f"Extraction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        metadata.write(f"Total Pages: {len(pdf_reader.pages)}\n")
        
        # PDF Metadata
        if pdf_reader.metadata:
            pdf_meta = pdf_reader.metadata
            metadata.write(f"\nTitle: {pdf_meta.get('/Title', 'Not specified')}\n")
            metadata.write(f"Author: {pdf_meta.get('/Author', 'Not specified')}\n")
            metadata.write(f"Subject: {pdf_meta.get('/Subject', 'Not specified')}\n")
            metadata.write(f"Creator: {pdf_meta.get('/Creator', 'Not specified')}\n")
            metadata.write(f"Producer: {pdf_meta.get('/Producer', 'Not specified')}\n")
            metadata.write(f"Creation Date: {pdf_meta.get('/CreationDate', 'Not specified')}\n")
            metadata.write(f"Modification Date: {pdf_meta.get('/ModDate', 'Not specified')}\n")
        
        metadata.write("\n" + "-"*60 + "\n\n")
        
        # Extract text from each page
        metadata.write("--- EXTRACTED TEXT CONTENT ---\n\n")
        
        total_text = ""
        for page_num, page in enumerate(pdf_reader.pages, 1):
            metadata.write(f"--- PAGE {page_num} ---\n")
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    metadata.write(page_text)
                    total_text += page_text + "\n"
                else:
                    metadata.write("[No extractable text on this page]\n")
            except Exception as e:
                metadata.write(f"[Error extracting text: {str(e)}]\n")
            metadata.write("\n" + "-"*60 + "\n\n")
        
        # Summary
        metadata.write("--- EXTRACTION SUMMARY ---\n")
        metadata.write(f"Total characters extracted: {len(total_text)}\n")
        metadata.write(f"Total words (approx): {len(total_text.split())}\n")
        metadata.write(f"Total lines (approx): {len(total_text.splitlines())}\n")
        
    except Exception as e:
        metadata.write(f"\n❌ Error reading PDF: {str(e)}\n")
    
    metadata.write("\n" + "="*60 + "\n")
    metadata.write("END OF PDF EXTRACTION REPORT\n")
    metadata.write("="*60 + "\n")
    
    return metadata.getvalue()


if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension in ['dxf', 'dwg']:
            # Process DXF or DWG file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            with st.spinner(f'Processing AutoCAD {file_extension.upper()} file...'):
                # ezdxf can read both DXF and DWG files (DWG requires additional setup)
                try:
                    doc = ezdxf.readfile(tmp_file_path)
                    metadata_text = extract_dxf_metadata(doc)
                    success_message = f"✅ {file_extension.upper()} metadata extracted successfully!"
                except ezdxf.DXFError as e:
                    if file_extension == 'dwg':
                        # DWG files need special handling
                        st.error("❌ DWG file processing error.")
                        st.warning("""
                        **DWG File Limitations:**
                        
                        The `ezdxf` library has limited DWG support. To process DWG files, you have two options:
                        
                        1. **Convert DWG to DXF first** (Recommended):
                           - Use AutoCAD: File → Save As → DXF
                           - Use free tools: LibreCAD, DraftSight, or online converters
                           - Use ODA File Converter (free from Open Design Alliance)
                        
                        2. **Install ODA File Converter** (Advanced):
                           - ezdxf requires ODA File Converter to be installed on the server
                           - This is typically only feasible for local deployments
                        
                        For now, please convert your DWG file to DXF format and upload again.
                        """)
                        os.unlink(tmp_file_path)
                        st.stop()
                    else:
                        raise e
            
            os.unlink(tmp_file_path)
            st.success(success_message)
            
        elif file_extension == 'pdf':
            # Process PDF file
            with st.spinner('Extracting text from PDF...'):
                uploaded_file.seek(0)  # Reset file pointer
                metadata_text = extract_pdf_metadata(uploaded_file)
            
            st.warning("⚠️ PDF processed - Text extraction only. For complete CAD data, convert to DXF format.")
        
        # Display metadata in text area
        st.text_area("Extracted Metadata", metadata_text, height=400)
        
        # Download button
        file_suffix = 'metadata' if file_extension in ['dxf', 'dwg'] else 'text_extraction'
        st.download_button(
            label=f"📥 Download {file_extension.upper()} Extraction as TXT",
            data=metadata_text,
            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_{file_suffix}.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info(f"Make sure you're uploading a valid {file_extension.upper()} file.")

else:
    st.info("👆 Please upload a DWG, DXF or PDF file to begin extraction.")
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload** your AutoCAD DWG/DXF or PDF file using the file uploader above
        2. Wait for the processing to complete
        3. **Review** the extracted metadata/text in the text area
        4. **Download** the extraction as a TXT file using the download button
        
        ### What's extracted from each format?
        
        #### DXF Files (Full CAD Metadata) ✅:
        - Drawing information (version, units, dates)
        - Layer details (names, colors, properties)
        - Entity statistics (counts of lines, circles, text, etc.)
        - Text content from the drawing
        - Block definitions
        - Detailed entity information with coordinates
        
        #### DWG Files (Native AutoCAD Format) ⚠️:
        - **Limited support** - DWG processing requires additional setup
        - **Recommended**: Convert DWG to DXF format first for best results
        - If DWG fails, the app will provide conversion instructions
        
        #### PDF Files (Text Extraction Only):
        - PDF document metadata (title, author, dates)
        - Text content from all pages
        - Page count and structure
        - ⚠️ **Note:** PDFs do NOT contain CAD layer data, entity coordinates, or drawing structure
        
        ### Supported file formats:
        - **DXF** (Drawing Exchange Format) - Full metadata extraction ✅
        - **DWG** (AutoCAD Native Format) - Limited support, convert to DXF recommended ⚠️
        - **PDF** (Portable Document Format) - Text extraction only
        
        ### Converting files:
        
        **DWG to DXF:**
        - Use AutoCAD: File → Save As → DXF
        - Use free tools: LibreCAD, DraftSight
        - Use ODA File Converter (free from Open Design Alliance)
        - Use online converters (e.g., Zamzar, CloudConvert)
        
        **PDF to DXF:**
        - Use AutoCAD's "PDF Import" feature
        - Use online converters (quality varies)
        - Use specialized software like Adobe Illustrator or Inkscape
        
        **Important Notes:**
        - DXF is the recommended format for complete metadata extraction
        - DWG files may require conversion to DXF for reliable processing
        - PDF-to-DXF conversion quality depends on how the PDF was created
        - PDFs from raster images will not convert well to vector DXF format
        """)