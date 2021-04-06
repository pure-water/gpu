all: wrap.dylib demo-bin disasm-bin
.PHONY: clean all
.SUFFIXES:

clean:
	rm -f wrap.dylib demo-bin agx_pack.h

CFLAGS := -g -Wall -Werror -Wextra -Wno-unused-variable -Wno-unused-function
WRAP_SRCS := $(wildcard lib/*.c)\
             $(wildcard wrap/*.c)

wrap.dylib: $(WRAP_SRCS) Makefile agx_pack.h
	clang -o $@ $(WRAP_SRCS) -I lib/ -dynamiclib -framework IOKit $(CFLAGS)

DEMO_SRCS := $(wildcard lib/*.c)\
             $(wildcard demo/*.c)\
             $(wildcard disasm/*.c)

demo-bin: $(DEMO_SRCS) Makefile agx_pack.h
	clang -o $@ $(DEMO_SRCS) -I lib/ -I /opt/X11/include -L /opt/X11/lib/ -lX11 -framework IOKit $(CFLAGS)

agx_pack.h: lib/gen_pack.py lib/cmdbuf.xml Makefile
	python3 lib/gen_pack.py lib/cmdbuf.xml > agx_pack.h

DISASM_SRCS := $(wildcard disasm/*.c)\
             disasm-driver.c

disasm-bin: $(DISASM_SRCS) Makefile
	clang -o $@ $(DISASM_SRCS) $(CFLAGS)
