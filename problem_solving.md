# 🔧 트러블슈팅: Node Exporter 수집 문제

[**English**](problem_solving.en.md) | [**한국어**](problem_solving.md)

## 🔴 문제 상황 (Issue)

- **환경**: 
    - Master Node: 일반 서버 (정상 동작)
    - Worker Node: **Jetson Orin Nano**
- **증상**: 
    - 마스터 노드의 Node Exporter는 Prometheus에서 정상적으로 수집됨.
    - **워커 노드(Jetson Orin Nano)의 Node Exporter는 수집되지 않음.**
- **로그 분석**:
    - `cpu frequency` 수집 시 파일이 너무 크다는 에러 로그 발생.
    - 데몬셋 설정에서 `cpufreq` 수집을 비활성화했으나 해결되지 않음.
- **원인 파악**:
    - [Github Issue](https://github.com/prometheus/node_exporter/issues/3071)에서 유사 사례 확인.
    - **`thermal_zone`** 메트릭 수집 과정에서 문제가 발생하는 것으로 확인됨.

---

## 🟢 해결 방법 (Solution)

Node Exporter의 DaemonSet 설정에서 `thermal_zone` 수집을 비활성화해야 합니다.

### 1. DaemonSet 편집
다음 명령어를 실행하여 `prometheus-node-exporter` 데몬셋을 수정합니다.

```bash
kubectl edit daemonset prometheus-prometheus-node-exporter -n monitoring
```
*(배포 환경에 따라 데몬셋 이름이 다를 수 있습니다. `kubectl get ds -n monitoring`으로 확인하세요.)*

### 2. Args 수정
`containers` 섹션의 `args`에 `--no-collector.thermal_zone` 옵션을 추가합니다.

```yaml
spec:
  containers:
  - name: node-exporter
    args:
      - --path.procfs=/host/proc
      - --path.sysfs=/host/sys
      - --path.rootfs=/host/root
      - --no-collector.thermal_zone  #  <-- 이 줄을 추가하세요
```

### 3. 저장 및 적용
파일을 저장하고 닫으면(vi 기준 `:wq`) DaemonSet이 자동으로 재시작되며 설정이 적용됩니다. 이후 Prometheus에서 워커 노드의 메트릭이 정상적으로 수집되는지 확인하세요.
