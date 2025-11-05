import subprocess
import time
import csv
from pathlib import Path

# Hardcoded audio file path
AUDIO_PATH = "/Users/talinezeidan/Documents/LAU/whisper_streaming/experiments/riad.wav"

# List of MLX Whisper models to test
MODELS = [
    "tiny",
    "base",
    "small",
    "medium",
    "large",
    "large-v1",
    "large-v2",
    "large-v3",
    "large-v3-turbo"
]

# Path to your main whisper_online.py script
WHISPER_SCRIPT = "/Users/talinezeidan/Documents/LAU/whisper_streaming/whisper_online.py"

# Output CSV file
RESULTS_FILE = Path("/Users/talinezeidan/Documents/LAU/whisper_streaming/experiments/mlx_offline_benchmark_results.csv")


def run_and_capture_output(cmd):
    """Run the transcription command, return transcript text and time."""
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {cmd}")
        return None, None

    end = time.time()
    elapsed = end - start
    return result.stdout, elapsed


def extract_transcript_text(raw_output):
    """Extract only the transcribed text lines from the Whisper output."""
    lines = raw_output.splitlines()
    text_lines = []
    for line in lines:
        parts = line.strip().split(" ", 3)
        if len(parts) == 4:
            text = parts[3].strip()
            if text:
                text_lines.append(text)
    return " ".join(text_lines).strip()


def main():
    print("Starting MLX Whisper OFFLINE benchmark...\n")

    results = []
    for model in MODELS:
        print(f"Testing model (offline): {model}")

        cmd = (
            f"python {WHISPER_SCRIPT} {AUDIO_PATH} "
            f"--backend mlx-whisper "
            f"--lan ar "
            f"--model {model} "
            f"--offline"
        )

        raw_output, elapsed = run_and_capture_output(cmd)

        if raw_output is None:
            results.append({"model": model, "time_sec": "ERROR", "transcript": ""})
            continue

        transcript_text = extract_transcript_text(raw_output)

        print(f"{model} completed in {elapsed:.2f} seconds. Transcript length: {len(transcript_text)} characters.\n")

        results.append({
            "model": model,
            "time_sec": round(elapsed, 2),
            "transcript": transcript_text
        })

    # Write all results to CSV
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "time_sec", "transcript"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nOffline benchmark complete. Results saved to: {RESULTS_FILE}")

    print("\nSummary:")
    for r in results:
        print(f"{r['model']:>12} | {r['time_sec']} sec | {len(r['transcript'])} chars")


if __name__ == "__main__":
    main()
