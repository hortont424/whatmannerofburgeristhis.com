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

check-links:
	python2.6 ./build/testLinks.py

push:
	ssh jayne.hortont.com "(cd /srv/share/private/hortont/hortont.com && git --git-dir=/srv/share/private/hortont/hortont.com/.git --work-tree=/srv/share/private/hortont/hortont.com pull ; make ; rsync -avz -e \"ssh -i /srv/share/private/hortont/.ssh/id_dsa_hortontcom\" /srv/share/private/hortont/hortont.com/output/ hortont.com:hortont.com/blog)"

.PHONY: build-posts build-static build-archive all clean copy-data push
