import argparse
from time import sleep
from jtop import jtop
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily


class JetsonExporter:
    def __init__(self, update_period=1.0):
        if update_period < 0.5:
            print("[Warning] update_period too low. Falling back to 1.0s.")
            update_period = 1.0
        self.interval = update_period
        self.jtop = jtop(interval=self.interval)
        self.jtop.start()
        self.jtop_stats = {}

    def update(self):
        self.jtop_stats = {
            "stats": self.jtop.stats,
            "cpu": self.jtop.cpu,
            "mem": self.jtop.memory,
            "gpu": self.jtop.gpu,
            "tmp": self.jtop.temperature
        }

    def cpu(self):
        gauge = GaugeMetricFamily(
            name="jetson_cpu",
            documentation="CPU frequency and idle statistics per core",
            labels=["core", "statistic"],
            unit="Hz"
        )
        for core_num, core_data in enumerate(self.jtop_stats["cpu"]["cpu"]):
            gauge.add_metric([str(core_num), "freq"], core_data["freq"]["cur"])
            gauge.add_metric([str(core_num), "min_freq"], core_data["freq"]["min"])
            gauge.add_metric([str(core_num), "max_freq"], core_data["freq"]["max"])
            gauge.add_metric([str(core_num), "val"], core_data["idle"])
        return gauge

    def gpu(self):
        gauge = GaugeMetricFamily(
            name="jetson_gpu_freq",
            documentation="GPU frequency statistics",
            labels=["statistic", "nvidia_gpu"],
            unit="Hz"
        )
        for name, data in self.jtop_stats["gpu"].items():
            gauge.add_metric([name, "freq"], data["freq"]["cur"])
            gauge.add_metric([name, "min_freq"], data["freq"]["min"])
            gauge.add_metric([name, "max_freq"], data["freq"]["max"])
        return gauge

    def gpu_usage(self):
        gauge = GaugeMetricFamily(
            name="jetson_gpu_usage",
            documentation="GPU usage percentage",
            labels=["statistic", "nvidia_gpu"],
            unit="percent"
        )
        for name, data in self.jtop_stats["gpu"].items():
            gauge.add_metric([name, "usage"], data["status"]["load"])
        return gauge

    def gpuram(self):
        gauge = GaugeMetricFamily(
            name="jetson_gpu_memory",
            documentation="Shared GPU memory usage",
            labels=["statistic", "nvidia_gpu"],
            unit="kB"
        )
        for name in self.jtop_stats["gpu"].keys():
            gauge.add_metric([name, "mem"], self.jtop_stats["mem"]["RAM"]["shared"])
        return gauge

    def ram(self):
        gauge = GaugeMetricFamily(
            name="jetson_ram",
            documentation="System RAM statistics",
            labels=["statistic"],
            unit="kB"
        )
        ram = self.jtop_stats["mem"]["RAM"]
        gauge.add_metric(["total"], ram["tot"])
        for key in ["used", "buffers", "cached", "lfb", "free"]:
            if key in ram:
                gauge.add_metric([key], ram[key])
        return gauge

    def temperature(self):
        gauge = GaugeMetricFamily(
            name="jetson_temperature",
            documentation="Temperature by machine component",
            labels=["machine_part"],
            unit="Celsius"
        )
        for part, temp in self.jtop_stats["tmp"].items():
            gauge.add_metric([part], temp["temp"])
        return gauge

    def collect(self):
        self.update()
        yield self.cpu()
        yield self.gpu()
        yield self.gpu_usage()
        yield self.gpuram()
        yield self.ram()
        yield self.temperature()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=9101, help='Metrics collector port number')
    parser.add_argument('--update_period', type=float, default=1.0, help='Data update interval in seconds (must be greater than 0.5)')
    args = parser.parse_args()

    start_http_server(args.port)
    REGISTRY.register(JetsonExporter(args.update_period))

    while True:
        sleep(1)
