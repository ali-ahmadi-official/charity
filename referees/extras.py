from collections import defaultdict
from bidi.algorithm import get_display
import pdfplumber
import fitz
import re
import arabic_reshaper

def extract_combined_allele_risk(class1_pdf_path, class2_pdf_path):
    allele_prefixes = ("A", "B", "DQB1", "DRB1", "DRB3", "DRB4", "DRB5")
    risk_keywords = ["High Risk", "Moderate Risk", "Low Risk"]
    prefix_pattern = "|".join(allele_prefixes)
    allele_pattern = rf"\b(({prefix_pattern})\*\d{{2}}:\d{{2}})\b"

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

    def process_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        allele_risk_list = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")

            if "Allele" in text and "Risk Level" in text:
                spans = extract_spans(page)
                spans.sort(key=lambda x: (round(x["y0"], 1), x["x0"]))

                current_row = {}
                last_y = None
                for span in spans:
                    y = round(span["y0"], 1)
                    text = span["text"]

                    if last_y is None or abs(y - last_y) > 3:
                        if "allele" in current_row and "risk" in current_row:
                            allele_risk_list.append(current_row)
                        current_row = {}
                        last_y = y

                    if re.match(allele_pattern, text):
                        current_row["allele"] = text

                    for risk in risk_keywords:
                        if risk in text:
                            current_row["risk"] = risk

                if "allele" in current_row and "risk" in current_row:
                    allele_risk_list.append(current_row)

        return allele_risk_list

    combined_list = process_pdf(class1_pdf_path) + process_pdf(class2_pdf_path)

    unique_list = [dict(t) for t in {tuple(d.items()) for d in combined_list}]
    return unique_list

def analyze_uam_status(unique_list):
    grouped = defaultdict(list)

    for item in unique_list:
        allele = item['allele']
        risk = item['risk']

        if allele.startswith(('DRB3*', 'DRB4*', 'DRB5*')):
            base = allele.split('*')[0]
        else:
            base = allele.split(':')[0]

        grouped[base].append((allele, risk))

    uam_list = []
    warning_list = []

    for base, allele_risks in grouped.items():
        risks = [r for _, r in allele_risks]

        if all(r in ['High Risk', 'Moderate Risk'] for r in risks):
            uam_list.append(base)
        elif any(r in ['High Risk', 'Moderate Risk'] for r in risks):
            high_risk_alleles = [a for a, r in allele_risks if r == 'High Risk' or r == 'Moderate Risk']
            message = f"Due to the high risk of HLA antibody titer " + \
                        ", ".join(high_risk_alleles) + \
                        f", it is recommended that the patient be guided to undergo High Resolution testing."
            warning_list.append({
                'HLA': base,
                'message': message
            })

    return sorted(uam_list), warning_list

def reshape_farsi(text):
    if text:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return ""

def extract_by_line_rules(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result = {}

    if len(lines) >= 1:
        parts = lines[0].split()
        result["ﮐﺪ ﻣﻠﯽ"] = parts[0] if len(parts) > 0 else ""
        result["ﻧﺎﻡ"] = parts[1] if len(parts) > 1 else ""
        result["ﻧﺎﻡ ﺧﺎﻧﻮﺍﺩﮔﯽ"] = " ".join(parts[2:]) if len(parts) > 2 else ""

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

    if len(lines) >= 8:
        parts = lines[7].split()
        result["ﺗﻌﺪﺍﺩ ﺑﺎﺭﺩﺍﺭﯼ"] = parts[0] if len(parts) > 0 else ""
        result["ﺗﻌﺪﺍﺩ ﺳﻘﻂ"] = parts[1] if len(parts) > 1 else ""
        result["ﺳﺎﺑﻘﻪ ﺗﺰﺭﯾﻖ ﺧﻮﻥ"] = parts[2] if len(parts) > 2 else ""

    return result

def extract_patient_info_from_pdf(pdf_path):
    output_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        raw_text = first_page.extract_text()

        if raw_text:
            start_marker = "IgG"
            end_marker = "Reactive"

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
        "first_name": pdf_data.get("ﻧﺎﻡ", ""),
        "last_name": pdf_data.get("ﻧﺎﻡ ﺧﺎﻧﻮﺍﺩﮔﯽ", ""),
        "national_code": int(pdf_data.get("ﮐﺪ ﻣﻠﯽ", "0")),
        "gender": gender_map.get(pdf_data.get("ﺟﻨﺲ", "").strip(), ""),
        "pregnancies_number": int(pdf_data.get("ﺗﻌﺪﺍﺩ ﺑﺎﺭﺩﺍﺭﯼ", "0")) if pdf_data.get("ﺗﻌﺪﺍﺩ ﺑﺎﺭﺩﺍﺭﯼ", "").isdigit() else None,
        "age": int(pdf_data.get("ﺳﻦ", "0")),
        "blood_group": blood_map.get(pdf_data.get("ﮔﺮﻭﻩ ﺧﻮﻧﯽ", "").replace(" ", ""), "")
    }
