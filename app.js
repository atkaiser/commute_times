const express = require('express');
const backend = require('./backend.js');
const app = express();
const port = 10000;

const home_address = '5024+Ray+Ave,+Castro+Valley,+CA+94546';
const work_address = '777+Mariners+Island+Blvd,+San+Mateo,+CA+94404';

app.get('/', (req, res) => {
  console.log(req.query);
  res.send('Hello World!')
});

app.get('/status', (req, res) => res.send('Server is up'));

app.get('/time', async (req, res) => {
  var origin = req.query.origin.replace(/ /g, '+');
  var destination = req.query.destination.replace(/ /g, '+');
  var response = await backend.get_time(origin, destination);
  res.send(backend.min_from_string(response['time']).toString());
});

app.get('/time_to_work', async (req, res) => {
  var response = await backend.get_time(home_address, work_address);
  res.send(backend.min_from_string(response['time']).toString());
});

app.get('/time_to_home', async (req, res) => {
  var response = await backend.get_time(work_address, home_address);
  res.send(backend.min_from_string(response['time']).toString());
});

app.get('/all_info', async (req, res) => {
  var origin = req.query.origin.replace(/ /g, '+');
  var destination = req.query.destination.replace(/ /g, '+');
  var response = await backend.get_time(origin, destination);
  res.send(response);
});

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))