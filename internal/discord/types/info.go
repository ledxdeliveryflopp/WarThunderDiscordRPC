package types

type MainInfoStruct struct {
	ArmyType        string  `json:"army"`
	VehicleGameName string  `json:"type"`
	CrewTotal       float64 `json:"crew_total"`
	CrewCurrent     float64 `json:"crew_current"`
	Speed           float64 `json:"speed"`
}
