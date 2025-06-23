# Steam Headless Frontend

This project is the web frontend for the Steam Headless Docker container.


## Local dev

### 🛠️ Prerequisites

- A running `steam-headless` Docker container (via Docker Compose)
- Git access to clone this repo
- The ability to modify the container's volume mounts

### 🚀 Running

#### 1. Clone the Frontend Repository

On the host machine where `steam-headless` is running:
```bash
git clone --recurse-submodules https://github.com/Steam-Headless/frontend.git
cd frontend
```

Alternatively:
```bash
git clone https://github.com/Steam-Headless/frontend.git
cd frontend
git submodule init
git submodule update --depth 1 --recursive
```

#### 2. Bind-Mount the Frontend Into the Container

Update your Docker Compose service to include:

```yaml
    volumes:
      - type: bind
        source: /path/to/frontend
        target: /opt/frontend
```

#### 3. Rebuild the container
```bash
docker compose up -d
```

#### 4. Build the Frontend (Inside the Container)

```bash
docker compose exec --user default --workdir /opt/frontend steam-headless bash
```

Then build the project:
```bash
./utils/build.sh
```

Run in Dev Mode:
```bash
./utils/run-dev.sh 
```
This will stop the containers web service and start the development version


### 🚀 Vue development

You can develop just the Vue component inside this container also.
Just `cd` to the `./shui2/shui-vue/` directory and run:
```bash
npm run dev
```

> [!WARNING]  
> You will need to also be running the `./utils/run-dev.sh` script for this to work.
> You may need to open 2 terminals.
