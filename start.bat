@set path=./compilers/python-3.8;./compilers/MinGW;%path%
cd buildsys
gcc build.c -o build
gcc run.c -o run
cd ..
python ide.py
