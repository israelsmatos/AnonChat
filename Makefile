INT=$(shell which python3)
FLAG=-Bv
TARGET=main.py

main:
	$(INT) $(FLAG) $(TARGET)

clean:
	rm -rf __pycache__ *.pyc *.log