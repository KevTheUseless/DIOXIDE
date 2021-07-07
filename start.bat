@set path=./compilers/python-3.8;./compilers/MinGW;%path%
cd buildsys
g++ build.c -o build
g++ run.c -o run
cd ..
python ide.py
