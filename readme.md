# Guide
## How to build
```
mkdir build && cd build
cmake ..
make
```
## How to run
There are 2 parameters which can be delivered to the program.

The first parameter indicates the rendering mode:
p for PreRender; b for Baseline Render; a for Adaptive Render.

The second parameter indicates the samples per pixel(spp):
for PreRender and Baseline Render, spp is useful; for Adaptive Render, spp is of no use, so type any number you like.

In the build directory,
for baseline rendering, run:
```
./RayTracing b 16
```
for pre-rendering, run:
```
./RayTracing p 16
```
for adaptive rendering, run:
```
./RayTracing a 16
```