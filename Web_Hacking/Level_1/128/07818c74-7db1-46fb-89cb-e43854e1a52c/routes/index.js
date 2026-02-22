



module.exports = function(app, MongoBoard){
    app.get('/api/board', function(req,res){
        MongoBoard.find(function(err, board){
            if(err) return res.status(500).send({error: 'database failure'});  // error가 있다면 500번 에러를 발생
            res.json(board.map(data => {
                return {
                    _id: data.secret?null:data._id,     // body 대신에 id값이 들어있음
                    title: data.title,
                    author: data.author,
                    secret: data.secret,
                    publish_date: data.publish_date
                }
            }));
        })
    });

    //     var boardSchema = new Schema({
    //     title: {type:String, required: true},                   // O
    //     body: {type:String, required: true},                    // 
    //     author: {type:String, required: true},                  // O
    //     secret: {type:Boolean, default: false},                 // 
    //     publish_date: { type: Date, default: Date.now  }        // O
    // }, {versionKey: false });

    app.get('/api/board/:board_id', function(req, res){
        MongoBoard.findOne({_id: req.params.board_id}, function(err, board){
            if(err) return res.status(500).json({error: err});
            if(!board) return res.status(404).json({error: 'board not found'});
            res.json(board);
        })
    });

    app.put('/api/board', function(req, res){
        var board = new MongoBoard();
        board.title = req.body.title;
        board.author = req.body.author;
        board.body = req.body.body;
        board.secret = req.body.secret || false;        // js에서 req.body.secret의 값이 없으면 false를 넣음

        board.save(function(err){
            if(err){
                console.error(err);
                res.json({result: false});
                return;
            }
            res.json({result: true});
        });
    });
}

// 699a909a96ff5ff68d583ed4
// 699a909f96ff5ff68d583ed5

// 699a90a296ff5ff68d583ed7


// 몽고 DB 특징: NoSQL이고, JSON과 유사한 구조로 데이터를 저장함 -> Node.js는 자바스크립트를 쓰는데 이 점이 비슷함









