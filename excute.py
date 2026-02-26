import base64
import zlib

# 1. 대상 세션 값 (마점표로 구분된 첫 번째 토큰만 사용)
session_value = ".eJwtxrERgDAIAMBdskA4IJC4DQKxsTJ2nrvb-NU_ZaVfeZftz6oNcOzTabhOiSRJbmBB5hLck4wVQVWj09BEI4NUkCbIlGxc52lHeT_lABpb.aZ-kCw.l9YNBCqch-KPqnxx_Q7HWwiAKA8==="

# 첫 번째 마침표(.) 이후의 데이터가 실제 세션 내용입니다.
# 만약 값 맨 앞에 .이 있다면 이를 제외하고 첫 번째 세그먼트를 가져옵니다.
compressed_payload = session_value.split('.')[1]

try:
    # 2. Base64 디코딩 (URL-Safe 방식)
    # 패딩(=) 문제를 방지하기 위해 충분한 패딩을 추가해줍니다.
    decoded_payload = base64.urlsafe_b64decode(compressed_payload)

    # decompressed_payload = "ZUp3dHhyRVJnREFJQU1CZHNrQTRJSkM0RFFLeHNUSjJucnZiLU5VX1phVmZlWmZ0ejZvTmNPelRhYmhPaVNSSmJtQkI1aExjazR3VlFWV2owOUJFSTROVWtDYklsR3hjNTJsSGVUX2xBQnBiLmFaLWtDdy5sOVlOQkNxY2gtS1Bxbnh4X1E3SFd3aUFLQTg9PT0NCg"

    # 3. zlib 압축 해제 (Decompress)
    decompressed_data = zlib.decompress(decoded_payload)

    # 4. 결과 출력
    print("추출된 원본 데이터:", decompressed_data.decode('utf-8'))
except Exception as e:
    print("디코딩 중 오류 발생:", e)