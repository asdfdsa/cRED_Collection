from __future__ import division
from instamatic import TEMController
from dataconverter import fixDistortion
import adscimage
import numpy as np
import datetime
import msvcrt
import os
import glob
import fabio
from scipy import ndimage
import threading

pxd={'15': 0.00838, '20': 0.00623, '25': 0.00499, '30': 0.00412, '40': 0.00296, '50': 0.00238, '60': 0.00198, '80': 0.00148}
"""Pixel size table."""
mrc_header=b'\x04\x02\x00\x00\x04\x02\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x02\x00\x00\x04\x02\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4B\x00\x00\xb4B\x00\x00\xb4B\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x888Fx\x06sA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MAP DA\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00aaaaaaaaaaaaaaaaaaaaaa,aaaaaaaaaaa\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
"""MRC files as 516*516"""
ctrl=TEMController.initialize(camera="timepix")
t_stop=threading.Event()

def TiffToIMG(pathtiff,pathsmv,cl,startangle,osangle):
    import collections
    print "Tiff converting to IMG......"
    listing=glob.glob(os.path.join(pathtiff,"*.tiff"))

    px=pxd[cl]
    
    distance=483.89*0.00412/px
    
    filenamelist=[]
    
    for f in listing:
        fnm=os.path.splitext(os.path.basename(f))[0]
        filenamelist.append(fnm)
    
    pbc=[]
    for f in filenamelist:
        img=fabio.open(os.path.join(pathtiff,"{}.tiff".format(f)))
        pb=np.where(img.data>10000)
        pbc.append([np.mean(pb[0]),np.mean(pb[1])])
    
    pbc=np.asarray(pbc)
    pbc=pbc[~np.isnan(pbc)]
    pbc=np.reshape(pbc,[len(pbc)/2,2])
    pb=[np.mean(pbc[:,1]),np.mean(pbc[:,0])]

    print "Primary beam at: {}".format(pb)
    
    for f in filenamelist:
        img=fabio.open(os.path.join(pathtiff,"{}.tiff".format(f)))
        data=np.ushort(img.data)
        if len(data)==516:
            newdata=np.zeros([512,512],dtype=np.ushort)
            newdata[0:256,0:256]=data[0:256,0:256]
            newdata[256:,0:256]=data[260:,0:256]
            newdata[0:256,256:]=data[0:256,260:]
            newdata[256:,256:]=data[260:,260:]
            data=newdata
        data=np.ushort(data)
        header=collections.OrderedDict()
        header['HEADER_BYTES'] =512
        header['DIM'] =2
        header['BYTE_ORDER'] = "little_endian"
        header['TYPE'] = "unsigned_short"
        header['SIZE1'] = 512
        header['SIZE2'] = 512
        header['PIXEL_SIZE'] = 0.050000
        header['BIN'] = "1x1"
        header['BIN_TYPE'] = "HW"
        header['ADC'] = "fast"
        header['CREV'] = 1
        header['BEAMLINE'] = "ALS831"
        header['DETECTOR_SN'] = 926
        header['DATE'] = "Tue Jun 26 09:43:09 2007"
        header['TIME'] = 0.096288
        header['DISTANCE'] = "%.2f" % distance
        header['TWOTHETA'] = 0.00
        header['PHI'] = startangle
        header['OSC_START'] = startangle
        header['OSC_RANGE'] = osangle
        header['WAVELENGTH'] = 0.025080
        header['BEAM_CENTER_X'] = "%.2f" % pb[0]
        header['BEAM_CENTER_Y'] = "%.2f" % pb[1]
        header['DENZO_X_BEAM'] = "%.2f" % (pb[1]*0.05)
        header['DENZO_Y_BEAM'] = "%.2f" % (pb[0]*0.05)
        newimg=adscimage.adscimage(data,header)
        newimg.write(os.path.join(pathsmv,"{}.img".format(f)))
    
    return pb

#IMG files could not be recognized by XDS. But works if the original size is 512.
#Maybe also creating xds.inp here using the template

def affine_transform_ellipse_to_circle(azimuth, stretch, inverse=False):
    """Usage: 
    r = circle_to_ellipse_affine_transform(azimuth, stretch):
    np.dot(x, r) # x.shape == (n, 2)
    
    http://math.stackexchange.com/q/619037
    """
    sin = np.sin(azimuth)
    cos = np.cos(azimuth)
    sx    = 1 - stretch
    sy    = 1 + stretch
    
    # apply in this order
    rot1 = np.array((cos, -sin,  sin, cos)).reshape(2,2)
    scale = np.array((sx, 0, 0, sy)).reshape(2,2)
    rot2 = np.array((cos,  sin, -sin, cos)).reshape(2,2)
    
    composite = rot1.dot(scale).dot(rot2)
    
    if inverse:
        return np.linalg.inv(composite)
    else:
        return composite
       
