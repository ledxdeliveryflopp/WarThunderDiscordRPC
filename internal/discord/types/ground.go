package types

import (
	"WT_rich_presence/internal/configs"
	discordCommon "WT_rich_presence/internal/discord"
	collectorTools "WT_rich_presence/internal/tools"
	"fmt"
	"strings"
)

type IndicatorsGroundStruct struct {
	ReadableVehicleName string
	speed               float64
	TotalCrew           float64
	CurrentCrew         float64

	Img     string
	Details string
	State   string
	BigText string
}

func (s *IndicatorsGroundStruct) setVehicleImg(vehicleGameName *string) {
	s.Img = fmt.Sprintf("https://static.encyclopedia.warthunder.com/images/%s.png", *vehicleGameName)
	return
}

func (s *IndicatorsGroundStruct) SetSpeedCrewData(speed *float64, total *float64, current *float64) {
	s.speed = *speed
	s.TotalCrew = *total
	s.CurrentCrew = *current
	return
}

func (s *IndicatorsGroundStruct) SetGroundVehicleName(vehicleGameName *string, settings *configs.PresenceSettings) {
	fixedName := strings.Replace(*vehicleGameName, "tankModels/", "", 1)
	s.setVehicleImg(&fixedName)
	readableName := discordCommon.VehicleGroundDict[fixedName][settings.Lang]
	if readableName == "" {
		go collectorTools.SaveBasicVehicleName(&fixedName)
		strippedName := strings.Replace(fixedName, "_", " ", -1)
		s.ReadableVehicleName = strippedName
		return
	}
	s.ReadableVehicleName = readableName
	return
}

func (s *IndicatorsGroundStruct) SetBigImgText(settings *configs.PresenceSettings) {
	if settings.AltPresence == true {
		s.BigText = fmt.Sprintf("%s: %d | %s: %d/%d", discordCommon.VehicleStatesDict["speed_ground"][settings.Lang], int(s.speed),
			discordCommon.VehicleStatesDict["crew_count"][settings.Lang], int(s.TotalCrew), int(s.CurrentCrew))
		return
	} else {
		s.BigText = s.ReadableVehicleName
		return
	}
}

func (s *IndicatorsGroundStruct) SetState(settings *configs.PresenceSettings) {
	if settings.AltPresence == false {
		s.State = fmt.Sprintf("%s: %d | %s: %d/%d", discordCommon.VehicleStatesDict["speed_ground"][settings.Lang], int(s.speed),
			discordCommon.VehicleStatesDict["crew_count"][settings.Lang], int(s.TotalCrew), int(s.CurrentCrew))
		return
	} else {
		s.State = ""
		return
	}
}

func (s *IndicatorsGroundStruct) SetDetails(settings *configs.PresenceSettings) {
	s.Details = fmt.Sprintf("%s: %s", discordCommon.VehicleStatesDict["play_on"][settings.Lang], s.ReadableVehicleName)
	return
}
