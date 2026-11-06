#!/usr/bin/env python3
"""Seed synthetic metrics into the test stack's Prometheus (grafanacloud-prom).

Why: drilldown-metrics-lj and interactive-dashboards-lj expect node_cpu_* metrics and an
`up` series with environment/cluster/region labels. The stack's own Prometheus is empty.

How: Influx line protocol over HTTPS to Grafana Cloud's Influx endpoint (plain text, no
extra dependencies). Metric name = measurement + "_" + field, except field "value",
which keeps the bare measurement name (so `up value=1` becomes `up`).

Safe by default: prints what it would send and sends nothing. Pass --send to write.
Samples only stay queryable for a short recent window, so rerun right before each test.

  python3 test-stack/scripts/seed-metrics.py                  # dry run, prints a sample
  python3 test-stack/scripts/seed-metrics.py --send           # write the last 10 minutes
  python3 test-stack/scripts/seed-metrics.py --send --keep 30 # keep writing for 30 minutes

Credentials (never in the repo): ~/.config/grafana-docsteam-metrics.env with
  METRICS_USER=<Prometheus instance id>      (3694997 for this stack; not a secret)
  METRICS_TOKEN=<access policy token with metrics:write>
"""
import argparse, math, os, sys, time, urllib.request, urllib.error, base64

ENDPOINT = "https://prometheus-prod-05-gb-south-0.grafana.net/api/v1/push/influx/write"
ENV_FILE = os.path.expanduser("~/.config/grafana-docsteam-metrics.env")
STEP = 30  # seconds between samples

# environment, cluster, region, instances
TOPOLOGY = [
    ("production", "prod-us-1", "us-east", ["node-1", "node-2"]),
    ("production", "prod-eu-1", "eu-west", ["node-3", "node-4"]),
    ("staging", "stg-us-1", "us-east", ["node-5"]),
    ("development", "dev-eu-1", "eu-west", ["node-6"]),
]
CPUS = ["0", "1"]
MODES = ["idle", "user", "system", "iowait"]


def esc(v):
    return str(v).replace(",", r"\,").replace(" ", r"\ ").replace("=", r"\=")


def line(measurement, tags, field, value, ts_ns):
    t = ",".join(f"{esc(k)}={esc(v)}" for k, v in sorted(tags.items()))
    return f"{measurement},{t} {field}={value} {ts_ns}"


def samples(ts):
    """All lines for one timestamp `ts` (seconds)."""
    ns = int(ts * 1e9)
    out = []
    for env, cluster, region, instances in TOPOLOGY:
        base = {"environment": env, "cluster": cluster, "region": region, "job": "node"}
        for inst in instances:
            seed = sum(ord(c) for c in inst)
            wave = 0.5 + 0.4 * math.sin(seed)  # constant per instance so counters never decrease
            t = dict(base, instance=inst)
            out.append(line("up", t, "value", 1, ns))
            out.append(line("node_cpu_online", dict(t, cpu="0"), "value", 1, ns))
            out.append(line("node_cpu_hourly_cost", t, "value", round(0.0416 * (1 + seed % 3), 4), ns))
            for cpu in CPUS:
                for mode in MODES:
                    share = {"idle": 1 - wave, "user": wave * 0.6, "system": wave * 0.3, "iowait": wave * 0.1}[mode]
                    counter = round(ts * share / 4.0, 3)  # monotonically increasing counter
                    tt = dict(t, cpu=cpu, mode=mode)
                    out.append(line("node_cpu", tt, "seconds_total", counter, ns))
                out.append(line("node_cpu", dict(t, cpu=cpu), "guest_seconds_total", 0, ns))
                out.append(line("node_cpu", dict(t, cpu=cpu), "usage_seconds_total", round(ts * wave / 4.0, 3), ns))
            for method, status in [("GET", "200"), ("POST", "201"), ("GET", "500")]:
                n = round(ts * (0.2 if status != "500" else 0.01) * (1 + seed % 4), 3)
                out.append(line("http", dict(t, method=method, status=status), "requests_total", n, ns))
            out.append(line("node_memory", t, "MemAvailable_bytes", int(4e9 * (1 - wave * 0.5)), ns))
            out.append(line("node_filesystem", dict(t, mountpoint="/"), "avail_bytes", int(2e10 * (1 - wave * 0.1)), ns))
    return out


def load_creds():
    if not os.path.exists(ENV_FILE):
        sys.exit(f"Missing {ENV_FILE}. Create it first (see the docstring). Nothing was sent.")
    env = {}
    for raw in open(ENV_FILE):
        if "=" in raw and not raw.strip().startswith("#"):
            k, v = raw.strip().split("=", 1)
            env[k] = v
    for k in ("METRICS_USER", "METRICS_TOKEN"):
        if not env.get(k):
            sys.exit(f"{k} missing in {ENV_FILE}. Nothing was sent.")
    return env["METRICS_USER"], env["METRICS_TOKEN"]


def send(body, user, token):
    req = urllib.request.Request(ENDPOINT, data=body.encode(), method="POST")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{token}".encode()).decode())
    req.add_header("Content-Type", "text/plain")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:200]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="actually write (default is a dry run)")
    ap.add_argument("--backfill", type=int, default=10, help="minutes of recent history to write first")
    ap.add_argument("--keep", type=int, default=0, help="then keep writing for this many minutes")
    a = ap.parse_args()

    now = time.time()
    stamps = [now - m * 60 + 0 for m in range(a.backfill, 0, -1)]
    stamps = [now - (a.backfill * 60) + i * STEP for i in range(int(a.backfill * 60 / STEP) + 1)]
    lines = [l for ts in stamps for l in samples(ts)]
    series = len({l.rsplit(" ", 2)[0] + l.split(" ")[1].split("=")[0] for l in lines[: len(samples(now))]})
    print(f"{len(samples(now))} samples per step, {len(stamps)} steps, ~{series} series, {len(lines)} lines")
    if not a.send:
        print("DRY RUN. Sample lines:")
        for l in samples(now)[:6]:
            print("  " + l)
        print("Nothing sent. Use --send to write.")
        return
    user, token = load_creds()
    for i in range(0, len(lines), 5000):
        print("sent chunk", i // 5000 + 1, "->", send("\n".join(lines[i:i + 5000]), user, token))
    end = time.time() + a.keep * 60
    while time.time() < end:
        time.sleep(STEP)
        print("sent live ->", send("\n".join(samples(time.time())), user, token))


if __name__ == "__main__":
    main()
