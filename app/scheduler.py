import time
from app.ingestion.fetch_price import main as fetch_main
from app.worker.process_events import main as worker_main

INTERVAL = 60  # seconds

def run():
    while True:
        print("Running ingestion...")
        fetch_main()

        print("Running worker...")
        worker_main()

        print(f"Sleeping {INTERVAL} seconds...\n")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    run()