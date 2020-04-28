const backend = require('./backend.js');

var my_args = process.argv.slice(2);
if (my_args.length != 2) {
  console.log("Run with node get_time.js start destination");
  process.exit(1);
}
const start = my_args[0];
const destination = my_args[1];

const response = backend.get_time(start, destination)
  .then( (val) => console.log(val) );