rem Converts the all .mkv files to .mp4 within the current directory, including any subfolders
for /r %%i in (*.mkv) do ffmpeg -i "%%i" -c copy "%%~dpni.mp4"

rem Optional, remove the .mkv files after conversion
for /r %%i in (*.mkv) do del "%%i"

rem Optional, delete this file after running
del %0

exit
