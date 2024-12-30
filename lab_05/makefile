run:
	@go run  cmd/main/main.go

build:
	@go build -o app.exe cmd/main/main.go

tidy:
	@go mod tidy

db:
	cd ./deployment && sudo docker compose up --build -d