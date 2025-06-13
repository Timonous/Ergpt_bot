FROM golang:1.24 AS builder

WORKDIR /usr/local/src

COPY ["go.mod", "go.sum", "./"]
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o ./bin/app cmd/main/main.go

FROM alpine AS runner

WORKDIR /
COPY --from=builder /usr/local/src/bin/app /app

COPY .env .

EXPOSE 8080

CMD ["/app"]