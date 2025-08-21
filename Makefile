mode := dev

up:
	cd core && make up mode=$(mode)
	cd bff && make up mode=$(mode)

stop:
	cd bff && make stop mode=$(mode)
	cd core && make stop mode=$(mode)

down:
	cd bff && make down mode=$(mode)
	cd core && make down mode=$(mode)

rm:
	cd core && make rm mode=$(mode)
	cd bff && make rm mode=$(mode)