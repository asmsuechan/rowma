import axios from 'axios';
import io from 'socket.io-client';

class Rowma {
  constructor(geocode, opts = {}) {
    this.geocode = geocode;

    this.baseURL = opts.baseURL || 'http://18.176.1.219';
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 1000
    });
  }

  currentConnectionList() {
    const path = '/list_connections';
    const params = { geocode: this.geocode };
    return this.client.get(path, { params });
  }

  runLaunch(uuid, command) {
    const socket = io.connect(`${this.baseURL}/conn_device`);
    socket.on('connect', () => {
      console.log('payloads: ', { uuid, command });
      socket.emit('run_launch', { uuid, command });
      // TODO: Get response from server to wait some event
      socket.close();
    });
  }
}

export default Rowma;
