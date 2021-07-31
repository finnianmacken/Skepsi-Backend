from transformers import pipeline
from background_task import background
from ..models import Annotation

classifier = pipeline("zero-shot-classification")


@background(schedule=10)
def classify_topics_queue_manager(sequence, annotation_id):
    candidate_labels = ["biochemistry",
                        "mathematics",
                        "medical science",
                        "biomedical and health sciences"]
    annotation = Annotation.objects.get(pk=annotation_id)
    print("CLASSIFYING TOPICS")
    annotation.ai_data = classifier(sequence, candidate_labels, multi_label=True)
    annotation.save()
