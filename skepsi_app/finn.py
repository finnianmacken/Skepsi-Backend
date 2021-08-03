from transformers import pipeline
from .tasks import classify_topics_queue_manager

classifier = pipeline("zero-shot-classification")


def classify_topics(sequence):
    candidate_labels = ["biochemistry",
                        "mathematics",
                        "medical science",
                        "biomedical and health sciences"]
    return classifier(sequence, candidate_labels, multi_label=True)


def debug_celery():
    result = classify_topics_queue_manager
    print(result)
