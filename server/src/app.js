const bodyParser = require('body-parser');
const express = require('express');
const morgan = require('morgan');
const apiRoute = require('./routes/api');
const path = require('path');
const app = express();

app.use(morgan('dev'));
app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, '../../web/build')));

app.use('/api', apiRoute);

app.use((req, res, next) => {
    const err = new Error('Not Found');
    err.status = 404;
    next(err);
});

app.use((err, res) => {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: err
    });
});

module.exports = app;