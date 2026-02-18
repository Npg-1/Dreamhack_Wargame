<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XSS test page</title>
</head>
<body>
    <form method="GET" action="">
        <input type="text" name="user_name" >
        <button type="submit"> 전송 </button>
    </form>
    <?php
    
        $user_name=$_GET['user_name'];
 
        if(!$user_name)
        {
            echo "<p>이름을 입력해주세요.<br></p>";
        }
        
        else
        {
            echo "<p>".$user_name."님 환영합니다.<br></p>";
        }
 
    ?>
    
</body>
</html>
