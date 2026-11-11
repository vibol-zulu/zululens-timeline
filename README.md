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
| audience_m_audit | The Oct 2026 audit figure, kept for reference. Not used by the chart |
| audience_2000 | Optional. Audience in 2000, for outlets founded before 2000. If filled, the bubble starts at this size in 2000 instead of growing from launch |
| start | Launch date: `2015`, `2015-06` or `2015-06-01`. A year alone is placed mid-year |
| start_approx | `yes` adds "(approx.)" to the launch year |
| value | `estimate` or `draft`. Draft shows "Placeholder figure" in the tooltip |
| source | `main` or `swarm candidate`. Candidates show "not yet merged" |
| show | `yes` or `no`. Use `no` to hide a row without deleting it |
| note | Your own notes. Not shown |

Rows with no audience, no start date or `show = no` are skipped.

## Updating

- **Quick preview:** open the published page and drag an edited CSV onto it. Only you see this, and it resets on reload.
- **Make it live:** save the edited `channels.csv` here and republish the artifact.

Each bubble grows in a straight line from 0 at `start` to `audience_m` in October 2026. If `audience_2000` is filled, it moves in a straight line from that value in 2000 instead. Write "proposed" in `note` to flag a rough 2000 figure in the tooltip. Bubble area matches audience.
