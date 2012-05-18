python ./build/buildPosts.py &
python ./build/buildStatic.py &
python ./build/buildArchive.py &
python ./build/buildRSS.py &
python ./build/buildEverything.py &
python ./build/buildHistory.py &

wait
