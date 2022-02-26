const express = require('express')
const app = express()
const pg = require('pg');
const path = require('path');
const fetch = require('node-fetch');
const axios = require("axios")


app.get('/*', (req, res) => {
  //res.sendFile(path.join(__dirname, 'client', 'build', 'index.html'));
  res.json("we all good");
});

var server = app.listen(process.env.PORT || 5000, function () {
  var port = server.address().port;
  console.log("App now running on port", port);
});
