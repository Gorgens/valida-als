## Para chamar este script: exec(open('C:/FUSION/TAN_A01/validacaoPaisagens.py'.encode('utf-8')).read())

import subprocess
import os

FUSION_FOLDER = 'C:/FUSION'
LASTOOLS_FOLDER = 'C:/LAStools/bin'

NP_FOLDER = "C:/FUSION/TAN_A01/NP"
NP_DTM_FOLDER = "C:/FUSION/TAN_A01/NP_MDT"
DTM_FOLDER = "C:/FUSION/TAN_A01/MDT"
DTM_PREVIOUS = "C:/FUSION/TAN_A01/MDT_ANTERIOR"

VALIDA_FOLDER = 'C:/FUSION/TAN_A01/check'
PROJETO = 'TAN_A01'
crs = QgsCoordinateReferenceSystem("EPSG:31982")

print('Iniciando processamento da área %s.' % PROJETO)

## Criar pasta para projeto 
try:
   os.mkdir(VALIDA_FOLDER)
except OSError:
   print ("Etapa 1 de 16. Criação do diretório falhou.")
else:
   print ("Etapa 1 de 16. Diretório criado com sucesso.")


## Rodar FUSION::Catalog [switches] datafile [catalogfile]
try:
   subprocess.call(FUSION_FOLDER + '/Catalog /drawtiles /countreturns /density:5,4,8 ' +
                   NP_FOLDER + '/' + PROJETO + '*.las ' +
                   VALIDA_FOLDER + '/' + PROJETO +'catalog')
except OSError:
   print('Etapa 2 de 16. Catalog falhou.')
else:
   print('Etapa 2 de 16. Catalog criado com sucesso.')


## Rodar LASTOOLS::lasinfo
try:
   subprocess.call(LASTOOLS_FOLDER + '/lasinfo -cpu64 -i ' + 
                    NP_FOLDER + '/*.las -merged -odir ' + 
                    VALIDA_FOLDER + ' -o "report.txt" -cd -histo gps_time 20')
except OSError:
   print('Etapa 3 de 16. Lasinfo falhou.')
else:
   print('Etapa 3 de 16. Lasinfo criado com sucesso.')


## Computar densidade: ReturnDensity [switches] outputfile cellsize datafile1
try:
    subprocess.call(FUSION_FOLDER + '/ReturnDensity /ascii ' +
                    VALIDA_FOLDER + '/' + 'density.asc 5 ' +
                    NP_FOLDER + '/' + PROJETO + '*.las')
except OSError:
   print('Etapa 4 de 16. ReturnDensity falhou.')
else:
   print('Etapa 4 de 16. ReturnDensity criado com sucesso.')

densidade = QgsRasterLayer(VALIDA_FOLDER + '/' + 'density.asc', 'densidade')
densidade.setCrs(crs)
QgsProject.instance().addMapLayer(densidade)   

## Unir DTM entregue
try:
    mdts = []
    for filename in os.listdir(DTM_FOLDER):
        if filename.endswith(".flt"):
            mdts.append(os.path.join(DTM_FOLDER+'/'+filename))
    processing.run("gdal:merge", {'INPUT':mdts,
                         'PCT':False,
                         'SEPARATE':False,
                         'NODATA_INPUT':None,
                         'NODATA_OUTPUT':-9999, #Prevous None
                         'OPTIONS':'',
                         'EXTRA':'',
                         'DATA_TYPE':5,
                         'OUTPUT':VALIDA_FOLDER + '/' + 'mdtEntregue.tif'})
except OSError:
   print('Etapa 5 de 16. União dos MDT entregues falhou.')
else:
   print('Etapa 5 de 16. União dos MDT realizada com sucesso.')

mdtEntregue = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtEntregue.tif', "mdtEntregue")
mdtEntregue.setCrs(crs)
QgsProject.instance().addMapLayer(mdtEntregue)


## Computar hillshade
try:
    processing.run("native:hillshade", {'INPUT':VALIDA_FOLDER + '/' + 'mdtEntregue.tif',
                                        'Z_FACTOR':3,
                                        'AZIMUTH':300,
                                        'V_ANGLE':40,
                                        'OUTPUT':VALIDA_FOLDER + '/' + 'mdtHillshade.tif'})
except OSError:
   print('Etapa 6 de 16. Hillshade falhou.')
else:
   print('Etapa 6 de 16. Hillshade criado com sucesso.')
   
