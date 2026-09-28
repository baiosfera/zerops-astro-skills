export function calculateLeadScore(params: {
  explicitScore: number;
  implicitScore: number;
  semanticCosineDistance: number;
}) {
  const semanticSimilarity = Math.max(0, Math.min(100, (1 - params.semanticCosineDistance) * 100));

  const totalScore = Math.round(
    params.explicitScore * 0.35 +
    params.implicitScore * 0.25 +
    semanticSimilarity * 0.40
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
