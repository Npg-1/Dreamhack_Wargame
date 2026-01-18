from collections import Counter

def process_strings():
    raw_inputs = []
    
    print("문자열을 입력하세요. (종료하려면 'exit' 입력)")
    
    # 1. 문자열 입력 단계
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        # 입력과 동시에 '*' 제거 처리
        cleaned_input = user_input.replace('*', '')
        raw_inputs.append(cleaned_input)
    
    if not raw_inputs:
        print("입력된 데이터가 없습니다.")
        return

    # 2. 통계 계산
    # 각 문자열이 몇 번 나타났는지 계산
    counts = Counter(raw_inputs)
    
    # 중복 제거된 전체 리스트 (Set 활용)
    unique_strings = sorted(list(counts.keys()))
    
    # 중복된 문자열만 추출 (2번 이상 나타난 것)
    duplicates = [string for string, count in counts.items() if count > 1]

    # 3. 결과 출력
    print("\n" + "="*30)
    print(f"1. 전체 입력된 문자열 개수: {len(raw_inputs)}개")
    print(f"2. 중복 제거 후 리스트 크기: {len(unique_strings)}개")
    
    print("-" * 30)
    if duplicates:
        print(f"3. 중복된 문자열 ({len(duplicates)}종류):")
        for string in sorted(duplicates):
            print(f"   - '{string}' (총 {counts[string]}회 입력됨)")
    else:
        print("3. 중복된 문자열이 없습니다.")
    print("="*30)

    print("\n[최종 리스트]")
    print(unique_strings)

if __name__ == "__main__":
    process_strings()