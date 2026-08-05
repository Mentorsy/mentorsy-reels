"""
Mentorsy — voice picker

Generates the same line in five voices so you can listen and choose.
Set your favourite as VOICE in config.py.

    python voice_samples.py
"""
import asyncio, os
import config as C

LINE = ("Your child isn't bad at maths. They're two topics behind. "
        "And those two topics are almost always the same two.")

VOICES = {
    "1_GB_Sonia":   "en-GB-SoniaNeural",
    "2_GB_Libby":   "en-GB-LibbyNeural",
    "3_IN_Neerja":  "en-IN-NeerjaNeural",
    "4_US_Aria":    "en-US-AriaNeural",
    "5_AU_Natasha": "en-AU-NatashaNeural",
}

async def main():
    import edge_tts
    out = os.path.join(C.BASE_DIR, "voice_samples")
    os.makedirs(out, exist_ok=True)
    for name, v in VOICES.items():
        p = os.path.join(out, f"{name}.mp3")
        await edge_tts.Communicate(LINE, v, rate=C.VOICE_RATE).save(p)
        print(f"  ✓ {name}.mp3   ({v})")
    print(f"\nOpen {out} and listen. Put the winner in config.py as VOICE.")

if __name__ == "__main__":
    asyncio.run(main())
