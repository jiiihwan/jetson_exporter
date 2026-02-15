# 🔨 Jetson Exporter Build Guide

[**English**](BUILD.en.md) | [**한국어**](BUILD.md)

Follow this guide if you want to build and modify the image yourself.

---

## 📂 Dockerfile Location

The Dockerfile is located in the `jetson_exporter/` directory.

```bash
cd jetson_exporter
# Check and edit Dockerfile
vi Dockerfile
```

---

## 🛠️ Install Nerdctl & Buildkit (Jetson)

If you are using `containerd` as the runtime on Jetson, you need `nerdctl` and `buildkit`.

<details>
<summary>👉 See How to Install Nerdctl (Click)</summary>

1. **Create folder and move**
   ```bash
   mkdir nerdctl && cd nerdctl
   ```

2. **Download Nerdctl (arm64)**
   ```bash
   curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
   | grep "browser_download_url.*linux-arm64.tar.gz" \
   | cut -d '"' -f 4 \
   | wget -i -
   ```

3. **Extract and Install**
   ```bash
   tar xzvf nerdctl-full-*-linux-arm64.tar.gz
   sudo cp bin/nerdctl /usr/local/bin/
   sudo cp bin/buildctl /usr/local/bin/
   sudo cp bin/buildkitd /usr/local/bin/
   ```

4. **Check Version**
   ```bash
   nerdctl --version
   ```
</details>

---

## 🐋 Build & Push Image

Build the image using Nerdctl and push it to DockerHub.

```bash
# Run Buildkit (Background)
sudo nohup buildkitd > /dev/null 2>&1 &

# Login to NGC (Required for NVIDIA L4T base image)
nerdctl login nvcr.io

# Login to DockerHub
nerdctl login

# Build Image
nerdctl build -t <your_dockerhub_id>/jetson-exporter:latest .

# Push Image
nerdctl push <your_dockerhub_id>/jetson-exporter:latest
```
