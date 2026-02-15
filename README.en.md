# ✅ Jetson Exporter

[**English**](README.en.md) | [**한국어**](README.md)

> A Prometheus Exporter for monitoring GPU/NPU resource usage on Jetson devices.

This project is an extension of the [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard) and is based on [jetson-stats-grafana-dashboard](https://github.com/svcavallar/jetson-stats-grafana-dashboard). It has been designed to run as a **Kubernetes Pod** rather than a Linux service.

For building the image from source, please refer to the [**Build Guide (BUILD.en.md)**](BUILD.en.md).

---

## 📦 Installation & Deployment

### 1. Clone Repository
Run the following command on the Master Node:

```bash
git clone https://github.com/jiiihwan/jetson_exporter
cd jetson_exporter
```

### 2. Node Labeling
Jetson Exporter is deployed only to nodes with the `device=jetson` label.

```bash
# Check node list
kubectl get nodes --show-labels

# Add label (replace [jetson-node-name] with actual node name)
kubectl label nodes [jetson-node-name] device=jetson
```

### 3. Apply Resources
Deploy DaemonSet, Service, and ServiceMonitor.

```bash
# Deploy DaemonSet
kubectl apply -f k8s_resources/jetson-exporter-daemonset.yaml

# Deploy Service & ServiceMonitor (in monitoring namespace)
kubectl apply -f k8s_resources/jetson-exporter-service.yaml -n monitoring
kubectl apply -f k8s_resources/jetson-exporter-servicemonitor.yaml -n monitoring
```

> **Note**: Uses resources located in the `k8s_resources` directory.

---

## 📂 Kubernetes Resource Structure

| Resource | Label | Role |
|:---:|---|---|
| **Pod (DaemonSet)** | `app: jetson-exporter` | Creates Pods on nodes with `device=jetson` label |
| **Service** | `app: jetson-exporter`<br>`release: prometheus` | Exposes metrics by connecting to the Pod |
| **ServiceMonitor** | `release: prometheus` | Allows Prometheus to discover the Service |
