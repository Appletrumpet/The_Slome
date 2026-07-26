.PHONY: run web clean

# Run the game locally
run:
	python3 game.py

# Rebuild the browser version into docs/index.html (served by GitHub Pages)
web:
	rm -rf build
	mkdir -p build/the_slome docs
	cp game.py resources.pyxres build/the_slome/
	cd build && pyxel package the_slome the_slome/game.py && pyxel app2html the_slome.pyxapp
	mv build/the_slome.html docs/index.html
	sed -i '' '1s|^<!doctype html>|<!doctype html><link rel="icon" type="image/png" href="favicon.png">|' docs/index.html
	rm -rf build

clean:
	rm -rf build __pycache__
