package evaluator

type Evaluator struct {
	rubric *Rubric
}

func NewEvaluator(rubric *Rubric) *Evaluator {
	return &Evaluator{
		rubric: rubric,
	}
}

func (e *Evaluator) Score(essay string) (float64, error) {
	// In a real implementation, this would use the rubric to score the essay.
	// For now, it returns a dummy score.
	return 0.85, nil
}