package init

import (
	"fmt"
	"github.com/hugolgst/rich-go/client"
	log "github.com/sirupsen/logrus"
)

func ConnectDiscordRPC(discordCode string) error {
	err := client.Login(discordCode)
	if err != nil {
		return err
	}
	log.Infof("discord inited with code: %s", discordCode)
	fmt.Println("Successful connection to Discord rpc")
	return nil
}
