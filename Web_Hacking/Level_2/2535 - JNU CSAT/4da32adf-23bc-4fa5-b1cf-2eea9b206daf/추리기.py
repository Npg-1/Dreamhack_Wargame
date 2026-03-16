import re

def find_missing_ids(input_filename, output_filename):
    # 1. 파일에서 "id":숫자 패턴의 숫자만 모두 추출
    pattern = r'"id":\s*(\d+)'
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 추출된 문자열 숫자를 정수(int)형으로 변환하여 집합(set)에 저장
        existing_ids = set(map(int, re.findall(pattern, content)))
        
        # 2. 전체 범위(1~722) 생성
        full_range = set(range(1, 723))
        
        # 3. 차집합 연산: 전체 범위에서 존재하는 ID를 제외
        missing_ids = sorted(list(full_range - existing_ids))
        
        # 4. 결과 저장
        with open(output_filename, 'w', encoding='utf-8') as f:
            # 보기 좋게 쉼표로 구분하여 저장 (또는 한 줄에 하나씩 하려면 "\n".join 사용)
            result_str = ", ".join(map(str, missing_ids))
            f.write(result_str)
            
        print(f"체크 완료!")
        print(f"파일 내 발견된 ID 개수: {len(existing_ids)}개")
        print(f"제외된(없는) ID 개수: {len(missing_ids)}개")
        print(f"결과가 '{output_filename}'에 저장되었습니다.")

    except FileNotFoundError:
        print(f"에러: '{input_filename}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 실행: 'result.txt'를 읽어서 없는 번호만 'missing_ids.txt'에 저장
find_missing_ids('result.txt', 'missing_ids.txt')