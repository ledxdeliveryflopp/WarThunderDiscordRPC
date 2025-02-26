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
	RefreshTime time.Duration `json:"refresh_time"`
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
	if err != nil {
		log.Panicln(err)
	}
	if settings == (PresenceSettings{}) {
		fmt.Println("Empty settings file")
		fmt.Println("Close application...")
		time.Sleep(5 * time.Second)
		os.Exit(3)
	}
	if settings.RefreshTime < 5 {
		fmt.Println("The refresh timer cannot be less than 5")
		fmt.Println("Close application...")
		time.Sleep(5 * time.Second)
		os.Exit(3)
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
