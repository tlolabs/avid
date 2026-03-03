#!/usr/bin/env python3
import argparse
import platform
import sys
from pathlib import Path


def normalized_arch(machine: str) -> str:
    aliases = {
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "arm64": "arm64",
        "aarch64": "arm64",
    }
    return aliases.get(machine.lower(), machine.lower())


def ffmpeg_name(target_platform: str) -> str:
    return "ffmpeg.exe" if target_platform == "windows" else "ffmpeg"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that the expected bundled FFmpeg binary exists for the target platform."
    )
    parser.add_argument(
        "--platform",
        dest="target_platform",
        default=platform.system().lower(),
        help="Target platform: darwin, windows, or linux (default: current platform)",
    )
    parser.add_argument(
        "--arch",
        dest="target_arch",
        default=normalized_arch(platform.machine()),
        help="Target architecture: x86_64, arm64, etc. (default: current architecture)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="App root to validate (default: script directory)",
    )
    parser.add_argument(
        "--require-bundled-ffmpeg",
        action="store_true",
        help="Fail if the platform-specific bundled binary is missing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    binary_name = ffmpeg_name(args.target_platform)
    expected_path = args.root / "ffmpeg" / args.target_platform / args.target_arch / binary_name

    print(f"Target platform: {args.target_platform}")
    print(f"Target architecture: {args.target_arch}")
    print(f"Expected bundled FFmpeg path: {expected_path}")

    if expected_path.exists():
        print("Bundled FFmpeg check: OK")
        return 0

    if args.require_bundled_ffmpeg:
        print("Bundled FFmpeg check: MISSING", file=sys.stderr)
        return 1

    print("Bundled FFmpeg check: not present, but not required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
