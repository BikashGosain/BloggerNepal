from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Blog


def get_similar_posts(current_post, limit=5):

    posts = Blog.objects.filter(status='Published')

    documents = []

    for post in posts:
        documents.append(
            f"{post.title} {post.short_description} {post.blog_body}"
        )

    vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    post_list = list(posts)

    current_index = post_list.index(current_post)

    similarity_scores = list(
        enumerate(similarity_matrix[current_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similar_posts = []

    for idx, score in similarity_scores[1:limit+1]:
        similar_posts.append(post_list[idx])

    return similar_posts