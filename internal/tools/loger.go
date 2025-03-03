package tools

import (
	"fmt"
	log "github.com/sirupsen/logrus"
)

func LogPresenceStruct(state string, details string, largeImg string, largeText string, smallImg string, smallText string) {
	log.Infof("State: %s", state)
	log.Infof("Details: %s", details)
	log.Infof("largeImg: %s", largeImg)
	log.Infof("largeText: %s", largeText)
	log.Infof("SmallImg: %s", smallImg)
	log.Infof("largeText: %s", smallText)
	return
}

func ErrorLogPresenceStruct(err error, state string, details string, largeImg string, largeText string, smallImg string, smallText string) {
	fmt.Println("Error while set presence, see log file for info.")
	log.Println("-----------------------------------------------------------------")
	log.Error("error while set presence: ", err)
	log.Infof("State: %s", state)
	log.Infof("Details: %s", details)
	log.Infof("largeImg: %s", largeImg)
	log.Infof("largeText: %s", largeText)
	log.Infof("SmallImg: %s", smallImg)
	log.Infof("largeText: %s", smallText)
}

func ErrorLog(details string, err error) {
	log.Println("-----------------------------------------------------------------")
	log.Errorf("%s: %s", details, err)
	return
}
