package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

type Service struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Address string `json:"address"`
	Port    int    `json:"port"`
}

var (
	serviceRegistryURL = getEnv("SERVICE_REGISTRY_URL", "http://service-discovery:3000/services")
	services           []Service
	mu                 sync.RWMutex
)

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}

// Fetch services every 10 seconds
func startServicePolling() {
	ticker := time.NewTicker(10 * time.Second)
	go func() {
		for range ticker.C {
			updateServiceList()
		}
	}()
	updateServiceList() // do it once on start
}

func updateServiceList() {
	resp, err := http.Get(serviceRegistryURL)
	if err != nil {
		log.Printf("Failed to get services: %v", err)
		return
	}
	defer resp.Body.Close()

	var updated []Service
	body, _ := io.ReadAll(resp.Body)
	err = json.Unmarshal(body, &updated)
	if err != nil {
		log.Printf("Failed to decode services: %v", err)
		return
	}

	mu.Lock()
	defer mu.Unlock()
	services = updated
	log.Printf("Updated service list: %d services available", len(services))
}

func getRandomService() *Service {
	mu.RLock()
	defer mu.RUnlock()

	if len(services) == 0 {
		return nil
	}
	return &services[rand.Intn(len(services))]
}

func proxyHandler(c *gin.Context) {
	target := getRandomService()
	if target == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "No services available"})
		return
	}

	targetURL := &url.URL{
		Scheme: "http",
		Host:   target.Address + ":" + itoa(target.Port),
	}
	fmt.Println("Proxying to:", targetURL.String())
	proxy := httputil.NewSingleHostReverseProxy(targetURL)

	c.Request.URL.Scheme = targetURL.Scheme
	c.Request.URL.Host = targetURL.Host
	c.Request.Host = targetURL.Host

	proxy.ServeHTTP(c.Writer, c.Request)
}

func itoa(n int) string {
	return fmt.Sprintf("%d", n)
}

func main() {
	rand.Seed(time.Now().UnixNano())
	startServicePolling()

	router := gin.Default()
	router.Any("/*proxyPath", proxyHandler)

	log.Println("Load balancer running on :8080")
	router.Run(":8080")
}
