package types

import (
	"WT_rich_presence/internal/configs"
	discordCommon "WT_rich_presence/internal/discord"
	collectorTools "WT_rich_presence/internal/tools"
	"fmt"
	"io"
	"strings"
)

type IndicatorsAirStruct struct {
	ReadableVehicleName string
	Altitude            string
	TasSpeed            string

	Img     string
	Details string
	State   string
	BigText string
}

func (s *IndicatorsAirStruct) SetVehicleImg(vehicleGameName *string) {
	s.Img = fmt.Sprintf("https://static.encyclopedia.warthunder.com/images/%s.png", *vehicleGameName)
	return
}

func (s *IndicatorsAirStruct) SetAirVehicleName(vehicleGameName *string, settings *configs.PresenceSettings) {
	readableName := discordCommon.VehicleAirDict[*vehicleGameName][settings.Lang]
	if readableName == "" {
		go collectorTools.SaveBasicVehicleName(vehicleGameName)
		strippedName := strings.Replace(*vehicleGameName, "_", " ", -1)
		s.ReadableVehicleName = strippedName
		return
	}
	s.ReadableVehicleName = readableName
	return

}

func (s *IndicatorsAirStruct) BuildTasAltitudeInfo(body *io.Reader) error {
	bodyBytes, err := io.ReadAll(*body)
	if err != nil {
		return err
	}
	bodyString := string(bodyBytes)
	altitudeSplit := strings.Split(bodyString, ":")[8]
	s.Altitude = strings.Split(altitudeSplit, ",")[0]
	tasSplit := strings.Split(bodyString, ":")[9]
	s.TasSpeed = strings.Split(tasSplit, ",")[0]
	return nil
}

func (s *IndicatorsAirStruct) SetBigImgText(settings *configs.PresenceSettings) {
	if settings.AltPresence == true {
		s.BigText = fmt.Sprintf("%s: %s | %s: %s m", discordCommon.StatesDict["speed_tas"][settings.Lang],
			s.TasSpeed, discordCommon.StatesDict["altitude"][settings.Lang], s.Altitude)
		return
	} else {
		s.BigText = s.ReadableVehicleName
		return
	}
}

func (s *IndicatorsAirStruct) SetState(settings *configs.PresenceSettings) {
	if settings.AltPresence == false {
		s.State = fmt.Sprintf("%s: %s | %s: %s m", discordCommon.StatesDict["speed_tas"][settings.Lang],
			s.TasSpeed, discordCommon.StatesDict["altitude"][settings.Lang], s.Altitude)
		return
	} else {
		s.State = ""
		return
	}
}

func (s *IndicatorsAirStruct) SetDetails(settings *configs.PresenceSettings) {
	s.Details = fmt.Sprintf("%s: %s", discordCommon.StatesDict["play_on"][settings.Lang], s.ReadableVehicleName)
	return
}
