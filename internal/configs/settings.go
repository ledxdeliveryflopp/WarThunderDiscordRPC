package configs

import (
	"encoding/json"
	"fmt"
	log "github.com/sirupsen/logrus"
	"net/http"
	"os"
	"time"
)

type PresenceSettings struct {
	RefreshTime   time.Duration `json:"refresh_time"`
	MainLogoTheme string        `json:"main_logo_theme"`
}

func InitPresenceSettings() PresenceSettings {
	fileData, err := os.ReadFile("settings.json")
	if err != nil {
		fmt.Println("An error occurred when opening settings.json, see log for info")
		fmt.Println("Close application...")
		time.Sleep(3 * time.Second)
		log.Panicln(err)
	}
	var settings PresenceSettings
	err = json.Unmarshal(fileData, &settings)
	switch {
	case err != nil:
		fmt.Println("An error occurred when reading settings.json, see log for info")
		fmt.Println("Close application...")
		time.Sleep(5 * time.Second)
		log.Panicln(err)
	case settings == (PresenceSettings{}):
		fmt.Println("Empty settings file")
		fmt.Println("Close application...")
		time.Sleep(5 * time.Second)
		os.Exit(3)
	case settings.RefreshTime < 5:
		fmt.Println("The refresh timer cannot be less than 5")
		fmt.Println("Close application...")
		time.Sleep(5 * time.Second)
		os.Exit(3)
	case settings.MainLogoTheme != "main_red" == true:
		if settings.MainLogoTheme != "main_white" == true {
			fmt.Println("Bad main logo key, set white theme")
			settings.MainLogoTheme = "main_white"
		}
	}

	return settings
}

func InitHttpClient() *http.Client {
	client := &http.Client{
		Timeout: 5 * time.Second,
	}
	log.Println("Http client inited")
	return client
}
