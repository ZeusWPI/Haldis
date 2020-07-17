# Find a SASS preprocessor
SASS := $(shell command -v sass 2>/dev/null)
ifndef SASS
SASS := $(shell command -v sassc 2>/dev/null)
endif
ifndef SASS
$(error No SASS preprocessor found)
endif

SASSFLAGS := --sourcemap=auto --

.PHONY: all clean

# Detect SCSS files, use their CSS counterparts as `all` target
SCSS_FILES := $(wildcard *.scss)
all: $(SCSS_FILES:%.scss=%.css)

# Teach Make how to convert SCSS to CSS
%.css: %.scss
	$(SASS) $(SASSFLAGS) $< $@

clean:
	rm -rf $(SCSS_FILES:%.scss=%.css) $(SCSS_FILES:%.scss=%.css.map)
