const fs = require('fs');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const https = require('https');

const projectRoot = path.resolve(__dirname, '../../');
const logsDir = '/home/default/.cache/log';

// class Game {
//     constructor(name, isAdded) {

//     }
// }
// class Setting {
//     constructor(key, value) {

//     }
// }
class LogFile {
    LogFile(self, fileName, content) {
        this.fileName = fileName;
        this.content = content;
    }
}

const readConfig = () => {
    return {
        sunshineProxyPort: 3002,
    };
};

function logsList() {
    // get files in directory
    const files = fs.readdirSync(logsDir);

    // filter to get only log files
    const logFiles = files.filter((file) => file.endsWith('.log'));

    return logFiles.sort();
}

function logsContent(logName) {
    const finalLogFiles = [];

    try {
        let sortedLogFiles = logsList();

        for (logFile in sortedLogFiles) {
            if (logName === logFile) {
                const filepath = path.join(logsDir, logFile);

                const data = fs.readFileSync(filepath);
                const lines = data.split('\n');
                const endLines = lines.slice(-50); // last 50 lines
                const content = ''.join(endLines);
                finalLogFiles.push(LogFile(logFile, content));
            }
        }
        return finalLogFiles;
    } catch (e) {
        console.error(`Error fetching logs for file ${logName}: `, e);
    }
}

const basicAuth = (req, res, next) => {
    const authHeader = req.headers.authorization;

    // Check if Authorization header is provided
    if (!authHeader) {
        res.setHeader('WWW-Authenticate', 'Basic realm="Restricted Area"');
        return res.status(401).send('Authentication required.');
    }

    // Decode the base64 credentials
    const base64Credentials = authHeader.split(' ')[1];
    const credentials = Buffer.from(base64Credentials, 'base64').toString(
        'ascii'
    );
    const [username, password] = credentials.split(':');

    // Validate the username and password
    const webuiUser = process.env.WEBUI_USER || 'admin';
    const webuiPass = process.env.WEBUI_PASS || 'admin';
    if (username === webuiUser && password === webuiPass) {
        return next(); // Auth successful
    }

    // Authentication failed
    res.setHeader('WWW-Authenticate', 'Basic realm="Restricted Area"');
    return res.status(401).send('Invalid credentials.');
};

//  ____  _   _   _   _ ___
// / ___|| | | | | | | |_ _|
// \___ \| |_| | | | | || |
//  ___) |  _  | | |_| || |
// |____/|_| |_|  \___/|___|
//
//
// Create an app for main service and VNC proxy
const app = express();
app.use(basicAuth); // Apply basic auth to all requests to the main app

app.get('/api/config', (req, res) => {
    res.send(readConfig());
});

app.get('/api/logs/content/<file_name>', (req, res) => {
    const fileName = file_name;
    res.send(logsContent(fileName));
});

app.get('/api/logs/list', (req, res) => {
    res.send(logsList());
});

app.use('/web', express.static(path.join(projectRoot, 'web')));

app.use('/noVNC', express.static(path.join(projectRoot, 'noVNC')));

// Proxy websockify
// TODO: Read VNC_PORT from env
// TODO: Remove websockify references. We will need to update noVNC I think
app.use(
    '/websockify',
    createProxyMiddleware({
        target: 'http://localhost:32036',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
            '^/websockify': '',
        },
    })
);

// These routes below need to be the last routes in the list
// Serve static files from the Vue 3 compiled `dist` directory
app.use('/', express.static(path.join(projectRoot, 'shui2/shui-vue/dist')));
// Catch-all route to serve `index.html` for client-side routing
app.use((req, res) => {
    res.sendFile(path.join(projectRoot, 'shui2/shui-vue/dist/index.html'));
});

const appPort = 3001;
app.listen(appPort, () => {
    console.log(`VNC Proxy on port ${appPort}`);
});

//  ____                  _     _              ____
// / ___| _   _ _ __  ___| |__ (_)_ __   ___  |  _ \ _ __ _____  ___   _
// \___ \| | | | '_ \/ __| '_ \| | '_ \ / _ \ | |_) | '__/ _ \ \/ / | | |
//  ___) | |_| | | | \__ \ | | | | | | |  __/ |  __/| | | (_) >  <| |_| |
// |____/ \__,_|_| |_|___/_| |_|_|_| |_|\___| |_|   |_|  \___/_/\_\\__, |
//                                                                 |___/
//

// Create an app for the Sunshine proxy
const sunshineProxy = express();
sunshineProxy.use(basicAuth);

sunshineProxy.use(
    '/',
    createProxyMiddleware({
        target: 'https://localhost:47990',
        ws: true,
        changeOrigin: true,
        secure: false,
        agent: new https.Agent({ rejectUnauthorized: false }),
        onProxyReq: (proxyReq, req) => {
            // Pass the Authorization header from the original request
            if (req.headers.authorization) {
                proxyReq.setHeader('Authorization', req.headers.authorization);
            }
        },
    })
);

const sunshineProxyPort = 3002;
sunshineProxy.listen(sunshineProxyPort, () => {
    console.log(`Sunshine web proxy on port ${sunshineProxyPort}`);
});
