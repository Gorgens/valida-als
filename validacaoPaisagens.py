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

# ## Cria pasta para projeto 
# try:
   # os.mkdir(VALIDA_FOLDER)
# except OSError:
   # print ("Creation of the directory failed.")
# else:
   # print ("Successfully created the directory.")


# ## Roda FUSION::Catalog [switches] datafile [catalogfile]
# try:
   # subprocess.call(FUSION_FOLDER + '/Catalog /image /drawtiles /countreturns /density:1,4,8 ' +
                   # NP_DTM_FOLDER + '/' + PROJETO + '*.las ' +
                   # VALIDA_FOLDER + '/' + PROJETO +'catalog')
# except OSError:
   # print('Return density for %s was not computed.' % PROJETO)
# else:
   # print('Return density for %s was successfully computed!' % PROJETO)

# density = QgsRasterLayer(VALIDA_FOLDER + '/' + PROJETO + 'catalog_return_density.jpg', 'returnsDensity')
# density.setCrs(crs)
# QgsProject.instance().addMapLayer(density)


# ## Roda LASTOOLS::lasinfo
# try:
   # subprocess.call(LASTOOLS_FOLDER+'/lasinfo -cpu64 -i '+ NP_FOLDER + '/' + PROJETO + '*.las -merged -odir '+ 
                   # VALIDA_FOLDER + ' -o "report.txt" -cd -histo gps_time 20')
# except OSError:
   # print('Information for %s was not extracted.' % PROJETO)
# else:
   # print('Information for %s was successfully extracted!' % PROJETO)


# ## Computar densidade: ReturnDensity [switches] outputfile cellsize datafile1
# try:
    # subprocess.call(FUSION_FOLDER + '/ReturnDensity /ascii ' +
                    # VALIDA_FOLDER + '/' + 'density.asc 5 ' +
                    # NP_FOLDER + '/' + PROJETO + '*.las')
# except OSError:
   # print('Return density for %s was not computed.' % PROJETO)
# else:
   # print('Return density for %s was successfully computed!' % PROJETO)

# densidade = QgsRasterLayer(VALIDA_FOLDER + '/' + 'density.asc', 'densidade')
# densidade.setCrs(crs)
# QgsProject.instance().addMapLayer(densidade)   

# ## Unir DTM entregue
# try:
    # mdts = []
    # for filename in os.listdir(DTM_FOLDER):
        # if filename.endswith(".flt"):
            # mdts.append(os.path.join(DTM_FOLDER+'/'+filename))
    # processing.run("gdal:merge", {'INPUT':mdts,
                         # 'PCT':False,
                         # 'SEPARATE':False,
                         # 'NODATA_INPUT':None,
                         # 'NODATA_OUTPUT':-9999, #Prevous None
                         # 'OPTIONS':'',
                         # 'EXTRA':'',
                         # 'DATA_TYPE':5,
                         # 'OUTPUT':VALIDA_FOLDER + '/' + 'mdtEntregue.tif'})
# except OSError:
   # print('Previous DTM from %s was not merged.' % PROJETO)
# else:
   # print('Previous DTM from %s was successfully merged!' % PROJETO)

# mdtEntregue = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtEntregue.tif', "mdtEntregue")
# mdtEntregue.setCrs(crs)
# QgsProject.instance().addMapLayer(mdtEntregue)


# ## Computar hillshade
# try:
    # processing.run("native:hillshade", {'INPUT':VALIDA_FOLDER + '/' + 'mdtEntregue.tif',
                                        # 'Z_FACTOR':3,
                                        # 'AZIMUTH':300,
                                        # 'V_ANGLE':40,
                                        # 'OUTPUT':VALIDA_FOLDER + '/' + 'mdtHillshade.tif'})
# except OSError:
   # print('Hillshade for %s not created.' % PROJETO)
# else:
   # print('Hillshade for %s successfully computed!' % PROJETO)
   
# mdtHillshade = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtHillshade.tif', 'mdtHillshade')
# mdtHillshade.setCrs(crs)
# QgsProject.instance().addMapLayer(mdtHillshade)


# ## Gera o modelo digital de terreno a partir da nuvem entregue
# try:
   # subprocess.call(FUSION_FOLDER + '/GridSurfaceCreate ' +
                   # VALIDA_FOLDER + '/' + 'mdtCriado.dtm ' +
                   # '1 m m 0 0 0 0 ' + NP_DTM_FOLDER + '/' + PROJETO + '*.las')
                   
   # subprocess.call(FUSION_FOLDER + '/DTM2ASCII ' +
                   # VALIDA_FOLDER + '/' + 'mdtCriado.dtm ' +
                   # VALIDA_FOLDER + '/' + 'mdtCriado.asc')
# except OSError:
   # print('DTM for %s was not created.' % PROJETO)
# else:
   # print('DTM for %s created successfully!' % PROJETO)

# mdtCriado = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtCriado.asc', "mdtCriado")
# mdtCriado.setCrs(crs)
# QgsProject.instance().addMapLayer(mdtCriado)


# ## Unir tiles do DTM antigo
# try:
    # mdts = []
    # for filename in os.listdir(DTM_PREVIOUS):
        # if filename.endswith(".grd"):
            # mdts.append(os.path.join(DTM_PREVIOUS+'/'+filename))
    # processing.run("gdal:merge", {'INPUT':mdts,
                             # 'PCT':False,
                             # 'SEPARATE':False,
                             # 'NODATA_INPUT':None,
                             # 'NODATA_OUTPUT':-9999, #Prevous None
                             # 'OPTIONS':'',
                             # 'EXTRA':'',
                             # 'DATA_TYPE':5,
                             # 'OUTPUT':VALIDA_FOLDER + '/' + 'mdtAnterior.tif'})
