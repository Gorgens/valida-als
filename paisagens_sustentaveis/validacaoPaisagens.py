## Para chamar este script: exec(open('C:/FUSION/ST1_A01/validacaoPaisagens.py'.encode('utf-8')).read())

import subprocess
import os

FUSION_FOLDER = 'C:/FUSION'
LASTOOLS_FOLDER = 'C:/LAStools/bin'

NP_FOLDER = "C:/FUSION/ST1_A01/NP1"
NP_DTM_FOLDER = "C:/FUSION/ST1_A01/NP_MDT1"
DTM_FOLDER = "C:/FUSION/ST1_A01/MDT1"
DTM_PREVIOUS = "C:/FUSION/ST1_A01/MDT_ANTERIOR1" #None

VALIDA_FOLDER = 'C:/FUSION/ST1_A01/check1'
PROJETO = 'ST1_A01'
crs = QgsCoordinateReferenceSystem("EPSG:31982")

print('Iniciando processamento da área %s.' % PROJETO)


########################################################################################
## Criar pasta para projeto 
try:
   os.mkdir(VALIDA_FOLDER)
except OSError:
   print ("Etapa 1 de 18. Criação do diretório falhou.")
else:
   print ("Etapa 1 de 18. Diretório criado com sucesso.")


########################################################################################
## Rodar FUSION::Catalog [switches] datafile [catalogfile]
try:
   subprocess.call(FUSION_FOLDER + '/Catalog /drawtiles /countreturns /density:1,4,8 ' +
                   NP_FOLDER + '/' + PROJETO + '*.las ' +
                   VALIDA_FOLDER + '/' + PROJETO +'catalog')
except OSError:
   print('Etapa 2 de 18. Catalog falhou.')
else:
   print('Etapa 2 de 18. Catalog criado com sucesso.')


## Rodar LASTOOLS::lasinfo
try:
   subprocess.call(LASTOOLS_FOLDER + '/lasinfo -cpu64 -i ' + 
                    NP_FOLDER + '/*.las -merged -odir ' + 
                    VALIDA_FOLDER + ' -o "report.txt" -cd -histo gps_time 20')
except OSError:
   print('Etapa 3 de 18. Lasinfo falhou.')
else:
   print('Etapa 3 de 18. Lasinfo criado com sucesso.')


########################################################################################
## Computar densidade: ReturnDensity [switches] outputfile cellsize datafile1
try:
    subprocess.call(FUSION_FOLDER + '/ReturnDensity /ascii ' +
                    VALIDA_FOLDER + '/' + 'density.asc 1 ' +
                    NP_FOLDER + '/' + PROJETO + '*.las')
except OSError:
   print('Etapa 4 de 18. ReturnDensity falhou.')
else:
   print('Etapa 4 de 18. ReturnDensity criado com sucesso.')

density = QgsRasterLayer(VALIDA_FOLDER + '/' + 'density.asc', 'density')
density.setCrs(crs)
QgsProject.instance().addMapLayer(density)


########################################################################################
## Cria máscara de densidade inferior a 4 pts
try:
    parameters = {'INPUT_A' : VALIDA_FOLDER + '/' + 'density.asc',
            'BAND_A' : 1,
            'FORMULA' : '(A <= 4)',
            'OUTPUT' : VALIDA_FOLDER + '/' + 'maskBellow4pts.tif'}

    processing.run('gdal:rastercalculator', parameters)
except OSError:
   print('Etapa 5 de 18. Criação de máscara falhou.')
else:
   print('Etapa 5 de 18. Máscara criada com sucesso.')

maskBellow4pts = QgsRasterLayer(VALIDA_FOLDER + '/' + 'maskBellow4pts.tif', 'maskBellow4pts')
maskBellow4pts.setCrs(crs)
QgsProject.instance().addMapLayer(maskBellow4pts)


########################################################################################
## Computar densidade de primeiros retornos: ReturnDensity [switches] outputfile cellsize datafile1
try:
    subprocess.call(FUSION_FOLDER + '/ReturnDensity /first /ascii ' +
                    VALIDA_FOLDER + '/' + 'densityFirst.asc 1 ' +
                    NP_FOLDER + '/' + PROJETO + '*.las')
