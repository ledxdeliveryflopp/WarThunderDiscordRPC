package tools

import (
	discordTypes "WT_rich_presence/internal/discord/types"
	"io"
	"strings"
)

func BuildTasAltitudeInfo(indicators *discordTypes.TasAltitudeStruct, body io.Reader) error {
	bodyBytes, err := io.ReadAll(body)
	if err != nil {
		return err
	}
	bodyString := string(bodyBytes)
	altitudeSplit := strings.Split(bodyString, ":")[8]
	indicators.Altitude = strings.Split(altitudeSplit, ",")[0]
	tasSplit := strings.Split(bodyString, ":")[9]
	indicators.TasSpeed = strings.Split(tasSplit, ",")[0]
	return nil
}
