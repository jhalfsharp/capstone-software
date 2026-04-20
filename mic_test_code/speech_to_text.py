# Import
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Force offline setting (enable it if you want)
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"


# Model Setup
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_path = "./whisper-large-v3-turbo"   # local folder

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True, local_files_only=True,
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_path, local_files_only=True,)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

# USER Test Input
inputAudio = ("your-audio-file")

result = pipe(
    inputAudio,
    generate_kwargs={
        "language": "english",
        "task": "transcribe"
    }
)

print("\n\nBelow is the output text from speech:")
print(result["text"])