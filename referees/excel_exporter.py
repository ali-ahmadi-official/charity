import openpyxl
from django.http import HttpResponse

def export_to_excel(
    datasets: list,
    filename: str = "export.xlsx",
    sheet_names: list = None,
):
    """
    datasets: list of data
        each item can be:
        - dict
        - list
        - list of dict
        - list of list / tuple
        - simple list
    """

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    for index, data in enumerate(datasets):
        sheet_name = (
            sheet_names[index]
            if sheet_names and index < len(sheet_names)
            else f"Sheet_{index + 1}"
        )

        ws = wb.create_sheet(title=sheet_name)
        _fill_sheet(ws, data)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response


# ================= INTERNAL HELPERS =================

def _fill_sheet(ws, data):
    if data is None:
        ws.append(["No data"])
        return

    # 🔴 اول dict (خیلی مهم)
    if isinstance(data, dict):
        _write_dict(ws, data)
        return

    # 🔵 بعد list
    if isinstance(data, list):
        if not data:
            ws.append(["Empty list"])
            return

        # list of dict
        if all(isinstance(item, dict) for item in data):
            _write_list_of_dict(ws, data)
            return

        # list of list / tuple
        if all(isinstance(item, (list, tuple)) for item in data):
            _write_list_of_list(ws, data)
            return

        # simple list
        _write_simple_list(ws, data)
        return

    # fallback
    ws.append([str(data)])


def _write_dict(ws, data: dict):
    """
    Handles:
    - dict[str, value]
    - dict[str, list]
    """

    ws.append(["کلید", "مقدار"])

    for key, value in data.items():
        # اگر مقدار خودش dict بود
        if isinstance(value, dict):
            ws.append([key, str(value)])

        # اگر مقدار لیست یا تاپل بود
        elif isinstance(value, (list, tuple)):
            if len(value) == 1:
                ws.append([key, _safe_value(value[0])])
            else:
                for item in value:
                    ws.append([key, _safe_value(item)])

        else:
            ws.append([key, _safe_value(value)])


def _write_list_of_dict(ws, data: list):
    headers = list(data[0].keys())
    ws.append(headers)

    for row in data:
        ws.append([_safe_value(row.get(h)) for h in headers])


def _write_list_of_list(ws, data: list):
    for row in data:
        if isinstance(row, (list, tuple)):
            ws.append([_safe_value(cell) for cell in row])
        else:
            ws.append([_safe_value(row)])


def _write_simple_list(ws, data: list):
    ws.append(["Value"])
    for item in data:
        ws.append([_safe_value(item)])


def _safe_value(value):
    """
    Ensures value is safe for Excel cell
    """
    if isinstance(value, (list, dict, tuple)):
        return str(value)
    return value
