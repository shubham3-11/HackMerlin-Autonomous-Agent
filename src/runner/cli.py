"""
Command-line interface entry for the HackMerlin agent.
"""
import argparse
from datetime import datetime
from runner.agent import run_agent

def main():
    parser = argparse.ArgumentParser(description="Run the HackMerlin autonomous agent.")
    parser.add_argument("--engine", choices=["playwright", "selenium"], default="playwright",
                        help="Browser automation engine to use (default: playwright).")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode (no UI).")
    parser.add_argument("--max-attempts-per-level", type=int, default=8,
                        help="Maximum prompt attempts per level before giving up (default: 8).")
    parser.add_argument("--cooldown-sec", type=float, default=1.0,
                        help="Cooldown time in seconds between attempts (default: 1.0).")
    parser.add_argument("--outdir", type=str, default=None,
                        help="Directory to save run logs (transcript and summary). Default is runs/<timestamp>.")
    args = parser.parse_args()
    # Determine output directory
    if args.outdir:
        outdir = args.outdir
    else:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outdir = f"runs/{ts}"
    run_agent(engine=args.engine, headless=args.headless,
              max_attempts_per_level=args.max_attempts_per_level,
              cooldown=args.cooldown_sec,
              outdir=outdir)

if __name__ == "__main__":
    main()
