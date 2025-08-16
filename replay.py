#!/usr/bin/env python3
"""
@file replay.py
@brief Replays input samples from a DB dump or API, sending only segments where arm==True.

@details
  • Accepts data from a local file (JSON or Python-literal) or the API.
  • Detects segments bounded by arm==False at start and end.
  • Replays each True-only segment in order, POSTing each sample to /inputs/ (optional).
  • Supports fixed-rate playback or step_index-based pacing.

@usage
  # From file, dry-run (no POST), show segments
  python replay.py --from-file data.json --list

  # Replay all segments to local API at 20 Hz
  python replay.py --from-file data.json --server http://localhost:5000 --rate-hz 20 --post

  # Replay only the last segment, respecting step_index timing (1 step = 50 ms)
  python replay.py --from-file data.json --server http://localhost:5000 --post \
                   --segments last --step-dt 0.05 --pace step

  # Fetch from API and replay all segments (fixed 10 Hz)
  python replay.py --from-api --server http://localhost:5000 --rate-hz 10 --post
"""

from __future__ import annotations
import argparse
import time
import json
import ast
from typing import Any, Dict, List, Tuple, Iterable, Optional
import requests


def _coerce_list(obj: Any) -> List[Dict[str, Any]]:
    """
    @brief Convert loaded content into a list[dict]. Accepts JSON or Python-literal.
    """
    if isinstance(obj, list):
        return obj
    if isinstance(obj, str):
        # Try JSON first
        try:
            return json.loads(obj)
        except Exception:
            # Fallback: Python literal (handles single quotes)
            return ast.literal_eval(obj)
    raise ValueError("Unsupported data format; expected list or JSON string.")


def load_from_file(path: str) -> List[Dict[str, Any]]:
    """
    @brief Load samples from a file that contains either JSON or a Python-literal list of dicts.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    data = _coerce_list(text)
    if not all(isinstance(x, dict) for x in data):
        raise ValueError("File did not contain a list of objects.")
    return data


def load_from_api(base_url: str) -> List[Dict[str, Any]]:
    """
    @brief GET all inputs from the API.
    @param base_url e.g. http://localhost:5000
    """
    url = base_url.rstrip("/") + "/inputs/"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list):
        raise ValueError("API /inputs/ did not return a list.")
    return data


def sanitize_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    @brief Keep only fields required by InputSchema and coerce types.
    @return Dict with keys: step_index, x, y, z, yaw, s1, s2, s3, arm
    """
    out = {
        "step_index": int(rec.get("step_index", 0)),
        "x": float(rec.get("x", 0.0)),
        "y": float(rec.get("y", 0.0)),
        "z": float(rec.get("z", 0.0)),
        "yaw": float(rec.get("yaw", 0.0)),
        "s1": float(rec.get("s1", 0.0)),
        "s2": float(rec.get("s2", 0.0)),
        "s3": float(rec.get("s3", 0.0)),
        "arm": bool(rec.get("arm", False)),
    }
    return out


def find_true_segments(data: List[Dict[str, Any]]) -> List[Tuple[int, int]]:
    """
    @brief Find contiguous [start,end] index pairs where arm==True.
    @details A segment starts when arm switches False -> True, ends at the last True before the next False.
             If data starts with True, that counts as a segment start at index 0.
             If data ends with True, we end the final segment at the last index.

    @return List of (start_idx, end_idx) inclusive, referring to original 'data' indices.
    """
    segs: List[Tuple[int, int]] = []
    in_seg = False
    start = 0

    def is_true(i: int) -> bool:
        return bool(data[i].get("arm", False))

    for i in range(len(data)):
        if not in_seg and is_true(i):
            in_seg = True
            start = i
        elif in_seg and not is_true(i):
            segs.append((start, i - 1))
            in_seg = False

    if in_seg:
        # trailing True region
        segs.append((start, len(data) - 1))

    return segs


