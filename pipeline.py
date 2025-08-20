import os
import SimpleITK as sitk

import pymia.filtering.filter as fltr
import pymia.filtering.registration as fltr_reg

import util.structure as structure
import util.file_access_utilities as futil


def collect_image_paths(data_dir):
    image_keys = [structure.BrainImageTypes.T1w,
                  structure.BrainImageTypes.GroundTruth]

    class MyFilePathGenerator(futil.FilePathGenerator):
        @staticmethod
        def get_full_file_path(id_: str, root_dir: str, file_key, file_extension: str) -> str:
            if file_key == structure.BrainImageTypes.T1w:
                file_name = 'T1native'
            elif file_key == structure.BrainImageTypes.GroundTruth:
                file_name = 'labels_native'
            else:
                raise ValueError('Unknown key')
            return os.path.join(root_dir, file_name + file_extension)

    dir_filter = futil.DataDirectoryFilter()

    # todo: create an instance of futil.FileSystemDataCrawler and pass the correpsonding arguments
    crawler = None  # todo: modify here

    return crawler


def load_images(image_paths):
    # todo: read the images (T1 as sitk.sitkFloat32, GroundTruth as sitk.sitkUInt8)
    image_dict = {
        structure.BrainImageTypes.T1w: None,  # todo: modify here
        structure.BrainImageTypes.GroundTruth: None  # todo: modify here
    }

    return image_dict


def register_images(image_dict, atlas_img):

    registration = fltr_reg.MultiModalRegistration()
    registration_params = fltr_reg.MultiModalRegistrationParams(atlas_img)
    # todo execute the registration with the T1-weighted image and the registration parameters
    registered_t1 = None  # todo: modify here

    gt_img = image_dict[structure.BrainImageTypes.GroundTruth]
    # todo: apply transform to GroundTruth image (gt_img)
    #  (hint: sitk.Resample, referenceImage=atlas_img, transform=tegistration.transform,
    #  interpolator=sitk.sitkNearestNeighbor
    registered_gt = None  # todo: modify here

    return registered_t1, registered_gt


def preprocess_filter_rescale_t1(image_dict, new_min_val, new_max_val):
    class MinMaxRescaleFilterParams(fltr.FilterParams):
        def __init__(self, min_, max_) -> None:
            super().__init__()
            self.min = min_
            self.max = max_

    class MinMaxRescaleFilter(fltr.Filter):
        def execute(self, img: sitk.Image, params: MinMaxRescaleFilterParams = None) -> sitk.Image:
            resacaled_img = sitk.RescaleIntensity(img, params.min, params.max)
            return resacaled_img

    # todo: use the above filter and parameters to get the rescaled T1-weighted image
    filter = None # todo: modify here
    filter_params = None  # todo: modify here
    minmax_rescaled_img = None  # todo: modify here

    return minmax_rescaled_img


def extract_feature_median_t1(image_dict):

    class MedianFilter(fltr.Filter):
        def execute(self, img: sitk.Image, params: fltr.FilterParams = None) -> sitk.Image:
            med_img = sitk.Median(img)
            return med_img

    # todo: use the above filter class to get the median image feature of the T1-weighted image
    filter = None  # todo: modify here
    median_img = None  # todo: modify here

    return median_img

