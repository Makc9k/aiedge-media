# Tighten the ElevenLabs voiceover (Liam) for reel 2026-11-25: trim long pauses, light speed-up.
# Writes vo_1125.m4a + vo_1125.json (segment start/end in the final timeline).
import subprocess, json, sys
SRC = sys.argv[1]; OUTD = sys.argv[2]
SEG = [("hook", 0.0, 2.58), ("one", 3.05, 3.76), ("five", 4.24, 5.50), ("r1", 5.93, 6.84), ("r2", 7.70, 8.93),
       ("r3", 9.57, 10.94), ("r4", 11.69, 13.08), ("r5", 13.86, 15.20), ("pick", 16.00, 17.60),
       ("cta", 18.31, 19.17), ("cta_b", 19.91, 20.30), ("cta_c", 20.66, 21.83)]
GAP = {"cta_b": .10, "cta_c": .10}; DEF = .16; TEMPO = 1.07
parts, f, t, out = [], [], 0.0, {}
for i, (n, a, b) in enumerate(SEG):
    g = 0 if i == 0 else GAP.get(n, DEF)
    if g: f.append(f"anullsrc=r=44100:cl=stereo,atrim=0:{g}[g{i}]"); parts.append(f"[g{i}]")
    t += g
    f.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo[s{i}]"); parts.append(f"[s{i}]")
    out[n] = [round(t / TEMPO, 3), round((t + b - a) / TEMPO, 3)]; t += b - a
f.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,atempo={TEMPO},loudnorm=I=-14:TP=-1.5[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-filter_complex", ";".join(f), "-map", "[o]",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", OUTD + "/vo_1125.m4a"], check=True)
out["total"] = round(t / TEMPO, 3)
json.dump(out, open(OUTD + "/vo_1125.json", "w"), indent=1); print(out)