def iter_segment(data: List[Dict[str, Any]], start: int, end: int) -> Iterable[Dict[str, Any]]:
    """
    @brief Yield sanitized records in [start,end] where arm==True.
    """
    for i in range(start, end + 1):
        rec = sanitize_record(data[i])
        if rec["arm"]:
            yield rec


def post_record(base_url: str, rec: Dict[str, Any], timeout_s: float = 2.0) -> None:
    """
    @brief POST a record to /inputs/.
    """
    url = base_url.rstrip("/") + "/inputs/"
    r = requests.post(url, json=rec, timeout=timeout_s)
    if not (200 <= r.status_code < 300):
        raise RuntimeError(f"POST {url} failed: {r.status_code} {r.text}")


def replay_segments(
    data: List[Dict[str, Any]],
    base_url: str,
    which: str = "all",
    post: bool = False,
    pace: str = "fixed",
    rate_hz: float = 20.0,
    step_dt: float = 0.05,
    sleep_fn=time.sleep,
) -> None:
    """
    @brief Replay segments of True-arm data.

    @param data     Full list of samples (dicts).
    @param base_url Server base URL (used when post=True).
    @param which    "all" to replay all segments found, or "last" for only the last one.
    @param post     If True, POST each frame to /inputs/; otherwise just print (dry run).
    @param pace     "fixed" -> send at rate_hz; "step" -> send using step_index deltas * step_dt.
    @param rate_hz  Fixed rate (Hz) used when pace == "fixed".
    @param step_dt  Seconds per step_index increment when pace == "step".
    """

    segs = find_true_segments(data)
    if not segs:
        print("No True-arm segments found.")
        return

    if which == "last":
        segs = [segs[-1]]

    print(f"Segments to replay (inclusive indices): {segs}")
    for si, (a, b) in enumerate(segs, 1):
        print(f"\n--- Segment {si}/{len(segs)}: [{a}..{b}] ({b-a+1} frames) ---")
        last_step = None
        for rec in iter_segment(data, a, b):
            if post:
                try:
                    post_record(base_url, rec)
                except Exception as e:
                    print(f"POST error: {e}")
            else:
                print(rec)

            # pacing
            if pace == "fixed":
                sleep_fn(1.0 / max(1e-6, rate_hz))
            else:  # pace == "step"
                if last_step is not None:
                    dstep = max(0, rec["step_index"] - last_step)
                    sleep_fn(dstep * step_dt)
                last_step = rec["step_index"]
    print("\nReplay complete.")
    

def main():
    ap = argparse.ArgumentParser(description="Replay arm==True segments from file or API.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-file", type=str, help="Path to data file (JSON or Python-literal list).")
    src.add_argument("--from-api", action="store_true", help="Fetch data from /inputs/ API.")

    ap.add_argument("--server", type=str, default="http://localhost:5000", help="Base server URL (for POST).")
    ap.add_argument("--post", action="store_true", help="POST records to /inputs/ during replay.")
    ap.add_argument("--segments", choices=["all", "last"], default="all", help="Which segments to replay.")
    ap.add_argument("--pace", choices=["fixed", "step"], default="fixed", help="Replay pacing mode.")
    ap.add_argument("--rate-hz", type=float, default=20.0, help="Fixed replay rate (Hz) when --pace fixed.")
    ap.add_argument("--step-dt", type=float, default=0.05, help="Seconds per step_index when --pace step.")
    ap.add_argument("--list", action="store_true", help="Only list segments; do not replay.")

    args = ap.parse_args()

    time.sleep(60)

    # Load data
    if args.from_api:
        data = load_from_api(args.server)
    else:
        data = load_from_file(args.from_file)

    # Show segments
    segs = find_true_segments(data)
    print(f"Found {len(segs)} segments: {segs}")
    if args.list:
        return

    # Replay
    replay_segments(
        data=data,
        base_url=args.server,
        which=args.segments,
        post=args.post,
        pace=args.pace,
        rate_hz=args.rate_hz,
        step_dt=args.step_dt,
    )


if __name__ == "__main__":
    main()
