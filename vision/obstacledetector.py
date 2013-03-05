import glob
import os
import sys
import cv
import math
import util.sendsocket
import time
import configparse
import logging
import util.nullhandler

import util.kinectvideo as kv
from util.ticker import Ticker
#import util.openni_kinectvideo as kv
import util.vidmemreader
from abstractvisionmodule import AbstractVisionModule as avm
from obstacledetectorutil.segmentizer import Segmentizer

logging.getLogger('Borg.Brain.Vision.ObstacleDetector').addHandler(util.nullhandler.NullHandler())

class ObstacleDetector(avm):
    """
    Detects obstacles given a distance matrix
    basically the floor will be extracted from the matrix, remaining obstacles
    """

    def __init__(self, controller_ip=0, controller_port=0, source="kinect", standalone=False, filepath="default", test=0):
        self.logger = logging.getLogger("Borg.Brain.Vision.ObstacleDetector")
        avm.__init__(self, controller_ip, controller_port)

        if standalone:
            self.logger.setLevel("WARNING")
        # if detector is run as standalone, the kinect images will be retreived
        # directly from the kinect instead of from shared memory
        # set standalone true, if you want to use the obstacle detector without the architecture
        self.standalone = standalone

        # update frequency of the behaviour
        self.update_frequency = 20

        # bit depth of the used depth image
        self.imageDepth = 8

        #tolerance when it comes to detecting obstacles (don't set it too tight)
        # The higher the tollerance, the larger an obstacle should be before it is detected
        # when it's to low the risk is taken it will detect the floor as an obstacle...
        self.tolerance = 2.0
        self.minTolerance = self.tolerance
        self.maxTolerance = self.tolerance

        # calibration matrix (containing floor calibrated data)
        # min.cal, max.cal and avg.cal are files generated during calibrations.
        # They contain the distance min, max and average distance to the floor from the kinect.
        # The test files are used by obstacledetectortest.py
        if test == 0:
            minfile = os.environ['BORG'] + '/brain/src/vision/obstacledetectorutil/min.cal'
            maxfile = os.environ['BORG'] + '/brain/src/vision/obstacledetectorutil/max.cal'
            avgfile = os.environ['BORG'] + '/brain/src/vision/obstacledetectorutil/avg.cal'
        else:
            minfile = os.environ['BORG'] + '/brain/src/vision/obstacledetectorutil/testmin.cal'
            maxfile = os.environ['BORG'] + '/brain/src/vision/obstacledetectorutil/testmax.cal'
            avgfile = os.environ['BORG'] + '/brain/src/vision/obstacledetectorutil/testavg.cal'
        

        # read the calibration files and store the content in variables (multidimensional arrays).
        self.minMatrix = self.getCalibrationData(minfile)
        self.maxMatrix = self.getCalibrationData(maxfile)
        self.avgMatrix = self.getCalibrationData(avgfile)

        # current image where obstacles should be detected in.
        self.image = 0

        #segmentizer, used for segmentating images into segments
        self.segmentizer = Segmentizer()

        # specify the source (file or kinect)
        # reading from file is used for testing
        # when read from kinect, the depth images are read from the shared memory, or directly from the kinect (specified in self.standalone)
        self.source = source
        if source == "file":
            if filepath == "default":
                self.path = os.environ['BORG'] + '/brain/data/od_images/ball_left/'
            else:
                self.path = filepath
            self.filelist = glob.glob( os.path.join(self.path, '*.png') )
            self.framenumber = 0
        else:
            self.vid_mem_reader = util.vidmemreader.VidMemReader(["kinect_depth"])

    def setMinTolerance(self, tolerance):
        # the amount of tolerance towards the kinect. (i.e. deviations like small bumps or doorsteps are not recognized)
        self.minTolerance

    def setMaxTolerance(self, tolerance):
        # the amount of tolerance away from the kinect. (i.e. deviations like small gaps in the floor or not recognized)
        self.maxTolerance

    def run(self):
        """ used when run as behavior """
        print "Running obstacledetector."
        self.set_known_objects(['obstacle_matrix'])
        ticker = Ticker(self.update_frequency)
        while 1:
            # update the detector. This will:
            #     calculate an obstacle matrix from retreived Kinect images
            #     put the obstacle matrix into the memory
            ticker.tick()

            # get the obstacle matrix
            obstacleMatrix = self.getObstacleMatrix() # matrix containing all the found obstacles
            delay = time.time() - self.mtime

            # put the matrix into memory
            self.add_property('name', 'obstacle_matrix')
            self.add_property('matrix', obstacleMatrix)
            self.add_property('mtime', self.mtime)
            self.add_property('local_delay', delay)
            self.update()

    def train(self):
        pass

    def getObstacleMatrix(self, imagesPerDetection=3):
        """
        finds obstacles by comparing segment values witch calibration data
        returns a matrix with found obstacles marked as '1' (else '0')
        """

        # each image will be divided in to segments (reducing the resolution of the image)
        # each segment will represent a part of the image (the pixels will averaged in this part)
        segmentations = []

        # When detecting obstacles, a few (imagesPerDetection) captures will be taken together te reduce noise.
        # first each image (capture) will be segmentated, then append to the segmenatations array

        # @Changed: only do this when running standalone; because otherwise we
        # will request the same image from the vidmemwriter 3 times; doesn't
        # make sense. 
        if self.standalone:
            for i in range(imagesPerDetection):
                # segments extracted from the distance image
                self.image, self.mtime = self.getNextImage()
                segmentations.append(self.segmentizer.getSegments(self.image))

            # all the segmented images will be merged. The result will be used to detect obstacles
            segments = self.merge(segmentations)
        else:
            self.image, self.mtime = self.getNextImage()
            segments = self.segmentizer.getSegments(self.image)

        #create matrix where objects are markt as True
        obstacleMatrix = []

        # loop over each segment and compare the segment value to calibration data to determine if there is an obstacle or not.
        for x in range(len(segments)):
                row = []
                for y in range(len(segments[0])):
                    # this is where finally is determined wheter a segment contains an obstacle or is just a piece of floor
                    # since each segment contains the distance to a point in the 'image',
                    # if that distance is smaller (closer) than the distance at that point to the floor (determined using calibration),
                    # then its an object. The tolerance is the value that should be the minimum difference to be sure its an object,
                    # and not the floor
                    if segments[x][y] < self.minMatrix[x][y] - self.minTolerance: # obstacle (minMatrix contains calibrated values)
                        #row.append(self.minMatrix[x][y] - segments[x][y])
                        row.append(1)
                    elif segments[x][y] > self.maxMatrix[x][y] + self.maxTolerance: # gap in floor (maxMatrix contains calibrated values)
                        #row.append(self.maxMatrix[x][y] - segments[x][y])
                        row.append(1)
                    else:
                        row.append(0)
                obstacleMatrix.append(row)

        return obstacleMatrix


    def getNextImage(self):
        """returns a image which can be used for detection"""

        #return kinect frame
        if self.source == "kinect":
            # if standalone is true, the depth images will be retrieved directly from the kinect
            if self.standalone == True:
                if self.imageDepth == 8:
                    return (kv.GetDepth8(), time.time())
                elif self.imageDepth == 11 or self.imageDepth == 16:
                    return (kv.GetDepth11(), time.time())
                else:
                    print "Illegal image depth: '" + str(self.imageDepth) + "'. Using 8 bit"
                    return (kv.GetDepth8(), time.time())
            # the depth image will be retrieved from the memory (using architecture)
            else:
                last = self.vid_mem_reader.get_latest_image(mtimes = True)
                
                return last[0]

        # return testimage (used for testing
        elif self.source == "file":
            self.framenumber += 1
            if self.framenumber == len(self.filelist):
                self.framenumber = 0
            return (cv.LoadImage(self.filelist[self.framenumber],cv.CV_LOAD_IMAGE_GRAYSCALE), time.time())


    def getCalibrationData(self,filename):
        """ get the data from the calibration data file
            this file contains the mean values of the distances to the floor
        """
        calibrationdataList = []

        f = open(filename)
        while 1:
            line = f.readline()
            if not line: break
            #convert line to list
            calibrationdataList.append(eval(line))
        f.close()

        return calibrationdataList

    def merge(self, segmentations):
        """ merge some segmentations. The result will contain the lowest values
            this is used to remove noise from the segmentation data
        """
        merged = segmentations[0]

        for segments in segmentations:
            for y in range(len(segments)):
                for x in range(len(segments[0])):
                    if segments[y][x] < merged[y][x]:
                        merged[y][x] = segments[y][x]

        return merged
        

if __name__ == "__main__":
    """ run obstacledetector as an behavior """
    sec = "obstacledetector" #section in config_dict
    args = sys.argv[1:]
    option_dict = configparse.parse_args_to_param_dict(args, sec)

    #READ PARAMETERS:
    controller_ip    =     option_dict.get_option(sec,'host')
    controller_port  =     option_dict.get_option(sec,'port')

    print "OBSTACLE AVOIDANCE STARTING AT %s : %s" % (controller_ip, controller_port)

    detector = ObstacleDetector(controller_ip, controller_port)
    detector.connect()
    detector.run()

