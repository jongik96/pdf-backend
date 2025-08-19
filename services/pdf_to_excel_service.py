import os
import pandas as pd
import pdfplumber

def clean_cell(val):
    if pd.isna(val):
        return ''
    val = str(val)
    val = val.replace('\n', ' ').replace('\r', ' ')
    val = val.replace('"', "'")
    return val

def convert_pdf_to_excel(input_path, output_dir, excel_format="xlsx", timestr=""):
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    # output 파일명: base_name_시분초.xlsx 또는 .csv
    output_filename = f"{base_name}.{excel_format}" if not timestr else f"{base_name}_{timestr}.{excel_format}"
    output_path = os.path.join(output_dir, output_filename)

    all_tables = []
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    all_tables.append(table)

    if not all_tables:
        raise Exception("PDF에서 추출된 표가 없습니다.")

    dfs = [pd.DataFrame(table) for table in all_tables]
    result_df = pd.concat(dfs, ignore_index=True, sort=False)

    # 셀 전처리 적용 (줄바꿈, 따옴표 등)
    result_df = result_df.applymap(clean_cell)

    if excel_format == "csv":
        result_df.to_csv(output_path, index=False, header=False, encoding="utf-8-sig", sep="\t")
    else:
        result_df.to_excel(output_path, index=False, header=False)

    return output_path, output_filename