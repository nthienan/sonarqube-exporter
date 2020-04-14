# SonarQube Exporter

Usage:
```
usage: sqe [-h] --url URL --access-token ACCESS_TOKEN [--interval INTERVAL]
           [--ignore-ssl-verification] [--log-level LOG_LEVEL] [--port PORT]
           [--storage-info] [--users]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             SonarQube URL which will be monitored
  --user-token USER_TOKEN
                        Access token used for authentication against
                        SonarQube
  --interval INTERVAL   Interval in seconds
  --ignore-ssl-verification
  --log-level LOG_LEVEL
                        Log level. It can be DEBUG, INFO, WARNING, ERROR,
                        CRITICAL. Default is INFO
  --port PORT, -p PORT  The port that JAE will listen on. Default is 8998
```
Docker:
```bash
docker run -d -p 8999:8999 nthienan/sonarqube-exporter --storage-info --users --url https://sonarqube.example.com --user-token <USER_TOKEN>
```
Metrics:
