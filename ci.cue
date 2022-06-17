package main

import (
        "dagger.io/dagger"
        "universe.dagger.io/docker"
)

dagger.#Plan & {
	client: filesystem: {
		".": read: contents: dagger.#FS
	}
	actions: {
		_image: docker.#Dockerfile & {
			source: client.filesystem.".".read.contents
			dockerfile: path: "Dockerfile-ci"
		},

		isort: docker.#Run & {
			input: _image.output
			workdir: "/src"
			command: {
				name: "isort"
				args: ["."]
			}
		}

		format: docker.#Run & {
			input: isort.output
			workdir: "/src"
			command: {
				name: "black"
				args: ["."]
			}
		}

		lint: docker.#Run & {
			input: format.output
			workdir: "/src"
			command: {
				name: "pylint"
				args: ["./app"]
			}
		}
	}
}

