# Story voice lines (ElevenLabs Liam via tts worker) for 2026-11-25 stories 12:30 / 12:35.
# s1: trim pauses, 1.05x tempo -> vo_s1125a.m4a + segment starts in vo_s1125a.json.  s2: delayed 0.9 s -> vo_s1125b.m4a
import subprocess, json, sys
S1, S2, OUTD = sys.argv[1:4]
SEG = [("q", 0.0, 2.45), ("fix", 3.05, 4.33), ("more", 4.97, 6.60)]; GAP = .15; TEMPO = 1.05
f, parts, t, out = [], [], 0.0, {}
for i, (n, a, b) in enumerate(SEG):
    if i: f.append(f"anullsrc=r=44100:cl=stereo,atrim=0:{GAP}[g{i}]"); parts.append(f"[g{i}]"); t += GAP
    f.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo[s{i}]"); parts.append(f"[s{i}]")
    out[n] = [round(t / TEMPO, 3), round((t + b - a) / TEMPO, 3)]; t += b - a
f.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,atempo={TEMPO},loudnorm=I=-14:TP=-1.5[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", S1, "-filter_complex", ";".join(f), "-map", "[o]",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", OUTD + "/vo_s1125a.m4a"], check=True)
out["total"] = round(t / TEMPO, 3); json.dump(out, open(OUTD + "/vo_s1125a.json", "w"), indent=1); print(out)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", S2, "-af",
                "aformat=sample_rates=44100:channel_layouts=stereo,adelay=900|900,loudnorm=I=-14:TP=-1.5",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", OUTD + "/vo_s1125b.m4a"], check=True)
