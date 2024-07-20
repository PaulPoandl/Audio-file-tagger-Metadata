@echo off
title Audio Files Metadata Manager
:main_menu
cls
echo ===========================================
echo         Audio Files Metadata Manager
echo ===========================================
echo.
echo Welcome to the Audio Files Metadata Manager!
echo This program supports FLAC, M4A, MP3, PNG, and JPG files.
echo Made for tagging files after downloading with JDownloader.
echo JDownloader -> https://jdownloader.org (..JDownloader was not created by me..)
echo.
echo You can use this tool to:
echo - Add metadata to audio files 
echo - Add cover art to audio files
echo - Rename audio files 
echo   (This just removes (and content) from file name)
echo.
echo Please choose an option:
echo 1. Run Full Process (1-2-3)
echo 2. Run Cover Tagger only (1)
echo 3. Run Rename Tagger only (2)
echo 4. Run Metadata Tagger only (3)
echo 5. Exit
echo.
echo Info: The order is important, because Metadata Tagger automatically names 
echo the file (from the file name), and also sorts it by number, and if it's not renamed before,
echo the metadata title is wrong.
echo. 
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto full_process
if "%choice%"=="2" goto run_cover_tagger
if "%choice%"=="3" goto run_rename_tagger
if "%choice%"=="4" goto run_metadata_tagger
if "%choice%"=="5" exit /b
goto main_menu

:full_process
cls
echo ===========================================
echo           Running Full Process
echo ===========================================
echo.
echo Step 1: Adding Cover Art
call Cover_Tagger-1.exe
echo.
pause
echo Step 2: Renaming Files
call Rename_Tagger-2.exe
echo.
pause
echo Step 3: Adding Metadata
call Metadata_Tagger-3.exe
echo.
pause
echo Full process completed!
echo.
set /p retry="Would you like to run the process again? (y/n): "
if "%retry%"=="y" goto full_process
goto main_menu

:run_cover_tagger
cls
echo ===========================================
echo          Running Cover Tagger
echo ===========================================
echo.
call Cover_Tagger-1.exe
echo.
pause
goto main_menu

:run_rename_tagger
cls
echo ===========================================
echo          Running Rename Tagger
echo ===========================================
echo.
call Rename_Tagger-2.exe
echo.
pause
goto main_menu

:run_metadata_tagger
cls
echo ===========================================
echo         Running Metadata Tagger
echo ===========================================
echo.
call Metadata_Tagger-3.exe
echo.
pause
goto main_menu
