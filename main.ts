// A news-image-daily entry (Node 22, standard library only): its image is the
// entry.png beside this file, and the program copies it to /output/entry.png.
// The image is a newspaper front page summing up the world news of Tuesday
// 17 November 2026, drawn offline by generate.py (Pillow + DejaVu fonts)
// from real events reported that day (BBC, AP, Reuters, Al Jazeera, ABC News,
// Just Security). The gate takes a whole PNG of at most 1 MiB and 1024x1024.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
