"""
Logging utility to record runs (transcript and JSON lines).
"""
import json
import time

class RunLogger:
    def __init__(self, transcript_path: str, jsonl_path: str):
        self.start_time = time.time()
        self.transcript_file = open(transcript_path, "w", encoding="utf-8")
        self.jsonl_file = open(jsonl_path, "w", encoding="utf-8")

    def log(self, role: str, message: str, level: int = None, strategy: str = None):
        """
        Log a message from either the agent (user) or Merlin (assistant).
        role: "Agent" or "Merlin" or other descriptor.
        message: The text content of the message.
        """
        timestamp = time.time() - self.start_time
        # Write to human-readable transcript
        prefix = f"[{timestamp:0.2f}s] {role}: "
        self.transcript_file.write(prefix + message + "\n")
        self.transcript_file.flush()
        # Write structured log entry to JSONL
        entry = {"time": round(timestamp, 2), "role": role, "message": message}
        if level is not None:
            entry["level"] = level
        if strategy is not None:
            entry["strategy"] = strategy
        self.jsonl_file.write(json.dumps(entry) + "\n")
        self.jsonl_file.flush()

    def close(self):
        """Close the log files."""
        try:
            self.transcript_file.close()
        except Exception:
            pass
        try:
            self.jsonl_file.close()
        except Exception:
            pass
