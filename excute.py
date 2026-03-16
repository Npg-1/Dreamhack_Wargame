import unicodedata

msg = "｛｛　ｓｅｌｆ．＿＿ｉｎｉｔ＿＿．＿＿ｇｌｏｂａｌｓ＿＿［＇＿＿ｂｕｉｌｔｉｎｓ＿＿＇］［＇ｏｐｅｎ＇］（＇／ｈｏｍｅ／ｈａｎｇｕｌ／ｆｌａｇ＇）．ｒｅａｄ（）　｝｝"
msg = unicodedata.normalize("NFKC", msg)
print(msg)



















