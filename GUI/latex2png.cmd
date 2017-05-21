:: args :: Folder name were you put the tex.tex file
@echo off

:: compile to dvi
latex %1\tex.tex -halt-on-error -interaction=batchmode -disable-installer -aux-directory=%1 -output-directory=%1
:: make a png from the dvi
dvipng -T tight -z 9 --truecolor -o %1\tex.png %1\tex.dvi

:: cleanup
del %1\*.dvi
del %1\*.log
del %1\*.aux