except OSError:
   print('Etapa 6 de 18. ReturnDensity falhou.')
else:
   print('Etapa 6 de 18. ReturnDensity criado com sucesso.')

densityFirst = QgsRasterLayer(VALIDA_FOLDER + '/' + 'densityFirst.asc', 'densityFirst')
densityFirst.setCrs(crs)
QgsProject.instance().addMapLayer(densityFirst)      


########################################################################################
## Cria máscara para sem primeiro retornos
try:
    parameters = {'INPUT_A' : VALIDA_FOLDER + '/' + 'densityFirst.asc',
            'BAND_A' : 1,
            'FORMULA' : '(A = 0)',
            'OUTPUT' : VALIDA_FOLDER + '/' + 'maskNoFirst.tif'}

    processing.run('gdal:rastercalculator', parameters)
except OSError:
   print('Etapa 7 de 18. Criação de máscara NoFirst falhou.')
else:
   print('Etapa 7 de 18. Máscara NoFirst criada com sucesso.')

maskNoFirst = QgsRasterLayer(VALIDA_FOLDER + '/' + 'maskNoFirst.tif', 'maskNoFirst')
maskNoFirst.setCrs(crs)
QgsProject.instance().addMapLayer(maskNoFirst)


########################################################################################
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
   print('Etapa 8 de 18. União dos MDT entregues falhou.')
else:
   print('Etapa 8 de 18. União dos MDT realizada com sucesso.')

mdtEntregue = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtEntregue.tif', "mdtEntregue")
mdtEntregue.setCrs(crs)
QgsProject.instance().addMapLayer(mdtEntregue)


########################################################################################
## Computar hillshade do DTM entregue
try:
    processing.run("native:hillshade", {'INPUT':VALIDA_FOLDER + '/' + 'mdtEntregue.tif',
                                        'Z_FACTOR':3,
                                        'AZIMUTH':300,
                                        'V_ANGLE':40,
                                        'OUTPUT':VALIDA_FOLDER + '/' + 'mdtHillshade.tif'})
except OSError:
   print('Etapa 9 de 18. Hillshade falhou.')
else:
   print('Etapa 9 de 18. Hillshade criado com sucesso.')
   
mdtHillshade = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtHillshade.tif', 'mdtHillshade')
mdtHillshade.setCrs(crs)
QgsProject.instance().addMapLayer(mdtHillshade)


########################################################################################
## Gerar o modelo digital de terreno a partir da nuvem entregue
try:
   subprocess.call(FUSION_FOLDER + '/GridSurfaceCreate ' +
                   VALIDA_FOLDER + '/' + 'mdtCriado.dtm ' +
                   '1 m m 0 0 0 0 ' + NP_DTM_FOLDER + '/' + PROJETO + '*.las')
                   
   subprocess.call(FUSION_FOLDER + '/DTM2ASCII ' +
                   VALIDA_FOLDER + '/' + 'mdtCriado.dtm ' +
                   VALIDA_FOLDER + '/' + 'mdtCriado.asc')
except OSError:
   print('Etapa 10 de 18. Criação do MDT falhou.')
else:
   print('Etapa 10 de 18. MDT criado com sucesso.')

mdtCriado = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtCriado.asc', "mdtCriado")
mdtCriado.setCrs(crs)
QgsProject.instance().addMapLayer(mdtCriado)


########################################################################################
# Unir tiles do DTM antigo
if DTM_PREVIOUS is not None:
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
        print('Etapa 11 de 18. União dos MDTs antigos falhou')
    else:
        print('Etapa 11 de 18. MDTs antigos unidos com sucesso.')

    mdtAnterior = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtAnterior.tif', "mdtAnterior")
    mdtAnterior.setCrs(crs)
    QgsProject.instance().addMapLayer(mdtAnterior)

    ########################################################################################
    # Calcular diferença entre MDTs
    try:
       processing.run("saga:rastercalculator", {'GRIDS':mdtEntregue,
                                                'XGRIDS': mdtAnterior, 
                                                'FORMULA':'a-b',
                                                'RESAMPLING':3,
                                                'USE_NODATA':False,
                                                'TYPE':7,
                                                'RESULT': VALIDA_FOLDER + '/' + 'diffEntregueAnterior.tif'})
    except OSError:
       print('Etapa 12 de 18. Calculo da diferença MDT Entregue/Anterior falhou.')
    else:
       print('Etapa 12 de 18. Diferença MDT Entregue/Anterior calculado com sucesso.')
        
    diffEntregueAnterior = QgsRasterLayer(VALIDA_FOLDER + '/' + 'diffEntregueAnterior.sdat', 'diffEntregueAnterior')
    diffEntregueAnterior.setCrs(crs)
    QgsProject.instance().addMapLayer(diffEntregueAnterior)


