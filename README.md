# ✅ jetson_exporter
> A Prometheus exporter for monitoring resource(GPU) usage on Jetson Orin Nano

- This project is extension of [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard)
- based on https://github.com/svcavallar/jetson-stats-grafana-dashboard
- linux service가 아닌 k8s의 pod로 띄울 수 있게 개선

## 🔨 0. jetson-exporter 바로 설치
직접 제작하는 방법을 따라하고 싶다면 1. Dockerfile 작성부터 따라하기
그렇지 않다면 아래에 있는 과정만 하면 된다

### git clone
마스터노드에서 입력
```bash
git clone https://github.com/jiiihwan/jetson_exporter
```

### 모두 적용

```bash
kubectl apply -f jetson-exporter-daemonset.yaml
kubectl apply -f jetson-exporter-service.yaml -n monitoring
kubectl apply -f jetson-exporter-servicemonitor.yaml -n monitoring
```

---


## 📄 1. Dockerfile 작성
```bash
vim Dockerfile
```

[Dockerfile](Dockerfile) 참고

## 🔨 2. nerdctl 및 buildkit 설치
이미지 build를 위해 보통 docker를 사용하지만 컨테이너 런타임을 containerd로 사용하고 있으므로 nerdctl과 buildkit을 사용한다

### 2.1. nerdctl 파일용 폴더 생성
```bash
mkdir nerdctl
cd nerdctl
```

### 2.2. nerdctl 설치
만약 오류나면 latest가 아닌 다른 버전으로 시도해 볼 것.
현재 시스템에서는 2.0.4 를 사용했다

또한 본인이 설치하고자 하는 기기의 os에 따라서 arm64, amd64용 압축파일을 선택해서 명령어를 입력해야하니 주의 할 것

```bash
curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
| grep "browser_download_url.*linux-arm64.tar.gz" \
| cut -d '"' -f 4 \
| wget -i -
```
### 2.3. 압축해제
```
tar xzvf nerdctl-full-2.0.4-linux-arm64.tar.gz
```

### 2.4. buildkit 포함 nerdctl 설치
```bash
sudo cp bin/nerdctl /usr/local/bin/
sudo cp bin/buildctl /usr/local/bin/
sudo cp bin/buildkitd /usr/local/bin/
```
### 2.5. 버전 확인
```
nerdctl --version
```

## 🐋 3. 이미지 build & push

### 3.1. buildkitd 실행
```
sudo nohup buildkitd > /dev/null 2>&1 &
```

### 3.2. l4t basefile 을 위해서 ngc회원가입 및 로그인
api키 발급(https://org.ngc.nvidia.com/setup/api-keys)
```bash
nerdctl login nvcr.io
Enter Username: $oauthtoken
Enter Password: <APIKEY>
```

### 3.3. dockerfile 빌드
직접 빌드를 한다면 build 명령어의 본인의 도커허브 레포지토리를 쓰면 된다.

```bash
cd ~/jetson_stats_node_exporter
nerdctl build -t <your_dockerhub> .
```
### 3.4. Dockerhub에 푸시

Dockerhub 회원가입 필요
```
nerdctl push <your_dockerhub>
```

## 🏷️ 4. 노드 라벨링
jetson orin nano에 `device=jetson` 이라는 라벨링 추가

이 라벨링을 통해서 daemonset이 jetson 종류의 기기에만 jetson-exporter를 배포한다
  
```
kubectl get nodes --show-labels
kubectl label nodes [node_name] device=jetson
```

## 🔋 5. k8s resource 파일 작성
### 동작 방식
- 라벨을 이용해서 daemonset, service, service monitor가 target을 찾을 수 있게 한다

| 리소스              | 라벨                                     | 라벨 용도                             |
|---------------------|--------------------------------------------------|----------------------------------------|
| `Pod` (DaemonSet)   | `app: jetson-exporter`                            | Service가 Pod 선택하는 기준           |
| `Service`           | `app: jetson-exporter`, `release: prometheus`     | ServiceMonitor가 Service 찾는 기준    |
| `ServiceMonitor`    | `release: prometheus`                            | Prometheus가 ServiceMonitor 찾는 기준 |

### 📤 5.1. Daemonset 작성 및 배포
- 마스터노드에서 작성
- 포트는 metrics-server가 기본적으로 9100포트를 사용하고 있으므로 9101포트를 사용하도록 한다

```bash
vim jetson-exporter-daemonset.yaml
```

[jetson-exporter-daemonset.yaml](https://github.com/jiiihwan/jetson_exporter/blob/main/jetson-exporter-daemonset.yaml) 참고

```bash
kubectl apply -f jetson-exporter-daemonset.yaml
kubectl get pods -n monitoring -o wide

#restart 할때
kubectl rollout restart daemonset jetson-exporter -n monitoring
```

### 🖥️ 5.2. 서비스 & 서비스모니터 설정
```bash
vim jetson-exporter-service.yaml
```

[jetson-exporter-service.yaml](https://github.com/jiiihwan/jetson_exporter/blob/main/jetson-exporter-service.yaml) 참고

```bash
vim jetson-exporter-servicemonitor.yaml
```

[jetson-exporter-servicemonitor.yaml](https://github.com/jiiihwan/jetson_exporter/blob/main/jetson-exporter-servicemonitor.yaml) 참고

```bash
kubectl apply -f jetson-exporter-service.yaml -n monitoring
kubectl apply -f jetson-exporter-servicemonitor.yaml -n monitoring
```

## 🔧 tip) Jetson Orin Nano 에서 node-exporter 작동 안하는 문제
[problem_solving.md](https://github.com/jiiihwan/jetson_exporter/blob/main/problem_solving.md) 참고
