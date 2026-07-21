# Sample FFmpeg commands (§24, §35)

These are the actual commands GCL builds. Reproduce with `--dry-run` on any
`gcl.cli render` call. On a full ffmpeg install the `drawtext` lower-third title is
appended automatically; on a minimal build it is skipped (see
`editing/assembler.py`).

## Assemble a normal video from a captured frame sequence

```bash
ffmpeg -hide_banner -y \
  -framerate 30 -i workspace/raw_capture/demo_frames/frame_%05d.png \
  -f lavfi -i anullsrc=r=44100:cl=stereo \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium \
  -c:a aac -b:a 192k -shortest -movflags +faststart \
  workspace/renders/<job_id>/video.mp4
```

`anullsrc` supplies a silent audio track so the output always has an audio stream
(the Quality Gate's "no audio" check stays meaningful). Replace it with a real
narration/BGM input (`-i narration.wav`) once TTS/BGM are wired.

## With a burned-in JP lower-third title (full ffmpeg build)

Append to `-vf`:
```
,drawtext=fontfile='/path/to/jp-gothic.ttf':text='食料を失った村で…':\
fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=16:\
x=(w-text_w)/2:y=h-text_h-80
```

## Extract a thumbnail candidate (§26)
```bash
ffmpeg -y -i video.mp4 -vf "select=eq(n\,60)" -vframes 1 thumb.png
```

## Quality-gate probes (planned, §27)
```bash
ffmpeg -i video.mp4 -vf blackdetect=d=0.5 -f null -      # black frames
ffmpeg -i video.mp4 -af silencedetect=n=-50dB:d=1 -f null -  # silence
```
