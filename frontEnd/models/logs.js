var mongoose = require('mongoose');
// var bcrypt = require('bcrypt');

var logsSchema = new mongoose.Schema({
  url: {
    type: String,
    required: true,
    trim: true
  },
  time: {
    type: String,
    required: true,
    trim: true
  },
  body: {
    type: String,
    required: false,
  },
  title: {
    type: String,
    required: false,
  },
  searchString: {
      type: String,
      required: false,
  },
  url_category: {
      type: String,
      required: false,
  },
  user_id: {
      type: String,
      required: true,
  }
});

logsSchema.post('save', function (done, next) {
    var log = this;
    // console.log(log.url);
    next();
});

const logs = mongoose.model('logs', logsSchema);
module.exports = logs;

// "url":
// "https://www.google.com/search?source=hp&ei=SZuuW5usIb2S0PEP-uyukAo&q=health+tips&btnK=Google+Search&oq=health+tips&gs_l=psy-ab.3..35i39j0i67l5j0j0i67l2j0.378.2017..2936...0.0..2.618.3607.2j2j5j1j2j1......0....1..gws-wiz.....6..0i20i264j0i131j0i20i263i264j0i131i20i263i264j0i10j0i20i263.agbA17gMxpc",
//   "time":"Fri Sep 28 2018 14:32:38 GMT-0700 (Pacific Daylight Time)",
//   "body": "<body> <p> Some body content here!!!</p></body>",
//   "title": "<h1> Health tips about someting, this will be there only for blogs </h1>",
//   "searchString": "health+tips",
//   "url_category": "search/social_networking/blog/jobs_portal/ecommerce",
//   "user_id":"5bae8cee37bae414020ac748"
// }