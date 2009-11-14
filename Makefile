all: clean unclean build-static build-posts build-archive build-rss copy-data

clean:
	rm -rf output
	rm -rf build/*.pyc

unclean:
	mkdir output

build-posts:
	python ./build/buildPosts.py

build-static:
	python ./build/buildStatic.py

build-archive:
	python ./build/buildArchive.py

build-rss:
	python ./build/buildRSS.py

copy-data:
	cp -r images output/images
	cp -r styles output/styles
	cp -r scripts output/scripts

.PHONY: build-posts build-static build-archive all clean copy-data
