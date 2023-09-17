/**
 * File: webaudio.js
 * File Created: Sunday, 17th September 2023 6:09:10 pm
 * Author: Josh.5 (jsunnex@gmail.com)
 * -----
 * Last Modified: Sunday, 17th September 2023 7:54:33 pm
 * Modified By: Josh.5 (jsunnex@gmail.com)
 */


export default class WebAudio {
    constructor(url) {
        this.url = url

        this.connected = false;

        //constants for audio behavior
        this.maximumAudioLag = 1.5; //amount of seconds we can potentially be behind the server audio stream
        this.syncLagInterval = 5000; //check every x milliseconds if we are behind the server audio stream
        this.updateBufferEvery = 20; //add received data to the player buffer every x milliseconds
        this.reduceBufferInterval = 500; //trim the output audio stream buffer every x milliseconds so we don't overflow
        this.maximumSecondsOfBuffering = 1; //maximum amount of data to store in the play buffer
        this.connectionCheckInterval = 500; //check the connection every x milliseconds

        //register all our background timers. these need to be created only once - and will run independent of the object's streams/properties
        this.updateCheck = null;
        this.syncCheck = null;
        this.reduceCheck = null;
        this.ConnCheck = null;

    }

    //registers all the event handlers for when this stream is closed - or when data arrives.
    registerHandlers() {
        this.mediaSource.addEventListener('sourceended', e => this.socketDisconnected(e))
        this.mediaSource.addEventListener('sourceclose', e => this.socketDisconnected(e))
        this.mediaSource.addEventListener('error', e => this.socketDisconnected(e))
        this.buffer.addEventListener('error', e => this.socketDisconnected(e))
        this.buffer.addEventListener('abort', e => this.socketDisconnected(e))
    }

    //starts the web audio stream. only call this method on button click.
    start() {
        if (!!this.connected) return;
        if (!!this.audio) this.audio.remove();
        this.queue = null;

        if (this.updateCheck === null) this.updateCheck = setInterval(() => this.updateQueue(), this.updateBufferEvery);
        if (this.syncCheck === null) this.syncCheck = setInterval(() => this.syncInterval(), this.syncLagInterval);
        if (this.reduceCheck === null) this.reduceCheck = setInterval(() => this.reduceBuffer(), this.reduceBufferInterval);
        if (this.ConnCheck === null) this.ConnCheck = setInterval(() => this.tryLastPacket(), this.connectionCheckInterval);

        this.mediaSource = new MediaSource()
        this.mediaSource.addEventListener('sourceopen', e => this.onSourceOpen())
        //first we need a media source - and an audio object that contains it.
        this.audio = document.createElement('audio');
        this.audio.src = window.URL.createObjectURL(this.mediaSource);

        //start our stream - we can only do this on user input
        this.audio.play();
    }

    stop() {
        // Clear all interval timers
        clearInterval(this.updateCheck);
        clearInterval(this.syncCheck);
        clearInterval(this.reduceCheck);
        clearInterval(this.ConnCheck);
        // Close the socket
        this.socket.close();
        this.connected = false;
        // Reset timers to null
        this.updateCheck = null;
        this.syncCheck = null;
        this.reduceCheck = null;
        this.ConnCheck = null;
    }

    wsConnect() {
        if (!!this.socket) this.socket.close();

        this.socket = new WebSocket(this.url, ['binary', 'base64'])
        this.socket.binaryType = 'arraybuffer'
        this.socket.addEventListener('message', e => this.websocketDataArrived(e), false);
    }

    //this is called when the media source contains data
    onSourceOpen(e) {
        this.buffer = this.mediaSource.addSourceBuffer('audio/webm; codecs="opus"')
        this.registerHandlers();
        this.wsConnect();
    }

    //whenever data arrives in our websocket this is called.
    websocketDataArrived(e) {
        this.lastPacket = Date.now();
        this.connected = true;
        this.queue = this.queue == null ? e.data : this.concat(this.queue, e.data);
    }

    //whenever a disconnect happens this is called.
    socketDisconnected(e) {
        console.log(e);
        this.connected = false;
    }

    tryLastPacket() {
        if (this.lastPacket == null) return;
        if ((Date.now() - this.lastPacket) > 1000) {
            this.socketDisconnected('timeout');
        }
    }

    //this updates the buffer with the data from our queue
    updateQueue() {
        if (!(!!this.queue && !!this.buffer && !this.buffer.updating)) {
            return;
        }

        this.buffer.appendBuffer(this.queue);
        this.queue = null;
    }

    //reduces the stream buffer to the minimal size that we need for streaming
    reduceBuffer() {
        if (!(this.buffer && !this.buffer.updating && !!this.audio && !!this.audio.currentTime && this.audio.currentTime > 1)) {
            return;
        }

        this.buffer.remove(0, this.audio.currentTime - 1);
    }

    //synchronizes the current time of the stream with the server
    syncInterval() {
        if (!(this.audio && this.audio.currentTime && this.audio.currentTime > 1 && this.buffer && this.buffer.buffered && this.buffer.buffered.length > 1)) {
            return;
        }

        var currentTime = this.audio.currentTime;
        var targetTime = this.buffer.buffered.end(this.buffer.buffered.length - 1);

        if (targetTime > (currentTime + this.maximumAudioLag)) this.audio.fastSeek(targetTime);
    }

    //joins two data arrays - helper function
    concat(buffer1, buffer2) {
        var tmp = new Uint8Array(buffer1.byteLength + buffer2.byteLength);
        tmp.set(new Uint8Array(buffer1), 0);
        tmp.set(new Uint8Array(buffer2), buffer1.byteLength);
        return tmp.buffer;
    };
}
