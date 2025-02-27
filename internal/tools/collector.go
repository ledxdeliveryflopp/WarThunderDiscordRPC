package tools

import (
	"bufio"
	"errors"
	log "github.com/sirupsen/logrus"
	"os"
	"strings"
)

func checkVehicleNameAdded(name string) bool {
	file, err := os.Open("vehicle.txt")
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Error("error occurred while open collector file for check:", err)
		return false
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.Contains(line, name) == true {
			return true
		}
	}
	return false
}

func InitCollectorTxt() {
	_, err := os.Stat("vehicle.txt")
	if errors.Is(err, os.ErrNotExist) {
		_, err = os.Create("vehicle.txt")
		if err != nil {
			log.Println("-----------------------------------------------------------------")
			log.Error("error occurred while create collector file:", err)
			return
		}
		log.Infof("collector file inited")
		return
	} else {
		log.Infof("collector file already exist.")
		return
	}
}

func SaveBasicVehicleName(name *string) {
	file, err := os.OpenFile("vehicle.txt", os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Error("error occurred while open collector file for write:", err)
		return
	}
	defer file.Close()
	check := checkVehicleNameAdded(*name)
	if check == true {
		return
	}
	writer := bufio.NewWriter(file)
	_, err = writer.WriteString(*name + "\n")
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Error("error occurred while write string in collector file:", err)
		return
	}
	err = writer.Flush()
	if err != nil {
		log.Println("-----------------------------------------------------------------")
		log.Error("error occurred while flushing a buffer:", err)
		return
	}
	return
}
