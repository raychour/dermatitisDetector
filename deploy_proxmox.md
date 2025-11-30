# Deploying to Proxmox (x86 + NVIDIA GPU)

This guide explains how to deploy the Dermatitis Detector application on your Proxmox server (x86_64) with NVIDIA GPU support.

## Prerequisites

On your Proxmox host (or the VM/LXC container where you plan to run Docker):

1.  **Docker**: Ensure Docker is installed.
2.  **NVIDIA Drivers**: Ensure NVIDIA drivers for your RTX 2070 Super are installed.
3.  **NVIDIA Container Toolkit**: This is required to allow Docker containers to access the GPU.
    - Installation guide: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Deployment Steps

### 1. Transfer Files
Copy the project files to your server (e.g., via `scp` or `git clone`).

### 2. Build the Docker Image
Run the following command in the project directory:

```bash
docker build -t dermatitis-detector .
```

### 3. Run the Container
Run the container with GPU support enabled:

```bash
docker run -d \
  --name dermatitis-app \
  --gpus all \
  --security-opt seccomp=unconfined \
  -p 5000:5000 \
  --restart unless-stopped \
  dermatitis-detector
```

- `--gpus all`: Passes all available GPUs to the container.
- `--security-opt seccomp=unconfined`: Required on some Proxmox/LXC setups to allow socket creation.
- `-p 5000:5000`: Maps port 5000 on the host to port 5000 in the container.
- `--restart unless-stopped`: Automatically restarts the container if it crashes or the server reboots.

### 4. Verify Deployment
Check if the container is running:

```bash
docker ps
```

View logs to ensure the server started correctly:

```bash
docker logs dermatitis-app
```

You should see output indicating `Uvicorn running on http://0.0.0.0:5000`.

### 5. Access the App
Open your browser and navigate to:
`http://192.168.2.100:5000`

## Troubleshooting

### "could not select device driver" Error
If you see an error like `docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]].`, it means the NVIDIA Container Toolkit is not configured correctly.
Run `sudo nvidia-ctk runtime configure --runtime=docker` and restart Docker.

### Model Loading Issues
If the app starts but fails when you try to analyze an image, check the logs (`docker logs dermatitis-app`). If you see errors about "CPU-only machine" or model incompatibility, you might need to retrain your `export.pkl` model using FastAI v2 on a machine with a GPU (or use the updated notebook).
