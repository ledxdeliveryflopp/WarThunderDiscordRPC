package main

import (
	config "WT_rich_presence/internal/configs"
	discordHanlder "WT_rich_presence/internal/discord/hanlder"
	discordInit "WT_rich_presence/internal/discord/init"
	"fmt"
)

func main() {
	config.InitLogrus()
	settings := config.InitPresenceSettings()
	httpClient := config.InitHttpClient()
	err := discordInit.ConnectDiscordRPC("1344195597485211790")
	if err != nil {
		return
	}
	fmt.Println("Start updating presence")
	discordHanlder.RunUpdatePresenceLoop(&settings, *httpClient)
}
