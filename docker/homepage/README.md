# Homepage

A highly customizable dashboard/application homepage with Docker and service API integrations.

![preview.gif](./preview.gif)

- Official code source: https://github.com/gethomepage/homepage

## Docker Compose Quickstart

```yaml
version: "3.3"
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    restart: unless-stopped
    ports:
      - 3000:3000
    volumes:
      - ./config:/app/config
```

**Folder Structure:** (Setup)

```
./homepage/
    └── docker-compose.yaml
```

**Folder Structure:** (Deployed)

```
./homepage/
    ├── config/
    │   ├── logs/
    │   ├── bookmarks.yaml
    │   ├── custom.css
    │   ├── custom.js
    │   ├── docker.yaml
    │   ├── kubernetes.yaml
    │   ├── services.yaml
    │   ├── settings.yaml
    │   └── widgets.yaml
    └── docker-compose.yaml
```

## [Documentation](https://gethomepage.dev/latest/)