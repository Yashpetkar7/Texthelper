from datetime import datetime
import io, csv
from pathlib import Path

def to_upper(text): return text.upper()
def to_lower(text): return text.lower()
def strip_text(text): return "\n".join(line.strip() for line in text.splitlines()).strip()
def replace_text(text, old, new): return text.replace(old, new)
def count_substring(text, sub): return text.count(sub)
def get_preview_lines(text, n=20): return text.splitlines()[:n]
def get_stats(text): 
    lines = text.splitlines()
    return len(lines), sum(len(l.split()) for l in lines), len(text)
def validate_extension(ext): return ext.lower() == ".txt"
def make_timestamp(fmt="%Y-%m-%d %H:%M:%S"): return datetime.now().strftime(fmt)
def convert_text_for_format(text, base, fmt):
    fmt = fmt.lower()
    if fmt in [".txt", ".md"]: 
        return text.encode("utf-8"), f"{base}_edited{fmt}"
    if fmt == ".html":
        html = f"<html><body><pre>{text}</pre></body></html>"
        return html.encode("utf-8"), f"{base}_edited.html"
    if fmt == ".csv":
        buf = io.StringIO(); w = csv.writer(buf)
        for line in text.splitlines(): w.writerow([line])
        return buf.getvalue().encode("utf-8"), f"{base}_edited.csv"
    return text.encode("utf-8"), f"{base}_edited.txt"
