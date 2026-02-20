from sentence_transformers import SentenceTransformer, util
import torch


class Model:
    def __init__(self, categories, model: str):
        self._model = SentenceTransformer(model)
        self._categories = categories

        self._category_embeddings = self._model.encode(
            list(categories.values()),
            convert_to_tensor=True
        )

    def classify(self, embeddings):

        cosine_scores = util.cos_sim(
            embeddings,
            self._category_embeddings
        )

        best_match_indices = torch.argmax(cosine_scores, dim=1)

        results = []

        for i, idx in enumerate(best_match_indices):
            confidence = float(cosine_scores[i][idx].item())

            if confidence < 0.30:
                category = "other"
            else:
                category = list(self._categories.keys())[idx]

            results.append({
                "category": category,
                "confidence": confidence
            })

        return results
