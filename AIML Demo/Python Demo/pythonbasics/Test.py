   # Function to compute cosine similarity and retrieve top matches
   # Compute similarities for all chunks
   similarities = []
   for i, (embedding, text) in enumerate(zip(embeddings, texts)):
        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
        similarities.append((similarity, text))

    # Sort by similarity in descending order and select top_k chunks
    top_chunks = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]

    # Print the top chunks with their similarity scores
    for i, (similarity, content) in enumerate(top_chunks, start=1):
        print(f"Top Chunk {i}:")
        print(content)
        print(f"Cosine Similarity: {similarity * 100:.4f}")
        print("#" * 100)  # Separator for readability
