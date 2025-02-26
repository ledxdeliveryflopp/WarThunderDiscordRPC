package types

import (
	discordCommon "WT_rich_presence/internal/discord"
	"fmt"
	"strings"
	"sync"
)

type IndicatorsStruct struct {
	Vehicle         string `json:"type"`
	FixedTankName   string
	ReadableVehicle string
	Army            string  `json:"army"`
	SpeedTank       float64 `json:"speed"`
	CrewTotal       float64 `json:"crew_total"`
	CrewCurrent     float64 `json:"crew_current"`
	Img             string
}

func (s *IndicatorsStruct) FixAirVehicleName(wg *sync.WaitGroup) {
	readableName := discordCommon.VehicleAirDict[s.Vehicle]
	defer wg.Done()
	if readableName == "" {
		strippedName := strings.Replace(s.Vehicle, "_", " ", -1)
		s.ReadableVehicle = strippedName
		return
	}
	s.ReadableVehicle = readableName
	return
}

func (s *IndicatorsStruct) BuildTankInfo() {
	fixedName := strings.Replace(s.Vehicle, "tankModels/", "", 1)
	s.FixedTankName = fixedName
	s.Img = fmt.Sprintf("https://static.encyclopedia.warthunder.com/images/%s.png", s.FixedTankName)
	readableName := discordCommon.VehicleGroundDict[s.FixedTankName]
	if readableName == "" {
		fmt.Println(s.FixedTankName)
		strippedName := strings.Replace(s.FixedTankName, "_", " ", -1)
		s.ReadableVehicle = strippedName
		return
	}
	s.ReadableVehicle = readableName
	return
}
