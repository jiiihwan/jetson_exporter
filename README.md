# ✅ Jetson Exporter

[**English**](README.en.md) | [**한국어**](README.md)

> Jetson Orin Nano와 같은 Jetson 장치에서 GPU/NPU 리소스 사용량을 모니터링하기 위한 Prometheus Exporter입니다.

이 프로젝트는 [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard)의 확장 기능으로, [jetson-stats-grafana-dashboard](https://github.com/svcavallar/jetson-stats-grafana-dashboard)를 기반으로 합니다. 기존의 Linux 서비스 방식이 아닌 **Kubernetes Pod** 형태로 실행되도록 개선되었습니다.

직접 이미지를 빌드하려면 [**빌드 가이드 (BUILD.md)**](BUILD.md)를 참고하세요.

---

## 📦 설치 및 배포 (Installation & Deployment)

### 1. 레포지토리 클론
마스터 노드에서 다음 명령어를 실행합니다.

```bash
git clone https://github.com/jiiihwan/jetson_exporter
cd jetson_exporter
```

### 2. 노드 라벨링 (Node Labeling)
Jetson Exporter는 `device=jetson` 라벨이 붙은 노드에만 배포됩니다.

```bash
# 노드 목록 확인
kubectl get nodes --show-labels

# 라벨 추가 (워커 노드 이름이 jetson-node인 경우)
kubectl label nodes [jetson-node-name] device=jetson
```

### 3. 리소스 적용 (Apply Resources)
DaemonSet, Service, ServiceMonitor를 배포합니다.

```bash
# DaemonSet 배포
kubectl apply -f k8s_resources/jetson-exporter-daemonset.yaml

# Service & ServiceMonitor 배포 (모니터링 네임스페이스)
kubectl apply -f k8s_resources/jetson-exporter-service.yaml -n monitoring
kubectl apply -f k8s_resources/jetson-exporter-servicemonitor.yaml -n monitoring
```

> **참고**: `k8s_resources` 디렉토리 내의 파일들을 사용합니다.

---

## 📂 Kubernetes 리소스 구조

| 리소스 | 라벨 (Label) | 역할 |
|:---:|---|---|
| **Pod (DaemonSet)** | `app: jetson-exporter` | `device=jetson` 라벨이 있는 노드에 Pod 생성 |
| **Service** | `app: jetson-exporter`<br>`release: prometheus` | Pod와 연결하여 메트릭 노출 |
| **ServiceMonitor** | `release: prometheus` | Prometheus가 Service를 발견하도록 연결 |
