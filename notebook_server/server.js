const express = require('express');
const cors = require('cors');

const PORT = 3000;

const app = express();

app.use(express.json());
app.use(cors());


app.get('/', (req, res) => {
    res.send('Hello world!')
})

app.get('/request', (req, res) => {
    console.log('request received');
    return res
        .status(200)
        .json({
            ok: 'GET request success!'
        });
});

app.post('/click', (req, res) => {
    const body = req.body;
    console.log(body);
    return res
        .status(201)
        .json({
            ok: 'Received'
        });
});

app.listen(PORT, ()=> console.log(`Listening on port ${PORT}...`));
