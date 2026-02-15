# 🔧 Troubleshooting: Node Exporter Collection Issue

[**English**](problem_solving.en.md) | [**한국어**](problem_solving.md)

## 🔴 Issue

- **Environment**:
    - Master Node: General Server (Working Fine)
    - Worker Node: **Jetson Orin Nano**
- **Symptoms**:
    - Node Exporter on the Master Node is scraping correctly by Prometheus.
    - **Node Exporter on the Worker Node (Jetson Orin Nano) is NOT being scraped.**
- **Log Analysis**:
    - Error logs indicating files are too large when collecting `cpu frequency`.
    - Disabling `cpufreq` collection in DaemonSet configuration did not resolve the issue.
- **Root Cause**:
    - Identified similar cases in [Github Issue](https://github.com/prometheus/node_exporter/issues/3071).
    - The issue is caused by the **`thermal_zone`** metric collection on Jetson devices.

---

## 🟢 Solution

Disable `thermal_zone` collection in the Node Exporter DaemonSet configuration.

### 1. Edit DaemonSet
Run the following command to edit the `prometheus-node-exporter` DaemonSet.

```bash
kubectl edit daemonset prometheus-prometheus-node-exporter -n monitoring
```
*(Note: DaemonSet name may vary depending on your deployment. Check with `kubectl get ds -n monitoring`.)*

### 2. Modify Args
Add the `--no-collector.thermal_zone` option to the `args` section under `containers`.

```yaml
spec:
  containers:
  - name: node-exporter
    args:
      - --path.procfs=/host/proc
      - --path.sysfs=/host/sys
      - --path.rootfs=/host/root
      - --no-collector.thermal_zone  #  <-- Add this line
```

### 3. Save and Apply
Save and close the file (e.g., `:wq` in vi). The DaemonSet will automatically restart with the new configuration. Check Prometheus to ensure metrics from the worker node are now being scraped.