def affine_transform_circle_to_ellipse(azimuth, stretch):
    """Usage: 
    r = circle_to_ellipse_affine_transform(azimuth, stretch):
    np.dot(x, r) # x.shape == (n, 2)
    """
    return affine_transform_ellipse_to_circle(azimuth, stretch, inverse=True)

def apply_transform_to_image(img, transform, center=None):
    """Applies transformation matrix to image and recenters it
    http://docs.sunpy.org/en/stable/_modules/sunpy/image/transform.html
    http://stackoverflow.com/q/20161175
    """
    
    if center is None:
        center = (np.array(img.shape)[::-1]-1)/2.0
    
    displacement = np.dot(transform, center)
    shift = center - displacement
    
    img_tf = ndimage.interpolation.affine_transform(img, transform, offset=shift, mode="constant", order=3, cval=0.0)
    return img_tf

def fixDistortion(image,directXY):
    
    radianAzimuth = np.radians(90)
    stretch = 1.3 * 0.01
    
    center = np.copy(directXY)
    if directXY[0]>(255):
        center[0] += 1
    if directXY[0]>(256):
        center[0] += 2
    if directXY[0]>(257):
        center[0] += 1
            
    if directXY[1]>(255):
        center[1] += 1
    if directXY[1]>(256):
        center[1] += 2
    if directXY[1]>(257):
        center[1] += 1
         
    c2e = affine_transform_circle_to_ellipse(radianAzimuth, stretch)
    newImage = apply_transform_to_image(image[::-1,:], c2e, center)[::-1,:]

    return newImage
        
def MRCCreator(pathtiff,pathred,header,pb):
    print "Tiff converting to MRC......"
    listing=glob.glob(os.path.join(pathtiff,"*.tiff"))
    filenamelist=[]
    for f in listing:
        fnm=os.path.splitext(os.path.basename(f))[0]
        filenamelist.append(int(fnm))
    filenamelist=np.sort(filenamelist)
    ind=10000
    for f in filenamelist:
        img=fabio.open(os.path.join(pathtiff,"{}.tiff".format(f)))
        data=img.data.astype(np.int16)[::-1,:]
            
        with open(os.path.join(pathred,"{}.mrc".format(ind)), "wb") as mrcf:
            mrcf.write(header)
            data=fixDistortion(data,pb)
            mrcf.write(data.tobytes())
        ind=ind+1
    
def ED3DCreator(pathtiff,pathred,pxs,startangle,endangle):
    print "Creating ed3d file......"
    listing=glob.glob(os.path.join(pathtiff,"*.tiff"))
    filenamelist=[]
    for f in listing:
        fnm=os.path.splitext(os.path.basename(f))[0]
        filenamelist.append(fnm)

    ed3d=open(os.path.join(pathred,"1.ed3d"),'w')
    
    low=startangle
    up=endangle
    nb=len(listing)
    step=(up-low)/nb
    
    ed3d.write("WAVELENGTH    0.02508\n")
    ed3d.write("ROTATIONAXIS    -38.5\n")
    ed3d.write("CCDPIXELSIZE    {}\n".format(pxs))
    ed3d.write("GINIOTILTSTEP    {}\n".format(step))
    ed3d.write("BEAMTILTSTEP    0\n")
    ed3d.write("BEAMTILTRANGE    0.000\n")
    ed3d.write("STRETCHINGMP    0.0\n")
    ed3d.write("STRETCHINGAZIMUTH    0.0\n")
    ed3d.write("\n")
    ed3d.write("FILELIST\n")

    ind=10000
    for j in range(0,nb):
        ed3d.write("FILE {}.mrc    {}    0    {}\n".format(ind,low+step*j,low+step*j))
        """MRC files are named as 10???.mrc"""
        ind=ind+1
    
    ed3d.write("ENDFILELIST")
    ed3d.close()
    print "Ed3d file created in path: {}".format(pathred)
    
def XDSINPCreator(pathsmv,indend,startangle,lowres,highres,pb,cl,osangle,RA):
    print "Creating XDS inp file......"
    from math import cos,pi
    px=pxd[cl]
    distance=483.89*0.00412/px
    print "Creating XDS inp file in foler: {}...".format(pathsmv)
    f=open('XDS_template.INP','r')
    f_xds=open(os.path.join(pathsmv,'XDS.INP'),'w')
    nb_line=1
    for line in f:
        if nb_line==54:
            f_xds.write("DATA_RANGE=           {} {}\n".format(1,indend))
        elif nb_line==56:
            f_xds.write("SPOT_RANGE=           {} {}\n".format(1,indend))
        elif nb_line==58:
            f_xds.write("BACKGROUND_RANGE=           {} {}\n".format(1,indend))
        elif nb_line==69:
            f_xds.write("STARTING_ANGLE= {}\n".format(startangle))
        elif nb_line==134:
            f_xds.write("INCLUDE_RESOLUTION_RANGE= {}   {}\n".format(lowres,highres))
        elif nb_line==156:
            f_xds.write("ORGX= {}    ORGY= {}       !Detector origin (pixels). Often close to the image center, i.e. ORGX=NX/2; ORGY=NY/2\n".format(pb[0],pb[1]))
        elif nb_line==157:
            f_xds.write("DETECTOR_DISTANCE= +{}   ! can be negative. Positive because the detector normal points away from the crystal.\n".format(distance))
        elif nb_line==159:
            f_xds.write(" OSCILLATION_RANGE= {}\n".format(osangle))
        elif nb_line==162:
            f_xds.write("ROTATION_AXIS= {} {} 0\n".format(cos(RA/180*pi),cos((RA+90)/180*pi)))
        else:
            f_xds.write(line)
        nb_line=nb_line+1
    
    print "XDS.inp file created. Modify .img path accordingly in your Linux machine."
    
