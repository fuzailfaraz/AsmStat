@echo off
echo Building AsmStat Shared Library (DLL)...
"D:\Program Files (x86)\NASM\nasm.exe" -f win64 math.asm -o math.obj
gcc -shared -o math.dll math.obj
echo Build complete! You can now run the Streamlit app.
