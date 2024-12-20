from transformers import pipeline

class SummAI:
    def __init__(self):
        self.model_dir = '/home/user/SummAI_model'
        self.summarizer = pipeline("summarization", model=self.model_dir, tokenizer=self)

    @staticmethod
    def summarize(content):
        summary = self.summarizer(content, max_length=150, min_length=40, do_sample=False)
        return summary[0]['summary_text']