package api

import (
	discordTypes "WT_rich_presence/internal/discord/types"
	"WT_rich_presence/internal/tools"
	"encoding/json"
	"io"
	"net/http"
)

func MainInfoRequest(indicators *discordTypes.MainInfoStruct, httpClient *http.Client) error {
	indicatorsResponse, err := httpClient.Get("http://127.0.0.1:8111/indicators")
	if err != nil {
		tools.ErrorLog("error while make main info request", err)
		return err
	}
	err = json.NewDecoder(indicatorsResponse.Body).Decode(&indicators)
	if err != nil {
		tools.ErrorLog("error while decode response body in main info", err)
		return err
	}
	return nil
}

func MapRequest(mapData *discordTypes.MapStruct, httpClient *http.Client) error {
	mapResponse, err := httpClient.Get("http://127.0.0.1:8111/map_info.json")
	if err != nil {
		tools.ErrorLog("error while make map request", err)
		return err
	}
	err = json.NewDecoder(mapResponse.Body).Decode(&mapData)
	if err != nil {
		tools.ErrorLog("error while decode map json", err)
		return err
	}
	return nil
}

func AirStateRequest(httpClient *http.Client) (error, io.Reader) {
	stateResponse, err := httpClient.Get("http://127.0.0.1:8111/state")
	if err != nil {
		tools.ErrorLog("error while make state request", err)
		return err, nil
	}
	return nil, stateResponse.Body
}
