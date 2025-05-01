#include "Renderer.hpp"
#include "Scene.hpp"
#include "Triangle.hpp"
#include "Sphere.hpp"
#include "Vector.hpp"
#include "global.hpp"
#include <chrono>

// In the main function of the program, we create the scene (create objects and
// lights) as well as set the options for the render (image width and height,
// maximum recursion depth, field-of-view, etc.). We then call the render
// function().
int main(int argc, char** argv)
{

    // 检查参数数量
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <render_mode> <spp>\n";
        std::cerr << "  <render_mode>: p for PreRender, b for Baseline Render, a for Adaptive Render\n";
        std::cerr << "  <spp>: Number of samples per pixel\n";
        return 1;
    }

    // 解析参数
    char render_mode = argv[1][0]; // 渲染模式
    int spp = std::stoi(argv[2]);         // 每像素采样数

    // 检查参数有效性
    if (render_mode != 'p' && render_mode != 'b' && render_mode != 'a') {
        std::cerr << "Invalid render_mode. Use p for PreRender, b for Baseline Render, or a for Adaptive Render.\n";
        return 1;
    }
    if (spp <= 0) {
        std::cerr << "Invalid spp. It must be a positive integer.\n";
        return 1;
    }
    // Change the definition here to change resolution
    Scene scene(784, 784);

    Material* red = new Material(DIFFUSE, Vector3f(0.0f));
    red->Kd = Vector3f(0.63f, 0.065f, 0.05f);
    Material* green = new Material(DIFFUSE, Vector3f(0.0f));
    green->Kd = Vector3f(0.14f, 0.45f, 0.091f);
    Material* white = new Material(DIFFUSE, Vector3f(0.0f));
    white->Kd = Vector3f(0.725f, 0.71f, 0.68f);
    Material* light = new Material(DIFFUSE, (8.0f * Vector3f(0.747f+0.058f, 0.747f+0.258f, 0.747f) + 15.6f * Vector3f(0.740f+0.287f,0.740f+0.160f,0.740f) + 18.4f *Vector3f(0.737f+0.642f,0.737f+0.159f,0.737f)));
    light->Kd = Vector3f(0.65f);

    MeshTriangle floor("../models/cornellbox/floor.obj", white);
    MeshTriangle shortbox("../models/cornellbox/shortbox.obj", white);
    MeshTriangle tallbox("../models/cornellbox/tallbox.obj", white);
    MeshTriangle left("../models/cornellbox/left.obj", red);
    MeshTriangle right("../models/cornellbox/right.obj", green);
    MeshTriangle light_("../models/cornellbox/light.obj", light);

    scene.Add(&floor);
    scene.Add(&shortbox);
    scene.Add(&tallbox);
    scene.Add(&left);
    scene.Add(&right);
    scene.Add(&light_);

    scene.buildBVH();

    Renderer r;

    auto start = std::chrono::system_clock::now();
    if (render_mode == 'p') {
        std::cout << "PreRender mode selected.\n";
        r.PreRender(scene, spp);
    } else if (render_mode == 'b') {
        std::cout << "Baseline Render mode selected.\n";
        r.Render(scene);
    } else if (render_mode == 'a') {
        std::cout << "Adaptive Render mode selected.\n";
        r.AdaptiveRender(scene);
    }
    auto stop = std::chrono::system_clock::now();

    // auto start = std::chrono::system_clock::now();
    // // r.Render(scene);
    // r.PreRender(scene, 2);
    // auto stop = std::chrono::system_clock::now();

    std::cout << "Render complete: \n";
    std::cout << "Time taken: " << std::chrono::duration_cast<std::chrono::hours>(stop - start).count() << " hours\n";
    std::cout << "          : " << std::chrono::duration_cast<std::chrono::minutes>(stop - start).count() << " minutes\n";
    std::cout << "          : " << std::chrono::duration_cast<std::chrono::seconds>(stop - start).count() << " seconds\n";

    return 0;
}