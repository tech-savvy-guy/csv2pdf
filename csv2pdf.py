import csv
from fpdf import FPDF

def convert(source:str, destination:str, orientation="P", delimiter=",",
            font=None, headerfont=None, align="C", size=8, headersize=10) -> None:

    """
    # CONVERTS A CSV FILE TO PDF FILE ( .csv ➜ .pdf )
        
    :param `source`: `***str*** : ***Required*** : The file path of the CSV FILE to be converted.

    :param `destination`: ***str*** : ***Required*** :The file path of the PDF FILE to be generated.

    :param `orientation`: ***str*** : *Optional* : The orientation in which the PDF will be created. ***Default ➜ "P"***
    
    ***Possible Values** ➜ **'P' ➣ Potrait** --- **'L' ➣ Landscape***

    :param `delimiter`: ***str*** : *Optional* : The delimiter to be used for reading the CSV FILE. ***Default ➜ ","***

    :param `font`: ***str*** : *Optional* : Path of the font to be used for the CSV data. ***Default ➜ None***

    :param `headerfont`: ***str*** : *Optional* : Path of the font to be used for the CSV headers. ***Default ➜ None***

    :param `align`: ***str*** : *Optional* : Alignment for the cells in PDF. ***Default ➜ "C"***

    ***Possible Values** ➜ **'J' ➣ Justify** --- **'C' ➣ Center** --- **'L ➣ Left** --- **'R' ➣ Right***

    :param `size`: ***int*** : *Optional* : Specify the font size for the CSV data. ***Default size ➜ 8***
    
    :param `headersize`: ***int*** : *Optional* : Specify the font size for the CSV header. ***Default size ➜ 10*** 
    """
    
    if orientation not in ["P", "L"]:
        raise Exception("Orientation Error: Invalid orientation parameter!\
            \nExpected values: 'P' ➣ Potrait | 'L ➣ Landscape")

    if align not in ["J", "C", "L", "R"]:
        raise Exception("Alignment Error: Invalid alignment parameter!\
            \nExpected values: 'J' ➣  Justify | 'C' ➣ Center | 'L ➣ Left | 'R' ➣ Right")

    if not (isinstance(size, int) and isinstance(headersize, int)):
        raise Exception("Type Error: Font Size should be of int data type")

    PDF = FPDF(orientation)
    PDF.add_page()

    if font == None:
        PDF.add_font("normal-font", "", r"Fonts\rs_normal.ttf", uni=True)
    else:
        PDF.add_font("normal-font", "", font, uni=True)        

    if headerfont == None:
        PDF.add_font("header-font", "", r"Fonts\rs_bold.ttf", uni=True)
    else:
        PDF.add_font("header-font", "", headerfont, uni=True)

    with open(source) as CSV:
        data = [row for row in csv.reader(CSV, delimiter =delimiter )]
        header = data[0]
        rows = data[1:]

    max = len(header)
    for row in rows:
        if len(row) > max:
            max = len(row)

    header.extend(list(" "*(max - len(header))))
    for row in rows:
        row.extend(list(" "*(max - len(row))))

    PDF.set_font("header-font", size=headersize)
    line_height = PDF.font_size * 2.5
    col_width = PDF.epw / max
    
    for cell in header:
        PDF.multi_cell(col_width, line_height, cell, align=align, border=1,
        ln=3, max_line_height=PDF.font_size)
    PDF.ln(line_height)

    PDF.set_font("normal-font", size=size)
    line_height = PDF.font_size * 2.5

    for cells in rows:
        for cell_value in cells:
            PDF.multi_cell(col_width, line_height, cell_value, align=align, border=1,
            ln=3, max_line_height=PDF.font_size)
        PDF.ln(line_height)
    
    PDF.output(destination)
    