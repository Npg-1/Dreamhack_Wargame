import base64
import urllib

user_input_str = __builtins__.input("입력값: ")

print('변환 전: ', user_input_str)
print('변환 후: ', urllib.parse.quote(user_input_str))