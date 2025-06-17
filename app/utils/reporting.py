from typing import List, Dict
from io import BytesIO
from weasyprint import HTML
from openpyxl import Workbook


def generate_pdf(data: List[Dict], title: str) -> bytes:
    """Generate simple PDF report from list of dicts."""
    headers = list(data[0].keys()) if data else []
    rows = "".join(
        "<tr>" + "".join(f"<td>{item[h]}</td>" for h in headers) + "</tr>"
        for item in data
    )
    header_row = "".join(f"<th>{h}</th>" for h in headers)
    html = f"""
    <h1>{title}</h1>
    <table border='1' cellspacing='0' cellpadding='4'>
        <thead><tr>{header_row}</tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """
    return HTML(string=html).write_pdf()


def generate_excel(data: List[Dict], sheet_name: str = "Sheet1") -> bytes:
    """Generate Excel report from list of dicts."""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    if data:
        ws.append(list(data[0].keys()))
    for item in data:
        ws.append(list(item.values()))
    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()
