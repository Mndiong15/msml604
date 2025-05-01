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
### Pre-rendering
Merely calculate the variance of the scene by distributing the samples uniformly and store it in `variance.txt` and also in `scene.variance` during the program. This mode does not output a picture.
### Baseline rendering
Render the picture by distributing the samples uniformly and output it as `binary.ppm`.
### Adaptive rendering
Render the picture by adaptively allocating the samples according to calculated sample distribution. 

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
Note that for adaptive rendering, there must be a file in the build directory named `sampledistribution.txt` recording how many samples should be allocated to each pixel. The mode of `sampledistribution.txt` should be similar to `variance.txt`, i.e. one line for each pixel. Otherwise, the program will crash.
