package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"time"

	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/mem"
	"github.com/shirou/gopsutil/net"
)

// Status struct
type Status struct {
	CPU  float64 `json:"cpu"`
	RAM  uint64  `json:"ram"`
	Net  uint64  `json:"net"`
}

func getStatus() Status {
	// Get CPU Usage
	percent, _ := cpu.Percent(time.Second, false)

	// Get RAM Usage
	memStats, _ := mem.VirtualMemory()

	// Get Network Usage
	netStats, _ := net.IOCounters(false)

	return Status{
		CPU: percent[0],
		RAM: memStats.Used / 1024 / 1024, // MB
		Net: netStats[0].BytesRecv / 1024, // KB
	}
}

func main() {
	// Open socket to Rust bar
	ln, err := net.Listen("tcp", "127.0.0.1:8080")
	if err != nil {
		log.Fatal(err)
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Println(err)
			continue
		}

		go func(c net.Conn) {
			defer c.Close()
			for {
				status := getStatus()
				data, _ := json.Marshal(status)
				c.Write(data)
				time.Sleep(1 * time.Second)
			}
		}(conn)
	}
}