def wait():
    msvcrt.getch()
    
def stopCollection():
    tx0=ctrl.stageposition.a
    while True:
        tx=ctrl.stageposition.a
        if tx-tx0<0.02: #should be smaller than the rotation speed but larger than the instability of goniometer reading when still
            break
    t_stop.set()

def main(path,stopEvent,exposure):
    #path=raw_input("Please copy the path of EMPTY folder where you want to put the image files:\n")
    while True:
        dn=raw_input("Please give the name of your dataset:\n")
        path=os.path.join(path,dn)
        
        log=open(os.path.join(path,"Continuous_Rotation_log.txt"),'w')
        
        cl=ctrl.magnification.get()
        print "Camera length now is {} cm, please ensure you are in diffraction mode and change camera length if you need now.".format(int(cl/10))
        print "Press enter if adjusted camera length."
        wait()
        tstart=datetime.datetime.now()
        log.write("Continuous Rotation start: {}\n".format(tstart))
        
        if not os.path.exists(os.path.join(path,"tiff")):
            os.makedirs(os.path.join(path,"tiff"))
        pathtiff=os.path.join(path,"tiff")
        
        if not os.path.exists(os.path.join(path,"SMV")):
            os.makedirs(os.path.join(path,"SMV"))
        pathsmv=os.path.join(path,"SMV")
        
        if not os.path.exists(os.path.join(path,"RED")):
            os.makedirs(os.path.join(path,"RED"))
        pathred=os.path.join(path,"RED")
            
        print "log file created."
        print "Please rotate the particle to the starting angle (i.e. -45 degree)."
        print "Please adjust z height. Press enter if done the preparation."
        wait()
        
        a0=ctrl.stageposition.a
        a=a0
        print "Please start to rotate the goniometer..."
        
        while (a0-a)<0.5:
            a=ctrl.stageposition.a
            if a - a0 > 0.5: #In order to prevent the instability of goniometer reading and status
                break
            
        """t=threading.Thread(name='Checking TEM tiltx start',target=stopCollection)
        t.start()"""
        ind=10001
        print "Data recording started..."
        startangle=a
        
        ctrl.cam.block()
        while True:
            if msvcrt.kbhit():
                break
            ctrl.getImage(exposure, 1, out=os.path.join(pathtiff,"{}.tiff".format(ind)), header_keys=None)
            ind=ind+1
        ctrl.cam.unblock()
        
        endangle=ctrl.stageposition.a
        
        cl=ctrl.magnification.get()
        spotsize=ctrl.spotsize
        log.write("Camera Length: {} cm\n".format(int(cl/10)))
        log.write("Spot size: {}\n".format(spotsize))
        log.write("starting angle: {}\n".format(startangle))
        log.write("Ending angle:{}\n".format(endangle))
        
        listing=glob.glob(os.path.join(pathtiff,"*.tiff"))
        numfr=len(listing)
        osangle=(endangle-startangle)/numfr
    
        log.write("Oscillation angle:{}\n".format(osangle))
        log.close()
        print "Tiff files (Cross corrected files, size 516*516) saved in folder: {}\n".format(pathtiff)
        
        pb=TiffToIMG(pathtiff,pathsmv,str(int(cl/10)),startangle,osangle)
        print "SMV files (size 512*512) saved in folder: {}\n".format(pathsmv)
        
        pxs=pxd[str(int(cl/10))]
        ED3DCreator(pathtiff, pathred, pxs, startangle, endangle)
        MRCCreator(pathtiff, pathred, header=mrc_header,pb=pb)
        print "MRC (size 516*516) and ed3d files saved in folder {}\n".format(pathred)
        
        RA=-38.5
        XDSINPCreator(pathsmv,ind,startangle,20,0.8,pb,str(int(cl/10)),osangle,RA)
        
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        
        cont=raw_input("Do you want to collect another dataset? Y/N\n")
        if cont == 'N' or cont == 'n':
            break
        
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
    print "Data collection done. Close the live window to end the session.\n"
    

if __name__ == '__main__':
    path=raw_input("Please enter an EMPTY path where you want to save your files:\n")
    path=r"{}".format(path)
    expt=raw_input("Please indicate desired exposure time: s\n 0.5") or '0.5'
    expt=float(expt)
    main(path,stopEvent=t_stop,exposure=expt)
