package configs

import (
	log "github.com/sirupsen/logrus"
	"os"
)

func InitLogrus() {
	file, err := os.OpenFile("logrus.log", os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Panicln(err)
		return
	}
	log.SetOutput(file)
	log.SetReportCaller(true)
	log.Info("Logrus initer")
}
