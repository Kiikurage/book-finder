const express = require('express');
const router = express.Router();
const debug = require('debug')('express:router:api');
const multer = require('multer');
const client = require('cheerio-httpcli');

router.post('/search', (req, res, next) => {
    let query = req.body.q;
    if (!query) {
        res.status(400);
        throw Error('query is null.');
    }

    debug('query', query);

    client.fetch(`http://www.amazon.co.jp/s/?url=search-alias%3Dstripbooks&field-keywords=${encodeURIComponent(query)}`, (err, $, proxyRes, body) => {
        let data = $('li[id^="result_"]')
            .toArray()
            .map((item, i) => {
                let $item = $(item);
                return {
                    title: $item.find('h2').text(),
                    image: $item.find('img').attr('src')
                }
            });

        debug(data);

        res.send(JSON.stringify(data));
    });
});

// router.post('/find', multer({dest: 'uploaded/'}).single('image'), (req, res, next) => {
router.post('/find', multer({dest: 'uploaded/'}).none(), (req, res, next) => {
    let imageUrl = req.body.imageUrl;
    if (!imageUrl) {
        res.status(400);
        throw Error('imageUrl is null.');
    }

    debug('imageUrl', imageUrl);

    // client.fetch(`http://www.amazon.co.jp/s/?url=search-alias%3Dstripbooks&field-keywords=${encodeURIComponent(query)}`, (err, $, proxyRes, body) => {
    //     let data = $('li[id^="result_"]')
    //         .toArray()
    //         .map((item, i) => {
    //             let $item = $(item);
    //             return {
    //                 title: $item.find('h2').text(),
    //                 image: $item.find('img').attr('src')
    //             }
    //         });
    //
    //     console.log(data);

    res.send('');
    // });
});

module.exports = router;