mdtHillshade = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtHillshade.tif', 'mdtHillshade')
mdtHillshade.setCrs(crs)
QgsProject.instance().addMapLayer(mdtHillshade)


## Gerar o modelo digital de terreno a partir da nuvem entregue
try:
   subprocess.call(FUSION_FOLDER + '/GridSurfaceCreate ' +
                   VALIDA_FOLDER + '/' + 'mdtCriado.dtm ' +
                   '1 m m 0 0 0 0 ' + NP_DTM_FOLDER + '/' + PROJETO + '*.las')
                   
   subprocess.call(FUSION_FOLDER + '/DTM2ASCII ' +
                   VALIDA_FOLDER + '/' + 'mdtCriado.dtm ' +
                   VALIDA_FOLDER + '/' + 'mdtCriado.asc')
except OSError:
   print('Etapa 7 de 16. Criação do MDT falhou.')
else:
   print('Etapa 7 de 16. MDT criado com sucesso.')

mdtCriado = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtCriado.asc', "mdtCriado")
mdtCriado.setCrs(crs)
QgsProject.instance().addMapLayer(mdtCriado)


## Unir tiles do DTM antigo
try:
    mdts = []
    for filename in os.listdir(DTM_PREVIOUS):
        if filename.endswith(".grd"):
            mdts.append(os.path.join(DTM_PREVIOUS+'/'+filename))
    processing.run("gdal:merge", {'INPUT':mdts,
                             'PCT':False,
                             'SEPARATE':False,
                             'NODATA_INPUT':None,
                             'NODATA_OUTPUT':-9999, #Prevous None
                             'OPTIONS':'',
                             'EXTRA':'',
                             'DATA_TYPE':5,
                             'OUTPUT':VALIDA_FOLDER + '/' + 'mdtAnterior.tif'})
except OSError:
    print('Etapa 8 de 16. União dos MDTs antigos falhou')
else:
    print('Etapa 8 de 16. MDTs antigos unidos com sucesso.')

mdtAnterior = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtAnterior.tif', "mdtAnterior")
mdtAnterior.setCrs(crs)
QgsProject.instance().addMapLayer(mdtAnterior)


## Calcular diferença entre MDTs
try:
   processing.run("saga:rastercalculator", {'GRIDS':mdtEntregue,
                                            'XGRIDS': mdtAnterior, 
                                            'FORMULA':'a-b',
                                            'RESAMPLING':3,
                                            'USE_NODATA':False,
                                            'TYPE':7,
                                            'RESULT': VALIDA_FOLDER + '/' + 'diffEntregueAnterior.tif'})
except OSError:
   print('Etapa 9 de 16. Calculo da diferença MDT Entregue/Anterior falhou.')
else:
   print('Etapa 9 de 16. Diferença MDT Entregue/Anterior calculado com sucesso.')
    
diffEntregueAnterior = QgsRasterLayer(VALIDA_FOLDER + '/' + 'diffEntregueAnterior.sdat', 'diffEntregueAnterior')
diffEntregueAnterior.setCrs(crs)
QgsProject.instance().addMapLayer(diffEntregueAnterior)

# Calcular histograma para a diferença entre DTM
try:
    processing.run("qgis:rasterlayerhistogram",
                    {'INPUT':VALIDA_FOLDER + '/' + 'diffEntregueAnterior.sdat',
                    'BAND':1,
                    'BINS':1000,
                    'OUTPUT':VALIDA_FOLDER + '/' + 'HistdiffEntregueAnterior.html'})
except OSError:
   print('Etapa 10 de 16. Histograma da diferença Entregue/Anterior falhou.')
else:
   print('Etapa 10 de 16. Histograma da diferença Entregue/Anterior computado com sucesso.')
   
try:
   processing.run("saga:rastercalculator", {'GRIDS':mdtEntregue,
                                            'XGRIDS': mdtCriado, 
                                            'FORMULA':'a-b',
                                            'RESAMPLING':3,
                                            'USE_NODATA':False,
                                            'TYPE':7,
                                            'RESULT': VALIDA_FOLDER + '/' + 'diffEntregueCriado.tif'})
except OSError:
   print('Etapa 11 de 16. Calculo da diferença MDT Entregue/Criado falhou.')
else:
   print('Etapa 11 de 16. Diferença MDT Entregue/Criado calculado com sucesso.')
    
