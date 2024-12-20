export function computeConfusionMatrixMulticlass(target_true, target_pred) {
  // Lấy danh sách các lớp
  const classes = Array.from(new Set([...target_true, ...target_pred])).sort();

  // Tạo ma trận KxK (ban đầu toàn 0)
  const K = classes.length;
  const matrix = Array(K).fill(null).map(() => Array(K).fill(0));

  // Map lớp -> chỉ số
  const classIndex = {};
  classes.forEach((c, idx) => {
    classIndex[c] = idx;
  });

  // Duyệt qua tất cả các phần tử và đếm
  for (let i = 0; i < target_true.length; i++) {
    const actual = target_true[i];
    const pred = target_pred[i];
    const actualIdx = classIndex[actual];
    const predIdx = classIndex[pred];
    matrix[actualIdx][predIdx] += 1;
  }

  return { matrix, classes };
}