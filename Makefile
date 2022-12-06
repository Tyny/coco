run:
	./env/bin/python ./src/main.py ./examples/compras7.csv ./template.txt output.txt

debug:
	DEBUG=1 ./env/bin/python ./src/main.py ./examples/compras7.csv ./template.txt output.txt

