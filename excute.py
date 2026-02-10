def compare_strings(str1, str2):
    print(f"\n[비교 결과]")
    print(f"문자열 1: {str1}\n")
    print(f"문자열 2: {str2}\n")
    print("-" * 30)

    # 두 문자열이 완전히 동일한 경우
    if str1 == str2:
        print("\n\n두 문자열이 완벽하게 일치합니다.")
        return

    # 길이 차이 확인
    len1, len2 = len(str1), len(str2)
    max_len = max(len1, len2)
    found_diff = False

    for i in range(max_len):
        char1 = str1[i] if i < len1 else "[없음]"
        char2 = str2[i] if i < len2 else "[없음]"

        if char1 != char2:
            print(f"위치 {i}: '{char1}' vs '{char2}' (다름)")
            found_diff = True
    
    if len1 != len2:
        print(f"\n\n참고: 두 문자열의 길이가 다릅니다. (길이 {len1} vs {len2})")

# 사용자 입력 받기
input1 = input("첫 번째 문자열을 입력하세요: ")
input2 = input("\n\n두 번째 문자열을 입력하세요: ")

compare_strings(input1, input2)