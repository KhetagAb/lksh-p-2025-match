mode := dev

up:
	cd core && make up mode=$(mode)
	cd bff && make up

down:
	cd core && make down
	cd bff && make down