# From RTPM to SocketIO

Utilize an RTMP stream to process images with OpenCV, transmitting data via Socket.IO and serving images through Flask.

The main objective is read QR codes (or bar codes as well) to manage a warehouse inventory.

## Streaming via RTMP

### Server

In this project we are using a simple nginx configured to receive messages via RTMP and transmitting via HLS.

```nginx
rtmp {
    server {
        listen 1935;

        application live {
            live on;
            record off;
            hls on;
            hls_path /hls/live;
            hls_fragment 3;
        }
    }
}
```

## Running Flask

TO DO.

### Locally

TO DO.

### Docker

TO DO.
