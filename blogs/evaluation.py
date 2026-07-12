from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# python manage.py shell

# Then:

# from blogs.evaluation import evaluate_recommendation

# evaluate_recommendation()

from .models import Blog
from .similarity import get_similar_posts


def evaluate_recommendation(limit=5):

    posts = list(Blog.objects.filter(status="Published"))

    y_true = []
    y_pred = []

    for current_post in posts:

        recommendations = get_similar_posts(current_post, limit)

        for post in posts:

            if post == current_post:
                continue

            actual = (
                current_post.category == post.category
                and current_post.category is not None
            )

            predicted = post in recommendations

            y_true.append(int(actual))
            y_pred.append(int(predicted))

    cm = confusion_matrix(y_true, y_pred)

    print("Confusion Matrix")
    print(cm)

    print("Accuracy :", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, zero_division=0))
    print("Recall   :", recall_score(y_true, y_pred, zero_division=0))
    print("F1 Score :", f1_score(y_true, y_pred, zero_division=0))