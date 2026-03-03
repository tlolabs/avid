# A.V.I.D. – Audio Visual Integration & Distribution

A.V.I.D. can be used as either a GUI or CLI. It builds a single composite frame from an image, then encodes a video using FFmpeg for the full duration of the audio.

## What it does

- Loads one image.
- Creates a background layer by scaling the image to fill the full frame and applying a Gaussian blur radius of 40.
- Creates a foreground layer by scaling the image to fit inside a square based on the frame's smallest dimension.
- Centers the foreground on top of the blurred background.
- Uses FFmpeg to loop that composite frame for the full audio duration.
- Compresses audio with AAC.
- GUI presets for social media outlet, supported resolution, and matching aspect ratio.
- Checks for a bundled platform-specific FFmpeg binary before falling back to system `ffmpeg`.
- On launch, the GUI guides the user to current FFmpeg download pages if FFmpeg is missing.

## Setup

1. Install FFmpeg and ensure `ffmpeg` is on your PATH.
2. Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

### Bundled FFmpeg

A.V.I.D. looks for a bundled FFmpeg binary in this order:

- `ffmpeg/<platform>/<arch>/ffmpeg`
- `ffmpeg/<platform>/ffmpeg`
- `ffmpeg/ffmpeg`

On Windows, the binary name must be `ffmpeg.exe`.

Example bundle paths:

- `ffmpeg/darwin/arm64/ffmpeg`
- `ffmpeg/windows/x86_64/ffmpeg.exe`
- `ffmpeg/linux/x86_64/ffmpeg`

To validate a release build before packaging:

```bash
python3 check_ffmpeg_bundle.py --require-bundled-ffmpeg
```

To validate for a different target:

```bash
python3 check_ffmpeg_bundle.py --platform windows --arch x86_64 --require-bundled-ffmpeg
```

## Usage

### GUI

```bash
python3 avid_gui.py
```

The GUI now uses platform-specific presets:

- `Social media outlet` filters the available aspect ratios.
- `Aspect ratio` filters the available resolutions.
- `Resolution` shows the valid sizes for the selected platform and aspect ratio.
- On launch, if FFmpeg is missing, A.V.I.D. shows the expected bundle path and offers to open platform-specific download pages.
- A live preview thumbnail shows the styled frame with the selected aspect ratio and composition treatment, without forced square letterboxing.
- The progress bar uses FFmpeg progress updates to show an approximate percentage and ETA.
- A collapsible FFmpeg console tray below the UI shows the exact command and live progress output.
- The render button switches to a stop action shortly after rendering starts.

### CLI

```bash
python3 avid.py input.jpg input.wav output.mp4 --size 1080x1920
```

Check FFmpeg availability from the CLI:

```bash
python3 avid.py --check-ffmpeg
```

### Options

- `--size WIDTHxHEIGHT` output dimensions (default: `1080x1920`)
- `--flip-horizontal` flip image layers horizontally
- `--flip-vertical` flip image layers vertically
- `--audio-bitrate` AAC bitrate, e.g. `96k`, `128k`, `192k` (default: `128k`)
- `--fps` video fps (default: `30`)

### Example

```bash
python3 avid.py photo.png voice.wav result.mp4 --size 1920x1080 --flip-horizontal --audio-bitrate 96k
```
