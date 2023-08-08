from core.similarity_finder import SimilarityFinder

finder = SimilarityFinder()
similarities = finder.find_similar_images("C:\\Users\\spenc\\Desktop\\mel\\test", 1)
# finder.find_similar_images("C:\\Users\\spenc\\Desktop\\mel", 1)
for item, similarity in similarities.items():
    print(f"|\n_{item}")
    for sim in similarity:
        print(f"|\t|_{sim}")
        for i in similarity[sim]:
            print(f"|\t  |_{i}")