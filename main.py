from composition import *

def main():
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    driveVideo = "./source/drive.mp4"
    
    startVideo(driveVideo, handleImg)
    
if __name__ == "__main__":
    main()
