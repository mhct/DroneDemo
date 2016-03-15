# DroneDemo

## Environment Setup
In order to run tests automatically we need the following software
- fswatch - https://github.com/emcrisostomo/fswatch

You can install it via homebrew:
    $ brew install fswatch

Then execute the following command at the root of the project
    $ fswatch -o Server/test* | xargs -n1 -I{} py.test


