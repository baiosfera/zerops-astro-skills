export interface LeadScoringWeights {
  explicitWeight?: number;
  implicitWeight?: number;
  semanticWeight?: number;
}

export function calculateLeadScore(params: {
  explicitScore: number;
  implicitScore: number;
  semanticCosineDistance: number;
  weights?: LeadScoringWeights;
}) {
  const wExplicit = params.weights?.explicitWeight ?? 0.35;
  const wImplicit = params.weights?.implicitWeight ?? 0.25;
  const wSemantic = params.weights?.semanticWeight ?? 0.40;

  // Normalized cosine similarity between 0 and 100
  const semanticSimilarity = Math.max(0, Math.min(100, (1 - params.semanticCosineDistance) * 100));

  const totalScore = Math.round(
    params.explicitScore * wExplicit +
    params.implicitScore * wImplicit +
    semanticSimilarity * wSemantic
  );

  let grade: "A_HOT" | "B_WARM" | "C_NURTURE" | "D_COLD" = "D_COLD";
  if (totalScore >= 75) grade = "A_HOT";
  else if (totalScore >= 50) grade = "B_WARM";
  else if (totalScore >= 30) grade = "C_NURTURE";

  return {
    explicitScore: params.explicitScore,
    implicitScore: params.implicitScore,
    semanticScore: Math.round(semanticSimilarity),
    totalScore,
    grade
  };
}

/**
 * Reciprocal Rank Fusion (RRF) for hybrid search scoring
 * Formula: RRF(d) = sum(1 / (k + rank_i))
 */
export function calculateRrfScore(denseRank: number, sparseRank: number, k = 60): number {
  const denseComponent = 1 / (k + denseRank);
  const sparseComponent = 1 / (k + sparseRank);
  return denseComponent + sparseComponent;
}
