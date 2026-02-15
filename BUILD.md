# 🔨 Jetson Exporter 빌드 가이드

[**English**](BUILD.en.md) | [**한국어**](BUILD.md)

이미지를 직접 빌드하고 수정하고 싶다면 아래 가이드를 따르세요.

---

## 📂 Dockerfile 위치

Dockerfile은 `jetson_exporter/` 디렉토리에 위치해 있습니다.

```bash
cd jetson_exporter
# Dockerfile 확인 및 수정
vi Dockerfile
```

---

## 🛠️ Nerdctl 및 Buildkit 설치 (Jetson)

Jetson 환경에서 `containerd`를 런타임으로 사용하는 경우 `nerdctl`과 `buildkit`이 필요합니다.

<details>
<summary>👉 Nerdctl 설치 방법 보기 (클릭)</summary>

1. **폴더 생성 및 이동**
   ```bash
   mkdir nerdctl && cd nerdctl
   ```

2. **Nerdctl 다운로드 (arm64)**
   ```bash
   curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
   | grep "browser_download_url.*linux-arm64.tar.gz" \
   | cut -d '"' -f 4 \
   | wget -i -
   ```

3. **압축 해제 및 설치**
   ```bash
   tar xzvf nerdctl-full-*-linux-arm64.tar.gz
   sudo cp bin/nerdctl /usr/local/bin/
   sudo cp bin/buildctl /usr/local/bin/
   sudo cp bin/buildkitd /usr/local/bin/
   ```

4. **버전 확인**
   ```bash
   nerdctl --version
   ```
</details>

---

## 🐋 이미지 빌드 및 푸시

Nerdctl을 사용하여 이미지를 빌드하고 DockerHub에 푸시합니다.

```bash
# Buildkit 실행 (백그라운드)
sudo nohup buildkitd > /dev/null 2>&1 &

# NGC 로그인 (NVIDIA L4T 베이스 이미지 사용 시 필요)
nerdctl login nvcr.io

# DockerHub 로그인
nerdctl login

# 이미지 빌드
nerdctl build -t <your_dockerhub_id>/jetson-exporter:latest .

# 이미지 푸시
nerdctl push <your_dockerhub_id>/jetson-exporter:latest
```
