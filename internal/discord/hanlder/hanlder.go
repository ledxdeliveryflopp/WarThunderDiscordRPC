package hanlder

import (
	configs "WT_rich_presence/internal/configs"
	discordCommon "WT_rich_presence/internal/discord"
	discordTypes "WT_rich_presence/internal/discord/types"
	gameRequests "WT_rich_presence/internal/game/api"
	"WT_rich_presence/internal/tools"
	"fmt"
	"github.com/hugolgst/rich-go/client"
	log "github.com/sirupsen/logrus"
	"net/http"
	"time"
)

// setPresence - Функция, для установки статуса в Discord
//
// Аргументы: state string - Состояние, details string - Основное описание,
// largeImg string - Ссылка или код основного изображения, largeText string - Текст основного изображения
func setPresence(state string, details string, largeImg string, largeText string, smallImg string, smallText string) error {
	err := client.SetActivity("1344195597485211790", client.Activity{
		State:      state,
		Details:    details,
		LargeImage: largeImg,
		LargeText:  largeText,
		SmallImage: smallImg,
		SmallText:  smallText,
		Timestamps: &client.Timestamps{
			Start: &discordCommon.GameTime,
		},
	})
	go tools.LogPresenceStruct(state, details, largeImg, largeText, smallImg, smallText)
	if err != nil {
		go tools.ErrorLogPresenceStruct(err, state, details, largeImg, largeText, smallImg, smallText)
		return err
	}
	fmt.Println("Success set presence.")
	return nil
}

func setGroundState(settings *configs.PresenceSettings, mainInfo *discordTypes.MainInfoStruct) error {
	var groundIndicators discordTypes.IndicatorsGroundStruct
	groundIndicators.SetGroundVehicleName(&mainInfo.VehicleGameName, settings)
	groundIndicators.SetSpeedCrewData(&mainInfo.Speed, &mainInfo.CrewTotal, &mainInfo.CrewCurrent)
	groundIndicators.SetBigImgText(settings)
	groundIndicators.SetState(settings)
	groundIndicators.SetDetails(settings)
	tools.PrintString("Setting up an ground combat presence.")
	err := setPresence(groundIndicators.State, groundIndicators.Details, groundIndicators.Img, groundIndicators.BigText, settings.MainLogoTheme, "War Thunder")
	if err != nil {
		return err
	}
	return nil
}

func setAirState(settings *configs.PresenceSettings, httpClient http.Client, mainInfo *discordTypes.MainInfoStruct) error {
	err, stateBody := gameRequests.AirStateRequest(&httpClient)
	if err != nil {
		tools.PrintString("Error while send request to WT API, maybe timeout error or json decode error, see log for info.")
		return err
	}
	var airIndicators discordTypes.IndicatorsAirStruct
	err = airIndicators.BuildTasAltitudeInfo(&stateBody)
	if err != nil {
		tools.PrintString("Error while set TAS/Altitude for vehicle, skip presence.")
		return err
	}
	airIndicators.SetAirVehicleName(&mainInfo.VehicleGameName, settings)
	airIndicators.SetVehicleImg(&mainInfo.VehicleGameName)
	airIndicators.SetBigImgText(settings)
	airIndicators.SetState(settings)
	airIndicators.SetDetails(settings)
	tools.PrintString("Setting up an air combat presence.")
	err = setPresence(airIndicators.State, airIndicators.Details, airIndicators.Img, airIndicators.BigText, settings.MainLogoTheme, "War Thunder")
	if err != nil {
		return err
	}
	return nil
}

// RunUpdatePresenceLoop - Функция, для
//
// Аргументы: state string - Состояние, details string - Основное описание,
// largeImg string - Ссылка или код основного изображения, largeText string - Текст основного изображения
func RunUpdatePresenceLoop(settings *configs.PresenceSettings, httpClient http.Client) {
	for {
		time.Sleep(settings.RefreshTime * time.Second)
		var mapData discordTypes.MapStruct
		err := gameRequests.MapRequest(&mapData, &httpClient)
		if err != nil {
			tools.PrintString("Error while send request to WT API, maybe timeout error or json decode error, see log for info.")
			continue
		}
		log.Println("-----------------------------")
		log.Printf("Map Data: %t", mapData.Valid)
		if mapData.Valid == true {
			var indicators discordTypes.MainInfoStruct
			err = gameRequests.MainInfoRequest(&indicators, &httpClient)
			if err != nil {
				tools.PrintString("Error while send request to WT API, maybe timeout error or json decode error, see log for info.")
			}
			switch {
			case indicators.ArmyType == "dummy_plane" || indicators.VehicleGameName == "dummy_plane":
				tools.PrintString("Setting up an loading presence.")
				err = setPresence(discordCommon.BasicStateDict["loading"][settings.Lang], "", settings.MainLogoTheme, "War Thunder", "", "")
				if err != nil {
					tools.PrintString("Error while set loading presence, see log for info.")
					continue
				}
			case indicators.ArmyType == "air":
				tools.PrintString("Setting up an air presence.")
				err = setAirState(settings, httpClient, &indicators)
				if err != nil {
					tools.PrintString("Error while set air presence, see log for info.")
					continue
				}
				continue
			case indicators.ArmyType == "tank":
				tools.PrintString("Setting up an ground presence.")
				err = setGroundState(settings, &indicators)
				if err != nil {
					tools.PrintString("Error while set ground presence, see log for info.")
					continue
				}
			}
		} else {
			tools.PrintString("Setting up an hangar presence.")
			err = setPresence(discordCommon.BasicStateDict["hangar"][settings.Lang], "", settings.MainLogoTheme, "War Thunder", "", "")
			if err != nil {
				tools.PrintString("Error while set hangar presence, see log for info.")
				continue
			}
			continue
		}
	}
}
