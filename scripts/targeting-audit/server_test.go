package main

// Copied into a disposable, pinned recommender checkout by run.py.
// Calls the production HTTP handler, not a reimplementation of its matcher or ranker.
import (
	"encoding/json"
	"github.com/grafana/grafana-recommender/internal/recommender"
	"go.uber.org/zap"
	"os"
	"reflect"
	"strconv"
	"testing"
)

type auditScenario struct {
	Name    string                            `json:"name"`
	Context recommender.RecommendationContext `json:"context"`
	Include []string                          `json:"include"`
	Exclude []string                          `json:"exclude"`
}
type auditInput struct {
	Before    []V1Rule        `json:"before"`
	After     []V1Rule        `json:"after"`
	Scenarios []auditScenario `json:"scenarios"`
}

func TestTutorialCatalogAudit(t *testing.T) {
	setupV1RecommendHandlerTest(t)
	logger = zap.NewNop().Sugar()
	ruleRecommender = recommender.NewMockRuleRecommenderWithData(nil)
	var input auditInput
	data, err := os.ReadFile(os.Getenv("AUDIT_INPUT"))
	if err != nil {
		t.Fatal(err)
	}
	if err = json.Unmarshal(data, &input); err != nil {
		t.Fatal(err)
	}
	output := map[string]map[string]map[string][]V1Recommendation{}
	for _, phase := range []string{"before", "after"} {
		rules := input.Before
		if phase == "after" {
			rules = input.After
		}
		populatePackageRules(t, rules)
		output[phase] = map[string]map[string][]V1Recommendation{}
		for _, scenario := range input.Scenarios {
			output[phase][scenario.Name] = map[string][]V1Recommendation{}
			for _, cap := range []int{10000, 10, 3} {
				t.Setenv("MAX_RECOMMENDATIONS", strconv.Itoa(cap))
				w := postV1Recommend(t, scenario.Context)
				if w.Code != 200 {
					t.Fatalf("%s: HTTP %d: %s", scenario.Name, w.Code, w.Body.String())
				}
				var response V1RecommenderResponse
				if err := json.Unmarshal(w.Body.Bytes(), &response); err != nil {
					t.Fatal(err)
				}
				output[phase][scenario.Name][strconv.Itoa(cap)] = response.Recommendations
				if phase == "after" && cap == 10000 {
					ids := map[string]bool{}
					for _, r := range response.Recommendations {
						if r.Manifest != nil {
							ids[r.Manifest.ID] = true
						}
					}
					for _, id := range scenario.Include {
						if !ids[id] {
							t.Errorf("%s: missing %s", scenario.Name, id)
						}
					}
					for _, id := range scenario.Exclude {
						if ids[id] {
							t.Errorf("%s: unexpectedly admitted %s", scenario.Name, id)
						}
					}
				}
			}
			full := output[phase][scenario.Name]["10000"]
			for _, cap := range []int{3, 10} {
				want := full
				if len(want) > cap {
					want = want[:cap]
				}
				if !reflect.DeepEqual(want, output[phase][scenario.Name][strconv.Itoa(cap)]) {
					t.Errorf("%s/%s: cap %d changed ordering", phase, scenario.Name, cap)
				}
			}
		}
	}
	data, err = json.Marshal(output)
	if err != nil {
		t.Fatal(err)
	}
	if err = os.WriteFile(os.Getenv("AUDIT_OUTPUT"), data, 0600); err != nil {
		t.Fatal(err)
	}
}
