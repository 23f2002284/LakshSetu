
# The "trend" you want to match against
job_description = """
We are looking for a Senior Python Developer with a strong background in AWS, Docker, and PostgreSQL.
The ideal candidate will lead the design of scalable microservices and mentor junior engineers.
Experience with CI/CD pipelines is a must.
"""

# 1. Embed the trend/query
job_embedding = embedding_model.encode(job_description).tolist()

# 2. Query the vector DB to find the 3 most similar profiles
results = profiles_collection.query(
    query_embeddings=[job_embedding],
    n_results=3
)

print("\n🔍 Top matching profiles for the job:")
for i, user_id in enumerate(results['ids'][0]):
    distance = results['distances'][0][i]
    metadata = results['metadatas'][0][i]
    print(f"  - User ID: {user_id}, Name: {metadata.get('name')} (Similarity Score: {1 - distance:.2f})")