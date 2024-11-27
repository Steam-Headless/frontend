const fs = require('fs');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const express = require('express');
const app = express();
const port = process.env.SERVER_PORT || 3001;

const logsDir = "/home/default/.cache/log";

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
        this.fileName = fileName
        this.content = content;
    }
}

function logsList() {
    // get files in directory
    const files = fs.readdirSync(logsDir);

    // filter to get only log files
    const logFiles = files.filter(file => file.endsWith('.log'));

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
                const content = "".join(endLines);
                finalLogFiles.push(LogFile(logFile, content));
            }
        }
        return finalLogFiles;
    } catch (e) {
        console.error(`Error fetching logs for file ${logName}: `, e);
    }
}


app.get('/api/logs/content/<file_name>', (req, res) => {
    const fileName = file_name
    res.send(logsContent(fileName));
});

app.get('/api/logs/list', (req, res) => {
    res.send(logsList());
});

// TODO: Read as relative path to this script
app.use('/web', express.static('/home/default/frontend/web'))
app.use('/noVNC', express.static('/home/default/frontend/noVNC'))

// Proxy websockify
// TODO: Read VNC_PORT from env
// TODO: Remove websockify references. We will need to update noVNC I think
app.use(
    '/websockify',
    createProxyMiddleware({
        target: 'http://localhost:32036',   // Forward to port 32039 (VNC_PORT)
        ws: true,                           // Enable WebSocket proxying
        changeOrigin: true,                 // Update the Host header to match the target
        pathRewrite: {
            '^/websockify': '',             // Remove `/websockify` from the forwarded request
        },
    })
);

app.listen(port, () => {
    console.log(`Example app on port ${port}`);
});