# # 설치: pip install pymongo
# from bson.objectid import ObjectId

# def id_to_time(object_id_str):
#     # 16진수 문자열을 ObjectId 객체로 변환
#     obj_id = ObjectId(object_id_str)
#     # 생성 시간 추출 (UTC 기준)
#     return obj_id.generation_time

# # 예시: 아까 계산했던 2026-02-22 06:05:12의 ID (뒷자리는 예시값)
# # sample_id = "699a9c9dc6a6ae5fbb70b8bb"
# sample_id = input("sample_id: ")
# print(f"생성 시간: {id_to_time(sample_id)}\n")

from bson.objectid import ObjectId
from datetime import datetime

def time_to_objectid(time_str):
    # 1. 입력받은 문자열을 datetime 객체로 변환 (밀리초 포함 처리)
    # 마지막 'Z'는 UTC를 의미하므로 제거하거나 포맷에 반영합니다.
    dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt = datetime.strptime(time_str, dt_format)
    
    # 2. datetime 객체를 사용하여 해당 시간의 가장 빠른 ObjectId 생성
    # 이 ID는 [4바이트 시간] + [8바이트 0으로 채움] 형태가 됩니다.
    oid = ObjectId.from_datetime(dt)
    
    return oid

# 테스트 데이터
time_input = input("시간 입력: ")
result_id = time_to_objectid(time_input)

# print(f"입력 시간: {time_input}")
print(f"변환된 ObjectId: {result_id}")
print(f"16진수 타임스탬프 부분: {str(result_id)[:8]}")