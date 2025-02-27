package hanlder

import (
	configs "WT_rich_presence/internal/configs"
	discordCommon "WT_rich_presence/internal/discord"
	discordTypes "WT_rich_presence/internal/discord/types"
	gameRequests "WT_rich_presence/internal/game/api"
	"fmt"
	"github.com/hugolgst/rich-go/client"
	log "github.com/sirupsen/logrus"
	"net/http"
	"sync"
	"time"
)

// setPresence - Функция, для установки статуса в Discord
//
// Аргументы: state string - Состояние, details string - Основное описание,
// largeImg string - Ссылка или код основного изображения, largeText string - Текст основного изображения
func setPresence(state string, details string, largeImg string, largeText string, smallImg string, smallText string) {
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
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Error("error while set presence: ", err)
		log.Infof("State: %s", state)
		log.Infof("Details: %s", details)
		log.Infof("largeImg: %s", largeImg)
		log.Infof("largeText: %s", largeText)
		log.Infof("SmallImg: %s", smallImg)
		log.Infof("largeText: %s", smallText)
		return
	}
	fmt.Println("Presence set success")
	return
}

// RunUpdatePresenceLoop - Функция, для
//
// Аргументы: state string - Состояние, details string - Основное описание,
// largeImg string - Ссылка или код основного изображения, largeText string - Текст основного изображения
func RunUpdatePresenceLoop(settings *configs.PresenceSettings, httpClient http.Client) {
	wg := new(sync.WaitGroup)
	for {
		wg.Add(2)
		time.Sleep(settings.RefreshTime * time.Second)
		var indicators discordTypes.IndicatorsStruct
		var mapData discordTypes.MapStruct
		indicatorsErrorChan := make(chan error)
		mapErrorChan := make(chan error)
		go gameRequests.IndicatorsRequest(indicatorsErrorChan, wg, &indicators, &httpClient)
		go gameRequests.MapRequest(mapErrorChan, wg, &mapData, &httpClient)
		errIndicators := <-indicatorsErrorChan
		errMap := <-mapErrorChan
		wg.Wait()
		close(indicatorsErrorChan)
		close(mapErrorChan)
		switch {
		case errIndicators != nil:
			fmt.Println("Error while send request to WT API, maybe timeout error or json decode error")
			continue
		case errMap != nil:
			fmt.Println("Error while send request to WT API, maybe timeout error or json decode error")
			continue
		}
		switch {
		case indicators.Vehicle == "dummy_plane" && mapData.Valid == true:
			setPresence("loading", "", settings.MainLogoTheme, "War Thunder", "", "")
			continue
		case indicators.Army == "air" && mapData.Valid == true:
			indicators.Img = fmt.Sprintf("https://static.encyclopedia.warthunder.com/images/%s.png", indicators.Vehicle)
			wg.Add(2)
			ErrorChan := make(chan error)
			var indicatorsTasAltitude discordTypes.TasAltitudeStruct
			go gameRequests.StateRequest(ErrorChan, &indicatorsTasAltitude, wg, &httpClient)
			go indicators.FixAirVehicleName(wg)
			err := <-ErrorChan
			wg.Wait()
			close(ErrorChan)
			if err != nil {
				fmt.Println("Error while building air state info, see log for info")
				continue
			}
			state := fmt.Sprintf("Speed Tas: %s | Altitude:%s m", indicatorsTasAltitude.TasSpeed, indicatorsTasAltitude.Altitude)
			details := fmt.Sprintf("Plays on: %s", indicators.ReadableVehicle)
			setPresence(state, details, indicators.Img, indicators.ReadableVehicle, settings.MainLogoTheme, "War Thunder")
			continue
		case indicators.Army == "tank" && mapData.Valid == true:
			indicators.BuildTankInfo()
			state := fmt.Sprintf("speed: %d | crew: %d/%d", int(indicators.SpeedTank), int(indicators.CrewTotal),
				int(indicators.CrewCurrent))
			details := fmt.Sprintf("Plays on: %s", indicators.ReadableVehicle)
			setPresence(state, details, indicators.Img, indicators.ReadableVehicle, settings.MainLogoTheme, "War Thunder")
			continue
		default:
			setPresence("In the hangar", "", settings.MainLogoTheme, "War Thunder", "", "")
			continue
		}
	}
}
