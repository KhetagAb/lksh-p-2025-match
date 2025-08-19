mode := dev

up:
	cd core && make up mode=$(mode)
	cd bff && make up mode=$(mode)

down:
	cd core && make stop mode=$(mode)
	cd bff && make stop mode=$(mode)

rm:
	cd core && make rm mode=$(mode)
	cd bff && make rm mode=$(mode)