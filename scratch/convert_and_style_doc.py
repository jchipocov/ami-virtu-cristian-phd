import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"c:\Users\jchip\Downloads\learning_analytics_ami-20260917T111531Z-1-001\learning_analytics_ami"
PANDOC_EXE = r"C:\Users\jchip\AppData\Local\Pandoc\pandoc.exe"
INPUT_MD = os.path.join(BASE_DIR, r"data\outputs\oe1_caracterizacion_20260802\Capitulo_4_Secciones_Depuracion_y_OE1.md")
OUTPUT_DOCX = os.path.join(BASE_DIR, r"data\outputs\oe1_caracterizacion_20260802\Capitulo_4_Secciones_Depuracion_y_OE1_APA.docx")
MAIN_DOCX = os.path.join(BASE_DIR, r"data\outputs\oe1_caracterizacion_20260802\Capitulo_4_Secciones_Depuracion_y_OE1.docx")

def run_pandoc():
    print(f"Executing Pandoc on {INPUT_MD}...")
    cmd = [
        PANDOC_EXE,
        INPUT_MD,
        "-o", OUTPUT_DOCX,
        "--from=markdown+pipe_tables+grid_tables+table_captions+tex_math_dollars",
        "--to=docx"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Pandoc stderr:", res.stderr)
        raise RuntimeError(f"Pandoc failed with code {res.returncode}")
    print("Pandoc completed successfully.")

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table):
    """Apply APA 7th style table borders: top line, header bottom line, table bottom line, no verticals."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="333333"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="333333"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_cell_shading(cell, color_hex="F2F4F7"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def polish_docx():
    print(f"Polishing Word document {OUTPUT_DOCX}...")
    doc = docx.Document(OUTPUT_DOCX)
    
    # 1. Page Margins (1 inch / 2.54 cm all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # 2. Typography & Styles
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(11.5)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # Process paragraphs
    for p in doc.paragraphs:
        # Check heading styles
        if p.style.name.startswith('Heading 1'):
            p.style.font.name = 'Times New Roman'
            p.style.font.size = Pt(15)
            p.style.font.bold = True
            p.style.font.color.rgb = RGBColor(0x11, 0x22, 0x44)
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
        elif p.style.name.startswith('Heading 2'):
            p.style.font.name = 'Times New Roman'
            p.style.font.size = Pt(13)
            p.style.font.bold = True
            p.style.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
        elif p.style.name.startswith('Heading 3'):
            p.style.font.name = 'Times New Roman'
            p.style.font.size = Pt(12)
            p.style.font.bold = True
            p.style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
        elif p.style.name == 'Blockquote':
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.right_indent = Inches(0.2)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10.5)
        else:
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            for run in p.runs:
                if not run.font.name:
                    run.font.name = 'Times New Roman'

    # 3. Tables Polish
    # Table column proportions (total width ~ 6.5 inches = 468 pt)
    table_col_widths = {
        0: [Inches(1.10), Inches(1.20), Inches(0.48), Inches(0.52), Inches(0.60), Inches(0.60), Inches(0.50), Inches(1.50)], # Table 4.1 (sum = 6.5 in)
        1: [Inches(1.55), Inches(2.20), Inches(0.65), Inches(0.65), Inches(1.45)], # Table 4.2 (sum = 6.5 in)
        2: [Inches(1.30)] + [Inches(0.40)] * 13, # Table 4.3 (sum = 1.30 + 5.20 = 6.5 in)
        3: [Inches(1.30), Inches(0.60), Inches(0.60), Inches(1.00), Inches(1.00), Inches(1.00), Inches(0.50), Inches(0.50)], # Table 4.4 (sum = 6.5 in)
        4: [Inches(1.25), Inches(0.70), Inches(0.70), Inches(0.75), Inches(0.70), Inches(0.90), Inches(1.50)] # Table 4.5 (sum = 6.5 in)
    }

    for idx, table in enumerate(doc.tables):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)
        
        # Set repeating header and prevent row split across pages
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            if r_idx == 0:
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
                # Style header cells
                for cell in row.cells:
                    set_cell_shading(cell, "F0F4F8")
                    set_cell_margins(cell, top=120, bottom=120, left=80, right=80)
                    for p in cell.paragraphs:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.line_spacing = 1.0
                        for r in p.runs:
                            r.font.name = 'Times New Roman'
                            r.font.bold = True
                            if idx == 2: # Table 4.3 (14 cols)
                                r.font.size = Pt(8.0)
                            else:
                                r.font.size = Pt(9.5)
            else:
                # Alternate row shading or clean white
                bg_color = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
                for c_idx, cell in enumerate(row.cells):
                    if r_idx % 2 == 1:
                        set_cell_shading(cell, bg_color)
                    set_cell_margins(cell, top=80, bottom=80, left=70, right=70)
                    for p in cell.paragraphs:
                        p.paragraph_format.space_after = Pt(1)
                        p.paragraph_format.space_before = Pt(1)
                        p.paragraph_format.line_spacing = 1.0
                        for r in p.runs:
                            r.font.name = 'Times New Roman'
                            if idx == 2: # Table 4.3
                                r.font.size = Pt(8.5)
                            else:
                                r.font.size = Pt(9.5)

        # Apply specific column widths if defined
        if idx in table_col_widths:
            widths = table_col_widths[idx]
            for row in table.rows:
                for c_idx, w in enumerate(widths):
                    if c_idx < len(row.cells):
                        row.cells[c_idx].width = w

    doc.save(OUTPUT_DOCX)
    print(f"Polished document successfully saved to: {OUTPUT_DOCX}")

if __name__ == '__main__':
    run_pandoc()
    polish_docx()
