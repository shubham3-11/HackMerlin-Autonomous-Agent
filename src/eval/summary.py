"""
Generate a run summary file from collected results.
"""
import json

def write_run_summary(level_results: list, output_path: str):
    """
    level_results: list of dicts with keys:
        level (int), success (bool), password (str or None), strategies (list of str)
    """
    summary = {
        "levels": level_results,
        "total_levels_cleared": sum(1 for lvl in level_results if lvl.get("success"))
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
