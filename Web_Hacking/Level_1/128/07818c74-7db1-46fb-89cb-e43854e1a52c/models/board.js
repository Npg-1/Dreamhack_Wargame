var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var boardSchema = new Schema({
    title: {type:String, required: true},                   // O
    body: {type:String, required: true},                    // 
    author: {type:String, required: true},                  // O
    secret: {type:Boolean, default: false},                 // 
    publish_date: { type: Date, default: Date.now  }        // O
}, {versionKey: false });

module.exports = mongoose.model('board', boardSchema);