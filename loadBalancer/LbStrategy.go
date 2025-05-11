package main

import (
	"math/rand"
)

type LbStrategy interface {
	getNextService(svcs *[]Service) *Service
}

type Rmd struct{}

func (l *Rmd) getNextService(svcsPtr *[]Service) *Service {
	mu.RLock()
	defer mu.RUnlock()
	svcs := *svcsPtr
	if len(svcs) == 0 {
		return nil
	}
	return &svcs[rand.Intn(len(services))]
}

type RoundRobin struct{}

func (l *RoundRobin) getNextService(svcsPtr *[]Service) *Service {
	mu.RLock()
	defer mu.RUnlock()
	svcs := *svcsPtr
	if len(svcs) == 0 {
		return nil
	}
	var temp = svcs[0] // remove first service
	svcs = svcs[1:]
	svcs = append(svcs, temp) // add it to the end
	*svcsPtr = svcs           // update the original slice
	return &svcs[0]
}

type LoadBalancer struct {
	strategy LbStrategy
}

func (c *LoadBalancer) setStrategyAlgo(e LbStrategy) {
	c.strategy = e
}

func initLb(e LbStrategy) *LoadBalancer {
	return &LoadBalancer{
		strategy: e,
	}
}
