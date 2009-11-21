# hortont.com build system

all: clean unclean build-static build-posts build-archive build-rss build-everything copy-data

clean:
	rm -rf output
	rm -rf build/*.pyc

unclean:
	mkdir output

build-posts:
	python2.6 ./build/buildPosts.py

build-static:
	python2.6 ./build/buildStatic.py

build-archive:
	python2.6 ./build/buildArchive.py

build-rss:
	python2.6 ./build/buildRSS.py

build-everything:
	python2.6 ./build/buildEverything.py

new-post:
	python2.6 ./build/newPost.py

copy-data:
	cp -r images output/images
	cp -r styles output/styles
	cp -r scripts output/scripts

.PHONY: build-posts build-static build-archive all clean copy-data