########################################################################################
#Calcular histograma para a diferença entre DTM
try:
    processing.run("qgis:rasterlayerhistogram",
                    {'INPUT':VALIDA_FOLDER + '/' + 'diffEntregueAnterior.sdat',
                    'BAND':1,
                    'BINS':1000,
                    'OUTPUT':VALIDA_FOLDER + '/' + 'HistdiffEntregueAnterior.html'})
except OSError:
   print('Etapa 13 de 18. Histograma da diferença Entregue/Anterior falhou.')
else:
   print('Etapa 13 de 18. Histograma da diferença Entregue/Anterior computado com sucesso.')
   
try:
   processing.run("saga:rastercalculator", {'GRIDS':mdtEntregue,
                                            'XGRIDS': mdtCriado, 
                                            'FORMULA':'a-b',
                                            'RESAMPLING':3,
                                            'USE_NODATA':False,
                                            'TYPE':7,
                                            'RESULT': VALIDA_FOLDER + '/' + 'diffEntregueCriado.tif'})
except OSError:
   print('Etapa 11 de 18. Calculo da diferença MDT Entregue/Criado falhou.')
else:
   print('Etapa 11 de 18. Diferença MDT Entregue/Criado calculado com sucesso.')
    
diffEntregueCriado = QgsRasterLayer(VALIDA_FOLDER + '/' + 'diffEntregueCriado.sdat', 'diffEntregueCriado')
diffEntregueCriado.setCrs(crs)
QgsProject.instance().addMapLayer(diffEntregueCriado)


########################################################################################
## Calcula histograma para a diferença entre DTM
try:
    processing.run("qgis:rasterlayerhistogram",
                    {'INPUT':VALIDA_FOLDER + '/' + 'diffEntregueCriado.sdat',
                    'BAND':1,
                    'BINS':1000,
                    'OUTPUT':VALIDA_FOLDER + '/' + 'diffEntregueCriado.html'})
except OSError:
   print('Etapa 14 de 18. Histograma da diferença Entregue/Criado falhou.')
else:
   print('Etapa 14 de 18. Histograma da diferença Entregue/Criado computado com sucesso.')


########################################################################################
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
   print('Etapa 15 de 18. Hmean falhou.')
else:
   print('Etapa 15 de 18. Hmean computado com sucesso.')


########################################################################################
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
    print('Etapa 16 de 18. União de Hmean falhou.')
else:
    print('Etapa 16 de 18. Hmean unido com sucesso.')
    

hmean = QgsRasterLayer(VALIDA_FOLDER + '/' + 'hmean.tif', "hmean")
hmean.setCrs(crs)
QgsProject.instance().addMapLayer(hmean)


########################################################################################
## Calcular CHM
try:
    subprocess.call(FUSION_FOLDER + '/CanopyModel /ground:' + VALIDA_FOLDER + '/' + 'mdtCriado.dtm' +
                    ' /ascii ' + VALIDA_FOLDER + '/' + 'chmCriado.dtm 1 m m 1 0 0 0 ' +
                    NP_FOLDER + '/' + PROJETO + '*.las')
except OSError:
   print('Etapa 17 de 18. CHM falhou.')
else:
   print('Etapa 17 de 18. CHM criado com sucesso.')

chm = QgsRasterLayer(VALIDA_FOLDER + '/' + 'chmCriado.asc', "chm")
chm.setCrs(crs)
QgsProject.instance().addMapLayer(chm)

print('Finalizado processamento da área %s.' % PROJETO)                     