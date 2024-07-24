FROM python:3.11.9-slim

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libxrender1 \
    libxext6 \
    libxtst6 \
    && apt-get clean

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

# Assumes the workload and PresentMon file names are workload.exe and PresentMon64.exe`
CMD ["python", "-m", "automation.cli", "--presentmon", "PresentMon64.exe", "--workload", "workload.exe"]
