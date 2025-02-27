package api

import (
	discordTools "WT_rich_presence/internal/discord/tools"
	discordTypes "WT_rich_presence/internal/discord/types"
	"encoding/json"
	log "github.com/sirupsen/logrus"
	"net/http"
	"sync"
)

func IndicatorsRequest(errorChan chan error, wg *sync.WaitGroup, indicators *discordTypes.IndicatorsStruct, httpClient *http.Client) {
	indicatorsResponse, err := httpClient.Get("http://127.0.0.1:8111/indicators")
	defer wg.Done()
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Errorf("error while make indicators request: %s", err)
		errorChan <- err
		return
	}
	err = json.NewDecoder(indicatorsResponse.Body).Decode(&indicators)
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Errorf("error while decode indicators json: %s", err)
		errorChan <- err
		return
	}
	errorChan <- nil
	return
}

func MapRequest(errorChan chan error, wg *sync.WaitGroup, mapData *discordTypes.MapStruct, httpClient *http.Client) {
	mapResponse, err := httpClient.Get("http://127.0.0.1:8111/map_info.json")
	defer wg.Done()
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Errorf("error while make map request: %s", err)
		errorChan <- err
		return
	}
	err = json.NewDecoder(mapResponse.Body).Decode(&mapData)
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Errorf("error while decode map json: %s", err)
		errorChan <- err
		return
	}
	errorChan <- nil
	return
}

func StateRequest(errorChan chan error, indicatorsTasAltitude *discordTypes.TasAltitudeStruct, wg *sync.WaitGroup, httpClient *http.Client) {
	stateResponse, err := httpClient.Get("http://127.0.0.1:8111/state")
	defer wg.Done()
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Errorf("error while make state request: %s", err)
		errorChan <- err
		return
	}
	err = discordTools.BuildTasAltitudeInfo(indicatorsTasAltitude, stateResponse.Body)
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Errorf("error while build tas/altitude: %s", err)
		errorChan <- err
		return
	}
	errorChan <- nil
	return
}
