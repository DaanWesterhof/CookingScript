SOURCES := compiled_cook.asm

HEADERS :=

SEARCH :=

TARGET = arduino_due

SERIAL_PORT := COM3

include MakeCompile

# set REATIVE to the next higher directory
# and defer to the Makefile.due there
RELATIVE := $(RELATIVE)../
include $(RELATIVE)Makefile.due