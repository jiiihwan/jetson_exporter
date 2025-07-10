# jetson_exporter
A Prometheus exporter for monitoring resource(GPU) usage on Jetson Orin Nano

# 🛠️ jetson stats exporter설치
- based on 
- linux service가 아닌 k8s의 pod로 띄울 수 있게 변형했다

## 🔨 0. jetson-exporter 바로 설치
직접 제작하는 방법을 따라하고 싶다면 Dockerfile 작성부터 따라하기
그렇지 않다면 아래에 있는 과정만 하면 된다

### git clone
```bash
git clone https://github.com/jiiihwan/k8s-dashboard/tree/main/exporter
```

### 모두 적용
```bash
kubectl apply -f jetson-exporter-daemonset.yaml
kubectl apply -f jetson-exporter-service.yaml -n monitoring
kubectl apply -f jetson-exporter-servicemonitor.yaml -n monitoring
```


## 📄 1. Dockerfile 작성
```bash
vim Dockerfile
```

[Dockerfile](Dockerfile) 참고

## 🔨 2. nerdctl 및 buildkit 설치
이미지 build를 위해 보통 docker를 사용하지만 컨테이너 런타임을 containerd로 사용하고 있으므로 nerdctl과 buildkit을 사용한다

### nerdctl 파일용 폴더 생성
```bash
mkdir nerdctl
cd nerdctl
```

### nerdctl 설치
```bash
curl -s https://api.github.com/repos/containerd/nerdctl/releases/latest \
| grep "browser_download_url.*linux-arm64.tar.gz" \
| cut -d '"' -f 4 \
| wget -i -
```
### 압축해제
```
tar xzvf nerdctl-full-2.0.4-linux-arm64.tar.gz
```

### buildkit 포함 nerdctl 설치
```bash
sudo cp bin/nerdctl /usr/local/bin/
sudo cp bin/buildctl /usr/local/bin/
sudo cp bin/buildkitd /usr/local/bin/
```
### 버전 확인
```
nerdctl --version
```

## 🐋 3. 이미지 build & push

### buildkitd 실행
```
sudo nohup buildkitd > /dev/null 2>&1 &
```

### l4t basefile 을 위해서 ngc회원가입 및 로그인
api키 발급(https://org.ngc.nvidia.com/setup/api-keys)
```bash
nerdctl login nvcr.io
Enter Username: $oauthtoken
Enter Password: <APIKEY>
```

### dockerfile 빌드
직접 빌드를 한다면 build 명령어의 본인의 도커허브 레포지토리를 쓰면 된다.

```bash
cd ~/jetson_stats_node_exporter
nerdctl build -t yjh2353693/jetson-exporter:latest .
```
### Dockerhub에 푸시

Dockerhub 회원가입 필요
```
nerdctl push yjh2353693/jetson-exporter:latest
```

## 🏷️ 4. 노드 라벨링
jetson orin nano에 device=jetson 이라는 라벨링 추가

이 라벨링을 통해서 daemonset이 jetson 종류의 기기에만 jetson-exporter를 배포한다
  
```
kubectl get nodes --show-labels
kubectl label nodes [node_name] device=jetson
```

## 📤 5. Daemonset 작성 및 배포
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

## 🖥️ 6. 서비스 & 서비스모니터 설정
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
