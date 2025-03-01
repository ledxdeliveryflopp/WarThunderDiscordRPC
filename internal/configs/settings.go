package configs

import (
	"encoding/json"
	"fmt"
	langOs "github.com/cloudfoundry-attic/jibber_jabber"
	log "github.com/sirupsen/logrus"
	"net/http"
	"os"
	"time"
)

type PresenceSettings struct {
	RefreshTime   time.Duration `json:"refresh_time"`
	MainLogoTheme string        `json:"main_logo_theme"`
	AltPresence   bool          `json:"alt_presence"`
	Lang          string        `json:"lang"`
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
		fmt.Println("Set basic settings")
		settings.Lang = "en"
		settings.AltPresence = false
		settings.RefreshTime = 7
		settings.MainLogoTheme = "main_white"
		log.Println("Set basic settings success")
	case settings.RefreshTime < 5:
		fmt.Println("The refresh timer cannot be less than 5")
		fmt.Println("Set 7 sec refresh time")
		settings.RefreshTime = 7
	case settings.MainLogoTheme != "main_red" == true:
		if settings.MainLogoTheme != "main_white" == true {
			fmt.Println("Bad main logo key, set white theme")
			settings.MainLogoTheme = "main_white"
		}
	case settings.Lang != "ru" == true || settings.Lang != "en" == true:
		systemName, err := langOs.DetectLanguage()
		if err != nil {
			fmt.Println("Error while get system lang, set en lang")
			log.Errorf("error while get system lang: %s", err)
			settings.Lang = "en"
		} else if systemName == "ru" == true || systemName == "en" == true {
			fmt.Printf("Detected system lang, lang code - %s. Set %s lang. \n", systemName, systemName)
			settings.Lang = systemName
		} else {
			fmt.Printf("unknown system lang - %s, set en lang \n", systemName)
			settings.Lang = "en"
		}
	}
	log.Println("settings inited")
	log.Infof("Settings: %+v", settings)
	return settings
}

func InitHttpClient() *http.Client {
	client := &http.Client{
		Timeout: 5 * time.Second,
	}
	log.Println("Http client inited")
	return client
}
