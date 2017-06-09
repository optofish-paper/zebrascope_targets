# Zebrascope targets
An ImageJ plugin for selecting cells and saving their coordinates for two-photon excitation.
To use, copy `Zebra_Ablate.py` into `Fiji.app\plugins` folder. Open an image stack, click `Plugins` > `Zebra ablate`, 
and set up ablation/excitation parameters. Once excitation targets are selected, press Enter to save them in a file.
Output: 
1. A text file `EProfile.txt` with ablation targets in Zebrascope-compatible format.
2. A zip file `EProfile.txt.zip`, which contains ROIs for FIJI ROI manager. Drag it into FIJI to re-open the ROIs.

Ignore console error `console: Failed to install '': java.nio.charset.UnsupportedCharsetException: cp0.`, it is meaningless.
Plugin requires [Java 8](https://java.com/en/) and latest [Fiji](https://fiji.sc/#download) distibution.