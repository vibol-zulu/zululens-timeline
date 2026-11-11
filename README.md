# ZuluLens Timeline

An interactive bubble timeline of US news and commentary channels from 2000 to 2026. Teal bubbles are corporate outlets and peach bubbles are independent channels. Bubble area matches estimated monthly audience. Press Play or drag the progress bar to watch smaller independent channels grow around corporate media.

The data is provisional and will change. Sizes are rough estimates for comparison only. See the Methodology pop-up (the "i" button) for details.

## Run it locally

The page loads `channels.csv` with `fetch`, so it needs a local web server rather than opening the file directly:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Host it

Upload `index.html` and `channels.csv` to the same folder on any static host (GitHub Pages, Netlify, Vercel).

`index.html` draws the timeline. `channels.csv` holds all the data. To update the chart, edit the CSV only.

## channels.csv columns

| Column | What to put |
|---|---|
| name | Channel name, shown on the bubble and in the tooltip (text in brackets is hidden on the bubble) |
| type | `corporate` or `independent` (sets the colour) |
| lean | Political lean, shown in the tooltip |
| audience_m | Oct 2026 monthly audience in millions (e.g. `24.1`, `0.35`) |
| views_m | Monthly views in millions (Oct 2026). If audience_m is blank, the page sets audience = views x the platform ratio |
| platform_type | One of: Long-form podcast (0.588), Interview (0.565), Daily show / analysis (0.550), News commentary (0.535), Rumble / X / TikTok (0.512), Live stream (0.488), X-only (0.475) |
| audience_published | Previous figure (2025 value x YouTube change) for channels switched to the sheet formula in Nov 2026. Not used by the chart |
| audience_m_audit | The Oct 2026 audit figure, kept for reference. Not used by the chart |
| audience_2000 | Optional. Audience in 2000, for outlets founded before 2000. If filled, the bubble starts at this size in 2000 instead of growing from launch |
| start | Launch date: `2015`, `2015-06` or `2015-06-01`. A year alone is placed mid-year |
| start_approx | `yes` adds "(approx.)" to the launch year |
| value | `estimate` or `draft`. Draft shows "Placeholder figure" in the tooltip |
| source | `main` or `swarm candidate`. Candidates show "not yet merged" |
| show | `yes` or `no`. Use `no` to hide a row without deleting it |
| caveat | Optional. A short warning shown in the tooltip, e.g. that the main platform does not publish audience numbers |
| note | Your own notes. Not shown |

Rows with no audience, no start date or `show = no` are skipped.

Display cutoff: only channels with an October 2026 audience of at least 0.5M are shown. Smaller rows are kept with `show = no` and the note "Hidden Nov 2026: under the 0.5M display cutoff".

## Adding a new channel

Add a row with name, type, lean, start, `views_m`, `platform_type`, `show = yes` and a source in `note`. Leave `audience_m` blank and the page works out the size from the views, using the same ratios as the 2025 research.

## Updating

Edit `channels.csv` (and `quarterly.csv` for 2024–2026), then push to GitHub and republish the artifact.

Each bubble grows in a straight line from 0 at `start` to `audience_m` in October 2026. If `audience_2000` is filled, it moves in a straight line from that value in 2000 instead. Write "proposed" in `note` to flag a rough 2000 figure in the tooltip. Bubble area matches audience.

## Quarterly data (2024 to 2026)

`quarterly.csv` holds audience estimates for each quarter from 2024 Q1 to 2026 Q3 for independent channels with YouTube history. Each independent value = that quarter's median monthly YouTube views x the sheet's audience share for the platform type (the same formula as the October 2026 figure). TV networks use quarterly Nielsen ratings plus YouTube, from vidIQ monthly history. Negative months are skipped; months above 5x the channel's usual level are capped. The `name` must match `channels.csv`. Channels not listed grow in a straight line.

## Records

- `ZuluLens_UMA_Records.xlsx` — how each figure was calculated: platform factors, the October 2026 legacy recalculation (with live formulas), sources and a change log.
- `legacy_2026_calc.csv` — the same legacy recalculation as plain data.

## Export a video

`export_video.py` renders the animation to MP4 (no icons or play button), using Playwright and ffmpeg:

```bash
python export_video.py                  # 1920x1080
python export_video.py --size square    # 1080x1080
python export_video.py --size vertical  # 1080x1920
```

Add `--theme dark` for dark mode. Videos are saved in `video/` (not committed). The script opens `index.html?record`, which hides the controls and lets the script step the animation one frame at a time.
