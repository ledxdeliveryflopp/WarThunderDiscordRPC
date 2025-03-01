package main

import (
	config "WT_rich_presence/internal/configs"
	discordHanlder "WT_rich_presence/internal/discord/hanlder"
	discordInit "WT_rich_presence/internal/discord/init"
	collector "WT_rich_presence/internal/tools"
	"fmt"
	log "github.com/sirupsen/logrus"
	"time"
)

func main() {
	config.InitLogrus()
	settings := config.InitPresenceSettings()
	httpClient := config.InitHttpClient()
	err := discordInit.ConnectDiscordRPC("1344195597485211790")
	if err != nil {
		fmt.Println("Error while connecting to Discord RPC.")
		time.Sleep(5 * time.Second)
		log.Panicln(err)
		return
	}
	collector.InitCollectorTxt()
	fmt.Println("Start updating presence")
	log.Println("start logging main loop")
	log.Println("----------------------------------------------")
	discordHanlder.RunUpdatePresenceLoop(&settings, *httpClient)
}