diffEntregueCriado = QgsRasterLayer(VALIDA_FOLDER + '/' + 'diffEntregueCriado.sdat', 'diffEntregueCriado')
diffEntregueCriado.setCrs(crs)
QgsProject.instance().addMapLayer(diffEntregueCriado)

## Calcula histograma para a diferença entre DTM
try:
    processing.run("qgis:rasterlayerhistogram",
                    {'INPUT':VALIDA_FOLDER + '/' + 'diffEntregueCriado.sdat',
                    'BAND':1,
                    'BINS':1000,
                    'OUTPUT':VALIDA_FOLDER + '/' + 'diffEntregueCriado.html'})
except OSError:
   print('Etapa 12 de 16. Histograma da diferença Entregue/Criado falhou.')
else:
   print('Etapa 12 de 16. Histograma da diferença Entregue/Criado computado com sucesso.')


## Extrair Hmean
try:
    for filename in os.listdir(NP_FOLDER):
        if filename.endswith(".las"):
           # os.path.join(NP_FOLDER+'/'+filename)
           subprocess.call(FUSION_FOLDER + '/GridMetrics /nointensity /nocsv /raster:mean /ascii ' +
                           VALIDA_FOLDER + '/' + 'mdtCriado.dtm 10 10 ' +
                           VALIDA_FOLDER + '/' + os.path.splitext(filename)[0]+'.asc ' +
                           os.path.join(NP_FOLDER+'/'+filename))
except OSError:
   print('Etapa 13 de 16. Hmean falhou.')
else:
   print('Etapa 13 de 16. Hmean computado com sucesso.')

## Unir tiles do Hmean
try:
    mdts = []
    for filename in os.listdir(VALIDA_FOLDER):
        if filename.endswith("_mean.asc"):
            mdts.append(os.path.join(VALIDA_FOLDER+'/'+filename))
    processing.run("gdal:merge", {'INPUT':mdts,
                             'PCT':False,
                             'SEPARATE':False,
                             'NODATA_INPUT':None,
                             'NODATA_OUTPUT':-9999, #Prevous None
                             'OPTIONS':'',
                             'EXTRA':'',
                             'DATA_TYPE':5,
                             'OUTPUT':VALIDA_FOLDER + '/' + 'hmean.tif'})
except OSError:
    print('Etapa 14 de 16. União de Hmean falhou.')
else:
    print('Etapa 14 de 16. Hmean unido com sucesso.')
    

hmean = QgsRasterLayer(VALIDA_FOLDER + '/' + 'hmean.tif', "hmean")
hmean.setCrs(crs)
QgsProject.instance().addMapLayer(hmean)

## Extrair Hmax
try:
    for filename in os.listdir(NP_FOLDER):
        if filename.endswith(".las"):
           # os.path.join(NP_FOLDER+'/'+filename)
           subprocess.call(FUSION_FOLDER + '/GridMetrics /nointensity /nocsv /raster:max /ascii ' +
                           VALIDA_FOLDER + '/' + 'mdtCriado.dtm 10 1 ' +
                           VALIDA_FOLDER + '/' + os.path.splitext(filename)[0]+'.asc ' +
                           os.path.join(NP_FOLDER+'/'+filename))
except OSError:
   print('Etapa 15 de 16. Hmax falhou.')
else:
   print('Etapa 15 de 16. Hmax computado com sucesso.')

## Unir tiles do Hmax
try:
    mdts = []
    for filename in os.listdir(VALIDA_FOLDER):
        if filename.endswith("_max.asc"):
            mdts.append(os.path.join(VALIDA_FOLDER+'/'+filename))
    processing.run("gdal:merge", {'INPUT':mdts,
                             'PCT':False,
                             'SEPARATE':False,
                             'NODATA_INPUT':None,
                             'NODATA_OUTPUT':-9999, #Prevous None
                             'OPTIONS':'',
                             'EXTRA':'',
                             'DATA_TYPE':5,
                             'OUTPUT':VALIDA_FOLDER + '/' + 'hmax.tif'})
except OSError:
    print('Etapa 16 de 16. União de Hmax falhou.')
else:
    print('Etapa 16 de 16. Hmax unido com sucesso.')


hmax = QgsRasterLayer(VALIDA_FOLDER + '/' + 'hmax.tif', "hmax")
hmax.setCrs(crs)
QgsProject.instance().addMapLayer(hmax)      

print('Finalizado processamento da área %s.' % PROJETO)                     