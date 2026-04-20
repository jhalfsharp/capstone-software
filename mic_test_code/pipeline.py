import os
import torch
import sounddevice as sd
import soundfile as sf
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_path = "./whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True, local_files_only=True,
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_path, local_files_only=True)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

sample_rate = 48000
channels = 2
duration = 5
audio_file = "temp_capture.wav"
output_text_file = "transcription.txt"

print("Recording started...")
audio_data = sd.rec(
    int(sample_rate * duration),
    samplerate=sample_rate,
    channels=channels,
    dtype='int32'
)
sd.wait()
sf.write(audio_file, audio_data, sample_rate)
print("Recording complete. Transcribing...")

result = pipe(
    audio_file,
    generate_kwargs={
        "language": "english",
        "task": "transcribe"
    }
)

with open(output_text_file, "w", encoding="utf-8") as f:
    f.write(result["text"].strip())

print(result["text"].strip())