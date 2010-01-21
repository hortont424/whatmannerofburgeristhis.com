# hortont.com build system

.IGNORE:
.SILENT:

baseurl=$(shell PYTHONPATH=build python2.6 -c 'import settings; print settings.www_prefix')

all: clean unclean copy-data build-static build-posts build-archive build-rss build-everything
	echo $(shell du -h -k -d 0 output | sed -e 's/\s*output//') total kilobytes
	echo $(shell find output | wc -l | sed -e 's/^[ \t]*//') total files

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
	
	python2.6 ./build/substituteSettings.py output/styles
	python2.6 ./build/cssmin.py output/styles

check-links:
	python2.6 ./build/testLinks.py

push:
	ssh jayne.hortont.com "ssh-agent zsh -c '(ssh-add /srv/share/private/hortont/.ssh/id_dsa_hortontcom && cd /srv/share/private/hortont/hortont.com && git --git-dir=/srv/share/private/hortont/hortont.com/.git --work-tree=/srv/share/private/hortont/hortont.com pull ; make ; rsync -avz -e \"ssh -i /srv/share/private/hortont/.ssh/id_dsa_hortontcom\" /srv/share/private/hortont/hortont.com/output/ hortont.com:hortont.com)'"

.PHONY: build-posts build-static build-archive all clean copy-data push
