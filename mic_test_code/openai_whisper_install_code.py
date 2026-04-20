from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

repo_id = "openai/whisper-large-v3-turbo"
save_dir = "./whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(repo_id)
processor = AutoProcessor.from_pretrained(repo_id)

model.save_pretrained(save_dir)
processor.save_pretrained(save_dir)