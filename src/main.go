package main

import (
	"bytes"
	"devops/config"
	"devops/routes"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
)

type Service struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Address string `json:"address"`
	Port    int    `json:"port"`
}

func main() {
	config.ConnectDatabase()
	r := gin.Default()
	routes.SetupRoutes(r)

	// Get a random available port by binding to ":0"
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("Failed to get a random available port: %v", err)
	}
	// Extract actual host:port info
	// port := ln.Addr().(*net.TCPAddr).Port
	addr := os.Getenv("HOST_NAME")
	if addr == "" {
		log.Println(err)
		addr, _ = os.Hostname() // Fallback to localhost if hostname retrieval fails
	}
	log.Println("Using address: ", addr)

	log.Printf("Service started on port %d", 8080)

	// Register service in a goroutine (non-blocking)
	go registerService("go-api", addr, 8080)

	// Serve using the existing listener
	if err := r.RunListener(ln); err != nil {
		log.Fatalf("Failed to start Gin: %v", err)
	}

}

func registerService(name, address string, port int) {
	serviceID := fmt.Sprintf("%s-%d", name, port) // Unique ID based on service name and port

	service := Service{
		ID:      serviceID,
		Name:    name,
		Address: address,
		Port:    port,
	}

	// Marshal the service into JSON
	serviceData, err := json.Marshal(service)
	if err != nil {
		log.Fatalf("Failed to marshal service data: %v", err)
	}
	serviceHost := os.Getenv("SERVICE_HOST")
	if serviceHost == "" {
		serviceHost = "localhost"
	}
	// Send the registration request to the service registry
	registrationURL := "http://" + serviceHost + ":3000/register"
	fmt.Println("Service registration URL: " + registrationURL)
	req, err := http.NewRequest("POST", registrationURL, bytes.NewBuffer(serviceData))
	if err != nil {
		log.Fatalf("Failed to create registration request: %v", err)
	}

	req.Header.Set("Content-Type", "application/json")

	// Make the HTTP request to register the service
	client := &http.Client{Timeout: 5 * time.Second} // Add a timeout for robustness
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalf("Failed to register service: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		log.Fatalf("Failed to register service, status code: %d", resp.StatusCode)
	}

	log.Printf("Service registered successfully: %s:%d", address, port)
}
