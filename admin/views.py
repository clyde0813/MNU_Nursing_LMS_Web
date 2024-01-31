from django.shortcuts import render
from models.models import *

# Create your views here.
def checklistUpdate(request):
    if request.method == "POST":
        excel_file = request.FILES['excel']
        # excel = pd.ExcelFile(excel_file)
        # # 시트 이름 목록 가져오기
        # sheet_names = excel.sheet_names
        #
        # # 시트 이름 출력
        # print("시트 이름 목록:", sheet_names)
        # # 각 시트별로 데이터를 불러와서 딕셔너리에 저장
        # sheet_data = {}
        # for sheet_name in sheet_names:
        #     # 각 시트별로 데이터를 DataFrame으로 불러오기
        #     df = pd.read_excel(excel_file, sheet_name=sheet_name)
        #
        #     # 딕셔너리에 시트 이름을 키로 데이터를 저장
        #     sheet_data[sheet_name] = df
        #
        # # 시트별로 불러온 데이터 확인
        # for sheet_name, df in sheet_data.items():
        #     print(f"시트: {sheet_name}")
        #     print(df["content"])
        #     print("\n")

    return render(request, "admin/checklistUpdate.html")
