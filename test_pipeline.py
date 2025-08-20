import os
import SimpleITK as sitk
import util.structure as structure
import util.file_access_utilities as futil

import pipeline as pl


def test_collect_image_paths():
    """
    TEST_COLLECT_IMAGE_PATHS tests if the collect_image_paths function
    is implemented correctly.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    crawler = pl.collect_image_paths(os.path.join(root_dir, "data"))
    if isinstance(crawler, futil.FileSystemDataCrawler):
        image_paths_ = crawler.data
        subject_x_paths = image_paths_.get("subjectX")  # only consider subjectX
        identifier = subject_x_paths.pop("subjectX", "")
        collect_ok = all(
            (
                identifier.endswith("subjectX"),
                structure.BrainImageTypes.GroundTruth in subject_x_paths,
                structure.BrainImageTypes.T1w in subject_x_paths,
            )
        )
    else:
        collect_ok = False
        subject_x_paths = None  # for load_images
    assert collect_ok


def test_load_images():
    """
    TEST_LOAD_IMAGES tests if the load_images function
    is implemented correctly.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    crawler = pl.collect_image_paths(os.path.join(root_dir, "data"))
    image_paths_ = crawler.data
    subject_x_paths = image_paths_.get("subjectX")

    if isinstance(subject_x_paths, dict):
        subject_x_images = pl.load_images(subject_x_paths)
        image_type_ok = all(
            isinstance(img, sitk.Image) for img in subject_x_images.values()
        )
        load_ok = isinstance(subject_x_images, dict) and image_type_ok
    else:
        load_ok = False
        subject_x_images = None  # for preprocess_filter_rescale_t1
    assert load_ok


def test_register_images():
    """
    TEST_REGISTER_IMAGES tests if the register_images function
    is implemented correctly.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    crawler = pl.collect_image_paths(os.path.join(root_dir, "data"))
    image_paths_ = crawler.data
    subject_x_paths = image_paths_.get("subjectX")
    subject_x_images = pl.load_images(subject_x_paths)

    atlas_img_ = sitk.ReadImage(os.path.join(root_dir, "data", "mni_icbm152_t1_tal_nlin_sym_09a.nii.gz"))
    if isinstance(subject_x_paths, dict):
        registered_img, registered_gt_ = pl.register_images(
            subject_x_images, atlas_img_
        )
        if isinstance(registered_img, sitk.Image) and isinstance(
            registered_gt_, sitk.Image
        ):
            stats = sitk.LabelStatisticsImageFilter()
            stats.Execute(registered_img, registered_gt_)
            labels = tuple(sorted(stats.GetLabels()))
            register_ok = registered_img.GetSize() == registered_gt_.GetSize() == (
                197,
                233,
                189,
            ) and labels == tuple(range(6))
        else:
            register_ok = False
    else:
        register_ok = False
    assert register_ok


def test_preprocess_filter_rescale_t1():
    """
    TEST_PREPROCESS_FILTER_RESCALE_T1 tests if the preprocess_filter_rescale_t1 function
    is implemented correctly.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    crawler = pl.collect_image_paths(os.path.join(root_dir, "data"))
    image_paths_ = crawler.data
    subject_x_paths = image_paths_.get("subjectX")
    subject_x_images = pl.load_images(subject_x_paths)

    if isinstance(subject_x_images, dict):
        pre_rescale = pl.preprocess_filter_rescale_t1(subject_x_images, -3, 101)
        if isinstance(pre_rescale, sitk.Image):
            min_max = sitk.MinimumMaximumImageFilter()
            min_max.Execute(pre_rescale)
            pre_ok = min_max.GetMinimum() == -3 and min_max.GetMaximum() == 101
        else:
            pre_ok = False
    else:
        pre_ok = False
    assert pre_ok


def test_extract_feature_median_t1():
    """
    TEST_EXTRACT_FEATURE_MEDIAN_T1 tests if the extract_feature_median_t1 function
    is implemented correctly.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    crawler = pl.collect_image_paths(os.path.join(root_dir, "data"))
    image_paths_ = crawler.data
    subject_x_paths = image_paths_.get("subjectX")
    subject_x_images = pl.load_images(subject_x_paths)

    if isinstance(subject_x_images, dict):
        median_img_ = pl.extract_feature_median_t1(subject_x_images)
        if isinstance(median_img_, sitk.Image):
            median_image_path = os.path.join(root_dir, "data", "subjectX", "T1med.nii.gz")
            median_ref = sitk.ReadImage(median_image_path)
            min_max = sitk.MinimumMaximumImageFilter()
            min_max.Execute(median_img_ - median_ref)
            median_ok = min_max.GetMinimum() == 0 and min_max.GetMaximum() == 0
        else:
            median_ok = False
    else:
        median_ok = False
    assert median_ok
