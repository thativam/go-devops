# Step 1: Build the Go app
FROM golang:1.24.2 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod tidy

COPY . .

# 👇 This is key for Alpine compatibility
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Step 2: Minimal runtime image
FROM alpine:latest

RUN apk --no-cache add ca-certificates

COPY --from=builder /app/main /main

EXPOSE 8080

CMD ["/main"]