# except OSError:
    # print('Previous DTM from %s was not merged.' % PROJETO)
# else:
    # print('Previous DTM from %s was successfully merged!' % PROJETO)

# mdtAnterior = QgsRasterLayer(VALIDA_FOLDER + '/' + 'mdtAnterior.tif', "mdtAnterior")
# mdtAnterior.setCrs(crs)
# QgsProject.instance().addMapLayer(mdtAnterior)


# ## Calcula diferença entre MDTs
# try:
   # processing.run("saga:rastercalculator", {'GRIDS':mdtEntregue,
                                            # 'XGRIDS': mdtAnterior, 
                                            # 'FORMULA':'a-b',
                                            # 'RESAMPLING':3,
                                            # 'USE_NODATA':False,
                                            # 'TYPE':7,
                                            # 'RESULT': VALIDA_FOLDER + '/' + 'diffEntregueAnterior.tif'})
# except OSError:
   # print('Diff between DTMs for %s was not computed.' % PROJETO)
# else:
   # print('Diff between DTMs for %s successfully computed!' % PROJETO)
    
# diffEntregueAnterior = QgsRasterLayer(VALIDA_FOLDER + '/' + 'diffEntregueAnterior.sdat', 'diffEntregueAnterior')
# diffEntregueAnterior.setCrs(crs)
# QgsProject.instance().addMapLayer(diffEntregueAnterior)

# try:
   # processing.run("saga:rastercalculator", {'GRIDS':mdtEntregue,
                                            # 'XGRIDS': mdtCriado, 
                                            # 'FORMULA':'a-b',
                                            # 'RESAMPLING':3,
                                            # 'USE_NODATA':False,
                                            # 'TYPE':7,
                                            # 'RESULT': VALIDA_FOLDER + '/' + 'diffEntregueCriado.tif'})
# except OSError:
   # print('Diff between DTMs for %s was not computed.' % PROJETO)
# else:
   # print('Diff between DTMs for %s successfully computed!' % PROJETO)
    
# diffEntregueCriado = QgsRasterLayer(VALIDA_FOLDER + '/' + 'diffEntregueCriado.sdat', 'diffEntregueCriado')
# diffEntregueCriado.setCrs(crs)
# QgsProject.instance().addMapLayer(diffEntregueCriado)


# ## Extrair Hmean
# try:
    # for filename in os.listdir(NP_FOLDER):
        # if filename.endswith(".las"):
           # # os.path.join(NP_FOLDER+'/'+filename)
           # subprocess.call(FUSION_FOLDER + '/GridMetrics /nointensity /nocsv /raster:mean /ascii ' +
                           # VALIDA_FOLDER + '/' + 'mdtCriado.dtm 10 10 ' +
                           # VALIDA_FOLDER + '/' + os.path.splitext(filename)[0]+'.asc ' +
                           # os.path.join(NP_FOLDER+'/'+filename))
# except OSError:
   # print('Hmean for %s was not computed.' % PROJETO)
# else:
   # print('Hmean for %s successfully computed!' % PROJETO)

# ## Unir tiles do Hmean
# try:
    # mdts = []
    # for filename in os.listdir(VALIDA_FOLDER):
        # if filename.endswith("_mean.asc"):
            # mdts.append(os.path.join(VALIDA_FOLDER+'/'+filename))
    # processing.run("gdal:merge", {'INPUT':mdts,
                             # 'PCT':False,
                             # 'SEPARATE':False,
                             # 'NODATA_INPUT':None,
                             # 'NODATA_OUTPUT':-9999, #Prevous None
                             # 'OPTIONS':'',
                             # 'EXTRA':'',
                             # 'DATA_TYPE':5,
                             # 'OUTPUT':VALIDA_FOLDER + '/' + 'hmean.tif'})
# except OSError:
    # print('Hmean from %s was not merged.' % PROJETO)
# else:
    # print('Hmean from %s was successfully merged!' % PROJETO)
    

# hmean = QgsRasterLayer(VALIDA_FOLDER + '/' + 'hmean.tif', "hmean")
# hmean.setCrs(crs)
# QgsProject.instance().addMapLayer(hmean)

# ## Extrair Hmax
# try:
    # for filename in os.listdir(NP_FOLDER):
        # if filename.endswith(".las"):
           # # os.path.join(NP_FOLDER+'/'+filename)
           # subprocess.call(FUSION_FOLDER + '/GridMetrics /nointensity /nocsv /raster:max /ascii ' +
                           # VALIDA_FOLDER + '/' + 'mdtCriado.dtm 10 1 ' +
                           # VALIDA_FOLDER + '/' + os.path.splitext(filename)[0]+'.asc ' +
                           # os.path.join(NP_FOLDER+'/'+filename))
# except OSError:
   # print('Hmax for %s was not computed.' % PROJETO)
# else:
   # print('Hmax for %s successfully computed!' % PROJETO)

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
    print('Hmax from %s was not merged.' % PROJETO)
else:
    print('Hmax from %s was successfully merged!' % PROJETO)


hmax = QgsRasterLayer(VALIDA_FOLDER + '/' + 'hmax.tif', "hmax")
hmax.setCrs(crs)
QgsProject.instance().addMapLayer(hmax)                           