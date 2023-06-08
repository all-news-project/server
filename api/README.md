# Server API

### Docker Build

```shell
docker build -t server-api-<version> .
```

### Docker Run

```shell
docker run -d -p 80:5000 server-api-<version>
```

### Set url

Access your API: With the container running, your Flask API should be accessible via the host machine's IP address or domain name using port 80. If the IP address of your Ubuntu machine is 192.168.0.100, you can access your API at http://192.168.0.100.
Make sure to configure any necessary firewall rules or port forwarding settings to allow inbound connections to port 80 on your Ubuntu machine.

Note: If you want to make your API accessible from the internet, you'll need to configure port forwarding on your router to forward incoming traffic on port 80 to the internal IP address of your Ubuntu machine.

That's it! Your Flask API is now deployed on Docker, and other applications can connect to it using the specified URL.