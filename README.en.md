# ✅ Jetson Exporter

[**English**](README.en.md) | [**한국어**](README.md)

> A Prometheus Exporter for monitoring GPU resource usage on NVIDIA Jetson devices.

**Jetson Exporter** is an extension of the [k8s dashboard](https://github.com/jiiihwan/k8s-dashboard) and is based on [jetson-stats-grafana-dashboard](https://github.com/svcavallar/jetson-stats-grafana-dashboard). It has been designed to run as a **Kubernetes Pod** rather than a Linux systemd service.

For building the image from source, please refer to the [**Build Guide (BUILD.en.md)**](BUILD.en.md).

---

## 📖 Introduction

**This exporter** collects system metrics (GPU, CPU, Memory, Temperature, etc.) from NVIDIA Jetson devices and exports them to Prometheus.

### How it Works
1.  **jtop (jetson-stats)**: Uses the [jtop](https://github.com/rbonghi/jetson_stats) library to read real-time hardware status from the Jetson device.
2.  **Prometheus Client**: Uses Python's `prometheus_client` to convert data into metrics and exposes them via an HTTP server (default port 9101).
3.  **DaemonSet**: Deployed as a Pod on every Jetson node (`device=jetson` label) in the Kubernetes cluster to collect metrics from each node.

### Collected Metrics
- **GPU**: Usage (`jetson_gpu_usage`), Frequency (`jetson_gpu_freq`), Memory Usage (`jetson_gpu_memory`)
- **CPU**: Frequency and Idle stats per core (`jetson_cpu`)
- **Memory**: RAM usage, buffers, cache (`jetson_ram`)
- **Temperature**: Temperature by component (`jetson_temperature`)

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

### 3. Deploy Resources

> **Prerequisites**
> This project assumes that the monitoring stack (Prometheus Operator, Grafana) from **[k8s-dashboard](https://github.com/jiiihwan/k8s-dashboard)** is already installed.
> If not, please follow the guide in that repository first.

Choose one of the following methods to deploy.

#### **[Option A] Install via Helm Chart (Recommended)**
This is the easiest way if Helm is installed.

```bash
# 1. Add Helm Repo
helm repo add jetson-exporter https://jiiihwan.github.io/jetson_exporter
helm repo update

# 2. Verify Namespace (uses 'monitoring' namespace from k8s-dashboard)
kubectl get ns monitoring

# 3. Install Helm Chart (Release name: jetson-exporter)
helm install jetson-exporter jetson-exporter/jetson-exporter -n monitoring
```

> **Note**: To install from local source, use `cd helm/jetson-exporter && helm install jetson-exporter . -n monitoring`.

#### **[Option B] Install via Kubectl**
Applying Kubernetes manifest (`yaml`) files directly.

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
