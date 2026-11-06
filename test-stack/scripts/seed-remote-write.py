#!/usr/bin/env python3
"""Seed series whose names Influx ingestion cannot carry (colons) via Prometheus remote write.

Why: drilldown-metrics-lj milestone 2 highlights the Select button for the metric
`asserts:resource:threshold`. Influx line protocol rewrites colons to underscores, so
seed-metrics.py cannot create it. Remote write keeps metric names as given.

How: Prometheus remote write v1 = protobuf WriteRequest, snappy-compressed, POSTed with
Basic auth. Stdlib only: the protobuf is hand-encoded and the snappy payload uses
uncompressed literal blocks, which is valid snappy.

Safe by default: dry run encodes and self-checks the payload but sends nothing.
Pass --send to write. Samples only stay queryable for a short recent window, so rerun
right before each test.

  python3 test-stack/scripts/seed-remote-write.py          # dry run
  python3 test-stack/scripts/seed-remote-write.py --send   # write the last 10 minutes

Credentials: same file as seed-metrics.py (~/.config/grafana-docsteam-metrics.env).
"""
import argparse, base64, struct, sys, time, urllib.request, urllib.error, importlib.util, os

ENDPOINT = "https://prometheus-prod-05-gb-south-0.grafana.net/api/prom/push"
STEP = 30  # seconds between samples

# metric name -> list of (labels, value)
THRESHOLD = "asserts:resource:threshold"
SERIES = []
for rtype, level, value in [
    ("cpu:usage", "warning", 70), ("cpu:usage", "critical", 90),
    ("memory:usage", "warning", 75), ("memory:usage", "critical", 90),
]:
    SERIES.append((
        {"__name__": THRESHOLD, "job": "node", "asserts_env": "production", "asserts_site": "us-east",
         "asserts_resource_type": rtype, "asserts_threshold_level": level},
        float(value),
    ))


# --- protobuf (just the fields remote write needs) ---
def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def ld(field, payload):  # length-delimited field
    return varint((field << 3) | 2) + varint(len(payload)) + payload


def label(name, value):
    return ld(1, name.encode()) + ld(2, value.encode())


def sample(value, ts_ms):
    return varint((1 << 3) | 1) + struct.pack("<d", value) + varint((2 << 3) | 0) + varint(ts_ms)


def timeseries(labels, samples):
    body = b"".join(ld(1, label(k, v)) for k, v in sorted(labels.items()))
    body += b"".join(ld(2, sample(v, t)) for v, t in samples)
    return body


def write_request(series_with_samples):
    return b"".join(ld(1, timeseries(l, s)) for l, s in series_with_samples)


# --- snappy raw block, literals only ---
def snappy_literals(data):
    out = bytearray(varint(len(data)))
    i = 0
    while i < len(data):
        chunk = data[i:i + 65536]
        n = len(chunk) - 1
        if n < 60:
            out.append(n << 2)
        elif n < 256:
            out += bytes([60 << 2, n])
        else:
            out += bytes([61 << 2]) + struct.pack("<H", n)
        out += chunk
        i += len(chunk)
    return bytes(out)


def snappy_decode_literals(buf):  # self-check only
    n, shift, i = 0, 0, 0
    while True:
        b = buf[i]; i += 1
        n |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            break
    out = bytearray()
    while i < len(buf):
        tag = buf[i]; i += 1
        assert tag & 3 == 0, "non-literal element"
        ln = tag >> 2
        if ln < 60:
            ln += 1
        elif ln == 60:
            ln = buf[i] + 1; i += 1
        else:
            ln = struct.unpack("<H", buf[i:i + 2])[0] + 1; i += 2
        out += buf[i:i + ln]; i += ln
    assert len(out) == n
    return bytes(out)


def build(now):
    count = int(10 * 60 / STEP) + 1
    stamps = [int((now - 10 * 60 + i * STEP) * 1000) for i in range(count)]
    return [(lbls, [(val, t) for t in stamps]) for lbls, val in SERIES], count


def load_creds():
    spec = importlib.util.spec_from_file_location("seed", os.path.join(os.path.dirname(__file__), "seed-metrics.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.load_creds()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="actually write (default is a dry run)")
    a = ap.parse_args()

    payload, steps = build(time.time())
    raw = write_request(payload)
    body = snappy_literals(raw)
    assert snappy_decode_literals(body) == raw, "snappy self-check failed"
    print(f"{len(payload)} series, {steps} samples each, {len(raw)} bytes protobuf, {len(body)} bytes snappy")
    for l, _ in payload:
        print("  " + l["__name__"] + "{" + ",".join(f'{k}="{v}"' for k, v in sorted(l.items()) if k != "__name__") + "}")
    if not a.send:
        print("DRY RUN. Nothing sent. Use --send to write.")
        return
    user, token = load_creds()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{token}".encode()).decode())
    req.add_header("Content-Type", "application/x-protobuf")
    req.add_header("Content-Encoding", "snappy")
    req.add_header("X-Prometheus-Remote-Write-Version", "0.1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("sent ->", r.status)
    except urllib.error.HTTPError as e:
        print(f"sent -> HTTP {e.code}: {e.read().decode()[:200]}")


if __name__ == "__main__":
    main()
