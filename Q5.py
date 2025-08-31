# realtime_pipeline.py —— Minimal local prototype for real-time pipeline
import queue, threading, time, random, hashlib

# Queues simulating Kafka topics
Q_ingest = queue.Queue(maxsize=10000)
Q_clean  = queue.Queue(maxsize=10000)

SEEN_KEYS = set()  # Idempotent sink (replace with external KV/DB in production)

def producer():
    """Simulate streaming ingestion of Reddit posts."""
    while True:
        post = {"id": random.randint(1, 1_000_000),
                "ts": time.time(),
                "text": "Hello Reddit"}
        Q_ingest.put(post)  # Backpressure: blocks if full
        time.sleep(0.005)   # ~200 msgs/sec

def cleaner():
    """Clean and normalize posts."""
    while True:
        x = Q_ingest.get()
        x["text"] = x["text"].lower().strip()
        Q_ingest.task_done()
        Q_clean.put(x)

def scorer():
    """Score posts (dummy sentiment score)."""
    while True:
        x = Q_clean.get()
        x["score"] = hashlib.md5(x["text"].encode()).digest()[0] / 255.0
        Q_clean.task_done()
        sink(x)

def sink(x):
    """Idempotent sink to avoid duplicates (upsert in real DB)."""
    key = (x["id"], round(x["ts"], 1))
    if key in SEEN_KEYS: 
        return
    SEEN_KEYS.add(key)
    # TODO: replace with database write, e.g. upsert_to_postgres(x)

if __name__ == "__main__":
    for f in (producer, cleaner, scorer):
        threading.Thread(target=f, daemon=True).start()
    time.sleep(2.0)
    print("inflight:", Q_ingest.qsize(), "unique_writes:", len(SEEN_KEYS))
