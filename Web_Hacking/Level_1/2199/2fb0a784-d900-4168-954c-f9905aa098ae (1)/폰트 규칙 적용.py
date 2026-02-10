def transform_string(input_str):
    result = []
    
    for char in input_str:
        # 소문자 a, b, c 처리 (+3)
        if 'a' <= char <= 'c':
            new_char = chr(ord(char) + 3)
            result.append(new_char)
        
        # 소문자 x, y, z 처리 (+6)
        elif 'x' <= char <= 'z':
            # 26자 순환을 고려하여 % 26 사용
            new_char = chr((ord(char) - ord('a') + 6) % 26 + ord('a'))
            result.append(new_char)
        
        # 나머지 문자는 그대로 유지
        else:
            result.append(char)
            
    return "".join(result)

# --- 테스트 코드 ---
test_input = input("입력 문자열: ")
output = transform_string(test_input)

print(f"\n\n\n출력: {output}")