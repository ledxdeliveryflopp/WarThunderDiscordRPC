package configs

import (
	"fmt"
	log "github.com/sirupsen/logrus"
	"os"
)

func InitLogrus() {
	file, err := os.OpenFile("logrus.log", os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		fmt.Println("Cant create log file:", err)
		log.SetOutput(os.Stdout)
		log.Println("Using standard stdout for logging")
		return
	}
	log.SetOutput(file)
	log.Info("Logrus initer")
}
