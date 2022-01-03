REM Processamento de nova coleta LiDAR

REM groundfilter
C:\FUSION\GroundFilter64 C:\FUSION\ducke_2021\gnd\groundpoints.laz 8 C:\FUSION\ducke_2021\las\*.laz

REM dtm
REM C:\FUSION\GridSurfaceCreate64 C:\FUSION\ducke_2021\mdt\terrain.dtm 1 m m 0 0 0 0 C:\FUSION\ducke_2021\gnd\*.laz
REM C:\FUSION\DTM2ASCII64 /raster C:\FUSION\ducke_2021\mdt\terrain.dtm C:\FUSION\ducke_2021\mdt\terrain.asc

REM chm
REM C:\FUSION\CanopyModel64 /ground:C:\FUSION\ducke_2021\mdt\terrain.dtm /ascii C:\FUSION\ducke_2021\chm\chm.dtm 1 m m 0 0 0 0 C:\FUSION\ducke_2021\las\*.laz
 
REM cover 1
REM C:\FUSION\Cover64 C:\FUSION\ducke_2021\mdt\terrain.dtm C:\FUSION\ducke_2021\cvr\strata.dtm 5 10 m m 0 0 0 0 C:\FUSION\ducke_2021\las\*.laz
REM C:\FUSION\DTM2ASCII64 /raster C:\FUSION\ducke_2021\cvr\strata.dtm C:\FUSION\ducke_2021\cvr\strata.asc

REM cover 2
REM C:\FUSION\Cover64 /upper:5 C:\FUSION\ducke_2021\mdt\terrain.dtm C:\FUSION\ducke_2021\cvr\mdr.dtm 1 10 m m 0 0 0 0 C:\FUSION\ducke_2021\las\*.laz
REM C:\FUSION\DTM2ASCII64 /raster C:\FUSION\ducke_2021\cvr\mdr.dtm C:\FUSION\ducke_2021\cvr\mdr.asc
