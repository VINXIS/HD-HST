# HD-HST
High-Duration Hardware Stress Tester. A tool that conducts long duration stress tests on hardware.

## Installation
1. Clone the repository

```bash
git clone https://github.com/VINXIS/HD-HST
```

2. Install the required packages

```bash
pip install -r requirements.txt
```

## Usage
1. Run the script

```bash
python -m automation.cli [--presentmon PRESENTMON FILE/PATH] [--workload WORKLOAD FILE/PATH]
```

2. The script will start running the stress test. The script will run for 70 hours.