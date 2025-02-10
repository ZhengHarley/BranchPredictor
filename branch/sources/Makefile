# Compiler and flags
CC = riscv64-unknown-elf-gcc
CFLAGS = -Wall -Wextra -g -lm
QUIET_FLAG = -DQUIET

# Directories
SRC_DIR = .
OUT_DIR = elfs
TRACE_DIR = ../traces

# Tools
SPIKE = ../tools/spike
PK = ../tools/pk

# Source files and their corresponding executables
SOURCES = $(wildcard $(SRC_DIR)/*.c)
ELFS = $(patsubst $(SRC_DIR)/%.c, $(OUT_DIR)/%, $(SOURCES))
TRACE_FILES = $(patsubst $(OUT_DIR)/%, $(TRACE_DIR)/%.trace, $(ELFS))

# Default target
all: setup $(ELFS)

# Rule for quiet build
quiet: CFLAGS += $(QUIET_FLAG)
quiet: setup $(ELFS)

# Rule to compile individual .c files
$(OUT_DIR)/%: $(SRC_DIR)/%.c
	$(CC) $< $(CFLAGS) -o $@

# Traces target
traces: setup-trace $(TRACE_FILES)

# Rule to generate individual trace files
$(TRACE_DIR)/%.trace: $(OUT_DIR)/%
	$(SPIKE) --log-branches=$@ $(PK) $<

# Setup the output directory
setup:
	mkdir -p $(OUT_DIR)

setup-trace:
	mkdir -p $(TRACE_DIR)

# Clean up
clean:
	rm -rf $(OUT_DIR) $(TRACE_DIR)
