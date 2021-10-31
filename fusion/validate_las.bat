c:\FUSION\LAStools\bin\laszip -i C:\FUSION\GED_A01_ID37\*.las -odir "c:\FUSION\GED_A01_ID37" -olaz -lax -append

c:\FUSION\Catalog /drawtiles /countreturns /density:1,4,8 C:\FUSION\GED_A01_ID37\*.laz C:\FUSION\GED_A01_ID37\catalog

for %%f in (C:\FUSION\GED_A01_ID37\*.laz) do (

c:\FUSION\GroundFilter C:\FUSION\GED_A01_ID37\ground%%~nf.laz 8 %%f
					   
c:\FUSION\GridSurfaceCreate C:\FUSION\GED_A01_ID37\mdt%%~nf.dtm 1 m m 0 0 0 0 C:\FUSION\GED_A01_ID37\ground%%~nf.laz
					   
c:\FUSION\DTM2ASCII C:\FUSION\GED_A01_ID37\mdt%%~nf.dtm C:\FUSION\GED_A01_ID37\mdt%%~nf.asc

REM echo %%~nf
c:\FUSION\GridMetrics /ascii /nointensity /raster:max C:\FUSION\GED_A01_ID37\mdt%%~nf.dtm 7 1 C:\FUSION\GED_A01_ID37\chm%%~nf %%f
)
pause
