# Set the base image to use
FROM golang:1.13-alpine

# Set the working directory inside the container
WORKDIR /go

# Copy the Go modules file to the container
RUN apk add --no-cache git --repository https://alpine.global.ssl.fastly.net/alpine/v3.13/community --repository https://alpine.global.ssl.fastly.net/alpine/v3.13/main
RUN go get github.com/jasonlvhit/gocron
RUN go get github.com/lib/pq

# Copy the Go source code to the container
COPY . .

# Build the Go binary inside the container
RUN go build -o main .



# Expose the port that the application will listen on
EXPOSE 8080

# Start the application inside the container
CMD ["./main"]
