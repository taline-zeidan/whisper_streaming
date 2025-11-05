from pydub import AudioSegment
from pathlib import Path

def convert_m4a_to_wav():
    # Hardcoded file path
    input_path = Path("/Users/talinezeidan/Documents/LAU/whisper_streaming/experiments/Boulos.m4a")
    output_path = input_path.with_suffix(".wav")  # same name, just .wav

    print(f"🔄 Converting {input_path} → {output_path} ...")

    # Load the .m4a file
    audio = AudioSegment.from_file(input_path, format="m4a")

    # Convert to mono + 16kHz
    audio = audio.set_frame_rate(16000).set_channels(1)

    # Export as WAV
    audio.export(output_path, format="wav")

    print(f"✅ Done! Saved to {output_path}")
    return output_path

if __name__ == "__main__":
    convert_m4a_to_wav()
