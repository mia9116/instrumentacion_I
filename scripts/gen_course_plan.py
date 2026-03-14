import pandas as pd
import subprocess
from pathlib import Path
import os
import re
from pylatex import Document, Package, Chapter, Section, Subsection, Subsubsection, Command,\
    Tabularx, LongTabularx, PageStyle, Head, Foot, NewPage,\
    VerticalSpace, HorizontalSpace, NewLine, Itemize, MiniPage, StandAloneGraphic,TextColor,\
    LongTable,MultiColumn,\
    TikZ, TikZNode, TikZOptions, TikZCoordinate
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic, escape_latex
from datetime import date, timedelta

root = Path(__file__).resolve().parent.parent

plan_dir = root / "plan"
images_dir = root / "figures" / "comunes"

course = "Instrumentación II"
id = "IF3503"


content = pd.read_csv(plan_dir / f"plan.csv").fillna("")

print(content.head())

def bulleted_lines_after_period(value):
    text = str(value).strip()
    if not text:
        return ""

    parts = [part.strip() for part in re.split(r"\.\s+", text) if part.strip()]
    lines = []
    for part in parts:
        clean_part = part if part.endswith("}") else f"{part}."
        rendered_part = clean_part if r"\href{" in clean_part else escape_latex(clean_part)
        lines.append(rf"\textbullet\ {rendered_part}")

    return NoEscape(r"\newline ".join(lines))


def make_plan_pdf(id,course,images_dir):
    logo_path = (images_dir / "logo.png").as_posix()
    # Opciones de geometría
    geometry_options = { 
        "left":         "10mm",
        "right":        "5mm",
        "top":          "21mm",
        "bottom":       "21mm",
        "headheight":   "15mm",
        "footskip":     "10mm"
    }
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["10pt","letterpaper","landscape"],
                   geometry_options=geometry_options)

    # Font
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish','activeacute']))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="fancyhdr"))
    doc.packages.append(Package(name="csquotes"))
    doc.packages.append(Package(name="easylist", options=['ampersand']))
    doc.packages.append(Package(name="biblatex", options=['style=ieee','backend=biber']))
    doc.packages.append(Package(name="tcolorbox",options=['skins','breakable']))
    doc.packages.append(Package(name="booktabs"))
    doc.packages.append(Package(name="textcomp"))
    doc.packages.append(Package("hyperref", options=[
        "pdfencoding=auto",
        "unicode",
        "bookmarks=false",
        "colorlinks=false",
        "pdfborder={0 0 0}",
        f"pdftitle={course}",
        "pdfauthor={Juan J. Rojas}",
        "pdfsubject={Course Plan}",
    ]))

    doc.add_color('gris','rgb','0.27,0.27,0.27') #70,70,70
    doc.add_color("verde", "rgb", "0.051,0.733,0.447")
    doc.add_color('azul','rgb','0.02,0.455,0.773') #5,116,197

    doc.preamble.append(Command('setmainfont','Arial'))

    # Set LongTabularx to have no space between tables and to be left aligned
    doc.preamble.append(NoEscape(r'\setlength{\LTpre}{0pt}'))
    doc.preamble.append(NoEscape(r'\setlength{\LTpost}{0pt}'))
    doc.preamble.append(NoEscape(r'\setlength\LTleft{0pt}'))
    doc.preamble.append(NoEscape(r'\setlength\LTright{0pt}'))

    doc.preamble.append(NoEscape(r"\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}"))
    doc.preamble.append(NoEscape(r"\newcolumntype{P}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}\vspace{2pt}}m{#1}}"))
    doc.preamble.append(NoEscape(r"\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}"))
    doc.preamble.append(NoEscape(r"\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}"))
    doc.preamble.append(NoEscape(r"\newcolumntype{T}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}\vspace{2pt}}m{#1}}"))
    doc.preamble.append(NoEscape(r"\newcolumntype{N}{@{}m{0pt}@{}}"))

    with doc.create(TikZ(
        options=TikZOptions
                (    
                "overlay",
                "remember picture"
                )
        )) as logo:
        logo.append(TikZNode(\
            options=TikZOptions
                (
                "inner sep = 0mm",
                "outer sep = 0mm",
                "anchor = north west",
                "xshift = 210mm",
                "yshift = 20mm"
                ),
            text=StandAloneGraphic(image_options="width=5cm", filename=logo_path).dumps(),\
            at=TikZCoordinate(0,0)
        ))
    doc.append(VerticalSpace("2mm", star=True))
    doc.append(NewLine())
    with doc.create(
        LongTabularx(
            table_spec=r"| C{0.04\linewidth} | L{0.24\linewidth} | L{0.24\linewidth} | L{0.18\linewidth} | L{0.18\linewidth} |",
            row_height=1.5,
            width=5
            )) as table:
        table.add_hline()
        table.add_row([
            MultiColumn(5,align="c",data=bold(f"Plan del curso {course}"))
        ])
        table.add_hline()
        table.add_row(["Sem.","Tema","Objetivo","Metodología","Evaluaciones"])
        table.add_hline()
        table.end_table_header()
        for _,row in content.iterrows():
            table.add_row([
                row.semana,
                bulleted_lines_after_period(row.tema),
                bulleted_lines_after_period(row.objetivo),
                bulleted_lines_after_period(row.metodo),
                bulleted_lines_after_period(row.evaluaciones),
            ])
            table.add_hline()
        



    doc.generate_pdf(plan_dir / course, clean=True, clean_tex=True, compiler='lualatex',silent=True)

make_plan_pdf(id,course,images_dir)

subprocess.run(["del", plan_dir / "*.aux"], shell=True, check=True)
subprocess.run(["del", plan_dir / "*.bcf"], shell=True, check=True)
subprocess.run(["del", plan_dir / "*.bbl"], shell=True, check=True)
subprocess.run(["del", plan_dir / "*.blg"], shell=True, check=True)
subprocess.run(["del", plan_dir / "*.log"], shell=True, check=True)
subprocess.run(["del", plan_dir / "*.run.xml"], shell=True, check=True)
