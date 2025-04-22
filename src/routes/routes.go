package routes

import (
    "github.com/gin-gonic/gin"
	"devops/handlers"
)

func SetupRoutes(r *gin.Engine) {
    r.GET("/ping", handlers.Ping)
    r.GET("/users", handlers.GetUsers)
    r.POST("/users", handlers.CreateUser)
}
