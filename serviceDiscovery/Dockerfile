FROM golang:1.24.2 AS build
WORKDIR /app
COPY . .
RUN go mod tidy
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=build /app/main /main
EXPOSE 3000
CMD ["/main"]
