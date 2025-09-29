from collections import defaultdict
from bidi.algorithm import get_display
import pdfplumber
import fitz
import re
import arabic_reshaper

def reshape_farsi(text):
    if text:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return ""

def map_pdf_data_to_form_fields(pdf_data):
    gender_map = {
        "ﻣﺮﺩ": "1",
        "ﺯﻥ": "2"
    }

    blood_map = {
        "A+": "A",
        "A-": "A",
        "B+": "B",
        "B-": "B",
        "AB+": "AB",
        "AB-": "AB",
        "O+": "O",
        "O-": "O",
        "ﻧﺎﻣﺸﺨﺺ": ""
    }

    return {
        "full_name": pdf_data.get("نام و نام خانوادگی", ""),
        "national_code": pdf_data.get("ﮐﺪ ﻣﻠﯽ", ""),
        "gender": gender_map.get(pdf_data.get("ﺟﻨﺲ", "").strip(), ""),
        "age": int(pdf_data.get("ﺳﻦ", "0")),
        "blood_group": blood_map.get(pdf_data.get("ﮔﺮﻭﻩ ﺧﻮﻧﯽ", "").replace(" ", ""), "")
    }

def extract_by_line_rules(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result = {}

    if len(lines) >= 2:
        parts = lines[1].split()
        result["ﮐﺪ ﻣﻠﯽ"] = parts[0] if len(parts) > 0 else ""
        result["نام و نام خانوادگی"] = " ".join(parts[1:]) if len(parts) > 1 else ""

    if len(lines) >= 5:
        parts = lines[4].split()
        blood_values = {"O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "ﻧﺎﻣﺸﺨﺺ"}
        if len(parts) >= 3 and parts[2] in blood_values:
            result["ﮔﺮﻭﻩ ﺧﻮﻧﯽ"] = parts[2]
            result["ﺳﻦ"] = parts[0]
            result["ﺟﻨﺲ"] = parts[1]
        else:
            result["ﮔﺮﻭﻩ ﺧﻮﻧﯽ"] = parts[0] if len(parts) > 0 else ""
            result["ﺳﻦ"] = parts[1] if len(parts) > 1 else ""
            result["ﺟﻨﺲ"] = parts[2] if len(parts) > 2 else ""

    return map_pdf_data_to_form_fields(result)

def extract_patient_info_from_pdf(pdf_path):
    output_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        raw_text = first_page.extract_text()

        if raw_text:
            start_marker = "PCR Based HLA Typing Test"
            end_marker = "Results"

            if start_marker in raw_text and end_marker in raw_text:
                start_index = raw_text.find(start_marker) + len(start_marker)
                end_index = raw_text.find(end_marker)
                header_text = raw_text[start_index:end_index].strip()

                lines = header_text.split("\n")
                for line in lines:
                    output_text += reshape_farsi(line) + "\n"
            else:
                return {"خطا": "❌ عبارت‌های مورد نظر پیدا نشدند"}

    return extract_by_line_rules(output_text)

def extract_alleles_from_pdf(file_obj):
    allele_prefixes = ("A", "B", "DQB1", "DRB1", "DRB3", "DRB4", "DRB5")
    prefix_pattern = "|".join(allele_prefixes)
    allele_pattern = rf"\b(({prefix_pattern})\*\d{{2}})\b"

    def extract_spans(page):
        blocks = page.get_text("dict")["blocks"]
        spans_data = []
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text:
                        spans_data.append({
                            "text": text,
                            "x0": span["bbox"][0],
                            "y0": span["bbox"][1]
                        })
        return spans_data

    doc = fitz.open(stream=file_obj.read(), filetype='pdf')
    page = doc[0]
    spans = extract_spans(page)
    spans.sort(key=lambda x: (round(x["y0"], 1), x["x0"]))

    allele_dict = defaultdict(list)

    for span in spans:
        text = span["text"]
        match = re.match(allele_pattern, text)
        if match:
            full_allele = match.group(1)
            prefix = full_allele.split("*")[0]
            allele_dict[prefix].append(full_allele)

        if text in ["DRB3", "DRB4", "DRB5"]:
            allele_dict["DRB"].append(text)

    drb_values = allele_dict.get("DRB", [])
    if len(drb_values) == 0:
        allele_dict["DRB"] = ["---", "---"]
    elif len(drb_values) == 1:
        allele_dict["DRB"] = [drb_values[0], "---"]

    return dict(allele_dict)
