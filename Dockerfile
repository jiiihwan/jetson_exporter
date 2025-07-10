#참고로 여기 버전은 홈페이지에서 잘 보고 적어야함
#https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-base
FROM nvcr.io/nvidia/l4t-base:r36.2.0

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /opt/jetson_exporter

# 필수 패키지 설치
RUN apt-get update && apt-get install -y python3-pip curl

# requirements.txt 복사 + 설치
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# jetson_exporter 전체 복사
COPY jetson_exporter.py .

# Prometheus가 수집할 포트 열기
EXPOSE 9101

# 실행 엔트리포인트
ENTRYPOINT ["python3", "jetson_exporter.py", "--port=9101"]
