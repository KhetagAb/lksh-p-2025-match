package main

import (
	"fmt"
	"match/internal/transport"
)

func main() {
	server := transport.GetServer()
	fmt.Println("Pomidorka")
	transport.RunServer(server)
}
