settings_description = """\
##### Explanation of Settings

###### Cropping Wavelength

At short wavelengths, the spectra can be noisy, thus Mocca allows you to pick a range of wavelengths to use.

**Min Wavelength**: Minimum wavelength that will be used

**Max Wavelength**: Maximum wavelength that will be used

###### Baseline correction

The baseline is first corrected using blank (if provided), and then further refined using Mocca algorithm.

**Baseline smoothness**: Higher values will make Mocca assume that the baseline is already smooth - if the baseline is not smooth, try decreasing this value.

###### Peak Picking

These settings determine which peaks will be picked and integrated.

**Min Peak Height**: Minimum absolute height of the peak (averaged over selected wavelengths).

**Min Relative Peak Height**: Minimum height relative to the tallest peak in the chromatogram.

**Min Retention Time**: Peaks with smaller elution time will not be analysed.

**Max Retention Time**: Peaks with higher elution time will not be analysed.

**Min Relative Peak Area**: Minimum area relative to largest peak in the chromatogram.

###### Determining peak borders

These settings change how peak borders (start and end time) are determined. Usually, they do not need to be changed.

**Max Peak Cutoff**: Maximum fraction of the peak height that can be cut off by the peak border.

**Split Peak Threshold**: Maximum relative height between two peaks so that they can be considered to be separate and non-overlapping.

###### Deconvolution

**Min Peak Purity**: Minimum fraction of data explained by the fitted peaks. Values closer to 1 will help identify more impurities.

###### Assigning Compounds

These settings determine how compounds from different chromatograms are identified to be the same.

**Max Peak Distance**: Maximum shift of elution time relative to peak width. Increase this value if the same compound has different elution times in different chromatograms.

**Min Spectrum Correl**: Minimum similarity in spectra for compounds to be considered the same. Values closer to 1 are more strict.

"""