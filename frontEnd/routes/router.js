var express = require('express');
var router = express.Router();
var User = require('../models/user');
var Logs = require('../models/logs');


//POST route for updating data
router.post('/', function (req, res, next) {
  // confirm that user typed same password twice
  if (req.body.password !== req.body.passwordConf) {
    var err = new Error('Passwords do not match.');
    err.status = 400;
    res.send("passwords dont match");
    return next(err);
  }

  if (req.body.email &&
    req.body.username &&
    req.body.password &&
    req.body.passwordConf) {

    var userData = {
      email: req.body.email,
      username: req.body.username,
      password: req.body.password,
      passwordConf: req.body.passwordConf,
    }

    User.create(userData, function (error, user) {
      if (error) {
        return next(error);
      } else {
        return res.send({id: user._id});
        
      }
    });

  } else if (req.body.logemail && req.body.logpassword) {
    User.authenticate(req.body.logemail, req.body.logpassword, function (error, user) {
      if (error || !user) {
                
        var err = new Error('Wrong email or password.');
        err.status = 401;
        return next(err);
      } else {
        req.session.userId = user._id;
        res.setHeader('content-type', 'text/javascript');
        return res.send({
          id: user._id,
          // username: user.username,
          // email: user.email
        });
      }
    });
  } else {
    var err = new Error('All fields required.');
    err.status = 400;
    return next(err);
  }
}) 


// POST route to save logs data
router.post('/logs', function(req, res){
      var logsData = {
      url: req.body.url,
      time: req.body.time,
      user_id: req.body.user_id,
      body: req.body.body,
      title: req.body.title,
      url_category: req.body.url_category,
      searchString: req.body.searchString,
  }

  Logs.create(logsData, function (error, log) {
    if (error) {
      return next(error);
    } else {
      return res.send({id: log._id});
    }
  });
}
);


// GET logs of all users
router.get('/logs', function(req, res) {
  Logs.find().then(eachOne =>{
    return res.json(eachOne);
  })
});


// GET all logs of given user_id
router.get('/logs/:user_id', function(req, res){
  Logs.find({user_id:req.params.user_id}).then(eachOne =>{
    return res.json(eachOne);
  })
});


module.exports = router;

// curl command to login//

// curl --header "Content-Type: application/json"   
// --request POST   
// --data '{"logemail":"test1@gmail.com","logpassword":"test1"}'   http://localhost:3000/

// curl command to load the browsing details to mongodb //

// curl --header "Content-Type: application/json"   
// --request POST   
// --data '{
// "url":
// "https://www.google.com/search?source=hp&ei=SZuuW5usIb2S0PEP-uyukAo&q=health+tips&btnK=Google+Search&oq=health+tips&gs_l=psy-ab.3..35i39j0i67l5j0j0i67l2j0.378.2017..2936...0.0..2.618.3607.2j2j5j1j2j1......0....1..gws-wiz.....6..0i20i264j0i131j0i20i263i264j0i131i20i263i264j0i10j0i20i263.agbA17gMxpc",
//   "time":"Fri Sep 28 2018 14:32:38 GMT-0700 (Pacific Daylight Time)",
//   "body": "<body> <p> Some body content here!!!</p></body>",
//   "title": "<h1> Health tips about someting, this will be there only for blogs </h1>",
//   "searchString": "health+tips",
//   "url_category": "search/social_networking/blog/jobs_portal/ecommerce",
//   "user_id":"5bae8cee37bae414020ac748"
// }'   http://localhost:3000/logs