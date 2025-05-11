package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
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

var (
	lb *LoadBalancer
)

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}

// Fetch services every 10 seconds
func startServicePolling() {
	ticker := time.NewTicker(20 * time.Second)
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

func proxyHandler(c *gin.Context) {
	target := lb.strategy.getNextService(&services)
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
	startServicePolling()
	lb = initLb(&RoundRobin{})
	router := gin.Default()
	log.Println("Default Lb strategy to: RR")
	router.OPTIONS("/lb/strategy/:strategy", func(c *gin.Context) {
		strategy := c.Param("strategy")
		log.Println("Setting strategy to:", strategy)

		switch strategy {
		case "roundrobin":
			lb.setStrategyAlgo(&RoundRobin{})
		case "random":
			lb.setStrategyAlgo(&Rmd{})
		default:
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid strategy"})
		}
	})
	router.GET("/*proxyPath", proxyHandler)
	router.POST("/*proxyPath", proxyHandler)
	router.PUT("/*proxyPath", proxyHandler)
	router.DELETE("/*proxyPath", proxyHandler)
	log.Println("Load balancer running on :8080")
	router.Run(":8080")
}
