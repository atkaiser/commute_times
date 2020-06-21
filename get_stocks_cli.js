const get_stocks = require('./get_stocks.js');

const response = get_stocks.get_sandp()
  .then( (val) => console.log(val) );

