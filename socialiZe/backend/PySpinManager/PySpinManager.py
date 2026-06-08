import PySpin

from .PySpinCam import PySpinCam, PySpinMultiCam


class PySpinManager(object):

    def __init__(self):
        # Retrieve singleton reference to system object
        self.system: PySpin.System = PySpin.System.GetInstance()
        # Get current library version
        version = self.system.GetLibraryVersion()
        
        # Get camera list
        cam_list = self.system.GetCameras()
        num_cameras = cam_list.GetSize()
        self.cams = []
        self.serial2idx = {}

        # Log the information
        print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))
        print('Number of cameras detected: %d' % num_cameras)

        self.camera_in_use = {i: False for i in range(num_cameras)}

        for i in range(num_cameras):
            self.cams.append(cam_list.GetByIndex(i))
            self.cams[-1].Init()
            serial = self.cams[-1].DeviceSerialNumber.ToString()
            self.serial2idx[serial] = i
            self.cams[-1].DeInit()

        cam_list.Clear()

    def get_camera(self, idx):
        if idx > 100:
            idx = str(idx)
        if isinstance(idx, str):
            idx = self.serial2idx[idx]
        elif isinstance(idx, int):
            pass
        else:
            raise PySpin.SpinnakerException('idx should be serial(str) or index(int)')
        
        if self.camera_in_use[idx] is not False:
            print(f"Camera {idx} is already in use.")
            return self.camera_in_use[idx]

        cam = self.cams[idx]
        spincam = PySpinCam(cam, self, idx)
        # TODO: Make this more robust
        spincam.cam.AcquisitionFrameRateEnable.SetValue(True)
        spincam.cam.AcquisitionFrameRate.SetValue(20)

        self.camera_in_use[idx] = spincam

        return spincam

    def get_multi_camera(self, idx):
        if not isinstance(idx, list):
            raise PySpin.SpinnakerException('idx should be list of index or serial')
        multi_cap = PySpinMultiCam()
        for it in idx:
            spincam = self.get_camera(it)
            spincam.set_software_trigger()
            multi_cap.add_camera(spincam)
        return multi_cap

    def release_camera(self, idx):
        if idx in self.camera_in_use:
            self.camera_in_use[idx] = False
        else:
            print(f"Camera {idx} not found in manager.")

    def release(self):
        print("PySpinManager.py: Releasing system.")

        # Release each camera if it's in use
        for idx in range(len(self.cams)):
            print(f"Examining camera with idx: {idx}")
            if self.camera_in_use[idx] is not False:
                print(f"Camera with idx `{idx}` will be released...")
                try:
                    cam = self.get_camera(idx)
                    if cam is not None:
                        cam.release()
                        del cam

                        # self.cam_list.Clear()
                except Exception as e:
                    print(f"Error releasing camera {idx}: {e}")
            
            # Release the camera in self.cams
            self.cams[idx].DeInit()
            
            del self.cams[idx]

        # Release system instance
        if self.system is not None:
            self.system.ReleaseInstance()
            self.system = None
        print('Released all resources')


    def __del__(self):
        self.release()