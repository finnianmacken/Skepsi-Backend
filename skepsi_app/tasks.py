# from transformers import pipeline
# from .models import Annotation
# from skepsi_backend.celery import app
# from celery import shared_task
#
# classifier = pipeline("zero-shot-classification")
#
#
# @shared_task(name='tasks.classify_topics')
# def classify_topics_queue_manager(sequence, annotation_id):
#     # don't use the character : at all here or you'll break the application
#     candidate_labels = ["animal sciences",
#                         "behavioural and social sciences",
#                         "biochemistry",
#                         "biomedical and health sciences",
#                         "cellular and molecular biology",
#                         "chemistry",
#                         "computational biology and bioinformatics",
#                         "earth and environmental sciences",
#                         "embedded systems",
#                         "energy, sustainable materials and design",
#                         "engineering mechanics",
#                         "environmental engineering",
#                         "materials science",
#                         "mathematics",
#                         "microbiology",
#                         "physics and astronomy",
#                         "plant sciences",
#                         "robotics and intelligent machines",
#                         "systems software",
#                         "translational medical science"
#                         ]
#     try:
#         annotation = Annotation.objects.get(pk=annotation_id)
#         print("CLASSIFYING TOPICS")
#         annotation.ai_data = classifier(sequence, candidate_labels, multi_label=True)
#         print('THIS IS THE CLASSIFIER', classifier)
#         annotation.save()
#         print("TOPICS CLASSIFIED")
#     except:
#         print('Topic classification was unsuccessful')
#
#
# def reclassify_all_annotations():
#     candidate_labels = ["animal sciences",
#                         "behavioural and social sciences",
#                         "biochemistry",
#                         "biomedical and health sciences",
#                         "cellular and molecular biology",
#                         "chemistry",
#                         "computational biology and bioinformatics",
#                         "earth and environmental sciences",
#                         "embedded systems",
#                         "energy, sustainable materials and design",
#                         "engineering mechanics",
#                         "environmental engineering",
#                         "materials science",
#                         "mathematics",
#                         "microbiology",
#                         "physics and astronomy",
#                         "plant sciences",
#                         "robotics and intelligent machines",
#                         "systems software",
#                         "translational medical science"
#                         ]
#     annotation_qs = Annotation.objects.all()
#     for annotation in annotation_qs:
#         annotation.ai_data = classifier(annotation.content,
#                                         candidate_labels,
#                                         multi_label=True)
#         annotation.save()
#
#
# def classify_topics(sequence):
#     candidate_labels = ["biochemistry",
#                         "mathematics",
#                         "medical science",
#                         "biomedical and health sciences"]
#     return classifier(sequence, candidate_labels, multi_label=True)
