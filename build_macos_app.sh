#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FFMPEG_BIN="${FFMPEG_BIN:-/opt/homebrew/bin/ffmpeg}"
FFPROBE_BIN="${FFPROBE_BIN:-/opt/homebrew/bin/ffprobe}"

if [[ ! -x "${FFMPEG_BIN}" ]]; then
  echo "Missing executable FFmpeg binary: ${FFMPEG_BIN}" >&2
  exit 1
fi

if [[ ! -x "${FFPROBE_BIN}" ]]; then
  echo "Missing executable ffprobe binary: ${FFPROBE_BIN}" >&2
  exit 1
fi

source "${ROOT_DIR}/.venv/bin/activate"
export PYINSTALLER_CONFIG_DIR="${ROOT_DIR}/.pyinstaller"

pyinstaller \
  --noconfirm \
  --windowed \
  --name AVID \
  --specpath "${ROOT_DIR}" \
  --workpath "${ROOT_DIR}/build" \
  --distpath "${ROOT_DIR}/dist" \
  --add-data "LICENSE:." \
  --add-binary "${FFMPEG_BIN}:." \
  --add-binary "${FFPROBE_BIN}:." \
  avid_gui.py

mkdir -p "${ROOT_DIR}/packages/dmg-root"
rm -rf "${ROOT_DIR}/packages/dmg-root/AVID.app"
cp -R "${ROOT_DIR}/dist/AVID.app" "${ROOT_DIR}/packages/dmg-root/AVID.app"
rm -f "${ROOT_DIR}/packages/AVID-macos-arm64.dmg"
hdiutil create \
  -volname AVID \
  -srcfolder "${ROOT_DIR}/packages/dmg-root" \
  -ov \
  -format UDZO \
  "${ROOT_DIR}/packages/AVID-macos-arm64.dmg"
