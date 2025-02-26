package tools

import (
	"bufio"
	log "github.com/sirupsen/logrus"
	"os"
	"strings"
)

func checkVehicleNameAdded(name string) bool {
	file, err := os.Open("vehicle.txt")
	if err != nil {
		log.Error("error occurred while open file", err)
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

func SaveBasicVehicleName(name *string) {
	file, err := os.OpenFile("vehicle.txt", os.O_WRONLY|os.O_CREATE|os.O_APPEND|os.O_RDONLY, 0666)
	if err != nil {
		log.Error("error occurred while create/open collector file", err)
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
		log.Error("error occurred while write string in collector file", err)
		return
	}
	err = writer.Flush()
	if err != nil {
		log.Error("error occurred while flushing a buffer", err)
		return
	}
	return
}
