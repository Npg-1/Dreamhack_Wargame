// require() Node.js에서 외부 라이브러리나 다른 파일의 코드를 가져올 때 사용하는 함수임
var express     = require('express');       // 'express'라는 패키지를 가져옴
var app         = express();                // 'express' 패키지로 
var bodyParser  = require('body-parser');
var mongoose    = require('mongoose');
var path        = require('path');



// 몽고DB 가져오기 및 연결
var db = mongoose.connection;
db.on('error', console.error);          // 'error'가 발생하면 console.error를 실행함
db.once('open', function(){             // 데이터베이스와 연결이 최초로 성공했을 때 딱 한 번 실행됨
    console.log("Connected to mongod server");
});
mongoose.connect('mongodb://localhost/mongoboard');


// 모델 가져오기
var Board = require('./models/board');  //현재 위치의 -> models -> board를 가져오기


// 앱 설정
app.use('/static', express.static(__dirname + '/public'));      // 사진, CSS, JS 등의 정적 파일은 public 폴더에서(/static) 에서 찾아가라
app.use(bodyParser.urlencoded({ extended: true }));             // HTML <form> 태그로 보낸 데이터를 해석할 수 있도록 하겠다
app.use(bodyParser.json());                                     // JSON 형태의 데이터를 해석할 수 있도록 하겠다

app.all('/*', function(req, res, next) {                        // app.get()은 GET요청만을 처리하지만 app.all은 모든 요청을 처리하고 /* 로 되어 있으니까 모든 주소에 아래 규칙을 적용함
  res.header("Access-Control-Allow-Origin", "*");                           // 모든 사이트에서 온 요청을 다 받음
  res.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT");    // 모든 
  res.header("Access-Control-Allow-Headers", "Content-Type");
  next();
});

// router
var router = require(__dirname + '/routes')(app, Board);
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

// run
var port = process.env.PORT || 8080;
var server = app.listen(port, function(){
 console.log("Express server has started on port " + port)
});




