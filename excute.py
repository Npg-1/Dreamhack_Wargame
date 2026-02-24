import hashlib

while True:
    def convert_to_sha256(text):
        # 1. 문자열을 바이트(bytes) 형태로 인코딩 (UTF-8 기준)
        encoded_text = text.encode('utf-8')
        
        # 2. sha256 객체 생성 및 해싱 실행
        sha256_hash = hashlib.sha256(encoded_text)
        
        # 3. 해싱된 결과를 16진수(hex) 문자열로 반환
        return sha256_hash.hexdigest()

    # 테스트
    # password = "guest"
    password = input("입력: ")
    result = convert_to_sha256(password)

    print(f"SHA-256 해시값: {result}\n\n")
