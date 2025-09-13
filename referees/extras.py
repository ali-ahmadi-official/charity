from collections import defaultdict
import fitz
import re

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
