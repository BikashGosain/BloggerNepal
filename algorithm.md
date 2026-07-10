# BloggerNepal Recommendation Algorithm

## Algorithm Name

**Content-Based Blog Recommendation using TF-IDF Vectorization and Cosine Similarity**

---

# Objective

To recommend blogs that are similar to the currently viewed blog by analyzing the textual content of all published blogs using TF-IDF Vectorization and Cosine Similarity.

---

# Input

- Current Blog (Current_Post)
- Published Blogs
- Recommendation Limit (K)

---

# Output

- Top K Similar Blogs

---

# Algorithm

```text
Algorithm: Content-Based Blog Recommendation

Input:
    Current_Post
    Recommendation Limit (K)

Output:
    Top K Similar Blogs

Begin

1. Retrieve all published blogs from the database.

2. For each blog:
      Combine
          Title
          Short Description
          Blog Body
      into a single document.

3. Store all documents in a document list.

4. Initialize TF-IDF Vectorizer
      with English stop-word removal.

5. Convert every document into
      TF-IDF vectors.

6. Compute Cosine Similarity
      between every pair of TF-IDF vectors.

7. Find the index of the
      currently viewed blog.

8. Retrieve similarity scores
      corresponding to the current blog.

9. Pair every similarity score
      with its respective blog.

10. Sort similarity scores
      in descending order.

11. Ignore the current blog
      because similarity = 1.

12. Return Top K blogs
      having highest similarity scores.

End
```

---

# Mathematical Formula

## 1. TF-IDF Vectorization

### Formula

\[
\boxed{
TF\text{-}IDF(t,d)=TF(t,d)\times IDF(t)
}
\]

Where

\[
\boxed{
TF(t,d)=\frac{f_{t,d}}{\sum_k f_{k,d}}
}
\]

Scikit-learn's **TfidfVectorizer** uses **Smoothed IDF**:

\[
\boxed{
IDF(t)=\log\left(\frac{1+N}{1+df(t)}\right)+1
}
\]

Therefore,

\[
\boxed{
TF\text{-}IDF(t,d)=
\frac{f_{t,d}}
{\sum_k f_{k,d}}
\times
\left(
\log
\left(
\frac{1+N}
{1+df(t)}
\right)
+1
\right)
}
\]

### Where

| Symbol | Meaning |
|---------|---------|
| t | Term (word) |
| d | Document (Blog) |
| \(f_{t,d}\) | Frequency of term **t** in document **d** |
| \(\sum_k f_{k,d}\) | Total words in document |
| N | Total number of blogs |
| \(df(t)\) | Number of blogs containing term **t** |

---

# 2. Cosine Similarity

### Formula

\[
\boxed{
CosineSimilarity(A,B)=
\frac{A\cdot B}
{||A||\times||B||}
}
\]

Expanded Formula

\[
\boxed{
CosineSimilarity(A,B)=
\frac{\sum_{i=1}^{n}A_iB_i}
{\sqrt{\sum_{i=1}^{n}A_i^2}
\times
\sqrt{\sum_{i=1}^{n}B_i^2}}
}
\]

### Where

| Symbol | Meaning |
|---------|---------|
| A | TF-IDF Vector of Blog A |
| B | TF-IDF Vector of Blog B |
| \(A_i\) | TF-IDF weight of ith term in Blog A |
| \(B_i\) | TF-IDF weight of ith term in Blog B |
| n | Total number of unique terms |

---

# Workflow

```text
Published Blogs
       │
       ▼
Retrieve Blogs
       │
       ▼
Combine
Title + Description + Blog Body
       │
       ▼
TF-IDF Vectorization
       │
       ▼
TF-IDF Matrix
       │
       ▼
Cosine Similarity Matrix
       │
       ▼
Current Blog Selected
       │
       ▼
Extract Similarity Scores
       │
       ▼
Sort Scores
       │
       ▼
Skip Current Blog
       │
       ▼
Top K Similar Blogs
```

---

# Time Complexity

| Operation | Complexity |
|------------|------------|
| Retrieve Blogs | O(n) |
| Document Preparation | O(n) |
| TF-IDF Vectorization | O(n × m) |
| Cosine Similarity | O(n²) |
| Sorting Similarity Scores | O(n log n) |

Where

- **n** = Number of Blogs
- **m** = Number of Unique Terms

Overall Complexity

```text
O(n²)
```

---

# Advantages

- Recommends blogs based on content similarity.
- No user ratings are required.
- Removes common English stop words.
- Works effectively for new users.
- Easy to integrate into Django applications.
- Produces relevant recommendations using textual features.

---

# Limitations

- Depends only on blog content.
- Does not consider user preferences.
- Does not learn from user interactions.
- Newly added blogs require recalculating TF-IDF vectors.

---

# Future Improvements

- Personalized recommendations using search history.
- Personalized recommendations using blog viewing history.
- Recommendation using bookmarked blogs.
- Hybrid Recommendation System.
- AI-powered semantic recommendation.
- Real-time recommendation updates.

---

# Implementation Mapping

| Algorithm Step | Project Code |
|----------------|--------------|
| Retrieve Published Blogs | `Blog.objects.filter(status='Published')` |
| Create Documents | `documents.append()` |
| TF-IDF Vectorization | `TfidfVectorizer()` |
| Generate TF-IDF Matrix | `fit_transform()` |
| Calculate Similarity | `cosine_similarity()` |
| Find Current Blog | `post_list.index(current_post)` |
| Extract Similarities | `similarity_matrix[current_index]` |
| Sort Similarities | `sorted()` |
| Skip Current Blog | `similarity_scores[1:]` |
| Return Top Blogs | `return similar_posts` |