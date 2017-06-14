# Zebrascope targets
This repo consists of 2 parts:
1. an [ImageJ plugin](/Fiji_plugin/Zebra_ablate.py "Zebra_ablate.py") for manual cell selection and saving their coordinates for two-photon ablation in file `EProfile.txt`.
2. an IPython [notebook](MultiviewRegistration/ExcitationProfileCorrection.ipynb "Coordinate correction notebook") which takes two TIFF stacks, registers second to the first (rigid registration) using [Multiview-Reconstruction plugin](https://imagej.net/Multiview-Reconstruction), and applies the drift/rotation correction to the ablation coordinates file `EProfile.txt` generated in step 1. This dramatically improves ablation accuracy of [Zebrascope](https://www.nature.com/nmeth/journal/v11/n9/full/nmeth.3040.html)

### Usage: Fiji Plugin
To use the Fiji plugin (part 1), copy [Zebra_ablate.py](/Fiji_plugin/Zebra_ablate.py "Zebra_ablate plugin") into your local `Fiji.app/plugins` folder. Restart Fiji, open an image stack, click `Plugins` > `Zebra ablate`, and set up ablation parameters.
 
![Plugin GUI](/Fiji_plugin/GUI_screenshot.png "GUI_screenshot.png")

Once excitation targets are selected, press **Enter** to save them.
![ROI_screenshot](/Fiji_plugin/ROI_screenshot.png "ROI_screenshot.png")

The plugin saves ablation coordinates in 2 files: 
* A text file `EProfile.txt` in Zebrascope-compatible format.
* A zip file `EProfile.txt.zip`, which contains ROIs for Fiji ROI manager. Drag it into Fiji, it opens the ROIs automatically.

### Usage: Rigid registration and coordinate correction
To correct the ablation coordinates for drift/rotation, the user needs two TIFF files. First file (reference) is a grayscale file corresponding to the stack used in part 1 for cell selection. Second file (pre-ablation) is acquired directly before ablation. 
![Stack0 and Stack1](/Fiji_plugin/Stack0_Stack1.png "Stack0_Stack1.png")
(they look similar but left stack is actually offset from right stack by (1.6, 0.7, 2.1) um in (x,y,z) )

The IPython [notebook](MultiviewRegistration/ExcitationProfileCorrection.ipynb "Coordinate correction notebook") registers second file to the first and applies the drift/rotation correction to the original coordinate files `EProfile.txt` and `EProfile.txt.zip`. Registration takes about 1 min.

### Dependencies
The Fiji plugin requires [Java 8](https://java.com/en/) and latest [Fiji](https://fiji.sc/#download) distibution.
The IPython notebook requires [Fiji](https://fiji.sc/#download) and [PymageJ/devel](https://github.com/Jhsmit/PymageJ/tree/devel) (a copy is included `MultiviewRegistration/PymageJ-devel`)

### Known bugs
When launching `Zebra_ablate` plugin, Fiji throws console error  `console: Failed to install '': java.nio.charset.UnsupportedCharsetException: cp0.`. This error can be safely ignored (a known Fiji bug).