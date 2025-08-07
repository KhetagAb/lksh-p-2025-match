package main

import "match/internal/transport"

func main() {
	server := transport.GetServer()
	transport.RunServer(server)
}
