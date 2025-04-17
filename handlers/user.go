package handlers

import (
    "net/http"
    "github.com/gin-gonic/gin"
	"devops/models"
)

func GetUsers(c *gin.Context) {
    users := []models.User{
        {ID: 1, Name: "Alice"},
        {ID: 2, Name: "Bob"},
    }
    c.JSON(http.StatusOK, users)
}

func CreateUser(c *gin.Context) {
    var newUser models.User
    if err := c.BindJSON(&newUser); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, newUser)
}
