"""All the text contained by the `plan` page. Dash supports markup"""

all_text = """\
# How to use MOCCA

#### Exporting raw HPLC data

This depends on the respective software.

In Empower, the data can be exported as described on the [support page](https://support.waters.com/KB_Inf/Empower_Breeze/WKB77571_How_to_export_3D_raw_data_from_Empower_to_a_Microsoft_Excel_spreadsheet). This way it is possible to export UV-VIS as well as MS data.

#### Uploading the chromatograms

On the **data** page, upload your blank and sample files. Then, fill in relevant information in the table below, such as compound names and concentrations for standards, and information about internal standards (ISTD) for samples that contain them.

Once you are happy with the data, you can **confirm the changes** and **download campaign** - the next time you can restore all data just by uploading the campaign file.

#### Processing the data

On the **process** page, you can adjust the settings used for data analysis. You can test the settings by processing single sample.

Once you are happy with the settings, you can **process all** - this usually takes a minute or two.

After processing the data, you can also download the campaign - this way you won't need to process it again when you want to look at the results later.

#### The results

On the **results** page, you can find summary of concentrations of compounds in individual samples, as well as raw 3D data and summary of compound properties.

The data from the tables can be copied and pasted into Excel.

"""
