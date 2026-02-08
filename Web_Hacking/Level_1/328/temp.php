<?php
    require("./lib.php"); // for FLAG


    # 뒤지게 신기하게 생겼네 md5에서 rand()를 3번 한 다음 나온 값을 다시 rand()한 값을 sha1에 집어넣어서 패스워드 생성 ㄷㄷ
    $password = sha1(md5(rand().rand().rand()).rand()); 

    # 여기서의 $_GET은 사용자 정의 변수가 아닌 PHP에서 만든 변수여서 사용자가 GET 요청으로 'view-source'를 하는 순간 해당 요청값이 $_GET에 담김
    if (isset($_GET['view-source'])) {      
        show_source(__FILE__);
        exit();
    }else if(isset($_POST['password'])){
        sleep(1); // do not brute force!
        if (strcmp($_POST['password'], $password) == 0) {
            echo "Congratulations! Flag is <b>" . $FLAG ."</b>";
            exit();
        } else {
            echo "Wrong password..";
        }
    }

?>
<br />
<br />
<form method="POST">
    password : <input type="text" name="password" /> <input type="submit" value="chk">
</form>
<br />
<a href="?view-source">view-source</a>