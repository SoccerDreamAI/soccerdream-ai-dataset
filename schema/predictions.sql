-- The table design behind data/graded_predictions.csv.
-- Constraints do the enforcing; application code is where discipline goes to die.

CREATE TABLE predictions (
    id              bigserial PRIMARY KEY,
    model_id        bigint      NOT NULL REFERENCES models(id),
    fixture_id      bigint      NOT NULL REFERENCES fixtures(id),
    p_home          numeric(5,4) NOT NULL CHECK (p_home BETWEEN 0 AND 1),
    p_draw          numeric(5,4) NOT NULL CHECK (p_draw BETWEEN 0 AND 1),
    p_away          numeric(5,4) NOT NULL CHECK (p_away BETWEEN 0 AND 1),
    created_at      timestamptz NOT NULL DEFAULT now(),
    content_hash    text        NOT NULL,
    prev_hash       text,
    inputs_snapshot jsonb       NOT NULL,
    UNIQUE (model_id, fixture_id)
);

ALTER TABLE predictions
  ADD CONSTRAINT probs_sum_to_one
  CHECK (abs(p_home + p_draw + p_away - 1) < 0.001);

-- Grading happens exactly once. The primary key makes a second grade
-- of the same prediction a physical impossibility.
CREATE TABLE grades (
    prediction_id bigint PRIMARY KEY REFERENCES predictions(id),
    outcome       char(1) NOT NULL CHECK (outcome IN ('H','D','A')),
    brier         numeric(6,5) NOT NULL,
    graded_at     timestamptz NOT NULL DEFAULT now(),
    result_id     bigint NOT NULL REFERENCES results(id)
);

-- Nothing in this schema permits UPDATE of a probability.
-- A wrong prediction stays wrong, with its timestamp intact.
