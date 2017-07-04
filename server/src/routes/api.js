const express = require('express');
const router = express.Router();
const debug = require('debug')('express:router:api');
const multer = require('multer');
const client = require('cheerio-httpcli');
const rp = require('request-promise');
const fs = require('fs');
const util = require('util');
const path = require('path');
const exec = require('child_process').exec;

const UPLOAD_FILE_ROOT = path.join(__dirname, '../../uploaded/');
const ENGINE_CWD = path.join(__dirname, '../../../engine/');

router.post('/search', async (req, res, next) => {
    let query = req.body.q;
    if (!query) {
        res.status(400);
        throw Error('query is null.');
    }

    debug('query', query);

    let amazonUrl = `http://www.amazon.co.jp/s/?url=search-alias%3Dstripbooks&field-keywords=${encodeURIComponent(query)}`;
    let $ = await util.promisify(client.fetch)(amazonUrl);

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

router.post('/find', multer({dest: 'uploaded/'}).single('targetImage'), async (req, res, next) => {
    let timestamp = Date.now();

    let bookImageUrl = req.body.bookImageUrl;
    if (!bookImageUrl) {
        res.status(400);
        throw Error('imageUrl is null.');
    }

    let bookImagePath = path.join(UPLOAD_FILE_ROOT, timestamp + path.extname(bookImageUrl));
    debug('bookImageUrl', bookImageUrl);
    debug('bookImagePath', bookImagePath);

    let targetImagePath = path.join(UPLOAD_FILE_ROOT, timestamp + '-target.jpg');
    debug('targetImagePath', targetImagePath);

    let resultImagePath = path.join(UPLOAD_FILE_ROOT, timestamp + '-result.jpg');
    debug('resultImagePath', resultImagePath);

    try {
        let res = await rp.get({
            url: bookImageUrl,
            encoding: null
        });
        await util.promisify(fs.writeFile)(bookImagePath, Buffer.from(res, 'utf8'));
        await util.promisify(fs.rename)(path.join(process.cwd(), req.file.path), targetImagePath);
    } catch (e) {
        res.status(503);
        throw e;
    }

    let command = `python image_processing.py ${bookImagePath} ${targetImagePath} ${resultImagePath}`;

    try {
        let result = await util.promisify(exec)(command, {
            cwd: ENGINE_CWD
        });

        res.setHeader('Content-Type', 'image/jpeg');
        res.sendFile(resultImagePath);
    } catch (e) {
        res.status(503);
        throw e;
    }
});

module.exports = router;