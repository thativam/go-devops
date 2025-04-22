package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
)

type Service struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Address string `json:"address"`
	Port    int    `json:"port"`
}

var (
	services = make(map[string]Service)
	mu       sync.Mutex
)

func main() {
	http.HandleFunc("/register", registerService)
	http.HandleFunc("/services", listServices)

	log.Println("Service registry is running on port 3000")
	log.Fatal(http.ListenAndServe(":3000", nil))
}

func registerService(w http.ResponseWriter, r *http.Request) {
	var s Service
	if err := json.NewDecoder(r.Body).Decode(&s); err != nil {
		http.Error(w, "Invalid service data", http.StatusBadRequest)
		return
	}

	mu.Lock()
	defer mu.Unlock()

	services[s.ID] = s

	log.Printf("Service %s registered", s.Name)
	w.WriteHeader(http.StatusOK)
}

func listServices(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	serviceList := []Service{}
	for _, s := range services {
		serviceList = append(serviceList, s)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(serviceList)
}
